# QA técnico independiente: Edel Impresiones `/nueva_v7/` (fase 19)

Fecha: 28-10-2026 · Servido desde `public/` en http://localhost:8787/nueva_v7/ · Playwright 1.63.0 con Chromium.
Scripts y resultados en bruto: `_qa/fase19/qa/` (`01_consola_cls_medios.js` → `r01.json`, `02_red.js` → `r02.json`, `03_a11y.js` → `r03.json` y `hero_muestras.json`, `04_responsive.js` → `r04.json` y `capturas/portada_*.png`, `05_reducido_sinjs.js` → `r05.json` y `capturas/*`).
No se modificó ningún archivo del proyecto.

Nota de entorno: el contenedor se reinició a mitad de la auditoría. Tras el reinicio, Playwright y Chromium seguían disponibles y no faltó ningún paquete. Las mediciones 1 a 4 se tomaron antes del reinicio, la 5 se recuperó de `r04.json` y la 6 se corrió después del reinicio. El iframe de Google Maps no carga en este entorno (proxy: `ERR_TUNNEL_CONNECTION_FAILED`). Es un problema del entorno y no de la web.

## Tabla de verificaciones

| # | Verificación | Medido | Meta | Resultado |
|---|---|---|---|---|
| 1 | Errores de consola / `pageerror` (412×915 y 1440×900) | 0 errores y 0 avisos en ambos | 0 | OK |
| 1 | Respuestas 4xx/5xx | 0 (61 URL distintas pedidas). Solo falla el iframe de Maps, por el proxy del entorno, y un `blob:` abortado sin efecto | 0 | OK |
| 2 | CLS recorriendo toda la página (ida y vuelta) | Celular 0,00014 · escritorio 0,00016 | < 0,01 | OK |
| 2 | LCP aproximado, sin limitar la red | Celular 5,08 s · escritorio 4,90 s (el H1 aparece cuando se abre la carga) | Informativo | Lo determina la pantalla de carga (decisión aprobada) |
| 3 | Peso hasta `.listo` con 4G medio (4 Mbps, 150 ms) | **4.284 KB** (≈4.170 KB con brotli en JS/CSS/HTML) | ≤ 1,5 MB | **FALLA** |
| 3 | Peso hasta `.listo` en roaming (1,5 Mbps, 300 ms) | 1.483 KB + HTML (≈1.380 KB comprimido). Queda bajo la meta solo porque el tope de 8 s corta la descarga | ≤ 1,5 MB | OK al límite |
| 3 | Tiempo hasta `#carga.listo` con 4G medio | **9,70 s** (performance.now) | ≤ 8 s | **FALLA** |
| 3 | Tiempo hasta `#carga.listo` en roaming | **9,66 s** | ≤ 8 s | **FALLA** |
| 3 | Tiempo hasta `.listo` sin limitar la red | 4,63 s celular · 4,68 s escritorio | ≤ 8 s | OK |
| 4 | Foco visible (anillo 3 px en todos los elementos tabulados) | Presente en todos menos el iframe del mapa | Presente | OK |
| 4 | Contraste del anillo de foco (cian `#3bb6e6`) contra el fondo | Papel 2,05:1 (botón «Siguiente trabajo») · naranja 1,32:1 (reseñas y flechas) | ≥ 3:1 (WCAG 1.4.11) | **FALLA** |
| 4 | Orden de tabulación | Sigue el DOM: saltar → logo → nav → Cotiza → portada → … → pie. Coherente | Lógico | OK |
| 4 | Nada enfocable invisible, después de la carga | 0 casos reales (los display:none no se enfocan) | 0 | OK |
| 4 | Nada enfocable invisible, durante la carga | El Tab llega a «Siguiente trabajo», a los flips y a Team Mate/Café, que quedan **debajo del velo de carga** | 0 | **FALLA** (deseable) |
| 4 | Menú del celular | role=dialog, aria-modal=true, aria-label; el foco va a «Cerrar»; Tab y Shift+Tab quedan atrapados (17/17 pasos dentro); Escape cierra y devuelve el foco a «Menú»; nav, main y pie quedan inert | Todo | OK |
| 4 | Foco tras usar un enlace del menú | Queda en `body` (se pierde) | Ir a la sección | Deseable |
| 4 | aria-labels | Todos los botones tienen nombre. `div.res-pista` lleva aria-label sin role (no está permitido en un genérico) | Válidos | Deseable |
| 4 | alt en ES y en EN | Las 9 imágenes y los 23 videos cambian a inglés. El logo del pie («Edel Impresiones») es nombre propio y no necesita traducción | Todos | OK |
| 4 | Contraste AA del texto (183 nodos medidos) | 3 fallas reales: pasos inactivos de Proceso **4,37:1** (opacidad .55; 2,67:1 sobre el resplandor `--uv-luz`) · teléfono `<small>` en el botón naranja **4,14:1** (opacidad .9) · enlaces naranja del menú del celular sobre azul **2,32:1** · idioma inactivo en el menú 2,97:1 | 4,5:1 (3:1 texto grande) | **FALLA** |
| 4 | Contraste del texto de portada sobre el video (muestreo de píxeles, 3 fotogramas) | «IMPRESIÓN» en naranja: mediana 2,5 a 3,9:1, p95 1,5 a 2,7:1 · «TU MARCA» en 1440 px: mediana 3,08, p95 2,06:1 | 3:1 (texto grande) | **FALLA** (por fotogramas) |
| 4 | Texto < 16 px | 0 nodos (escritorio y celular) | 0 | OK |
| 4 | Landmarks | 1 header, 2 nav con nombre, 1 main, 1 footer | Completos | OK |
| 4 | Encabezados en orden | h1 → h2 → h3, sin saltos. La sección `#resenas` no tiene encabezado | Orden y sección con título | Deseable |
| 4 | lang en citas | 8/8 blockquote tienen lang="es", también en modo EN. html lang cambia es→en | Correcto | OK |
| 5 | Desborde horizontal (360, 390, 412, 768, 1024, 1280, 1440, 1920) | scrollWidth = clientWidth en los 8; 0 elementos fuera de pantalla sin recorte | 0 | OK |
| 5 | La portada no deja ver la sección siguiente | `#intro` empieza exactamente en innerHeight en los 8 anchos | No asoma | OK |
| 5 | Títulos que se pisan, líneas `.ln` recortadas, nav con solapes | 0 en los 8 anchos (H1 bajo la nav, banda y botones dentro de la pantalla) | 0 | OK |
| 6 | prefers-reduced-motion: reduce | Sin carga, portada visible al instante, 23 videos en play, 0 animaciones CSS, sin errores | Todo visible | OK (ver nota sobre los videos en loop) |
| 6 | JavaScript desactivado | Todo el texto se lee **excepto el dorso de las 2 tarjetas de Equipo** (citas de la marca) · 22 videos sin fuente ni póster (solo el LQIP borroso) · en el celular, el botón «Menú» no hace nada y no hay navegación | Todo legible | **FALLA** (flip-b) |
| 7 | Videos con fuente y en play | 23/23 con src, 23/23 en play, readyState 4, todos avanzan en 2,5 s | Todos | OK |
| 7 | Ningún video depende del scroll | No hay pausa ni scrub ligados al scroll; seguían en play tras ir y volver. Solo la *carga* es perezosa (IO con un margen del 150 %) | — | OK |
| 7 | Duración de los loops | tarjetas 3,8 s · team 3,7 s · diplomas 6,0 · prendas 6,2 · letreros 6,3 · uv 6,6 · medallas 7,0 · laser 7,6 · proceso 12,8 | 8 a 10 s (regla de la casa) | Revisar contra las decisiones |
| 7 | Imágenes con naturalWidth 0 | 0/10 | 0 | OK |
| 7 | Anclas internas | 14/14 resuelven | 0 rotas | OK |
| 8 | Archivos internos en `public/` | 0 (.md/.py/.json/raw). Solo `_headers` y `_redirects` | 0 | OK |
| 8 | grep «vercel» y «github.io/github.com» | 0 | 0 | OK |
| 8 | grep «instagram.com/» | Solo `instagram.com/edel.chiloe/` (14) y `ig.me/m/edel.chiloe` (7) | Solo edel.chiloe | OK |
| 8 | `_headers` y caché | assets 7 d + swr · vendor 30 d immutable · brand 7 d · css/js 1 h + swr · nosniff y Referrer-Policy | Correcto | OK (mejoras deseables abajo) |
| 8 | meta robots noindex | `noindex,nofollow` en v7 y en las 6 copias congeladas; robots.txt `Disallow: /` | Presente | OK |
| 8 | og:image absoluta | `https://edelimpresiones.pages.dev/assets/og.jpg`, 1200×630, publicada | Absoluta | OK |

