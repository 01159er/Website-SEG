#!/usr/bin/env python3
"""Setzt die statischen Seiten aus src/ zusammen.

Elf Seiten teilen sich Kopf- und Fußbereich. Statt sie elfmal zu pflegen,
liegt die Hülle in src/shell.html und der Inhalt je Seite in src/pages/
bzw. src/ratgeber/. Heraus fallen fertige HTML-Dateien ohne Laufzeit-
Abhängigkeit — der Generator läuft beim Bauen, nicht beim Besuch.

Kopf jeder Seitendatei (bis zur Zeile ---):

    title: Seitentitel
    desc:  Meta-Beschreibung
    nav:   Kennung des aktiven Navigationspunkts
    path:  Ausgabepfad relativ zum Wurzelverzeichnis
    ogtype: website | article        (optional, Standard website)
    schema: name-der-schema-datei    (optional, aus src/schema/)

    python3 tools/build-site.py
"""

import pathlib
import re
import sys

HIER = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://scholz-growth-engine.de"


def lies_seite(datei):
    text = datei.read_text(encoding="utf-8")
    if "\n---\n" not in text:
        sys.exit(f"FEHLER: {datei} hat keinen Kopf (Trennzeile ---)")
    kopf_text, koerper = text.split("\n---\n", 1)
    kopf = {}
    for zeile in kopf_text.strip().splitlines():
        if not zeile.strip() or ":" not in zeile:
            continue
        schluessel, wert = zeile.split(":", 1)
        kopf[schluessel.strip()] = wert.strip()
    for pflicht in ("title", "desc", "path"):
        if pflicht not in kopf:
            sys.exit(f"FEHLER: {datei} fehlt '{pflicht}' im Kopf")
    return kopf, koerper


def setze_grafiken(koerper, quelle):
    """Ersetzt {{grafik:name}} durch den Inhalt von assets/img/name.svg.

    Inline statt <img>, damit die Schriften und CSS-Variablen der Seite
    im SVG greifen — als eigenständige Datei geladen könnten sie das nicht.
    """
    def ersetze(treffer):
        name = treffer.group(1)
        pfad = HIER / "assets" / "img" / f"{name}.svg"
        if not pfad.exists():
            sys.exit(f"FEHLER: {quelle} verweist auf fehlende Grafik {pfad}")
        return pfad.read_text(encoding="utf-8").strip()

    return re.sub(r"\{\{grafik:([a-z0-9-]+)\}\}", ersetze, koerper)


def main():
    huelle = (HIER / "src" / "shell.html").read_text(encoding="utf-8")
    schema_ordner = HIER / "src" / "schema"

    warnungen = []
    quellen = sorted((HIER / "src" / "pages").glob("*.html"))
    quellen += sorted((HIER / "src" / "ratgeber").glob("*.html"))
    if not quellen:
        sys.exit("FEHLER: keine Seiten in src/pages/ gefunden")

    for quelle in quellen:
        kopf, koerper = lies_seite(quelle)
        koerper = setze_grafiken(koerper, quelle)
        ziel = HIER / kopf["path"]

        # Wie viele Ebenen liegt die Seite unter der Wurzel?
        tiefe = len(pathlib.PurePosixPath(kopf["path"]).parts) - 1
        basis = "../" * tiefe

        schema = ""
        if kopf.get("schema"):
            pfad = schema_ordner / f"{kopf['schema']}.json"
            if not pfad.exists():
                sys.exit(f"FEHLER: {quelle} verweist auf fehlende Schema-Datei {pfad}")
            inhalt = pfad.read_text(encoding="utf-8").replace("{{SITE}}", SITE)
            schema = ('<script type="application/ld+json">\n'
                      + inhalt.strip() + "\n</script>")

        seite = huelle
        # Der Körper kommt zuerst, damit {{BASE}} auch darin ersetzt wird.
        for platzhalter, wert in (
            ("{{BODY}}", koerper.rstrip()),
            ("{{TITLE}}", kopf["title"]),
            ("{{DESC}}", kopf["desc"]),
            ("{{NAV}}", kopf.get("nav", "")),
            ("{{PATH}}", kopf["path"] if kopf["path"] != "index.html" else ""),
            ("{{OGTYPE}}", kopf.get("ogtype", "website")),
            ("{{BASE}}", basis),
            ("{{SITE}}", SITE),
            ("{{SCHEMA}}", schema),
        ):
            seite = seite.replace(platzhalter, wert)

        uebrig = [t for t in ("{{TITLE}}", "{{BODY}}", "{{BASE}}") if t in seite]
        if uebrig:
            sys.exit(f"FEHLER: {ziel} enthält noch Platzhalter {uebrig}")

        ziel.parent.mkdir(parents=True, exist_ok=True)
        ziel.write_text(seite, encoding="utf-8")

        # Eine Agentur für Sichtbarkeit darf sich abgeschnittene Titel nicht
        # leisten. Google kürzt Titel jenseits von rund 65 Zeichen und
        # Beschreibungen jenseits von rund 160.
        hinweise = []
        if len(kopf["title"]) > 65:
            hinweise.append(f"Titel {len(kopf['title'])} Zeichen (max. 65)")
        if not 50 <= len(kopf["desc"]) <= 160:
            hinweise.append(f"Beschreibung {len(kopf['desc'])} Zeichen (50-160)")
        warnungen.extend(f"{kopf['path']}: {h}" for h in hinweise)

        zeichen = "!" if hinweise else " "
        print(f" {zeichen} {kopf['path']:<34} {len(seite) // 1024:>3} KB")

    print(f"  {len(quellen)} Seiten gebaut")
    if warnungen:
        print("\n  Metadaten prüfen:")
        for w in warnungen:
            print(f"    ! {w}")


if __name__ == "__main__":
    main()
