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
    return before + start + "\n".join(replacement) + end + after

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

def main():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    adapters = data.get("adapters")
    if not isinstance(adapters, list) or not adapters:
        raise SystemExit("Registry must contain a non-empty adapters array")
    names = set()
    for a in adapters:
        if not a.get("name") or not a.get("chip"):
            raise SystemExit(f"Adapter is missing name/chip: {a}")
        key = a["name"].casefold()
        if key in names:
            raise SystemExit(f"Duplicate adapter name: {a['name']}")
        names.add(key)
        if a.get("engine_supported") and a.get("app_supported"):
            if not a.get("vid") or not a.get("pid"):
                raise SystemExit(f"Engine-enabled adapter requires VID/PID: {a['name']}")
    update_html(HU, adapters, "hu")
    update_html(EN, adapters, "en")
    update_form(HU_FORM, adapters)
    update_form(EN_FORM, adapters)
    print(f"Generated compatibility pages and issue forms for {len(adapters)} adapters.")

if __name__ == "__main__":
    main()
