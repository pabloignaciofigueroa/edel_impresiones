# Dibujo del isotipo en la pantalla de carga: especificación

Carpeta: `_qa/agentes/diseno/`
- `prueba.html`: prueba autocontenida, con deslizador de p y botón "Reproducir 4 s". Por defecto usa el **vector limpio** (`_qa/agentes/vector/iso_vector.json`, embebido). Parámetros: `?fiel` usa el calco `brand/_logo_paths.json`; `?vivo` relee el JSON del vector por http y recalcula la geometría; `?p=0.5` deja un cuadro fijo; `?rec` oculta los controles; `?mono` pinta las formas en blanco para medir píxeles.
- `prueba_celular.mp4`: 412×915 a DPR 2 (824×1830), p de 0 a 1 en 4 s, a 30 fps, con el vector limpio. Lo armé cuadro a cuadro con Playwright y ffmpeg, porque `recordVideo` graba a 1x e ignora el DPR 2.
- `cuadros.jpg`: 8 cuadros y 4 acercamientos 6x a la unión azul/naranja.
- `iso_rotado.json`: **los `d` que van al sitio**. Es el vector limpio reordenado para partir en la punta, con los mismos nodos y la misma forma. Incluye las constantes `f2` y `wMax`.

## Idea

**No hay un trazo aparte del logo.** Hay un solo elemento por medialuna: el relleno real del logo (`#isoA`, `#isoN`). Lo que se anima es su **máscara**, que es *el mismo path* trazado en blanco:

1. **Línea.** La máscara es el path trazado a 2 px con un guion bidireccional. Como la máscara solo deja ver lo que está dentro de la forma, de esos 2 px queda solo la mitad interior: una línea de **1,0 px hacia adentro**. El borde exterior de esa línea lo dibuja el relleno del logo, así que no lo aproxima un trazo.
2. **Relevo (no hay cambio de elemento).** Cuando la línea cierra, la misma máscara pierde el guion y su ancho crece desde 2 px hasta el grosor máximo de la medialuna. La línea se engrosa hacia adentro desde ambos bordes y se cierra por el centro. Las puntas se llenan primero y la panza al final.
3. **Cierre.** Con f = 1 se agrega a la máscara la forma rellena (`.cierre`). Así no quedan poros del trazo ancho y el resultado es el logo entero.

Así se cumple el pedido del dueño: "el contorno hacia adentro, para que cuando entre el real no exista diferencia". El borde exterior es siempre el del logo, desde el primer cuadro hasta el último.

## Verificación por píxeles (Chromium; DPR 2 y DPR 6; vector limpio y también el calco)
Medí cada medialuna aislada y comparé con el cuadro final (p = 0,70) en el anillo del borde y en el exterior:

| cuadro | azul | naranja |
|---|---|---|
| línea cerrada, justo antes del relevo (p 0,3999 / 0,4599) | **0 px distintos** | **0 px distintos** |
| relevo (0,40 / 0,46) y justo después (0,4001 / 0,4601) | 0 | 0 |
| relleno creciendo (0,45 / 0,50) y cerrando (0,5999 / 0,6299) | 0 | 0 |
| píxeles que sobresalen de la forma, en cualquier cuadro | 0 | 0 |

También medí la alternativa que probé primero, un trazo con `clip-path` de la propia forma. Ahí el borde de la línea difería hasta 0,25 de cobertura en unos cientos de píxeles, porque Chrome suaviza el recorte distinto que el relleno. La versión con máscara elimina esa diferencia. Con el trazo centrado (el método actual del sitio) sobresalen ~5.000 px a DPR 2.

## Valores

| parámetro | valor |
|---|---|
| grosor de la línea visible | **1,0 px CSS** (2,6 × 0,4). Se pide 2 px a la máscara y queda la mitad interior. Hoy son 2,6 px centrados |
| ancho de la máscara en unidades del logo | `2 / escala` (escala = `geo.s0`; en celular 412 px ≈ 0,491 → 4,07 u) |
| color de la línea azul | degradado propio `#gaC` (vertical): `#1aa8d8 → #0b90c6 (45 %) → #0a6cb0`. Es el azul del logo levantado para que 1 px se lea sobre `#05263f`. Entre p 0,30 y 0,40 pasa a ser exactamente `#099ece → #0182b9 → #035590` (`#ga`), antes del relevo |
| color de la línea naranja | el del logo, `#gn` (`#fa571c → #f97732`), sin cambios |
| remates | redondos (`stroke-linecap/linejoin: round` en la máscara). Al quedar recortados por la forma se ven como una punta limpia |
| línea azul | p **0,00 → 0,40**, easing `inOutSine` |
| línea naranja | p **0,14 → 0,46**, `inOutSine` (en serie con solape, entra cuando el azul va en ~1/3) |
| azul engrosa | p **0,40 → 0,60**, `inOutCubic`, ancho de máscara de 2 px → `wMax` **154 u** (vector; 160 con el calco) |
| naranja engrosa | p **0,46 → 0,63**, `inOutCubic`, de 2 px → `wMax` **140 u** (vector; 146 con el calco) |
| letras "edel" | p 0,63 → 0,92, lineal (como en nv5) |
| bajada | p 0,92 → 1, opacidad |

