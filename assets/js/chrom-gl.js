/* Scholz Growth Engine — irisierende Chromkugel in WebGL2.
 *
 * Wird von main.js nur auf Geräten nachgeladen, die sie tragen. Fällt
 * hier irgendetwas aus, passiert schlicht nichts: Die CSS-Fassung liegt
 * darunter und bleibt sichtbar.
 *
 * Bewusst ohne three.js. Für eine einzelne Vollbild-Fläche braucht es
 * keine Szenengraph-Bibliothek — ein Dreieck und ein Fragment-Shader
 * genügen, und das sind ein paar Kilobyte statt einiger hundert.
 *
 * Gerendert wird absichtlich unterhalb der Anzeigegröße (höchstens 640 px
 * Kante, Pixelverhältnis gedeckelt). Das Objekt ist weich und organisch,
 * die Hochskalierung sieht man nicht — die eingesparte Füllrate dagegen
 * merkt jedes Mittelklasse-Telefon.
 */

(function () {
  'use strict';

  var buehne = document.querySelector('[data-chrom]');
  if (!buehne) return;
  var leinwand = buehne.querySelector('.chrom__gl');
  if (!leinwand) return;

  var gl = leinwand.getContext('webgl2', {
    alpha: true,
    antialias: false,
    depth: false,
    stencil: false,
    powerPreference: 'low-power',
    failIfMajorPerformanceCaveat: true
  });
  if (!gl) return;

  var VERT = `#version 300 es
void main() {
  // Ein Dreieck, das den gesamten Clip-Raum überdeckt — günstiger als zwei.
  vec2 p = vec2((gl_VertexID << 1) & 2, gl_VertexID & 2);
  gl_Position = vec4(p * 2.0 - 1.0, 0.0, 1.0);
}`;

  var FRAG = `#version 300 es
precision mediump float;
uniform vec2 uRes;
uniform float uZeit;
out vec4 farbe;

float hash(vec2 p) {
  p = fract(p * vec2(123.34, 456.21));
  p += dot(p, p + 45.32);
  return fract(p.x * p.y);
}

float rauschen(vec2 p) {
  vec2 i = floor(p), f = fract(p);
  vec2 u = f * f * (3.0 - 2.0 * f);
  return mix(mix(hash(i), hash(i + vec2(1.0, 0.0)), u.x),
             mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), u.x), u.y);
}

float fbm(vec2 p) {
  float v = 0.0, a = 0.5;
  for (int i = 0; i < 4; i++) { v += a * rauschen(p); p = p * 2.03 + 17.0; a *= 0.5; }
  return v;
}

// Iridenz als Kosinus-Palette: violett, cyan, weiss, pfirsich, magenta
vec3 palette(float t) {
  return 0.58 + 0.42 * cos(6.28318 * (t + vec3(0.00, 0.28, 0.60)));
}

void main() {
  vec2 uv = (gl_FragCoord.xy * 2.0 - uRes) / min(uRes.x, uRes.y);
  float r = length(uv);
  if (r > 1.0) { farbe = vec4(0.0); return; }

  // Kugelnormale aus der Bildschirmposition
  float z = sqrt(max(0.0, 1.0 - r * r));
  vec3 n = normalize(vec3(uv, z));

  // Fliessende Verformung der Oberflaeche
  float t = uZeit * 0.075;
  vec2 q = n.xy * 1.6;
  float w1 = fbm(q + vec2(t, -t * 0.7));
  float w2 = fbm(q * 1.7 - vec2(t * 0.9, t * 0.4) + w1);
  vec3 nn = normalize(n + vec3(w1 - 0.5, w2 - 0.5, 0.0) * 0.6);

  vec3 blick = vec3(0.0, 0.0, 1.0);
  float fresnel = pow(1.0 - max(dot(nn, blick), 0.0), 2.2);

  vec3 col = palette(fresnel * 1.45 + w2 * 0.85 + t * 0.3);

  vec3 licht = normalize(vec3(-0.45, 0.6, 0.75));
  float glanz = pow(max(dot(reflect(-licht, nn), blick), 0.0), 44.0);

  // Chrom, nicht Seifenblase. Die Mitte bleibt nahezu schwarz, Farbe
  // entsteht nur dort, wo die Oberflaeche vom Betrachter wegkippt.
  // Das haelt die Kugel dunkel genug, dass die weisse Schrift darueber
  // lesbar bleibt — sonst waere der Hero unbrauchbar.
  float saum = pow(fresnel, 1.9);
  col = col * (0.035 + 0.62 * saum);
  col += vec3(glanz) * 0.5;
  col += 0.04 * pow(max(dot(nn, licht), 0.0), 4.0);

  farbe = vec4(col, smoothstep(1.0, 0.955, r));
}`;

  function baue(art, quelle) {
    var s = gl.createShader(art);
    gl.shaderSource(s, quelle);
    gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) { gl.deleteShader(s); return null; }
    return s;
  }

  var vs = baue(gl.VERTEX_SHADER, VERT);
  var fs = baue(gl.FRAGMENT_SHADER, FRAG);
  if (!vs || !fs) return;

  var prog = gl.createProgram();
  gl.attachShader(prog, vs);
  gl.attachShader(prog, fs);
  gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return;

  gl.useProgram(prog);
  var oRes = gl.getUniformLocation(prog, 'uRes');
  var oZeit = gl.getUniformLocation(prog, 'uZeit');
  var leer = gl.createVertexArray();
  gl.bindVertexArray(leer);
  gl.enable(gl.BLEND);
  gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);

  var KANTE_MAX = 640;
  var breite = 0, hoehe = 0;

  function messe() {
    var kasten = buehne.getBoundingClientRect();
    if (!kasten.width) return false;
    var dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    var seite = Math.min(Math.round(kasten.width * dpr), KANTE_MAX);
    if (seite === breite) return true;
    breite = hoehe = seite;
    leinwand.width = leinwand.height = seite;
    gl.viewport(0, 0, seite, seite);
    return true;
  }
  if (!messe()) return;

  var laeuft = true, sichtbar = true, angezeigt = false, start = 0;

  function zeichne(jetzt) {
    if (!laeuft) return;
    if (sichtbar && !document.hidden) {
      if (!start) start = jetzt;
      messe();
      gl.uniform2f(oRes, breite, hoehe);
      gl.uniform1f(oZeit, (jetzt - start) / 1000);
      gl.drawArrays(gl.TRIANGLES, 0, 3);
      if (!angezeigt) { angezeigt = true; leinwand.classList.add('ist-da'); }
    }
    requestAnimationFrame(zeichne);
  }
  requestAnimationFrame(zeichne);

  // Ausserhalb des Sichtfelds oder im Hintergrund wird nicht gerechnet.
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (e) { sichtbar = e[0].isIntersecting; })
      .observe(buehne);
  }
  document.addEventListener('visibilitychange', function () { start = 0; });

  // Verliert der Browser den Kontext, bleibt die CSS-Fassung uebrig.
  leinwand.addEventListener('webglcontextlost', function (e) {
    e.preventDefault();
    laeuft = false;
    leinwand.classList.remove('ist-da');
  });

  window.addEventListener('resize', function () { messe(); }, { passive: true });
})();
