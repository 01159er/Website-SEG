#!/usr/bin/env python3
"""Erzeugt die Diagramme in assets/img/.

Vier Grafiken, eine Bildsprache: gleiche Strichstärke, gleiche Radien,
gleiche Palette. Farbe tritt nur als Verlauf auf — überall dort, wo es
um das Ergebnis geht.

Die Dateien werden von tools/build-site.py per {{grafik:name}} direkt in
die Seiten eingesetzt. Dadurch greifen die Schriften und CSS-Variablen
der Seite im SVG; als <img> eingebunden könnten sie das nicht.

    python3 tools/build-grafiken.py
"""

import math
import pathlib

HIER = pathlib.Path(__file__).resolve().parent.parent
ZIEL = HIER / "assets" / "img"

# --- Palette ---------------------------------------------------------------
GRUND      = "#0B0B10"
FLAECHE    = "#101016"
FLAECHE_2  = "#16161E"
FLAECHE_3  = "#1C1C26"
KANTE      = "#2C2C38"
KANTE_HELL = "#3A3A48"
PAPIER     = "#FAFAFC"
GEDAEMPFT  = "#ADADBC"
LEISE      = "#90909F"

MONO = "'DM Mono', ui-monospace, monospace"
SANS = "'Space Grotesk', system-ui, sans-serif"

COS30, SIN30 = math.cos(math.radians(30)), math.sin(math.radians(30))


def verlauf(kennung, winkel=115):
    """Der irisierende Verlauf, einmal je Datei definiert."""
    rad = math.radians(winkel)
    x2, y2 = math.cos(rad), math.sin(rad)
    return f'''<linearGradient id="{kennung}" x1="0" y1="0" x2="{x2:.3f}" y2="{y2:.3f}">
      <stop offset="0%"   stop-color="#7C6BF5"/>
      <stop offset="32%"  stop-color="#4FD1FF"/>
      <stop offset="52%"  stop-color="#FAFAFC"/>
      <stop offset="72%"  stop-color="#FFB27A"/>
      <stop offset="100%" stop-color="#FF7AC8"/>
    </linearGradient>'''


def kasten(x, y, w, h, fill=FLAECHE, stroke=KANTE, r=10, extra=""):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1"{extra}/>')


def balken(x, y, w, h=8, fill=KANTE_HELL, opacity=1.0):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2:.1f}" '
            f'fill="{fill}" opacity="{opacity}"/>')


def text(x, y, inhalt, groesse=12, fill=GEDAEMPFT, familie=SANS,
         gewicht=400, anker="start", spur=0):
    s = (f'<text x="{x}" y="{y}" font-family="{familie}" font-size="{groesse}" '
         f'font-weight="{gewicht}" fill="{fill}" text-anchor="{anker}"')
    if spur:
        s += f' letter-spacing="{spur}"'
    return s + f'>{inhalt}</text>'


def marke(x, y, inhalt):
    """Kleine Versalien-Beschriftung in Mono."""
    return text(x, y, inhalt.upper(), 9, LEISE, MONO, spur=1.4)