**Orden y dirección.** Cada medialuna nace en una de sus puntas y avanzan a la vez el borde exterior y el interior. Se juntan exactamente en la otra punta, porque cada borde avanza en proporción a su largo.
- Azul: nace en la **punta superior** (445,48; 412,35) y muere en la inferior (448,12; 675,3). Es el sentido en que se escribe una "e".
- Naranja: nace en la **punta superior izquierda** (280,53; 382,51), que es la más cercana a la punta azul, y muere en la inferior (225,16; 580,54).
- En el vector las puntas son nodos. La prueba ajusta la punta aproximada al nodo más cercano, así que el trazo nace exactamente en la punta.
- `f2` = largo hasta la otra punta / largo total. Vector: azul **0,3992**, naranja **0,6611** (el vector recorre en sentido contrario al calco; el guion lo resuelve solo). Calco: 0,6013 / 0,3355.

## Integración en nueva_v5

### HTML (`nueva_v5/index.html`)
En el `<svg class="defs">` (línea 27), agregar **sin tocar `#ga`**, que también usa el logo del nav:
```html
<linearGradient id="gaC" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1aa8d8"/><stop offset=".45" stop-color="#0b90c6"/><stop offset="1" stop-color="#0a6cb0"/></linearGradient>
```
En `<svg id="ov">`, dentro de `<defs>` (junto a `#co` y `#mk`), agregar lo siguiente. `D_BLUE` y `D_ORANGE` salen de `iso_rotado.json` o del vector limpio:
```html
<mask id="mkA" maskUnits="userSpaceOnUse" x="-2000" y="-2000" width="5000" height="5000"><path d="D_BLUE"/><path class="cierre" d="D_BLUE"/></mask>
<mask id="mkN" maskUnits="userSpaceOnUse" x="-2000" y="-2000" width="5000" height="5000"><path d="D_ORANGE"/><path class="cierre" d="D_ORANGE"/></mask>
```
En `<g class="ap">`: **borrar `#trA` y `#trN`** y dejar los rellenos así:
```html
<path id="isoA" d="D_BLUE" fill="url(#gaC)" mask="url(#mkA)"/>
<path id="isoN" d="D_ORANGE" fill="url(#gn)" mask="url(#mkN)"/>
```

### CSS (`css/nv5/site.css`)
Borrar `#isoA,#isoN{fill-opacity:0}` y la regla `#trA,#trN{…}`. Agregar:
```css
#mkA path,#mkN path{fill:none;stroke:#fff;stroke-width:0;stroke-linejoin:round;stroke-linecap:round}
#mkA .cierre,#mkN .cierre{fill:#fff;stroke:none;visibility:hidden}
```

