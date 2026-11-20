#!/usr/bin/env python3
"""Import the adapter manifest from a published APK and render it on both compatibility pages."""
import html
import json
import os
import urllib.request
import zipfile
from datetime import datetime
from pathlib import Path

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
        tag = os.environ.get("RELEASE_TAG") or (event.get("inputs") or {}).get("tag") or (json.loads(RELEASE_JSON.read_text(encoding="utf-8")).get("tag_name") if RELEASE_JSON.exists() else None)
        if not tag:
            raise SystemExit("No release payload or manual-dispatch tag was provided")
        api = f"https://api.github.com/repos/szotsy/Zello-Android-Radio-Gateway/releases/tags/{tag}"
        req = urllib.request.Request(api, headers={"User-Agent": "Orfeusz-Gateway-Release-Sync", "Accept": "application/vnd.github+json"})
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
    preferred = [a for a in apk_assets if a.get("name") == f"Orfeusz.Gateway_v{tag}.apk"]
    asset = (preferred or apk_assets)[0]
    request = urllib.request.Request(asset["browser_download_url"],
                                     headers={"User-Agent": "Orfeusz-Gateway-Release-Sync"})
    with urllib.request.urlopen(request, timeout=90) as response:
        apk_bytes = response.read()

    import zipfile
    from io import BytesIO
    with zipfile.ZipFile(BytesIO(apk_bytes)) as apk:
        candidates = [n for n in apk.namelist() if n.endswith("usb-uart-adapters.json")]
        if len(candidates) != 1:
            raise SystemExit(f"Expected exactly one usb-uart-adapters.json in APK, found: {candidates}")
        manifest = json.loads(apk.read(candidates[0]).decode("utf-8"))

    adapters = manifest.get("adapters")
    if not isinstance(adapters, list) or not adapters:
        raise SystemExit("APK adapter manifest is empty or invalid")
    # The APK manifest may also contain candidate-only adapters that are
    # intentionally disabled. They are not part of the release-supported list.
    ids = []
    for adapter in adapters:
        if adapter.get("engine_supported") is not True:
            continue
        adapter_id = adapter.get("id")
        if not adapter_id:
            raise SystemExit(f"Enabled adapter entry is missing an id: {adapter}")
        ids.append(adapter_id)
    if not ids:
        raise SystemExit("The APK contains no engine-enabled USB-UART adapters")
    if len(ids) != len(set(ids)):
        raise SystemExit("Duplicate enabled adapter IDs in APK manifest")

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry_by_id = {a["id"]: a for a in registry.get("adapters", [])}
    unknown = set(ids) - set(registry_by_id)
    if unknown:
        raise SystemExit(f"APK contains adapter IDs missing from central registry: {sorted(unknown)}")

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
            state = a.get("status", "under_investigation")
            if lang == "hu":
                state_text = "Igazolt" if state == "verified" else ("Engine-ben engedélyezve · fizikai tesztre vár" if state == "not_verified" else "Ellenőrzendő")
            else:
                state_text = "Verified" if state == "verified" else ("Engine enabled · physical test pending" if state == "not_verified" else "Needs review")
            cards.append(
                f'<div class="engine-card"><strong>{esc(a["name"])}</strong>'
                f'<small>VID:PID {esc(vidpid)} · RTS / CTS</small>'
                f'<span class="state {"pending" if state != "verified" else ""}">{esc(state_text)}</span></div>'
            )
        kind = ("Előzetes kiadás" if lang == "hu" else "Pre-release") if release_data["prerelease"] else ("Stabil kiadás" if lang == "hu" else "Stable release")
        if lang == "hu":
            heading = "A legutóbbi kiadásban ténylegesen támogatott adapterek"
            intro = f'A kiadás: <a href="{esc(release_data["html_url"])}" target="_blank" rel="noopener">{esc(tag)}</a> · {kind} · publikálva: {esc(release_data["published_at"])}. Az alábbi lista az APK-ba csomagolt USB-UART manifestből készült.'
        else:
            heading = "Adapters actually supported by the latest release"
            intro = f'Release: <a href="{esc(release_data["html_url"])}" target="_blank" rel="noopener">{esc(tag)}</a> · {kind} · published: {esc(release_data["published_at"])}. This list is generated from the USB-UART manifest packaged inside the APK.'
        block = (f'<section class="engine-supported"><h2>{heading}</h2><p>{intro}</p>'
                 f'<div class="engine-grid">{"".join(cards)}</div></section>')
        text = path.read_text(encoding="utf-8")
        if START not in text or END not in text:
            raise SystemExit(f"Release section markers missing in {path}")
        before, rest = text.split(START, 1)
        _, after = rest.split(END, 1)
        path.write_text(before + START + "\n" + block + "\n" + END + after,
                        encoding="utf-8")
    print(f'Imported {len(ids)} adapter(s) from {tag} ({ "pre-release" if release_data["prerelease"] else "stable" }).')

if __name__ == "__main__":
    main()
