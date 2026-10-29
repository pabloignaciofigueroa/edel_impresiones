# QA técnico independiente: Edel Impresiones `/nueva_v8/` (fase 19, segunda ronda)

Fecha: 29-10-2026 (UTC). URL evaluada: http://localhost:8787/nueva_v8/ (servida desde `public/`). Herramientas: Playwright con Chromium. Perfiles: celular 412×915 (dpr 2,6, isMobile, táctil) y escritorio 1440×900.
Scripts y resultados en `_qa/fase19b/qa/`. Son los scripts 01 a 05 de la primera ronda, con la URL cambiada a nv8, más 02b (repeticiones de carga), 02c, 03b (contraste por píxel en la portada), 06 (menú, foco y Equipo sin JS), 07 (continuidad del video de portada), 08 (desborde) y 09.
No modifiqué ningún archivo del proyecto.

**Aviso de entorno.** Mientras corría esta ronda, el proyecto cambió en paralelo. A las 00:04 se regeneró `public/`: ahora hay `index.html` en la raíz (igual a nv8, salvo las rutas) y las copias `/nueva`…`/nueva_v7` desaparecieron. A las 00:15–00:17 cambiaron `site.js`, `site.css` y `nueva_v8/index.html`: se agregaron `html{overflow-x:clip}` y `.s-equipo{overflow-x:clip}`.
La primera pasada encontró un desborde horizontal nuevo, que el cambio de las 00:17 corrigió. Por eso repetí **toda la batería sobre el estado final**. Los hashes de ese estado están en `qa/estado_r2.sha1` y siguieron iguales hasta el final de la batería. Los resultados de la pasada anterior quedaron en `qa/ronda1_previo/`.
El iframe de Google Maps no carga en este entorno (`ERR_TUNNEL_CONNECTION_FAILED`, por el proxy). No es un problema de la web.

## Veredicto

**0 bloqueantes.** Los 3 bloqueantes de la primera ronda están resueltos. La regresión de desborde que apareció a mitad de la ronda también quedó resuelta en el estado final. Hay un punto que conviene ajustar antes de publicar: en roaming la apertura termina en 7,97–8,06 s, es decir, cumple la meta pero sin margen (ver D1).

## 1. Los bloqueantes de la primera ronda

| Bloqueante nv7 | nv8 medido | Estado |
|---|---|---|
| **B1 Carga 4G medio** (4000 kbps/150 ms): `.listo` a 9,70 s y 4.284 KB | Celular: `.listo` (fin de la apertura) a **4,81–4,89 s** en 3 corridas, más 8 corridas de diagnóstico entre 4,80 y 5,47 s. **1.225 KB** hasta `.listo` (≈1.103 KB comprimido). El % llega a 100 real, sin forzar, y la portada se reproduce desde el blob precargado | **Resuelto** |
| **B1 Carga roaming** (1500 kbps/300 ms): 9,66 s | Celular: **7,99 s** en las 3 corridas (`performance.now`; el reloj de Node marca 8,06 s). Se fuerza a los 6,3 s (con el % real entre 36 y 51) y la apertura termina justo antes de 8 s. **1.128–1.317 KB** hasta `.listo` | **Resuelto, pero al límite** (D1) |
| B1 Escritorio (informativo; la meta es para el celular) | 4G: 7,99–8,00 s, siempre forzado, con **3,5 MB** antes de abrir (`hero8.mp4` pesa 3,79 MB). Roaming: 7,97–8,00 s, 1,25 MB | Cumple el tiempo; el peso es alto (D2) |
| **B2 Dorso de Equipo sin JS** | Sin JS, `.flip-b` no gira (`.js .flip-b{transform:rotateY(180deg)}`, `site.css:230`) y aparece debajo de cada foto: visible, sin tapar y con contraste de 15,5:1 en el celular y en el escritorio (`capturas/equipo_sinjs_*.png`) | **Resuelto** |
| **B3 Contraste AA** | Medí 187 nodos de texto (1440) y 182 (412): **0 fallas reales**. Proceso en lila sólido; el teléfono de WhatsApp da 4,77:1; los enlaces del menú son blancos (7,14:1) con subrayado naranja. En la portada, por píxel en 3 fotogramas, el p5 del peor renglón es **4,95:1** en 1440 y **5,59:1** en 412 (en nv7 era 1,5–2,7:1). «IMPRESIÓN» va en blanco sobre la banda | **Resuelto** (queda un detalle menor: D5) |

Las únicas «fallas» que reporta 03 (1,00:1) corresponden a las etiquetas de las tarjetas 5 a 13 de la pila de Trabajos, que tienen opacidad 0 a propósito porque están fuera de la pila visible. Son falsos positivos.

## 2. Tabla de verificaciones (estado final)

