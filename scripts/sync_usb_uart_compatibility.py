#!/usr/bin/env python3
"""Generate bilingual USB-UART compatibility tables and issue-form choices from the central registry."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/usb-uart-compatibility.json"
HU = ROOT / "docs/usb-uart-compatibility.html"
EN = ROOT / "docs/usb-uart-compatibility-en.html"
HU_FORM = ROOT / ".github/ISSUE_TEMPLATE/usb_uart_compatibility.yml"
EN_FORM = ROOT / ".github/ISSUE_TEMPLATE/usb_uart_compatibility_en.yml"
INDEX_HU = ROOT / "docs/index.html"
INDEX_EN = ROOT / "docs/index-en.html"
README_HU = ROOT / "README_HU.md"
README_EN = ROOT / "README.md"

def esc(value):
    return html.escape(str(value), quote=True)

def status_label(adapter, lang):
    status = adapter.get("status", "under_investigation")
    enabled = bool(adapter.get("engine_supported") and adapter.get("app_supported"))
    if status == "verified":
        return ("Igazolt", "verified") if lang == "hu" else ("Verified", "verified")
    if enabled:
        return ("Engine-ben engedélyezve · Tesztelésre vár", "pending") if lang == "hu" else ("Engine enabled · Awaiting test", "pending")
    return ("Engine-integrációra vár", "testing") if lang == "hu" else ("Awaiting engine integration", "testing")

def row(adapter, lang):
    name = esc(adapter["name"])
    chip = esc(adapter.get("chip") or adapter["name"])
    vid = adapter.get("vid")
    pid = adapter.get("pid")
    ids = esc(f"{vid} / {pid}") if vid and pid else ("Eszközfüggő" if lang == "hu" else "Device-dependent")
    label, css = status_label(adapter, lang)
    note = esc(adapter.get("note_hu" if lang == "hu" else "note_en", ""))
    enabled = bool(adapter.get("engine_supported") and adapter.get("app_supported"))
    if adapter.get("status") == "verified":
        alt = "Igazolt" if lang == "hu" else "Verified"
        action = f'<span class="verified-check" role="img" aria-label="{alt}" title="{alt}">✓</span>'
    elif enabled:
        template = "usb_uart_compatibility.yml" if lang == "hu" else "usb_uart_compatibility_en.yml"
        title = "[USB-UART TESZT] " if lang == "hu" else "[USB-UART TEST] "
        title += adapter["name"]
        label_button = "Tesztjelentés küldése" if lang == "hu" else "Submit test report"
        url = "https://github.com/szotsy/Zello-Android-Radio-Gateway/issues/new?template=" + template + "&title=" + __import__("urllib.parse", fromlist=["quote"]).quote(title)
        action = f'<a class="report-link" href="{esc(url)}" target="_blank" rel="noopener">{label_button}</a>'
    else:
        msg = "Az engine-integráció után tesztelhető." if lang == "hu" else "Test submission will be available after engine integration."
        action = f"<small>{msg}</small>"
    return f'<tr><td><strong>{name}</strong><br><small>{chip} USB–UART</small></td><td>{ids}</td><td class="status {css}">{esc(label)}</td><td>{note}</td><td>{action}</td></tr>'

def replace_between(text, start, end, replacement, file):
    if start not in text or end not in text:
        raise SystemExit(f"Missing generation markers in {file}")
    before, rest = text.split(start, 1)
    _, after = rest.split(end, 1)
    return before + start + "\n" + "\n".join(replacement) + "\n" + end + after

def update_html(path, adapters, lang):
    text = path.read_text(encoding="utf-8")
    text = replace_between(text, "<!-- USB_UART_ROWS_START -->", "<!-- USB_UART_ROWS_END -->",
                           [row(a, lang) for a in adapters], path)
    path.write_text(text, encoding="utf-8")

def update_form(path, adapters):
    text = path.read_text(encoding="utf-8")
    options = [f'        - "{a["name"].replace(chr(34), chr(92)+chr(34))}"'
               for a in adapters if a.get("engine_supported") and a.get("app_supported")]
    text = replace_between(text, "      # USB_UART_OPTIONS_START", "      # USB_UART_OPTIONS_END",
                           options, path)
    path.write_text(text, encoding="utf-8")


def update_tested_devices(data):
    devices = data.get("tested_devices")
    if not isinstance(devices, list) or not devices:
        raise SystemExit("Registry must contain a non-empty tested_devices array")

    names = []
    for device in devices:
        if not isinstance(device, dict) or not device.get("name"):
            raise SystemExit(f"Invalid tested device entry: {device}")
        names.append(str(device["name"]).strip())
    if any(not name for name in names) or len({name.casefold() for name in names}) != len(names):
        raise SystemExit("Tested device names must be non-empty and unique")

    for path in (INDEX_HU, INDEX_EN):
        text = path.read_text(encoding="utf-8")
        device_list = "<br>".join(esc(name) for name in names)
        text = replace_between(text, "<!-- TESTED_DEVICES_START -->",
                               "<!-- TESTED_DEVICES_END -->", [device_list], path)
        path.write_text(text, encoding="utf-8")

    for path, lang in ((README_HU, "hu"), (README_EN, "en")):
        text = path.read_text(encoding="utf-8")
        if lang == "hu":
            rows = ["| Készülék | Tesztállapot |", "|---|---|"]
            rows.extend(f"| {esc(name)} | Tesztelve |" for name in names)
        else:
            rows = ["| Device | Test status |", "|---|---|"]
            rows.extend(f"| {esc(name)} | Tested |" for name in names)
        text = replace_between(text, "<!-- TESTED_DEVICES_TABLE_START -->",
                               "<!-- TESTED_DEVICES_TABLE_END -->", rows, path)
        path.write_text(text, encoding="utf-8")

def main():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    adapters = data.get("adapters")
    if not isinstance(adapters, list) or not adapters:
        raise SystemExit("Registry must contain a non-empty adapters array")

    manifest_path = ROOT / "app/src/main/assets/usb-uart-adapters.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    engine_adapters = manifest.get("adapters")
    if not isinstance(engine_adapters, list):
        raise SystemExit("Engine manifest must contain an adapters array")

    by_vid_pid = {}
    for item in engine_adapters:
        vid = str(item.get("vid", "")).upper().replace("0X", "")
        pid = str(item.get("pid", "")).upper().replace("0X", "")
        if not item.get("id") or not item.get("display_name") or len(vid) != 4 or len(pid) != 4:
            raise SystemExit(f"Invalid engine adapter profile: {item}")
        if item.get("engine_supported") is not True:
            raise SystemExit(f"Manifest entry is present but engine_supported is not true: {item.get('id')}")
        key = (vid, pid)
        if key in by_vid_pid:
            raise SystemExit(f"Duplicate engine VID/PID: {vid}:{pid}")
        by_vid_pid[key] = item

    registry_by_vid_pid = {}
    for adapter in adapters:
        if adapter.get("vid") and adapter.get("pid"):
            registry_by_vid_pid[(str(adapter["vid"]).upper(), str(adapter["pid"]).upper())] = adapter

    for adapter in adapters:
        key = (str(adapter.get("vid") or "").upper(), str(adapter.get("pid") or "").upper())
        engine_item = by_vid_pid.get(key)
        adapter["engine_supported"] = engine_item is not None
        adapter["app_supported"] = engine_item is not None
        if engine_item:
            adapter["vid"], adapter["pid"] = key

    for (vid, pid), item in by_vid_pid.items():
        if (vid, pid) not in registry_by_vid_pid:
            created = {
                "name": item["display_name"],
                "chip": item["display_name"],
                "vid": vid,
                "pid": pid,
                "status": "not_verified",
                "note_hu": "Az alkalmazás közös USB-UART engine-je támogatja; fizikai adapterteszt még nincs jóváhagyva.",
                "note_en": "Supported by the common application USB-UART engine; physical adapter testing has not yet been approved.",
                "app_supported": True,
                "engine_supported": True
            }
            adapters.append(created)
            registry_by_vid_pid[(vid, pid)] = created

    names = set()
    for a in adapters:
        if not a.get("name") or not a.get("chip"):
            raise SystemExit(f"Adapter is missing name/chip: {a}")
        key = a["name"].casefold()
        if key in names:
            raise SystemExit(f"Duplicate adapter name: {a['name']}")
        names.add(key)

    update_html(HU, adapters, "hu")
    update_html(EN, adapters, "en")
    update_form(HU_FORM, adapters)
    update_form(EN_FORM, adapters)
    update_tested_devices(data)
    print(f"Generated compatibility pages, issue forms and tested-device lists; {len(by_vid_pid)} adapters enabled in engine.")

if __name__ == "__main__":
    main()
