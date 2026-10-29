# Panel fase 19: Servicios y color · Entretención

Evaluamos http://localhost:8787/nueva_v7/ con Playwright y Chromium en 412×915 (dpr 2,6, touch), 360×780, 768×1024 y 1440×900, además de un contexto con `reducedMotion:'reduce'`. Grabamos la carga en video y la revisamos cuadro a cuadro. Las mediciones se hicieron con scripts propios: el contraste se calculó con colores computados y, sobre video, muestreando píxeles de la portada sin texto. Evidencia en `_qa/fase19/panelB/`.

Las decisiones de `justificacion.md` no restan puntos: carga con dibujo, IG-35 con rótulo, textos con su ortografía, etc. El mapa de Google sale vacío solo porque el entorno no tiene salida a google.com, así que no se evalúa.

## Notas

| Dimensión | Subcriterio | Nota |
|---|---|---|
| **A · Servicios y color** | Claridad de servicios | 5 / 8 |
| | Sistema de color y contraste | 4 / 6 |
| | Tipografía y jerarquía | 5 / 6 |
| | **Total A** | **14 / 20** (meta 17: no cumple) |
| **B · Entretención** | Diversión y sorpresa | 6 / 8 |
| | Fluidez y pulido | 5 / 6 |
| | Coherencia con la marca | 5 / 6 |
| | **Total B** | **16 / 20** (meta 17: no cumple) |
| | **Entretención global** | **3 / 4** (meta 4: no cumple) |

## Qué funciona (medido)

- **Sin desborde horizontal** en 360, 412, 768 y 1440 (scrollWidth = clientWidth). **0 textos bajo 16 px** en los cuatro anchos. **0 errores JS**.
- **Barra fija:** al saltar desde el menú a cada sección, la sección queda en y=59–66 bajo una barra que termina en 78. El primer texto queda en y≥154, nada tapado (falta Proceso, ver H-6).
- **Color:** la secuencia tinta → papel → azul → luz UV → papel con barra tornasol → madera → naranja → tinta es la de `brand/palette.md`, token por token. Los pares de texto sobre fondo plano cumplen: tinta sobre madera ≈ 6,5:1 y tinta sobre naranja ≈ 5,0:1. El tornasol solo va en formas (la barra y el brillo de la tarjeta), nunca detrás de texto.
- **Tipografía:** Anton a 1,22 de interlineado. CÓMO, DÍA, IMPRESIÓN y TAMAÑO no chocan con la línea de arriba en ningún ancho. **0 títulos (h1/h2/h3) con palabra sola.** Oswald con tracking sobre banda naranja #ce4204, como en sus piezas.
- **Carga y apertura** (video `carga_movil_412.webm`, cuadros `carga_cuadros_0..2.jpg`). El contorno se traza en azul y naranjo y luego se rellena sin salto de borde. Después se escribe «edel» trazo a trazo (la «d» ya no se lee «J») y aparece la bajada. El 100 % llega a los 3,5 s. «La e se abre» con el video dentro de la contraforma y un zoom limpio, y la portada queda armada a los ~4,8 s. Es el mejor momento de la web, sin destellos ni saltos.
- **Juegos que responden bien:**
  - Barrido de tinta en los h2 y troquel punteado que se dibuja (`d_serv_troquel_t0.4.png`).
  - Proceso: el paso activo sigue al video (1 durante 7 s, luego 2 y 3).
  - Pila de stickers: avanza con arrastre de mouse de 200 px, con swipe táctil de 240 px y con 3 clics rápidos en «Siguiente» (sin trabarse). Un swipe vertical sobre la pila hace scroll (Δ225 px) y no la despega: `touch-action` está bien.
  - Tarjetas del equipo que giran, con dorso legible.
  - Team Mate/Café: `aria-pressed` alterna bien y hay estallido.
  - Reseñas: avanzan solas (478 px cada ~4 s) y paran 8 s cuando el usuario las toca.
  - Botón magnético: se desplaza 22 px con el mouse.
  - Menú de celular: cortina, «Cerrar», ES/EN y salto a la sección.
- **Movimiento reducido:** sin carga (portada armada a 1,2 s), sin Lenis, 13/13 servicios visibles y reseñas quietas.

## Hallazgos priorizados

### BLOQUEANTES

