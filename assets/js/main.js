/* Scholz Growth Engine — die Seite funktioniert vollständig ohne dieses
   Skript. Es fügt nur ein zurückhaltendes Einblenden beim Scrollen hinzu. */

(function () {
  'use strict';

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  if (!('IntersectionObserver' in window)) return;

  var ziele = document.querySelectorAll(
    '.gegenueber__seite, .ebene, .schritt, .messwert, .branche, .code, .kontakt__karte'
  );
  if (!ziele.length) return;

  ziele.forEach(function (el, i) {
    el.style.opacity = '0';
    el.style.transform = 'translateY(14px)';
    el.style.transitionProperty = 'opacity, transform';
    el.style.transitionDuration = '.55s';
    el.style.transitionTimingFunction = 'cubic-bezier(.2,.7,.3,1)';
    el.style.transitionDelay = (i % 4) * 60 + 'ms';
  });

  var beobachter = new IntersectionObserver(
    function (eintraege) {
      eintraege.forEach(function (eintrag) {
        if (!eintrag.isIntersecting) return;
        eintrag.target.style.opacity = '1';
        eintrag.target.style.transform = 'none';
        beobachter.unobserve(eintrag.target);
      });
    },
    { rootMargin: '0px 0px -8% 0px', threshold: 0.1 }
  );

  ziele.forEach(function (el) { beobachter.observe(el); });
})();