| # | Verificación | Medido | Meta | Resultado |
|---|---|---|---|---|
| 1 | Consola / `pageerror` | 0 errores y 0 avisos (celular y escritorio) | 0 | OK |
| 1 | Respuestas 4xx/5xx | 0 en 63 URL. Solo falla Maps por el entorno, más un `blob:` abortado sin efecto | 0 | OK |
| 2 | CLS recorriendo toda la página (ida y vuelta) | Celular 0,00014 · escritorio 0,00021 | < 0,01 | OK |
| 3 | Apertura completa, celular, 4G medio | 4,81–4,89 s | < 8 s | OK |
| 3 | Apertura completa, celular, roaming | 7,99 s (×3) | < 8 s | OK al límite |
| 3 | Peso hasta abrir, celular | 4G 1.225 KB · roaming 1.128–1.322 KB | ≤ 1,5 MB | OK |
| 3 | Sin limitar la red | `.listo` 4,60 s (celular) · 4,62 s (escritorio) | — | OK |
| 4 | Tab durante la carga | Solo llega a «Saltar al contenido». nav, main y pie quedan inert hasta `edel:abierto` | Nada invisible | OK (era deseable en la ronda 1) |
| 4 | Anillo de foco | Doble anillo: tinta con halo blanco en secciones claras y blanco con halo tinta en las oscuras. ≥ 3:1 en los 41 elementos probados (mínimo: tinta sobre mostaza 6,54:1; sobre naranja 5,04:1) | ≥ 3:1 | OK (era deseable) |
| 4 | Menú del celular | dialog modal, foco en «Cerrar», Tab y Shift+Tab atrapados, Escape devuelve el foco a «Menú», y main, nav y pie quedan inert. Al usar un enlace, el foco pasa a `section#equipo` | Todo | OK (se corrigió el foco perdido) |
| 4 | Encabezados y landmarks | h1 → h2 → h3 sin saltos. Reseñas tiene h2 (`.sr`). 1 header, 2 nav, 1 main, 1 footer | — | OK |
| 4 | Texto < 16 px | 0 nodos | 0 | OK |
| 4 | alt y aria en EN | Todo se traduce. Solo queda sin traducir el logo del pie, que es nombre propio | — | OK |
| 5 | 8 anchos (360…1920): desborde horizontal | scrollWidth = clientWidth en los 8. `html` y `body` tienen `overflow-x:clip` | 0 | OK |
| 5 | La portada no deja ver la sección siguiente | `#intro` empieza exactamente en innerHeight en los 8 | — | OK |
| 5 | H1, banda y botones dentro de la pantalla; nav sin solapes; `.ln` sin recortes | 0 problemas en los 8 | — | OK |
| 6 | Movimiento reducido | Sin carga. Portada con póster (sin `src`). **0/23 videos con fuente y 23/23 con póster.** 0 animaciones activas, sin errores | Loops en póster | OK (decisión nv8) |
| 6 | Sin JS | Todo el texto se lee, incluido el dorso de Equipo | Todo legible | OK. Quedan detalles en D4 |
| 7 | Videos en play (con movimiento) | 23/23 con fuente, 23/23 en play, sin errores; ninguno depende del scroll. Portada a velocidad 1,00 durante 12 s, readyState 4 | Todos | OK |
| 7 | Duración de los loops | Trabajos 3,5 / 4,5 / 5,7 s · prendas 6,2 · team 7,6 · el resto entre 8,0 y 9,6 · equipo 10,6 · proceso 11,8 | 8–10 s | Las cortas son decisiones del dueño. Equipo (10,6 s) y proceso (11,8 s) quedan algo largos (D7) |
| 7 | Imágenes con naturalWidth 0 | 0/10 | 0 | OK |
| 7 | Anclas | 14/14 resuelven | 0 rotas | OK |
| 8 | Higiene de `public/` | 0 archivos .md/.py/.json/raw. Solo `_headers`, `_redirects`, `robots.txt`, `404.html`. Sin «vercel», «github» ni `localhost`. En nv8, `instagram.com/` solo aparece como `edel.chiloe` (más `ig.me/m/edel.chiloe`). Correo: `edelimpresiones@hotmail.com` (público, de fb.md) | Limpio | OK |
| 8 | noindex | `noindex,nofollow` en `nueva_v8/index.html` y en el nuevo `public/index.html`. `robots.txt` tiene `Disallow: /` | Presente | OK |
| 8 | og:image | `https://edelimpresiones.pages.dev/assets/og-edel.jpg` (1200×630), publicada | Absoluta | OK |

## 3. Bloqueantes

Ninguno.

Para que quede registrado: en la primera pasada de esta ronda (estado previo a las 00:17), el `.burst` de Team Mate/Café (`site.css:351`, `inset:-120px -40px -40px`) ensanchaba el documento 24 px en todos los anchos de 360 a 1280. En el celular, el layout viewport pasaba a 385 y 436 px, el botón «Menú» quedaba cortado en el borde derecho de la portada y la grilla de Servicios se veía descentrada. En 768–1280 se podía desplazar la página 20–24 px hacia los lados. La evidencia está en `ronda1_previo/r04.out` y `r08.out`. El estado final lo corrige con `html{overflow-x:clip}` y `.s-equipo{overflow-x:clip}` (`site.css:373,375`), y lo verifiqué en los 8 anchos (`r04.out`, `r08.out`).

## 4. Deseables (en orden de prioridad)