**H-1 · Servicios en celular: no se entienden de un vistazo (A, claridad).**
- En 412 px la sección mide **9.030 px** (≈ 10 pantallas) y en 360 px mide 8.369 px.
- Cada tarjeta ocupa ~690 px: medio 4:5 a todo el ancho y el rótulo (h3 en banda) va *debajo* del video. El rótulo aparece recién después de pasar ~470 px de imagen.
- La «carta» de la imprenta no se puede recorrer con la vista. Quien busca «Diplomas» o «Medallas» tiene que pasar 9 o 12 videos.
- *Propuesta:* bajo 700 px, usar una grilla de 2 columnas con medio 1:1 y banda **sobre** el borde inferior del medio. Quedan unos 13 × 260 / 2 ≈ 1.800 px.
- *Alternativa:* abrir la sección con un índice de las 13 bandas Oswald (chips que anclan a cada tarjeta), mantener las tarjetas y pasar el medio a 4:3.
- En cualquier caso, la banda va antes que la descripción y pegada al medio.

**H-2 · Portada en escritorio: el titular no tiene contraste AA sobre el video (A, color).**
- Se midió con el texto oculto, en 8 cuadros del video de 1440: la primera línea «TU MARCA» queda sobre las etiquetas blancas «RESERVADO». La mediana del fondo da **2,46:1** contra blanco (texto grande exige 3:1) y el p90 da 2,18:1 (`portada_sin_texto_d1440.png`).
- «IMPRESIÓN» en naranja #fa621f baja a **1,74:1** contra la mediana del fondo en escritorio y a 2,33:1 en celular.
- El degradado actual es solo .35 → .15 en la parte alta, justo donde está el titular.
- *Propuesta:* agregar un velo lateral o radial detrás del bloque de texto, por ejemplo `linear-gradient(90deg, rgba(5,38,63,.78) 0, rgba(5,38,63,.35) 55%, transparent)` en ≥900 px, y subir el inferior a .9.
- Para «IMPRESIÓN» hay dos caminos: ponerle la banda naranja #ce4204 con texto blanco (como en sus piezas) o mantener el naranja con `text-shadow: 0 2px 18px rgba(5,38,63,.6)`.
- Hay que volver a medir con el mismo método. Hoy en celular la mediana es 5,6:1, que cumple, pero el p90 de la primera línea es 3,87.

**H-3 · Proceso: los pasos inactivos no cumplen AA (A, color).**
- `.pasos li{opacity:.55}` deja blanco sobre UV #2e279f en **4,37:1** para texto de 18 px y números Anton de 22 px (ambos exigen 4,5).
- Siempre hay 2 de 3 pasos en ese estado, en los cuatro anchos.
- *Propuesta:* subir a `opacity:.7`, o mejor usar color en vez de opacidad: `color: #c9c6f2`, que da ≈ 7:1. Que el estado activo se marque con el círculo relleno y el desplazamiento, que ya existen.

**H-4 · Número de WhatsApp en el botón: 4,14:1 (A, color).**
- `.btn-wa small{opacity:.9}` sobre #ce4204 baja del 4,6:1 del blanco puro a **4,14:1** a 16 px. Pasa en Cotiza y en el menú.
- *Propuesta:* quitar la opacidad, porque blanco al 100 % sobre #ce4204 cumple. Para diferenciar se puede usar el peso 400.

### DESEABLES (ordenados por impacto)

**H-5 · Falta un momento memorable en Reseñas y en Cotiza (B, diversión).**
- Reseñas es un carrusel correcto pero plano. No tiene título propio: solo la banda «4,6 en Google · 100 % recomendado en Facebook». Las tarjetas de 240 px quedan medio vacías con citas cortas como «excelente calidad precio!».
- Cotiza solo tiene el magnético, que no funciona en táctil.
- *Propuestas, sin texto nuevo:*
  - Reseñas: tratar cada tarjeta como **sticker troquelado con esquina que se levanta** al avanzar (reutiliza el `::after` de la pila), o hacer que el «4,6» se cuente y quede «estampado» con un pequeño golpe de escala tipo sello.
  - Cotiza: que el título entre con el barrido y que el botón de WhatsApp se recorte con la **línea de troquel** que se cierra alrededor, en celular también.

**H-6 · Proceso en celular: el video va antes del título (A, claridad).**
- Al llegar a Proceso desde el menú, el h2 queda en y=840 de 915: se ve un video sin contexto.
- *Propuesta:* bajo 900 px, poner h2 y pasos antes del video (`order`), o el h2 sobre el video.

**H-7 · Brillo tornasol casi muerto en celular (B, diversión y fluidez).**
- `deviceorientation` en iOS exige `DeviceOrientationEvent.requestPermission()`, que el código no pide, así que en iPhone el brillo no se mueve.
- Con el dedo, el `pointermove` se corta por el scroll: en la prueba, un deslizamiento de 240 px solo movió `--tx` a 13 %.
- *Propuesta:* en `(pointer:coarse)`, animar `--tx/--ty` con el scroll de la tarjeta (ScrollTrigger con scrub). La tarjeta «brilla» al pasar sin pedir permisos.

