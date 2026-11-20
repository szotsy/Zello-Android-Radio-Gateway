#!/usr/bin/env python3
"""Import enabled adapters from a published APK and render release compatibility pages."""
import html
import json
import os
import urllib.request
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/usb-uart-compatibility.json"
RELEASE_JSON = ROOT / "docs/usb-uart-release.json"
PAGES = {
    "hu": ROOT / "docs/usb-uart-compatibility.html",
    "en": ROOT / "docs/usb-uart-compatibility-en.html",
}
START = "<!-- RELEASE_APK_SECTION_START -->"
END = "<!-- RELEASE_APK_SECTION_END -->"


def esc(value):
    return html.escape(str(value), quote=True)


def main():
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        raise SystemExit("GITHUB_EVENT_PATH is required")
    event = json.loads(Path(event_path).read_text(encoding="utf-8"))
    release = event.get("release") or {}
    if not release:
        tag = (os.environ.get("RELEASE_TAG")
               or (event.get("inputs") or {}).get("tag")
               or (json.loads(RELEASE_JSON.read_text(encoding="utf-8")).get("tag_name")
                   if RELEASE_JSON.exists() else None))
        if not tag:
            raise SystemExit("No release payload or manual-dispatch tag was provided")
        api = f"https://api.github.com/repos/szotsy/Zello-Android-Radio-Gateway/releases/tags/{tag}"
        headers = {
            "User-Agent": "Orfeusz-Gateway-Release-Sync",
            "Accept": "application/vnd.github+json",
        }
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        req = urllib.request.Request(api, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as response:
            release = json.loads(response.read().decode("utf-8"))
    if not release or not release.get("published_at"):
        raise SystemExit("The event does not identify a published GitHub Release")

    apk_assets = [a for a in release.get("assets", [])
                  if a.get("name", "").lower().endswith(".apk")
                  and not a.get("name", "").lower().endswith(".sha256.apk")]
    if not apk_assets:
        raise SystemExit("No APK asset found in the published Release")
    tag = release.get("tag_name", "")
    preferred = [a for a in apk_assets
                 if a.get("name") == f"Orfeusz.Gateway_v{tag}.apk"]
    asset = (preferred or apk_assets)[0]
    request = urllib.request.Request(
        asset["browser_download_url"],
        headers={"User-Agent": "Orfeusz-Gateway-Release-Sync"})
    with urllib.request.urlopen(request, timeout=90) as response:
        apk_bytes = response.read()

    with ZipFile(BytesIO(apk_bytes)) as apk:
        candidates = [n for n in apk.namelist()
                      if n.endswith("usb-uart-adapters.json")]
        if len(candidates) != 1:
            raise SystemExit(
                f"Expected exactly one usb-uart-adapters.json in APK, found: {candidates}")
        manifest = json.loads(apk.read(candidates[0]).decode("utf-8"))

    adapters = manifest.get("adapters")
    if not isinstance(adapters, list) or not adapters:
        raise SystemExit("APK adapter manifest is empty or invalid")

    enabled_by_id = {}
    for adapter in adapters:
        if adapter.get("engine_supported") is not True:
            continue
        adapter_id = adapter.get("id")
        if not adapter_id:
            raise SystemExit(f"Enabled adapter entry is missing an id: {adapter}")
        if adapter_id in enabled_by_id:
            raise SystemExit(f"Duplicate enabled adapter ID in APK manifest: {adapter_id}")
        enabled_by_id[adapter_id] = adapter
    if not enabled_by_id:
        raise SystemExit("The APK contains no engine-enabled USB-UART adapters")

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry_adapters = registry.get("adapters", [])
    registry_by_id = {a["id"]: a for a in registry_adapters}

    # Engine support and physical verification are separate facts. New IDs
    # found enabled in the APK are added as enabled-but-untested, never as verified.
    for adapter_id, manifest_adapter in enabled_by_id.items():
        item = registry_by_id.get(adapter_id)
        if item is None:
            name = (manifest_adapter.get("display_name")
                    or manifest_adapter.get("name") or adapter_id)
            vid = manifest_adapter.get("vid")
            pid = manifest_adapter.get("pid")
            if not vid or not pid:
                raise SystemExit(
                    f"New engine-enabled adapter {adapter_id} is missing VID/PID in APK manifest")
            item = {
                "id": adapter_id,
                "name": name,
                "chip": name,
                "vid": str(vid).upper().replace("0X", ""),
                "pid": str(pid).upper().replace("0X", ""),
                "status": "not_verified",
                "note_hu": "Az Orfeusz USB-UART engine engedélyezi; fizikai adapterteszt még nem igazolta az RTS/CTS és PTT működését.",
                "note_en": "Enabled in the Orfeusz USB-UART engine; physical adapter testing has not yet verified RTS/CTS and PTT operation.",
                "app_supported": True,
                "engine_supported": True,
                "rts_output": manifest_adapter.get("rts_output") is True,
                "cts_input": manifest_adapter.get("cts_input") is True,
            }
            registry_adapters.append(item)
            registry_by_id[adapter_id] = item
        else:
            # The APK is authoritative for current engine enablement; retain
            # the registry's independent physical-test status and notes.
            item["app_supported"] = True
            item["engine_supported"] = True
            if item.get("status") not in ("verified", "not_verified"):
                item["status"] = "not_verified"

    registry["adapters"] = registry_adapters
    REGISTRY.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")

    ids = list(enabled_by_id)
    release_data = {
        "tag_name": tag,
        "name": release.get("name") or tag,
        "prerelease": bool(release.get("prerelease")),
        "published_at": release["published_at"],
        "html_url": release.get("html_url", ""),
        "apk_asset": asset.get("name", ""),
        "adapter_ids": ids,
    }
    RELEASE_JSON.write_text(json.dumps(release_data, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")

    for lang, path in PAGES.items():
        cards = []
        for adapter_id in ids:
            a = registry_by_id[adapter_id]
            vidpid = f'{a.get("vid") or "?"}:{a.get("pid") or "?"}'
            state = a.get("status", "not_verified")
            if lang == "hu":
                state_text = ("Igazolt" if state == "verified"
                              else "Engine-ben engedélyezve · tesztelésre vár")
            else:
                state_text = ("Verified" if state == "verified"
                              else "Engine enabled · awaiting physical test")
            cards.append(
                f'<div class="engine-card"><strong>{esc(a["name"])}</strong>'
                f'<small>VID:PID {esc(vidpid)} · RTS / CTS</small>'
                f'<span class="state {"pending" if state != "verified" else ""}">{esc(state_text)}</span></div>'
            )
        kind = (("Előzetes kiadás" if lang == "hu" else "Pre-release")
                if release_data["prerelease"]
                else ("Stabil kiadás" if lang == "hu" else "Stable release"))
        if lang == "hu":
            heading = "A kiadásban engine-szinten engedélyezett adapterek"
            intro = (f'A kiadás: <a href="{esc(release_data["html_url"])}" target="_blank" '
                     f'rel="noopener">{esc(tag)}</a> · {kind} · publikálva: '
                     f'{esc(release_data["published_at"])}. A lista az APK USB-UART '
                     f'manifestjéből készült; az „Igazolt” státusz fizikai tesztet jelent.')
        else:
            heading = "Adapters enabled in the release engine"
            intro = (f'Release: <a href="{esc(release_data["html_url"])}" target="_blank" '
                     f'rel="noopener">{esc(tag)}</a> · {kind} · published: '
                     f'{esc(release_data["published_at"])}. This list comes from the APK '
                     f'USB-UART manifest; “Verified” indicates physical testing.')
        block = (f'<section class="engine-supported"><h2>{heading}</h2><p>{intro}</p>'
                 f'<div class="engine-grid">{"".join(cards)}</div></section>')
        text = path.read_text(encoding="utf-8")
        if START not in text or END not in text:
            raise SystemExit(f"Release section markers missing in {path}")
        before, rest = text.split(START, 1)
        _, after = rest.split(END, 1)
        path.write_text(before + START + "\n" + block + "\n" + END + after,
                        encoding="utf-8")
    print(f'Imported {len(ids)} engine-enabled adapter(s) from {tag}; '
          f'{sum(registry_by_id[i].get("status") == "verified" for i in ids)} physically verified.')


if __name__ == "__main__":
    main()
