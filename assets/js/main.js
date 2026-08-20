/* Scholz Growth Engine — Bewegung.
 *
 * Die Seite funktioniert vollständig ohne dieses Skript: Ohne JavaScript
 * fehlt die Klasse js-motion, und alle Elemente stehen sofort sichtbar da.
 * Erst wenn das Skript läuft, wird überhaupt etwas versteckt und dann
 * eingeblendet.
 *
 * Bewegt wird ausschließlich über transform und opacity — beides läuft
 * auf dem Compositor und erzwingt kein Neu-Layout.
 */

(function () {
  'use strict';

  var wurzel = document.documentElement;
  var sparsam = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (sparsam || !('IntersectionObserver' in window)) {
    starteChrom();            // Kugel bleibt, nur ohne Aufwertung
    return;
  }

  wurzel.classList.add('js-motion');

  /* ── Hero: Zeilen fahren nacheinander aus ihrem Fenster herein ─────── */

  var zeilen = document.querySelectorAll('.zeile');
  zeilen.forEach(function (zeile, i) {
    setTimeout(function () { zeile.classList.add('ist-da'); }, 90 + i * 95);
  });

  /* ── Einblenden beim Scrollen ──────────────────────────────────────── */

  var ziele = document.querySelectorAll('.heb');
  if (ziele.length) {
    var beobachter = new IntersectionObserver(function (eintraege) {
      eintraege.forEach(function (e) {
        if (!e.isIntersecting) return;
        // Geschwister leicht versetzt, damit Reihen gestaffelt erscheinen
        var versatz = Number(e.target.dataset.versatz || 0);
        setTimeout(function () { e.target.classList.add('ist-da'); }, versatz);
        beobachter.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0.12 });

    var gruppe = null, index = 0;
    ziele.forEach(function (el) {
      if (el.parentElement !== gruppe) { gruppe = el.parentElement; index = 0; }
      el.dataset.versatz = String(Math.min(index, 5) * 55);
      index++;
      beobachter.observe(el);
    });
  }

  starteChrom();

  /* ── Chromkugel: leichte Fassung sofort, WebGL nur wenn es trägt ───── */

  function starteChrom() {
    var buehne = document.querySelector('[data-chrom]');
    if (!buehne || sparsam) return;

    var verbindung = navigator.connection || {};
    var kerne = navigator.hardwareConcurrency || 4;
    var speicher = navigator.deviceMemory || 4;

    // Auf schwachen Geräten, im Sparmodus oder bei langsamer Verbindung
    // bleibt es bei der CSS-Fassung. Die sieht gut aus und kostet nichts.
    if (verbindung.saveData === true) return;
    if (/2g/.test(verbindung.effectiveType || '')) return;
    if (kerne < 4 || speicher < 4) return;

    var leerlauf = window.requestIdleCallback ||
                   function (fn) { return setTimeout(fn, 1200); };

    leerlauf(function () {
      var s = document.createElement('script');
      s.src = buehne.dataset.chrom;
      s.async = true;
      document.head.appendChild(s);
    }, { timeout: 3000 });
  }
})();
