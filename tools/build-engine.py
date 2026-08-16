#!/usr/bin/env python3
"""Erzeugt assets/img/engine.svg — die isometrische Maschine im Hero.

Echte isometrische Projektion:
    sx = (x - y) * cos(30°)
    sy = (x + y) * sin(30°) - z

Gezeichnet wird nach dem Maleralgorithmus: hintere Körper zuerst.
Jeder Quader zeigt genau die drei sichtbaren Flächen (+x, +y, +z).
Die drei Ebenen stehen für die drei Leistungen und werden nach oben
hin heller — oben tritt die Anfrage ein, unten verlässt die Antwort
die Maschine.

    python3 tools/build-engine.py
"""

import math
import pathlib

COS30 = math.cos(math.radians(30))
SIN30 = math.sin(math.radians(30))
UNIT = 26  # Pixel je Welteinheit

# --- Palette (deckungsgleich mit assets/css/main.css) -----------------------
# Jede Ebene: Deckfläche, +x-Fläche, +y-Fläche, Kante.
# Nach oben hin heller — oben tritt die Anfrage ein.
TIERS = {
    "sockel": ("#221E3C", "#191631", "#121026", "#3B3468"),
    "unten":  ("#2B2550", "#201B41", "#171331", "#463D82"),
    "mitte":  ("#372E6B", "#291F55", "#1D1642", "#564A9C"),
    "oben":   ("#4B3F92", "#372C72", "#261D55", "#7C6BF5"),
}
RAIL = ("#2A2549", "#1F1A38", "#161228", "#463D82")
TRACK = ("#372E6B", "#2A2152", "#201741", "#564A9C")
KNOB = ("#8E7FFF", "#5F4CD6", "#43339E", "#B4A9FF")

INDIGO = "#7C6BF5"
PFIRSICH = "#FFAD7A"
RASTER = "#312A57"

_bounds = [1e9, 1e9, -1e9, -1e9]  # minx, miny, maxx, maxy


def project(x, y, z):
    sx = (x - y) * COS30 * UNIT
    sy = (x + y) * SIN30 * UNIT - z * UNIT
    _bounds[0] = min(_bounds[0], sx)
    _bounds[1] = min(_bounds[1], sy)
    _bounds[2] = max(_bounds[2], sx)
    _bounds[3] = max(_bounds[3], sy)
    return sx, sy


def poly(points, fill, stroke, width=1.0):
    d = " ".join(f"{px:.2f},{py:.2f}" for px, py in points)
    return (
        f'<polygon points="{d}" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="{width}" stroke-linejoin="round"/>'
    )


def box(x, y, z, w, d, h, tier, width=1.0):
    """Ein Quader mit seinen drei sichtbaren Flächen (+y, +x, +z)."""
    top, right, left, edge = tier
    p = project
    faces = [
        ([p(x, y + d, z), p(x + w, y + d, z), p(x + w, y + d, z + h), p(x, y + d, z + h)], left),
        ([p(x + w, y, z), p(x + w, y + d, z), p(x + w, y + d, z + h), p(x + w, y, z + h)], right),
        ([p(x, y, z + h), p(x + w, y, z + h), p(x + w, y + d, z + h), p(x, y + d, z + h)], top),
    ]
    return "\n    ".join(poly(pts, fill, edge, width) for pts, fill in faces)


def grid_floor(x0, y0, size, step, z=0.0):
    """Feines Bodenraster — gibt der Szene Maßstab, ohne zu dominieren."""
    lines = []
    n = int(size / step)
    for i in range(n + 1):
        for (sx, sy), (ex, ey) in (
            (project(x0 + i * step, y0, z), project(x0 + i * step, y0 + size, z)),
            (project(x0, y0 + i * step, z), project(x0 + size, y0 + i * step, z)),
        ):
            lines.append(
                f'<line x1="{sx:.2f}" y1="{sy:.2f}" x2="{ex:.2f}" y2="{ey:.2f}" '
                f'stroke="{RASTER}" stroke-width="0.7"/>'
            )
    return "\n    ".join(lines)


def dot(x, y, z, r, fill, cls=None):
    sx, sy = project(x, y, z)
    c = f' class="{cls}"' if cls else ""
    return f'<circle cx="{sx:.2f}" cy="{sy:.2f}" r="{r * UNIT:.2f}" fill="{fill}"{c}/>'


def group(*bodies):
    return "<g>\n    " + "\n    ".join(bodies) + "\n  </g>"


