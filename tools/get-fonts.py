#!/usr/bin/env python3
"""Lädt die Schriften und schreibt assets/css/fonts.css.

Auswahl nach der ui-ux-pro-max-Datenbank (Paarung „Tech Startup“):
Space Grotesk für Überschriften, DM Sans für Fließtext. Ergänzt um
DM Mono — DM Sans und DM Mono sind als Familie aufeinander abgestimmt.

    python3 tools/get-fonts.py
"""

import re
import subprocess
import pathlib

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

# slug -> (Google-Fonts-Spezifikation, erwartete Schnitte)
FAMILIEN = {
    "space-grotesk": "Space+Grotesk:wght@400..700",
    "dm-sans":       "DM+Sans:opsz,wght@9..40,400..700",
    "dm-mono":       "DM+Mono:wght@400",
}

HIER = pathlib.Path(__file__).resolve().parent.parent


def hole(spec, slug, ziel):
    url = f"https://fonts.googleapis.com/css2?family={spec}&display=swap"
    css = subprocess.run(
        ["curl", "-sS", "--max-time", "30", "-H", f"User-Agent: {UA}", url],
        capture_output=True, text=True, check=True).stdout

    bloecke = re.findall(r"/\*\s*([\w\[\]-]+)\s*\*/\s*(@font-face\s*\{.*?\})", css, re.S)
    heraus = []
    for name, block in bloecke:
        if name != "latin":
            continue
        m = re.search(r"url\((https://[^)]+\.woff2)\)", block)
        if not m:
            continue
        datei = ziel / f"{slug}.woff2"
        subprocess.run(["curl", "-sS", "--max-time", "30", "-o", str(datei), m.group(1)],
                       check=True)
        block = block.replace(m.group(1), f"../fonts/{datei.name}")
        block = re.sub(r"\n\s*unicode-range:[^;]+;", "", block)
        heraus.append(block.strip())
        print(f"  {slug:<15} {datei.stat().st_size // 1024:>3} KB")
    return heraus


def main():
    ziel = HIER / "assets" / "fonts"
    ziel.mkdir(parents=True, exist_ok=True)
    for alt in ziel.glob("*.woff2"):
        if alt.stem not in FAMILIEN:
            alt.unlink()
            print(f"  entfernt: {alt.name}")

    teile = []
    for slug, spec in FAMILIEN.items():
        teile += hole(spec, slug, ziel)

    kopf = ("/* Selbstgehostet — keine externen Requests.\n"
            "   Erzeugt von tools/get-fonts.py, nicht von Hand bearbeiten. */\n\n")
    (HIER / "assets" / "css" / "fonts.css").write_text(kopf + "\n\n".join(teile) + "\n")
    print(f"  fonts.css geschrieben ({len(teile)} @font-face)")


if __name__ == "__main__":
    main()