### JS (`js/nv5/site.js`)
En la línea 37, quitar `trA`/`trN` de las referencias. Luego reemplazar `draw(p)` por:
```js
const mA = $('#mkA path'), mN = $('#mkN path'), cA = $('#mkA .cierre'), cN = $('#mkN .cierre');
// geometría precalculada. Si el vector cambia: abrir prueba.html?vivo por http y copiar lo que imprime la consola.
const GEO = { A: { f2: 0.3992, wMax: 154 }, N: { f2: 0.6611, wMax: 140 } };   // vector limpio (iso_rotado.json)
const g = (el, c) => { const L = el.getTotalLength(); return { L, s2: c.f2 * L, wMax: c.wMax }; };
const G = { A: g(isoA, GEO.A), N: g(isoN, GEO.N) };
const Le = edel.map(x => x.getTotalLength());
const inOutSine = t => -(Math.cos(Math.PI * t) - 1) / 2;
const inOutCubic = t => t < .5 ? 4 * t * t * t : 1 - (-2 * t + 2) ** 3 / 2;
const seg = (p, a, b) => clamp((p - a) / (b - a));
const LINE = [[26,168,216],[11,144,198],[10,108,176]], LOGO_A = [[9,158,206],[1,130,185],[3,85,144]];
const gaC = [...document.querySelectorAll('#gaC stop')];
const tono = t => gaC.forEach((st, i) => st.setAttribute('stop-color', 'rgb(' + LINE[i].map((v, j) => Math.round(v + (LOGO_A[i][j] - v) * t)) + ')'));
function iso(m, c, G, k, f) {                 // k: avance de la línea, f: avance del relleno
  const w0 = 2 / geo.s0;                       // 2 px CSS → queda 1 px dentro de la forma
  c.style.visibility = f >= 1 ? 'visible' : 'hidden';
  if (f > 0 || k >= 1) { m.style.strokeDasharray = 'none'; m.style.strokeWidth = w0 + inOutCubic(f) * (G.wMax - w0); }
  else if (k > 0) { const a = k * G.s2, b = k * (G.L - G.s2); m.style.strokeDasharray = `${a} ${Math.max(0, G.L - a - b)} ${b} 0`; m.style.strokeWidth = w0; }
  else m.style.strokeWidth = 0;
}
function draw(p) {
  tono(inOutSine(seg(p, 0.30, 0.40)));
  iso(mA, cA, G.A, inOutSine(seg(p, 0.00, 0.40)), seg(p, 0.40, 0.60));
  iso(mN, cN, G.N, inOutSine(seg(p, 0.14, 0.46)), seg(p, 0.46, 0.63));
  const te = Le.reduce((m, v) => m + v, 0); let acc = 0; const de = seg(p, 0.63, 0.92) * te;
  edel.forEach((x, i) => { const k = clamp((de - acc) / Le[i]); x.style.strokeDashoffset = 1 - k; x.style.visibility = k > 0 ? 'visible' : 'hidden'; acc += Le[i]; });
  sub.forEach(x => x.style.opacity = seg(p, 0.92, 1));
  pctEl.textContent = Math.round(p * 100);
}
```
`Le` se calcula una sola vez y no en cada cuadro como hoy. `draw` cuesta ~0,02 ms. `w0` usa `geo.s0`; durante `open()` la máscara ya está en `wMax`, así que el zoom no la afecta.

### Vector limpio
Ya está integrado en la prueba, en el video y en los cuadros. Los `d` de `iso_rotado.json` van en las 3 apariciones por medialuna: relleno, máscara y `.cierre`. El logo del nav puede usar el `d` original de `iso_vector.json`, porque es la misma forma.
Si el vector se vuelve a entregar:
1. Abrir `prueba.html?vivo` **por http**; en `file://` no funciona `fetch`. La consola imprime `geometría isotipo {…}` con `L`, `s1`, `s2` y `wMax`.
2. Copiar los `d` reordenados (`window.__geo.D`) y poner `f2 = s2/L` y `wMax` en `GEO`.
3. Funciona con cualquier path. Si no es M/C/Z absoluto, no se reordena y la partida se desplaza con `stroke-dashoffset = -s1`; en ese caso hay que agregarlo en la rama de la línea de `iso()`.

## Notas honestas
- El logo final de la carga es el relleno **con la máscara puesta** (así no hay relevo). Comparado con el mismo path sin máscara, Chrome suaviza el borde con otro redondeo: difiere hasta ~0,2 de cobertura en píxeles del borde. No se ve (lo revisé a 8x). Por eso **no hay que quitar la máscara al terminar**, porque eso sí produciría un cambio de un cuadro.
- Con el **calco** (`?fiel`), justo antes de que el relleno cierre pueden aparecer 1 a 8 píxeles sueltos con cobertura parcial. Son poros del trazo ancho sobre sus micro-ondulaciones y desaparecen al cerrar gracias a `.cierre`. Con el **vector limpio** medí 0 poros. El calco también tiene micro-escalones ("faceteo") que el vector elimina: 10 y 6 nodos, curvas lisas.
- La línea azul en su parte baja es el tono más oscuro. Por eso se levantó (`#gaC`); con el `#035590` puro casi no se leía a 1 px.
- No toqué las letras. Se observa que hacia p 0,75 la "d" aparece como una "J" (dibuja primero el asta y luego la panza). Viene de nv5 y se puede revisar aparte.
- Lo verifiqué en Chromium. Safari maneja las máscaras SVG de forma parecida, pero no lo probé.