## Hallazgos priorizados

### BLOQUEANTES

**B1. La carga se abre a los 9,7 s en 4G medio y en roaming (tope de 8 s) y en 4G descarga 4,3 MB antes de abrir (meta 1,5 MB).**
- Dónde: `tools/boceto_nv7.py:210-218` (`PRIMEROS`, `_lista`: el grupo 3 de la precarga suma stickers.mp4, plateados.mp4 y transparentes.mp4, 2,6 MB). `js/nv7/site.js:89-112`: el % real espera los 4,18 MB del celular (7,09 MB en escritorio).
- Medido: con 4 Mbps la lista completa no alcanza a bajar en 8 s, así que siempre se fuerza el tope. A los 8,0 s se suman la rampa de 350 ms (`site.js:107`) y la apertura GSAP de unos 1,3 s (`site.js:121-127`), y `.listo` llega a los 9,7 s. Es decir, el tope de 8 s marca el *inicio* de la apertura, no su fin.
- Propuesta:
  1. Sacar el grupo 3 (y quizás los pósters del grupo 2) del cálculo del %. Que el % cubra solo fuentes, póster y video de portada (unos 1,1 MB en el celular) y que el resto se pida después de `edel:abierto`, como ya hacen los videos diferidos.
  2. Si `.listo` debe ocurrir a los 8 s como máximo, forzar a los 6,3 s (`8000 - 350 - 1300`) o acortar la apertura cuando viene forzada.

  Con eso, en 4G la carga abriría en unos 4 a 5 s y con 1,1 a 1,2 MB.

