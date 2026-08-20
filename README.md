# Scholz Growth Engine — Website

Mehrseitige Website für SEG: technisches SEO, Google Business Profile und
GEO (Generative Engine Optimization) für Unternehmen jeder Branche.

Statisches HTML, CSS und zwei kurze Skripte. Kein Framework, keine
Laufzeit-Abhängigkeit, keine externen Requests.

---

## ⚠️ Vor der Veröffentlichung ersetzen

Die Seite enthält bewusst erkennbare Platzhalter und darf **nicht** live
gehen, bevor diese ersetzt sind:

| Ort | Was fehlt |
|---|---|
| `src/pages/kontakt.html` | E-Mail, Telefon, Erreichbarkeit (aktuell `kontakt@example.de`, `+49 000 0000000`) |
| `src/schema/start.json` | `address`, `telephone`, `email`, `areaServed`, `priceRange` |
| `src/pages/ueber-uns.html` | Die Menschen dahinter — Name, Werdegang, Foto |
| `src/pages/impressum.html` | Vollständig — Pflicht nach § 5 DDG |
| `src/pages/datenschutz.html` | Hoster, Anschrift, Speicherdauer der Logs |
| `tools/build-site.py` (`SITE`) | Domain — steuert Canonical, Open Graph und JSON-LD |
| `robots.txt`, `sitemap.xml` | Domain |

Bearbeitet wird **immer die Quelle in `src/`**, nie die erzeugte Datei im
Wurzelverzeichnis — die wird beim nächsten Bauen überschrieben.

Impressum und Datenschutzerklärung sind rechtlich verbindliche Texte. Die
hinterlegten Gerüste nennen die üblichen Pflichtangaben, ersetzen aber
keine anwaltliche Prüfung.

Ein Vorschaubild für soziale Netzwerke (`og:image`) fehlt noch — ohne Bild
zeigen Messenger und LinkedIn beim Teilen nur Text.

---

## Bauen

```bash
python3 tools/build-site.py        # Seiten aus src/ erzeugen
python3 tools/build-grafiken.py    # Diagramme neu zeichnen
python3 tools/get-fonts.py         # Schriften laden, fonts.css schreiben
```

`build-site.py` prüft dabei die Metadaten und meldet Titel über 65 und
Beschreibungen außerhalb von 50–160 Zeichen. Google schneidet längere ab;
eine Agentur für Sichtbarkeit sollte sich das nicht leisten.

## Ansehen

```bash
python3 -m http.server 8000
```

Dann <http://localhost:8000> öffnen. `file://` funktioniert nicht — die
Schriften werden dann wegen CORS nicht geladen.

## Aufbau

```
src/shell.html          Kopf- und Fußbereich, einmal für alle Seiten
src/pages/*.html        Inhalt je Seite, mit Kopfblock bis zur Zeile ---
src/ratgeber/*.html     Ratgeberbeiträge
src/schema/*.json       JSON-LD, per "schema:"-Zeile eingebunden

assets/css/main.css     Das gesamte Stylesheet
assets/css/fonts.css    Generiert von tools/get-fonts.py
assets/js/main.js       Bewegung; die Seite läuft auch ohne
assets/js/chrom-gl.js   WebGL-Kugel, wird nur bei Bedarf nachgeladen
assets/img/*.svg        Generiert von tools/build-grafiken.py

index.html … ratgeber/  Erzeugt. Nicht von Hand bearbeiten.
```

Im Seitenkörper stehen zwei Platzhalter zur Verfügung: `{{BASE}}` für den
Pfad zur Wurzel (wichtig in `ratgeber/`) und `{{grafik:name}}`, das eine
Grafik **inline** einsetzt. Inline deshalb, weil im SVG so die Schriften
und CSS-Variablen der Seite greifen — als eigenständig geladene Datei
könnten sie das nicht.

---

## Gestaltung

**Richtung:** fast-schwarzer Grund, Typografie in Plakatgröße, ein
einziges irisierendes Objekt. Die Seite ist monochrom, damit die
Chromkugel und die Ergebnispunkte in den Diagrammen die einzigen Stellen
bleiben, an denen Farbe auftritt.

**Schrift:** Space Grotesk für Überschriften, DM Sans für Fließtext,
DM Mono für Daten und Code. Ausgewählt über die ui-ux-pro-max-Datenbank
(Paarung „Tech Startup“).