**H-8 · Estallido Team Mate/Café modesto (B, diversión).**
- Son 14 emojis de 30 px recortados dentro de la tarjeta (`overflow:hidden`) que vuelan por encima del párrafo (`d_team_mate_estallido.png`, `m_team_cafe.png`). En celular se leen chicos y apagados.
- *Propuesta:* 20–24 piezas de 34–40 px, dejar que salgan de la tarjeta (burst en un contenedor sin recorte por encima de la sección) y sumar un pequeño «pop» de escala al botón elegido. El costo es mínimo.

**H-9 · Equipo en escritorio desbalanceado (A y B, pulido).**
- Las tarjetas que giran miden ~145 px de ancho al lado de un h2 enorme.
- La tarjeta Team estira su fondo tinta a la altura de la columna y deja ~200 px vacíos arriba y abajo del video (`hoja_d1440_3.jpg`).
- *Propuesta:* `align-self:start` en `.team` y fotos a 2 columnas de ≥220 px, o la grilla de fotos a todo el ancho y Team debajo.

**H-10 · Servicios en escritorio con remate irregular (A, claridad).**
- Las tres columnas terminan a alturas muy distintas. Medallas queda sola abajo en la columna 2, y «Pendones, Rollers, Adhesivos» flota a la izquierda bajo una columna más corta (`hoja_d1440_2.jpg`).
- *Propuesta:* repartir 5/4/4 de modo que la columna más larga sea la 1, que ya tiene la pieza grande, y alinear «Pendones…» con el remate de la última tarjeta o ponerlo como banda azul a todo el ancho.

**H-11 · Emojis solos en la última línea (A, tipografía).**
- `text-wrap: pretty` no evita que el emoji quede solo con una palabra.
- A 360 px pasa en 9 párrafos de servicios y equipo, por ejemplo «diseño 🙌», «gráfica ✨», «historias 📖» y «trabajar 🙂‍↔️✨». A 768 px pasa en Transparentes, donde «😏✨» queda solo en su línea.
- *Propuesta:* unir la última palabra y el emoji con NBSP (U+00A0) al generar el HTML. No cambia el texto literal.

**H-12 · Videos en loop siguen corriendo con movimiento reducido (B, coherencia y a11y).**
- Con `reduce`, 7 de 23 videos están reproduciendo y no hay control de pausa (WCAG 2.2.2).
- *Propuesta:* con `prefers-reduced-motion`, no dar `play()` y dejar el póster, o mostrar un botón pausa/play por video.

## Desglose de los juegos

| Juego | Funciona | Sensación | Nota |
|---|---|---|---|
| Carga con dibujo + «la e se abre» | Sí, 3,5 s + 1,3 s | Memorable, muy de marca | 10/10 |
| Barrido de tinta en h2 | Sí | Sutil, correcto | 8 |
| Troquel en servicios | Sí | Buena metáfora; repetido 13 veces en celular, cansa (H-1) | 7 |
| Brillo tornasol | Escritorio sí; celular casi no (H-7) | — | 5 |
| Proceso sincronizado con el video | Sí | Claro y didáctico; falla AA (H-3) | 8 |
| Pila de stickers | Sí: mouse, touch, botón; sin trabas | El mejor juego después de la carga | 9 |
| Tarjetas del equipo que giran | Sí | Bien, pero chicas en escritorio (H-9) | 7 |
| Team Mate / Team Café | Sí | Gracioso pero tímido (H-8) | 6 |
| Reseñas que avanzan solas | Sí, con pausa al tocar | Funcional, sin sorpresa (H-5) | 6 |
| Botones magnéticos | Sí, solo con mouse | Discreto | 7 |
| Menú del celular | Sí, accesible | Limpio, tipografía de marca | 8 |

## Qué subiría las notas a la meta
- A: H-1, H-2, H-3 y H-4 bastan para 17–18 (claridad 7/8, color 6/6). Con H-6 y H-11 llega a 19.
- B: H-5, H-7 y H-8 dan diversión 7–8/8. Con H-9 y H-12 queda en 18/20 y Entretención 4/4.

## Archivos en panelB/
- `carga_movil_412.webm` y `carga_cuadros_*.jpg`: carga y apertura cuadro a cuadro.
- `hoja_{m360,m412,t768,d1440}_*.jpg` y las capturas `*_NN.png`: recorrido completo.
- `portada_sin_texto_d1440.png`: fondo del titular con el que se midió H-2.
- `d_*`: juegos en escritorio. `m_*`: juegos en celular. `rm_*`: movimiento reducido. `hoja_juegos_*.jpg`: resumen.