**B2. Sin JavaScript no se lee el dorso de las tarjetas de Equipo** (dos frases literales de la marca). Esto incumple la regla «sin JS se lee todo».
- Dónde: `css/nv7/site.css:221-227` (`.flip-b` con `transform:rotateY(180deg)` y `backface-visibility:hidden`, sin condición `.js`). Marcado en `tools/boceto_nv7.py:362-363`.
- Propuesta: aplicar el giro solo con JS (`.js .flip-b{transform:rotateY(180deg)}` y `.js .flip-a,.js .flip-b{position:absolute…}`). Sin `.js`, mostrar el texto debajo de la foto.

**B3. Contraste AA insuficiente en textos reales** (regla «contraste AA»):
- Enlaces pares del menú del celular (Proceso, Equipo, Cotiza): naranja `#fa621f` sobre azul `#0358a5` da **2,32:1**, bajo el 3:1 de texto grande. `css/nv7/site.css:257`. Propuesta: usar `--cian-luz` sobre `--tinta`, o blanco y naranja sobre fondo `--tinta` en el menú (naranja sobre tinta da 5,04:1).
- Teléfono `<small>` en los botones WhatsApp: blanco con opacidad .9 sobre `#ce4204` da **4,14:1**. `css/nv7/site.css:160`. Propuesta: quitar `opacity:.9` (blanco puro da 4,77:1).
- Pasos inactivos de Proceso: opacidad .55, que da **4,37:1** sobre `--uv` y 2,67:1 donde cae el resplandor inferior. `css/nv7/site.css:109`. Propuesta: opacidad ≥ .7 o atenuar solo el número.
- «IMPRESIÓN» naranja y «TU MARCA» blanco sobre el video de portada: en los fotogramas con etiquetas rojas y blancas (ver `capturas/portada_1440.png`) el contraste baja a 1,5–2,7:1. `css/nv7/site.css:74`: el degradado solo llega a .15–.35 en la zona del H1. Propuesta: subir el degradado a ≥ .55 detrás del H1 (sobre todo en ≥ 900 px) o agregar `text-shadow`/`paint-order` oscuro al `em`.
- Menor: el idioma inactivo en el menú (blanco .5 sobre azul) da 2,97:1 (`site.css:65`).

### DESEABLES