**Bewegung:** ausschließlich `transform` und `opacity`, ein Easing für die
ganze Seite (`cubic-bezier(.16, 1, .3, 1)`, entspricht expo.out). Zwischen
Seiten blendet die View-Transitions-API über, wo der Browser sie kann.
`prefers-reduced-motion` schaltet alles ab, einschließlich der Kugel.

### Die Chromkugel

Zwei Fassungen, gestuft:

1. **CSS** — ein rotierender `conic-gradient` unter einer festen
   Kugelbeleuchtung. Kostet keinen einzigen Request, läuft auf jedem
   Gerät flüssig und ist sofort da.
2. **WebGL2** — ein Fragment-Shader mit fließender Verformung, Fresnel und
   spiegelndem Glanz. Rund 6 KB, **ohne three.js**: Für eine einzelne
   Fläche braucht es keinen Szenengraph, ein Dreieck genügt.

Nachgeladen wird die zweite Fassung nur, wenn alle Bedingungen stimmen:
mindestens vier Kerne und 4 GB Speicher, kein Datensparmodus, kein 2G,
kein `prefers-reduced-motion`, WebGL2 vorhanden **und** kein
`failIfMajorPerformanceCaveat` — letzteres schließt Software-Rendering
aus, das sonst ruckeln würde. Gerendert wird bei höchstens 640 px Kante
und gedeckeltem Pixelverhältnis; außerhalb des Sichtfelds und im
Hintergrundtab pausiert die Schleife.

Fällt irgendetwas davon aus, bleibt die CSS-Fassung stehen. Sie ist kein
Notbehelf, sondern sieht eigenständig gut aus.

---

## Geprüft

Automatisiert über alle zwölf Seiten nachgemessen:

- **0 externe Requests**, **0 Cookies**, kein `localStorage`
- **137 KB** Ressourcen gesamt, davon 99 KB Schriften
- Keine 404, keine JavaScript-Fehler
- Genau eine `h1` je Seite, keine Sprünge in der Überschriftenhierarchie
- Titel ≤ 65 Zeichen, Beschreibungen 50–160 Zeichen
- Kein horizontaler Überlauf bei 360, 768 und 1440 px
- **WCAG AA** für alle 18 Text-/Grund-Paare, schwächstes Paar 5,09:1
- Alle Tap-Ziele ≥ 44 px auf Geräten mit grobem Zeiger
- JSON-LD parst; Organization, ProfessionalService, WebSite, FAQPage

Die Zahlen im Abschnitt „Beweis“ auf der Startseite entsprechen diesen
Messungen. Wer sie ändert, sollte vorher nachmessen — eine SEO-Seite mit
falschen Angaben über sich selbst untergräbt genau das Argument, das sie
macht.

---

## Fallstricke, die schon einmal zugeschlagen haben

- **Verlauf auf einer geraden Linie rendert nicht.** Ein `linearGradient`
  in `objectBoundingBox`-Einheiten hat auf einer waagerechten oder
  senkrechten Linie eine Bounding-Box ohne Ausdehnung. Linien in den
  Diagrammen brauchen deshalb Volltonfarben.
- **Diagrammbreite aus dem Raster ableiten, nicht raten.** Eine
  hartkodierte `viewBox`-Breite schnitt die dritte Tafel ab.
- **`<code>` erbt die Schrift nicht vom `<pre>`.** Der Browser-Standard
  schlägt die Vererbung; ohne `.code__leib code { font: inherit }` läuft
  der Block in der Systemschrift.
- **Rasterplätze in der mobilen Kopfzeile explizit setzen.** Die
  Navigation steht im Quelltext vor dem Knopf und schöbe ihn sonst in
  eine dritte Zeile.
- **`.nav` braucht `min-width: 0`**, sonst verweigert das Flex-Element das
  Schrumpfen und `overflow-x` bleibt wirkungslos.
- **Deutsche Komposita** sprengen schmale Viewports. `hyphens: auto` steht
  auf allen Überschriften; bei neuen Überschriften bei 360 px gegenprüfen.

---

## Was bewusst fehlt

Keine erfundenen Referenzen, Kundenlogos, Bewertungen oder Erfolgszahlen.
Erfundener Social Proof auf einer Agenturseite ist rechtlich angreifbar
und fällt auf. Sobald echte Angaben vorliegen, gehören sie als eigene
Seite zwischen „Ergebnisse“ und „Über uns“ — mit `Review`- bzw.
`AggregateRating`-Auszeichnung im JSON-LD.

Kein Kontaktformular. Ein `mailto:`-Link braucht keinen Server, keine
Auftragsverarbeitung und kein Spam-Handling — und hält die Seite frei von
Cookies und Einwilligungsbanner.