**D1. Roaming sin margen: la apertura termina a 7,97–8,00 s.**
`js/nv8/site.js:103` fija `TOPE = 6300` y, sobre eso, suma 0,35 s de rampa y 1,3 s de GSAP. El tick cada 40 ms y los fotogramas agregan unos 20–60 ms. En 1 de 12 corridas forzadas, `.listo` cayó en 8,000 s (escritorio, roaming).
Propuesta: `TOPE = 6000`. Otra opción es acortar la apertura cuando viene forzada (por ejemplo, `tl.timeScale(1.3)` si `force`).

**D2. Al forzar la apertura, el video de portada se descarga dos veces.**
`site.js:91-100,119`: cuando el % no llegó a 100, `heroSrc()` usa la URL normal porque el blob todavía no existe, mientras el `fetch` de la precarga sigue bajando el mismo archivo. Pasó en todas las corridas forzadas (`pedidosHeroMp4: 2` en `r02b.json`). En roaming, las dos descargas compiten por la red justo cuando la portada empieza a reproducirse.
Propuesta: un `AbortController` en `bajar()` que aborte el mp4 en `open()` si no terminó. Así el `<video>` usa su propia petición con Range.
En escritorio, además, la lista `grande` precarga `hero8.mp4` completo (3,79 MB; `tools/boceto_nv8.py:228`), por lo que en 4G el % nunca llega a 100 y siempre se fuerza. Propuesta: una versión de 1080 px más liviana (≤ 1,5 MB) o precargar solo los primeros segundos.

**D3. Imagen perezosa que compite con la portada en roaming.**
`vehicular-1-1200.webp` (207 KB) baja antes de `.listo` porque Chrome, en redes lentas, adelanta las imágenes `loading=lazy` cercanas. Propuesta: `fetchpriority="low"` o pasarla a `data-src` hasta `edel:abierto`, como ya se hace con los videos.

**D4. Sin JavaScript (detalles):**
- En el celular, «Menú» es un botón que no hace nada (`site.css:252`). Team Mate/Café, las flechas de Reseñas y las tarjetas de Equipo tampoco responden, y la indicación «Toca las fotos para darlas vuelta» aparece aunque no se puedan dar vuelta. Propuesta: `html:not(.js) .menu-b, html:not(.js) .eq-tip, html:not(.js) .res-b{display:none}`.
- 22 videos quedan sin póster (`data-poster`, `boceto_nv8.py:94`) y Chromium los muestra como rectángulos grises con controles nativos (ver `capturas/equipo_sinjs_escritorio.png`). Propuesta: `<noscript><style>` con los pósters como `background-image`, o `poster` real en los videos de las primeras pantallas.

**D5. Idioma inactivo en el menú del celular:** «EN», en blanco con opacidad .5 sobre `--azul`, da **2,97:1** (`site.css:65`, `.lang span{opacity:.5}`). En el pie da 4,86:1. Propuesta: `.menu-lang .lang span{opacity:.7}` o quitar la opacidad y marcar el idioma activo con un subrayado.

**D6. `div.res-pista` tiene `aria-label` sin `role`** (`boceto_nv8.py:398`). Propuesta: `role="region"`.

**D7. Loops largos:** `equipo.mp4` dura 10,6 s y `proceso8.mp4` 11,8 s (meta 8–10 s). En Proceso el largo puede estar justificado por los 3 pasos (marcas en 2,6 y 7,3 s). Equipo podría recortarse a 10 s.

**D8. Publicación (fase 20):**
- `_redirects` envía `/nueva_v8/*` a `/` con 301, pero `public/nueva_v8/index.html` se sigue publicando. En Cloudflare Pages el redirect debería ganar, pero conviene confirmar qué se quiere: si nv8 se va a mostrar en `/nueva_v8/`, hay que sacar esa regla.
- `robots.txt: Disallow: /` impide que Google lea la meta noindex. Si la página llega a estar enlazada en algún sitio, podría aparecer indexada sin descripción. Propuesta: agregar `X-Robots-Tag: noindex` en `_headers` (es más robusto), o dejar `robots.txt` abierto mientras la página deba seguir sin indexarse.
- `_headers` no trae `Permissions-Policy` ni `frame-ancestors`. Es opcional.

**D9. Menores:** el iframe del mapa no muestra anillo de foco (propuesta: `.mapa:focus-within{outline:3px solid #fff}`). Las fuentes y el póster se piden dos veces (por fetch y por el elemento); la segunda sale de la caché de disco, así que no cuesta red.

## 5. Riesgos en Safari/iOS (código, no medidos)

Siguen vigentes los de la primera ronda: máscara SVG del velo animada en cada fotograma, `pathLength` con dasharray, `overflow:clip` (no funciona en Safari < 16; ahora también lo usa `html`, así que en iOS 15 el `.burst` podría volver a ensanchar la página: conviene `overflow-x:hidden` como respaldo en `.s-equipo`), `inert` (15.5+), blobs retenidos en memoria y `100svh`.
Lo nuevo del sello y de las reseñas que se despegan usa `transform` y `rotate` con variables CSS. No veo riesgos adicionales.