def huelle(breite, hoehe, koerper, titel, defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {breite} {hoehe}"
     role="img" aria-labelledby="t-{titel[0]}" fill="none">
  <title id="t-{titel[0]}">{titel[1]}</title>
  <defs>
    {verlauf("iris")}
    {defs}
  </defs>
  {koerper}
</svg>
'''


# ══ 1 · Der Wandel: Trefferliste gegen Antwort ═══════════════════════════

def wandel():
    t = []
    # linke Tafel — die Trefferliste
    t.append(kasten(0, 40, 300, 300, FLAECHE, KANTE, 14))
    t.append(marke(24, 74, "Bisher · Trefferliste"))
    for i in range(7):
        y = 96 + i * 30
        breit = [214, 168, 190, 146, 202, 158, 178][i]
        if i == 3:
            t.append(balken(24, y, breit, 9, PAPIER, .95))
            t.append(text(24 + breit + 10, y + 8, "Sie", 9, LEISE, MONO, spur=1.2))
        else:
            t.append(balken(24, y, breit, 9, KANTE_HELL, .55))
    t.append(text(24, 322, "Platz 4 von 10 — sichtbar durch Scrollen",
                  11, LEISE, SANS))

    # Pfeil in der Mitte. Bewusst mit Volltonfarbe: Ein Verlauf in
    # objectBoundingBox-Einheiten hat auf einer waagerechten Linie eine
    # Bounding-Box ohne Höhe und rendert dann gar nicht.
    t.append(f'<path d="M330 190 L392 190" stroke="{PAPIER}" stroke-width="1.5" '
             f'opacity="0.55"/>')
    t.append(f'<path d="M384 184 L392 190 L384 196" stroke="{PAPIER}" '
             f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" '
             f'opacity="0.55"/>')
    t.append(text(361, 176, "heute", 9, LEISE, MONO, anker="middle", spur=1.4))

    # rechte Tafel — die eine Antwort
    t.append(kasten(422, 40, 300, 300, FLAECHE_2, KANTE_HELL, 14))
    t.append(marke(446, 74, "Heute · KI-Antwort"))
    for i, breit in enumerate((246, 232, 158)):
        t.append(balken(446, 96 + i * 26, breit, 9, KANTE_HELL, .5))
    # drei genannte Anbieter
    for i, (bx, bw, name) in enumerate(((446, 84, "Anbieter A"),
                                        (540, 84, "Anbieter B"),
                                        (634, 64, "Sie"))):
        aktiv = name == "Sie"
        t.append(f'<rect x="{bx}" y="188" width="{bw}" height="30" rx="15" '
                 f'fill="none" stroke="{"url(#iris)" if aktiv else KANTE_HELL}" '
                 f'stroke-width="{1.5 if aktiv else 1}"/>')
        t.append(text(bx + bw / 2, 208, name, 11, PAPIER if aktiv else LEISE,
                      MONO, anker="middle"))
    for i, breit in enumerate((222, 190)):
        t.append(balken(446, 244 + i * 26, breit, 9, KANTE_HELL, .5))
    t.append(text(446, 322, "Drei Namen — oder keiner", 11, GEDAEMPFT, SANS))

    return huelle(722, 360, "\n  ".join(t),
                  ("wandel", "Vergleich: klassische Trefferliste gegenüber "
                             "einer KI-Antwort, die drei Anbieter namentlich nennt"))


# ══ 2 · Die drei Ebenen ══════════════════════════════════════════════════

def ebenen():
    t = []
    daten = [
        ("Ebene 3", "GEO-Basis", "Antwortsysteme erkennen und nennen Sie", True),
        ("Ebene 2", "Business Profile", "Ortsbezogene Suche und Karte", False),
        ("Ebene 1", "Technisches SEO", "Ladezeit, Auszeichnung, Indexierung", False),
    ]
    for i, (nr, titel, unter, betont) in enumerate(daten):
        y = 24 + i * 112
        # Breiteste Platte unten: Die Grundlage trägt, was darüber liegt.
        # Andersherum widerspräche das Bild der Bildunterschrift.
        einzug = (len(daten) - 1 - i) * 26
        w = 620 - einzug * 2
        t.append(kasten(einzug, y, w, 88, FLAECHE_2 if betont else FLAECHE,
                        KANTE_HELL if betont else KANTE, 12))
        if betont:
            t.append(f'<rect x="{einzug}" y="{y}" width="{w}" height="2" rx="1" '
                     f'fill="url(#iris)"/>')
        t.append(marke(einzug + 24, y + 30, nr))
        t.append(text(einzug + 24, y + 56, titel, 17, PAPIER, SANS, 700))
        t.append(text(einzug + 24, y + 76, unter, 11.5, LEISE, SANS))

    # Tragende Verbindung zwischen den Ebenen
    for i in range(2):
        y = 112 + i * 112
        t.append(f'<path d="M310 {y} L310 {y + 24}" stroke="{KANTE_HELL}" '
                 f'stroke-width="1" stroke-dasharray="3 3"/>')

    t.append(text(310, 372, "Jede Ebene trägt die darüber", 11, LEISE, SANS,
                  anker="middle"))
    return huelle(620, 392, "\n  ".join(t),
                  ("ebenen", "Die drei Leistungsebenen, aufeinander aufbauend: "
                             "technisches SEO, Business Profile, GEO-Basis"))


# ══ 3 · Die Maschine (isometrisch) ═══════════════════════════════════════

_grenzen = [1e9, 1e9, -1e9, -1e9]
EINHEIT = 24


def _pr(x, y, z):
    sx = (x - y) * COS30 * EINHEIT
    sy = (x + y) * SIN30 * EINHEIT - z * EINHEIT
    _grenzen[0] = min(_grenzen[0], sx); _grenzen[1] = min(_grenzen[1], sy)
    _grenzen[2] = max(_grenzen[2], sx); _grenzen[3] = max(_grenzen[3], sy)
    return sx, sy


def _quader(x, y, z, w, d, h, stufe, kante=KANTE_HELL, strich=1.0):
    """Drei sichtbare Flächen (+y, +x, +z) in absteigender Helligkeit."""
    oben, rechts, links = stufe
    flaechen = [
        ([_pr(x, y + d, z), _pr(x + w, y + d, z), _pr(x + w, y + d, z + h), _pr(x, y + d, z + h)], links),
        ([_pr(x + w, y, z), _pr(x + w, y + d, z), _pr(x + w, y + d, z + h), _pr(x + w, y, z + h)], rechts),
        ([_pr(x, y, z + h), _pr(x + w, y, z + h), _pr(x + w, y + d, z + h), _pr(x, y + d, z + h)], oben),
    ]
    aus = []
    for punkte, fuellung in flaechen:
        d_ = " ".join(f"{a:.1f},{b:.1f}" for a, b in punkte)
        aus.append(f'<polygon points="{d_}" fill="{fuellung}" stroke="{kante}" '
                   f'stroke-width="{strich}" stroke-linejoin="round"/>')
    return "\n  ".join(aus)


def maschine():
    global _grenzen
    _grenzen = [1e9, 1e9, -1e9, -1e9]
    t = []

    # Auf fast schwarzem Grund braucht der Körper deutlich mehr Helligkeit
    # als auf einem mittleren Untergrund, sonst verschwindet er.
    STUFEN = {
        "sockel": ("#1E1E27", "#16161D", "#101015"),
        "unten":  ("#2A2A34", "#1F1F27", "#16161C"),
        "mitte":  ("#373742", "#292932", "#1D1D24"),
        "oben":   ("#494957", "#363642", "#25252D"),
    }

    # Bodenraster
    linien = []
    for i in range(12):
        a, b = _pr(-0.5 + i, -0.5, -0.02), _pr(-0.5 + i, 10.5, -0.02)
        c, e = _pr(-0.5, -0.5 + i, -0.02), _pr(10.5, -0.5 + i, -0.02)
        for (sx, sy), (ex, ey) in ((a, b), (c, e)):
            linien.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" '
                          f'y2="{ey:.1f}" stroke="#26262F" stroke-width="0.6"/>')
    t.append('<g opacity="0.55">' + "".join(linien) + '</g>')

    t.append(_quader(0.6, 0.6, -0.45, 8.8, 8.8, 0.45, STUFEN["sockel"], KANTE_HELL))
    # Eingangsbahn
    t.append(_quader(-1.4, 3.55, 1.98, 4.2, 0.9, 0.2, STUFEN["mitte"], KANTE))
    for i in range(4):
        sx, sy = _pr(-1.0 + i * 0.62, 4.0, 2.2)
        t.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="2.6" fill="{PAPIER}" '
                 f'opacity="{0.28 + i * 0.16:.2f}"/>')

    t.append(_quader(1.4, 1.4, 0.0, 7.2, 7.2, 0.5, STUFEN["unten"], KANTE_HELL))
    t.append(_quader(1.9, 1.9, 0.85, 6.2, 6.2, 0.5, STUFEN["mitte"], KANTE_HELL))
    t.append(_quader(2.4, 2.4, 1.65, 5.2, 5.2, 0.5, STUFEN["oben"], "#5C5C6E", 1.2))

    # Bedienfeld
    for i, versatz in enumerate((2.5, 1.3, 2.05)):
        y = 3.2 + i * 1.3
        t.append(_quader(3.1, y, 2.15, 3.3, 0.28, 0.07,
                         ("#191921", "#131319", "#0E0E13"), KANTE))
        t.append(_quader(3.1 + versatz, y - 0.12, 2.15, 0.5, 0.52, 0.3,
                         ("#4A4458", "#332F3E", "#232029"), KANTE_HELL))

    # Ausgangsbahn — hier tritt das Ergebnis aus, deshalb Farbe
    t.append(_quader(8.15, 4.55, 0.3, 3.9, 0.9, 0.2, STUFEN["mitte"], KANTE))
    for i in range(4):
        sx, sy = _pr(9.15 + i * 0.62, 5.0, 0.52)
        t.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="3" fill="url(#iris)" '
                 f'opacity="{0.45 + i * 0.18:.2f}"/>')

    rand = 16
    minx, miny, maxx, maxy = _grenzen
    vb = f"{minx - rand:.0f} {miny - rand:.0f} {maxx - minx + 2 * rand:.0f} {maxy - miny + 2 * rand:.0f}"

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"
     role="img" aria-labelledby="t-maschine" fill="none">
  <title id="t-maschine">Isometrische Darstellung der drei Ebenen als Maschine: Die Anfrage läuft oben ein, die Antwort verlässt sie unten rechts</title>
  <defs>{verlauf("iris")}</defs>
  {"".join(t)}
</svg>
'''


# ══ 4 · Wo Sichtbarkeit entsteht ═════════════════════════════════════════

def flaechen():
    # Breite aus dem Raster ableiten statt sie zu raten — sonst ragt die
    # letzte Tafel aus dem viewBox und wird abgeschnitten.
    TAFEL, ABSTAND, ANZAHL = 190, 24, 3
    BREITE = ANZAHL * TAFEL + (ANZAHL - 1) * ABSTAND
    t = []
    spalten = [
        ("Trefferliste", "Klassische Suche", [(0, 150), (0, 118), (1, 132), (0, 96)]),
        ("Kartenausschnitt", "Ortsbezogene Suche", None),
        ("KI-Antwort", "Antwortsysteme", None),
    ]
    for i, (titel, unter, _) in enumerate(spalten):
        x = i * (TAFEL + ABSTAND)
        t.append(kasten(x, 30, TAFEL, 236, FLAECHE, KANTE, 12))
        t.append(marke(x + 20, 58, unter))
        t.append(text(x + 20, 84, titel, 15, PAPIER, SANS, 700))

        if i == 0:                                   # Trefferliste
            for j, (treffer, breit) in enumerate(((0, 150), (0, 118), (1, 132), (0, 96))):
                y = 112 + j * 26
                t.append(balken(x + 20, y, breit, 8,
                                "url(#iris)" if treffer else KANTE_HELL,
                                1 if treffer else .5))
        elif i == 1:                                 # Karte
            t.append(f'<rect x="{x + 20}" y="112" width="150" height="94" rx="8" '
                     f'fill="{FLAECHE_3}" stroke="{KANTE}"/>')
            for a, b in ((40, 140), (95, 128), (60, 178)):
                t.append(f'<path d="M{x + a} {b} l0 -14" stroke="{KANTE_HELL}" stroke-width="1"/>')
                t.append(f'<circle cx="{x + a}" cy="{b - 18}" r="4" fill="{KANTE_HELL}"/>')
            # Volltonfarbe statt Verlauf: senkrechte Linie, also eine
            # Bounding-Box ohne Breite — ein Verlauf darauf rendert nicht.
            t.append(f'<path d="M{x + 118} 166 l0 -18" stroke="#FFB27A" stroke-width="1.5"/>')
            t.append(f'<circle cx="{x + 118}" cy="144" r="5.5" fill="url(#iris)"/>')
        else:                                        # KI-Antwort
            for j, breit in enumerate((150, 132, 104)):
                t.append(balken(x + 20, 112 + j * 22, breit, 8, KANTE_HELL, .5))
            t.append(f'<rect x="{x + 20}" y="184" width="78" height="26" rx="13" '
                     f'fill="none" stroke="url(#iris)" stroke-width="1.5"/>')
            t.append(text(x + 59, 202, "Sie", 11, PAPIER, MONO, anker="middle"))

        t.append(text(x + 20, 240, "monatlich gemessen", 10, LEISE, MONO, spur=.8))

    return huelle(BREITE, 290, "\n  ".join(t),
                  ("flaechen", "Drei Flächen, auf denen Sichtbarkeit entsteht: "
                               "Trefferliste, Kartenausschnitt und KI-Antwort"))


if __name__ == "__main__":
    ZIEL.mkdir(parents=True, exist_ok=True)
    for name, bauer in (("wandel", wandel), ("ebenen", ebenen),
                        ("maschine", maschine), ("flaechen", flaechen)):
        pfad = ZIEL / f"{name}.svg"
        # Eindeutige Verlaufs-ID je Grafik. Liegen zwei Diagramme auf einer
        # Seite, würden gleiche IDs kollidieren und eines falsch einfärben.
        inhalt = (bauer()
                  .replace('id="iris"', f'id="iris-{name}"')
                  .replace('url(#iris)', f'url(#iris-{name})'))
        pfad.write_text(inhalt, encoding="utf-8")
        print(f"  {name + '.svg':<18} {pfad.stat().st_size // 1024:>3} KB")
    alt = ZIEL / "engine.svg"
    if alt.exists():
        alt.unlink()
        print("  engine.svg entfernt (ersetzt durch maschine.svg)")
