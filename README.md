# Scholz Growth Engine — Website

Einseitige Website für SEG: technisches SEO, Google Business Profile und
GEO (Generative Engine Optimization) für regional tätige Fachbetriebe.

Statisches HTML, CSS und ein kurzes Skript. Kein Framework, kein Build-Schritt,
keine Abhängigkeiten zur Laufzeit.

---

## ⚠️ Vor der Veröffentlichung ersetzen

Die Seite enthält bewusst erkennbare Platzhalter. Sie darf **nicht** live gehen,
bevor diese ersetzt sind:

| Ort | Was fehlt |
|---|---|
| `index.html` — Abschnitt Kontakt | E-Mail und Telefonnummer (aktuell `kontakt@example.de`, `+49 000 0000000`) |
| `index.html` — JSON-LD am Dateiende | `address`, `telephone`, `email`, `areaServed`, `priceRange` |
| `index.html` — `<head>` | Domain in `canonical` und den Open-Graph-Angaben |
| `impressum.html` | Vollständig — Pflicht nach § 5 DDG |
| `datenschutz.html` | Hoster, Anschrift, Speicherdauer der Logs |
| `robots.txt`, `sitemap.xml` | Domain |

Impressum und Datenschutzerklärung sind rechtlich verbindliche Texte.
Die hinterlegten Gerüste nennen die üblichen Pflichtangaben, ersetzen aber
keine anwaltliche Prüfung.

Ein Vorschaubild für Social Media (`og:image`) fehlt noch — ohne
Bild zeigen Messenger und soziale Netzwerke beim Teilen nur den Text.

---

## Aufbau

```
index.html            Die gesamte Seite
impressum.html        Gerüst, auszufüllen
datenschutz.html      Gerüst, auszufüllen
robots.txt            Crawler ausdrücklich zugelassen, auch die der KI-Anbieter
sitemap.xml
favicon.svg

assets/
  css/fonts.css       @font-face für die drei selbst gehosteten Schriften
  css/main.css        Das gesamte Stylesheet
  fonts/*.woff2       Archivo, Instrument Sans, Martian Mono (nur Latin)
  img/engine.svg      Die isometrische Maschine — generiert, nicht von Hand
  js/main.js          Einblenden beim Scrollen, rein optional

tools/build-engine.py Generator für engine.svg
```

## Ansehen

```bash
python3 -m http.server 8000
```

Dann <http://localhost:8000> öffnen. `file://` funktioniert nicht — die
Schriften werden dann wegen CORS nicht geladen.

## Die Maschine neu erzeugen

`assets/img/engine.svg` ist generiert. Änderungen an der Illustration gehören
in den Generator, nicht ins SVG:

```bash
python3 tools/build-engine.py
```

Das Skript projiziert Quader echt isometrisch (`sx = (x−y)·cos30`,
`sy = (x+y)·sin30 − z`) und zeichnet sie nach dem Maleralgorithmus von hinten
nach vorne. Jeder Körper zeigt genau die drei sichtbaren Flächen. Die Palette
oben im Skript ist deckungsgleich mit den CSS-Variablen — beide müssen
gemeinsam geändert werden.

---

## Gestaltung

**Leitidee:** Die Maschine im Hero *ist* das Versprechen. Links läuft eine
Suchanfrage ein, rechts kommt eine KI-Antwort heraus, die den Kunden nennt.
Die drei gestapelten Ebenen sind die drei Leistungen — die unterste trägt,
die oberste ist beleuchtet.

**Breite als Hierarchie.** Alle drei Schriften sind Variable Fonts mit
Breitenachse, und die Breite kodiert die Rolle:

| Rolle | Schrift | Breite |
|---|---|---|
| Überschriften | Archivo | 125 % (Expanded) |
| Fließtext | Instrument Sans | normal, von Natur aus schmal |
| Daten, Labels, Code | Martian Mono | 87,5 % |

Das greift die gestapelten Platten der Maschine auf: unterschiedliche
Grundflächen, gleiche Bauweise.

**Farbe.** Violett führt und markiert alles, was zur Maschine gehört.
Bernstein ist ausschließlich dem *Ergebnis* vorbehalten — der Nennung in der
Antwort, den Laufpunkten am Ausgang, den Kontaktpunkten. Es taucht nirgends
dekorativ auf. Der Grund ist nie reines Schwarz, sondern `#08070E` mit
Violettstich.

**Bewegung.** Nur die Laufpunkte im SVG bewegen sich, plus ein Puls am
Quellen-Punkt. Beide Hero-Karten stehen dauerhaft: Die Aussage muss auch
im Standbild lesbar sein. `prefers-reduced-motion` schaltet alles ab.

---

## Geprüft

Automatisiert nachgemessen, nicht geschätzt:

- **0 externe Requests** — Schriften liegen lokal, keine Fremdskripte, kein Tracker
- **0 Cookies**, kein `localStorage` → kein Einwilligungsbanner nötig
- **JSON-LD parst** und liefert vier Typen: Organization, ProfessionalService,
  WebSite, FAQPage
- **Kein horizontaler Überlauf** bei 360, 768 und 1440 px
- **WCAG AA** für alle Text-/Grund-Kombinationen (schwächstes Paar 4,73:1)
- Genau eine `h1`, keine Sprünge in der Überschriftenhierarchie
- Alle Bilder mit `alt`, alle Links mit zugänglichem Namen, `lang="de"`

Die Zahlen im Abschnitt „Beweis" auf der Seite entsprechen diesen Messungen.
Wer sie ändert, sollte sie vorher nachmessen — eine SEO-Seite mit falschen
Angaben über sich selbst untergräbt genau das Argument, das sie macht.

### Deutsche Typografie

`hyphens: auto` steht auf allen Überschriften und Fließtexten. Ohne das
sprengen Komposita wie „Arbeitsprobe" oder „Antwortschicht" schmale
Viewports — bei Archivo Expanded schon bei 360 px. Wer Überschriften
ergänzt, sollte bei 360 px gegenprüfen.

---

## Was bewusst fehlt

Keine erfundenen Referenzen, Kundenlogos, Bewertungen oder Fallzahlen.
Sobald echte vorliegen, gehören sie zwischen „Ablauf" und „Beweis" —
mit `Review`- bzw. `AggregateRating`-Auszeichnung im JSON-LD.

Kein Kontaktformular. Ein `mailto:`-Link braucht keinen Server, keine
Auftragsverarbeitung und kein Spam-Handling. Sobald ein Formular
gewünscht ist, kommt beides dazu.
