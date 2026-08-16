# Scholz Growth Engine — Website

Einseitige Website für SEG: technisches SEO, Google Business Profile und
GEO (Generative Engine Optimization) für regional tätige Fachbetriebe.

Das Angebot richtet sich an Unternehmen jeder Branche — Handwerk, Handel,
Gesundheit, Beratung, Gastronomie, Industrie, Bildung. Einzelne Branchen
kommen nur als Beispiel vor, nie als Einschränkung.

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
  css/fonts.css       Generiert — @font-face der drei Schriften
  css/main.css        Das gesamte Stylesheet
  fonts/*.woff2       Space Grotesk, DM Sans, DM Mono (nur Latin)
  img/engine.svg      Die isometrische Maschine — generiert, nicht von Hand
  js/main.js          Einblenden beim Scrollen, rein optional

tools/build-engine.py Generator für engine.svg
tools/get-fonts.py    Lädt die Schriften und schreibt fonts.css
```

## Ansehen

```bash
python3 -m http.server 8000
```

Dann <http://localhost:8000> öffnen. `file://` funktioniert nicht — die
Schriften werden dann wegen CORS nicht geladen.

## Schriften neu laden

`assets/css/fonts.css` ist generiert. Zum Wechseln einer Schrift die
Familien oben in `tools/get-fonts.py` ändern und laufen lassen:

```bash
python3 tools/get-fonts.py
```

Das Skript lädt nur den Latin-Schnitt, entfernt nicht mehr benötigte
Dateien und schreibt `fonts.css` neu. Danach die `preload`-Verweise im
`<head>` von `index.html` prüfen — sie zeigen auf konkrete Dateinamen.

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

**Schrift.** Ausgewählt über die ui-ux-pro-max-Datenbank (Paarung
„Tech Startup"), erzeugt von `tools/get-fonts.py`:

| Rolle | Schrift |
|---|---|
| Überschriften | Space Grotesk |
| Fließtext | DM Sans |
| Daten, Labels, Code | DM Mono |

Space Grotesk ist geometrisch mit flachen Endungen und einem eigenwilligen G,
DM Sans rund und offen. Die Paarung stellt Präzision neben Zugänglichkeit —
genau das ist das Angebot. DM Sans und DM Mono sind als Familie aufeinander
abgestimmt.

**Farbe.** Der Grund ist kein Schwarz, sondern ein tiefes Indigo-Pflaume
(`#13111F`). Indigo führt, Pfirsich markiert ausschließlich das *Ergebnis* —
die Nennung in der Antwort, die Laufpunkte am Ausgang —, Mint bestätigt.
Drei Töne statt eines grellen Akzents auf Schwarz.

Der Indigo-Grundton ist `#6353E0` und nicht heller, weil weiße Schrift auf
dem Knopf sonst unter 4,5:1 fällt. Für Text auf dunklem Grund gibt es das
hellere `--indigo-weich`; `--indigo-tief` ist ausschließlich für Verläufe
und trägt nie Schrift.

**Radien.** 16 px für Karten, 10 px für Knöpfe — der wirksamste Hebel
gegen einen strengen Eindruck.

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
- **WCAG AA** für alle 19 Text-/Grund-Kombinationen (schwächstes Paar 4,77:1;
  die Schrittnummern gelten als Großtext und liegen bei 3,17:1)
- Genau eine `h1`, keine Sprünge in der Überschriftenhierarchie
- Alle Bilder mit `alt`, alle Links mit zugänglichem Namen, `lang="de"`

Die Zahlen im Abschnitt „Beweis" auf der Seite entsprechen diesen Messungen.
Wer sie ändert, sollte sie vorher nachmessen — eine SEO-Seite mit falschen
Angaben über sich selbst untergräbt genau das Argument, das sie macht.

### Fallstricke, die schon einmal zugeschlagen haben

- `<code>` bekommt vom Browser eine eigene Schrift und ignoriert die
  Vererbung vom `<pre>`. Ohne `.code__leib code { font: inherit }` läuft
  der Codeblock nicht in DM Mono.
- In der mobilen Kopfzeile stehen die Rasterplätze explizit. Die Navigation
  steht im Quelltext vor dem Knopf und schöbe ihn sonst in eine dritte Zeile.
- `.nav` braucht `min-width: 0`, sonst verweigert das Flex-Element das
  Schrumpfen und `overflow-x` bleibt wirkungslos.

### Deutsche Typografie

`hyphens: auto` steht auf allen Überschriften und Fließtexten. Ohne das
sprengen Komposita wie „Arbeitsprobe" oder „Antwortschicht" schmale
Viewports — in Display-Größen schon bei 360 px. Wer Überschriften
ergänzt, sollte bei 360 px gegenprüfen.

---

## Was bewusst fehlt

Keine erfundenen Referenzen, Kundenlogos, Bewertungen oder Fallzahlen.
Sobald echte vorliegen, gehören sie zwischen „Ablauf" und „Beweis" —
mit `Review`- bzw. `AggregateRating`-Auszeichnung im JSON-LD.

Kein Kontaktformular. Ein `mailto:`-Link braucht keinen Server, keine
Auftragsverarbeitung und kein Spam-Handling. Sobald ein Formular
gewünscht ist, kommt beides dazu.