1. **Anillo de foco de bajo contraste** en las secciones claras y naranjas. Cian sobre papel da 2,05:1 y sobre naranja 1,32:1 (`css/nv7/site.css:8`). Afecta a «Siguiente trabajo», `.res-pista` y las flechas de reseñas. Propuesta: `.s-trab :focus-visible,.s-res :focus-visible{outline-color:var(--tinta)}` (como ya hace `.flip`).
2. **Foco detrás del velo de carga**: `site.js:293` vuelve inert solo `#nav`. Mientras carga, el Tab alcanza botones de `main` que no se ven. Propuesta: volver inert también `main` y `.pie` hasta `edel:abierto`.
3. **El foco se pierde al usar un enlace del menú** (`site.js:278`). Propuesta: después de `scrollTo`, `target.setAttribute('tabindex','-1'); target.focus({preventScroll:true})`.
4. **Sin JS, «Menú» es un botón muerto** y en el celular no hay navegación (`site.css:248`). Propuesta: `.menu-b` solo con `.js` (por ejemplo `html:not(.js) .menu-b{display:none}` y mostrar `.nav-links` en columna o un enlace a `#cotiza`). Pasa lo mismo, en menor grado, con Team Mate/Café y las flechas de reseñas.
5. **Sin JS, los 22 videos no tienen póster** (usan `data-poster`) y solo muestran el LQIP borroso de 9×16 px (`tools/boceto_nv7.py:83`). Propuesta: un `<noscript>` con `<img>` del póster, o poner `poster` real solo en las tarjetas visibles.
6. **Sección Reseñas sin encabezado** (`tools/boceto_nv7.py:380-386`). `.res-pista` usa aria-label sin role (`:383`). Propuesta: un `h2` (puede ser `.sr`) y `role="region"` en la pista.
7. **Videos en loop sin control para pausarlos**, también con `prefers-reduced-motion` (WCAG 2.2.2 para movimiento de más de 5 s). Propuesta: con `reduce`, no llamar a `play()` y mostrar el póster, o agregar un botón global de pausa.
8. **Descargas duplicadas** en la primera visita: las 4 fuentes, el póster de portada, stickers-poster y stickers.mp4 se piden por `fetch()` (precarga) y otra vez por el elemento. La segunda sale de caché de disco, sin costo de red, pero `equipo-2-poster.webp` (17 KB) se precarga y v7 no lo usa (`tools/boceto_nv7.py:211`, `POSTERS` toma todas las claves de media.json). Propuesta: armar `POSTERS` desde los videos usados en la página.
9. **Duraciones de loop fuera de 8 a 10 s** (tarjetas 3,8 s, team 3,7 s, proceso 12,8 s, entre otros). Hay que verificarlo contra `assets/video/media.json` y las decisiones del dueño.
10. **`_headers`**: no hay `X-Robots-Tag: noindex` (es más robusto que la meta). `robots.txt: Disallow: /` impide que Google lea la meta noindex: hay que cambiarlo en la fase 20. No hay `Permissions-Policy` ni `frame-ancestors`. `public/` publica las 6 copias congeladas y `hero-540.mp4` (1,3 MB), que v7 no usa: conviene revisarlo al cerrar.
11. Iframe del mapa: no muestra anillo de foco al tabular (Chromium). Propuesta: `.mapa:focus-within{outline:3px solid var(--cian-luz)}`.

## Riesgos en Safari/iOS (detectados en el código, no medidos)

- **Máscaras SVG del velo** (`boceto_nv7.py:104-111`): un `<rect>` de 2e5×2e5 con `mask` en `userSpaceOnUse`, más el trazo de la máscara reanimado en cada fotograma (`site.js:63-69`, `strokeWidth`/`strokeDasharray` cada 40 ms). En WebKit las máscaras se rasterizan en CPU y son caras de redibujar; es posible que haya tirones o un dibujo incompleto en iPhones medianos. Conviene probar en un dispositivo real; una alternativa es reducir el rect al viewport.
- **`pathLength="1"` + `stroke-dasharray:1`** en «edel» (`site.css:49`): WebKit tuvo errores con pathLength en el dash. Si falla, la palabra aparece entera o no aparece.
- **`text-wrap:balance` / `pretty`** (`site.css:245-246`): balance desde Safari 17.5 y pretty solo en versiones recientes. Se degrada sin romper (los títulos usan `.ln` manual).
- **`overflow:clip`** (`site.css:4, 21, 70`): Safari < 16 lo ignora. En iOS 15 `body{overflow-x:clip}` no actúa y elementos como `.troquel` (inset -7px) podrían generar scroll horizontal. Propuesta: agregar `overflow-x:hidden` como respaldo en `html`.
- **`inert`**: Safari 15.5+. En versiones anteriores, el menú y la nav durante la carga no bloquean el foco (el atrapado por teclado sí funciona).
- **Videos en `blob:`** (`site.js:97`): la portada y los 3 primeros servicios se reproducen desde un Blob en memoria. Funciona en iOS, pero sin Range y con toda la memoria retenida (unos 4 MB en el celular, que nunca se liberan con `revokeObjectURL`). En Modo de bajo consumo de iOS, `play()` se rechaza y solo queda el póster (aceptable, pero la portada queda quieta).
- **`deviceorientation`** (`site.js:206`): en iOS 13+ requiere `DeviceOrientationEvent.requestPermission()`, así que el brillo tornasol por inclinación nunca se activa en iPhone (sin error).
- **`100svh`** (Safari 15.4+) y **`aspect-ratio`** (15+): en versiones anteriores la portada y las tarjetas pierden la altura.
- **Volteo 3D** (`site.css:221-225`): `all:unset` + `perspective` + `backface-visibility` funciona con el prefijo `-webkit-` ya incluido. En iOS hay casos conocidos de parpadeo de la cara trasera durante la transición.