def build():
    parts = []

    # Bodenraster — knapp gehalten, damit die Maschine den Zuschnitt füllt
    parts.append(f'<g opacity="0.65">\n    {grid_floor(-0.6, -0.6, 11.2, 1.0, -0.02)}\n  </g>')

    # --- Sockel ------------------------------------------------------------
    parts.append(group(box(0.6, 0.6, -0.5, 8.8, 8.8, 0.5, TIERS["sockel"])))

    # --- Eingangsbahn: läuft von links oben in die oberste Ebene -----------
    # Deckfläche bündig mit der Oberkante der obersten Ebene (z = 2.2).
    parts.append(group(box(-1.4, 3.55, 1.98, 4.2, 0.9, 0.22, RAIL)))
    parts.append(
        group(*(dot(-1.0 + i * 0.62, 4.0, 2.21, 0.1, INDIGO, "eng-in") for i in range(4)))
    )

    # --- Drei Ebenen, gestapelt und nach oben hin heller --------------------
    parts.append(group(box(1.4, 1.4, 0.0, 7.2, 7.2, 0.55, TIERS["unten"])))
    for px, py in ((2.15, 2.15), (2.15, 6.85), (6.85, 2.15), (6.85, 6.85)):
        parts.append(group(box(px, py, 0.55, 0.34, 0.34, 0.35, RAIL)))

    parts.append(group(box(1.9, 1.9, 0.9, 6.2, 6.2, 0.55, TIERS["mitte"])))
    for px, py in ((2.65, 2.65), (2.65, 6.35), (6.35, 2.65), (6.35, 6.35)):
        parts.append(group(box(px, py, 1.45, 0.34, 0.34, 0.25, RAIL)))

    parts.append(group(box(2.4, 2.4, 1.7, 5.2, 5.2, 0.5, TIERS["oben"], 1.2)))

    # --- Bedienfeld auf der obersten Ebene: drei Stellschrauben -------------
    for i, versatz in enumerate((2.55, 1.35, 2.1)):
        y = 3.25 + i * 1.3
        parts.append(group(box(3.15, y, 2.2, 3.3, 0.3, 0.08, TRACK)))
        parts.append(group(box(3.15 + versatz, y - 0.12, 2.2, 0.52, 0.54, 0.32, KNOB)))

    # --- Ausgangsbahn: verlässt die unterste Ebene nach rechts -------------
    parts.append(group(box(8.15, 4.55, 0.33, 3.9, 0.9, 0.22, RAIL)))
    parts.append(group(box(11.1, 4.85, -0.5, 0.3, 0.3, 0.83, RAIL)))  # Stütze
    parts.append(
        group(*(dot(9.15 + i * 0.62, 5.0, 0.56, 0.1, PFIRSICH, "eng-out") for i in range(4)))
    )

    body = "\n  ".join(parts)

    pad = 8
    minx, miny, maxx, maxy = _bounds
    vb = (minx - pad, miny - pad, (maxx - minx) + 2 * pad, (maxy - miny) + 2 * pad)

    # Die Animation liegt im SVG selbst, damit sie auch als <img> läuft.
    style = """<style>
    .eng-in, .eng-out { opacity: 0 }
    .eng-in  { animation: eng-in  3.6s linear infinite }
    .eng-out { animation: eng-out 3.6s linear infinite }
    .eng-in:nth-of-type(2), .eng-out:nth-of-type(2) { animation-delay: .18s }
    .eng-in:nth-of-type(3), .eng-out:nth-of-type(3) { animation-delay: .36s }
    .eng-in:nth-of-type(4), .eng-out:nth-of-type(4) { animation-delay: .54s }
    @keyframes eng-in  { 0%,4% { opacity: 0 } 12%,30% { opacity: 1 } 42%,100% { opacity: 0 } }
    @keyframes eng-out { 0%,52% { opacity: 0 } 60%,80% { opacity: 1 } 92%,100% { opacity: 0 } }
    @media (prefers-reduced-motion: reduce) {
      .eng-in, .eng-out { opacity: .85; animation: none }
    }
  </style>"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="{vb[0]:.1f} {vb[1]:.1f} {vb[2]:.1f} {vb[3]:.1f}"
     fill="none" role="img" aria-hidden="true">
  <title>Isometrische Darstellung der Growth Engine</title>
  {style}
  {body}
</svg>
"""


if __name__ == "__main__":
    here = pathlib.Path(__file__).resolve().parent.parent
    out = here / "assets" / "img" / "engine.svg"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(), encoding="utf-8")
    print(f"{out.relative_to(here)} — {out.stat().st_size // 1024} KB")
