# Panel B, fase 19b: Servicios y color · Entretención (nueva_v8)

Evaluamos http://localhost:8787/nueva_v8/ con Playwright y Chromium en 412×915 (dpr 2,6, touch), 360×780, 768×1024 y 1440×900, además de un contexto con `reducedMotion:'reduce'`. Usamos los mismos métodos que en la primera ronda (`_qa/fase19/panel_servicios_entretencion.md`):
- Contraste con colores computados en todos los textos sobre fondo plano.
- Contraste del titular de portada medido sobre el video **sin texto**: se ocultaron `.hero-t` y `.nav`, se tomaron 8 cuadros cada 1,1 s y se calculó la luminancia por píxel dentro de la caja de cada línea.
- Juegos probados con mouse, touch CDP y temporizadores.

La evidencia está en `_qa/fase19b/panelB/`. Las decisiones de `justificacion.md` y las nuevas del BRIEF (grilla de 2 columnas, «Y también», sello 4,6, diplomas difuminados, videos cortos, etc.) no restan puntos.

## Notas

| Dimensión | Subcriterio | Ronda 1 (nv7) | **nv8** |
|---|---|---|---|
| **A · Servicios y color** | Claridad de servicios | 5 / 8 | **7 / 8** |
| | Sistema de color y contraste | 4 / 6 | **6 / 6** |
| | Tipografía y jerarquía | 5 / 6 | **5 / 6** |
| | **Total A** | 14 / 20 | **18 / 20 (meta 17: cumple)** |
| **B · Entretención** | Diversión y sorpresa | 6 / 8 | **7 / 8** |
| | Fluidez y pulido | 5 / 6 | **4 / 6** (por el desborde lateral B-1; con el arreglo, 6/6) |
| | Coherencia con la marca y a11y | 5 / 6 | **6 / 6** |
| | **Total B** | 16 / 20 | **17 / 20 (meta 17: cumple justo; 19 con B-1 resuelto)** |
| | **Entretención global** | 3 / 4 | **4 / 4** (condicionado a B-1) |

## Qué quedó resuelto (verificado)

| Hallazgo ronda 1 | Estado nv8 | Medición |
|---|---|---|
| H-1 Servicios en celular, 9.030 px | ✔ | Grilla de 2 columnas, medio 1:1, banda pegada al borde del medio. La sección mide **3.353 px en 412** (antes 9.030) y **3.463 px en 360** (antes 8.369). Se recorre de un vistazo (`hoja_m412_0.jpg`, `m412_02.png`). |
| H-2 Titular de portada sin AA sobre el video | ✔ | Mismo método, 8 cuadros sin texto. **1440:** mediana 12,0 / 12,8 / 13,9 por línea, peor 2 % ≥ 7,7:1 (antes 2,46 de mediana). **412:** mediana 10,3 / 12,0 / 13,6, peor 2 % ≥ 6,7:1. «IMPRESIÓN» va en blanco sobre banda #ce4204: 4,77:1, texto grande. El video sigue leyéndose bien bajo el velo (`portada_sin_texto_d1440.png`, `portada_sin_texto_m412.png`). |
| H-3 Pasos inactivos de Proceso | ✔ | Lila sólido #c9c6f2 sobre UV #2e279f: **6,73:1**. El activo, blanco: 11,0:1. |
| H-4 Teléfono en el botón WhatsApp | ✔ | Sin opacidad: blanco sobre #ce4204 = **4,77:1**. |
| Barrido general de contraste y tamaño | ✔ | **0 textos < 16 px y 0 pares bajo AA** en 360, 412, 768 y 1440. |
| H-5 Momento en Reseñas | ✔ | El sello «4,6» cae con escala y giro y la fila tiembla (`m_sello_100ms…900ms.png`). Al avanzar, la reseña se despega con esquina levantada (`m_resena_despega.png`, `d_resena_despega.png`). Es de marca: sticker troquelado. |
| H-6 Proceso en celular: video antes del título | ✔ | Ahora el h2 y los pasos van primero. Desde el menú, el primer texto queda en y=153 bajo una barra que termina en 78 (`m_proceso.png`). |
| H-7 Tornasol muerto en celular | ✔ | En táctil, `--tx` sigue al scroll: 35 → 47 → 58 → 69 → 80 → 92 % en pasos de 150 px, sin pedir permisos. |
| H-8 Estallido Mate/Café | ✔ | 22 piezas de 38 px que salen de la tarjeta, y el botón hace «pop» (`d_team_cafe.png`). En celular causa B-1. |
| H-9 Equipo en escritorio | ◐ | Team ya no tiene bloques vacíos y las fotos miden ~340 px. Queda la columna derecha vacía bajo Team (ver D-2). |
| H-10 Servicios en escritorio | ✔ | Grilla pareja de 3 columnas. Stickers ocupa 2 filas y la grilla cierra con «Y también: Pendones, Rollers, Adhesivos» en 5 filas exactas (`sec_d1440_servicios.png`). |
| H-11 Emoji solo en la última línea | ✔ | **0 líneas con solo emoji** en los 4 anchos. Única excepción: el «.”» de una reseña literal (ver D-4). |
| H-12 Loops con movimiento reducido | ✔ | Con `reduce`: **0 de 23 videos en play** y los 23 con póster. Sin carga, sin Lenis, 13/13 servicios visibles y reseñas quietas tras 5 s (`rm_*.png`). |
| Carga | ✔ | En local abre a ~4,6–4,9 s en los 4 anchos. Dibujo, «edel», bajada y «la e se abre» sin destellos (`carga_cuadros.jpg`, `carga_movil_412.webm`). |
| Proceso sincronizado | ✔ | Cambia de paso a los 2,6 s y 7,3 s del video, y vuelve a 1 al reiniciar el loop. |
| Pila, flip, menú, magnético | ✔ | Sin regresiones: swipe de 240 px y arrastre con mouse avanzan, 3 clics rápidos llevan de 2 a 5, el swipe vertical hace scroll (Δ181 px) y el magnético se mueve 20 px. Desde el menú, todas las secciones quedan con el primer texto en y ≥ 153. |

## BLOQUEANTE

**B-1 · En celular y tablet la página se desplaza 24 px hacia el lado y el botón de menú queda cortado (regresión de nv8).**
- **Medición:** `scrollWidth` es 385/360, 436/412 y 792/768, y `innerWidth` crece igual. En nv7 era 0. `.menu-b` termina en x=420 con una pantalla de 412 (o 369/360), así que la hamburguesa queda cortada en todas las capturas de celular.
- **Con un dedo:** un gesto lateral desplaza la vista 24 px y aparece una franja tinta a la derecha (`m412_tras_pan_horizontal.png`). Al tocar Team Mate, la vista queda corrida y «Cotiza» se sale del borde (`m_team_mate.png`).
- **Causa:** `public/css/nv8/site.css` **línea 351**, `.burst{inset:-120px -40px -40px;z-index:5}`. Los −40 px laterales del contenedor del estallido salen del ancho de página. El `overflow-x:clip` del `body` (línea 4) no lo contiene: se propaga al viewport y Chrome móvil igual ensancha el layout viewport.
- **Propuesta (probada inyectando el CSS, deja 360/412/768 en scrollWidth = innerWidth y el menú en x=344/396/752):**
  - Agregar `.s-equipo{overflow-x:clip}` (línea 129). Recorta solo en horizontal, así los emojis siguen saliendo de la tarjeta hacia arriba.
  - Como red de seguridad, agregar `html{overflow-x:clip}`.
  - Alternativa equivalente: `.burst{inset:-120px 0 -40px}`.
  - Después de arreglarlo, hay que volver a medir el desborde en 360, 412 y 768.

Es un arreglo de una línea, pero hoy el cliente lo notaría en su celular apenas abra la página (menú cortado y página que «baila» hacia el lado). Por eso es bloqueante.

## DESEABLES (por impacto)

**D-1 · Servicios en tablet (700–1099 px), largo.** A 768 la sección mide **5.093 px** (≈5 pantallas): 2 columnas con medio 4:5 de 357×634. *Propuesta:* extender el medio 1:1 del bloque `@media (max-width:699px)` hasta 1099 px, o usar 3 columnas desde 760 px. Quedaría en ~3.000 px.

**D-2 · Equipo en escritorio: hueco a la derecha.** Bajo la tarjeta Team quedan ~500 px de madera vacía junto al video grande del integrante (`sec_d1440_equipo.png`). *Propuesta:* subir el video del integrante a la columna derecha bajo Team (`.eq-fotos` a 2 columnas y el video con `grid-column:2` en la grilla `.eq`), o hacer que la grilla de fotos ocupe todo el ancho con Team al lado de las dos fotos.

**D-3 · Tarjetas de reseña en celular con mucho blanco.** Citas cortas como «Muy responsables en la fecha de entrega.» quedan en tarjetas de ~240 px de alto con más de la mitad vacía (`hoja_juegos_movil.jpg`). *Propuesta:* `align-items:start` en la pista y alto natural, o bajar `min-height` a 0 en < 700 px.

**D-4 · Bandas de servicio en 2 líneas con palabra sola (360 px).**
- 7 bandas parten en 2 líneas, como «STICKERS Y / ETIQUETAS» o «PLATEADOS / TORNASOL». Se leen bien, pero quedan desparejas entre columnas.
- En una reseña literal, el «.”» final queda solo en su línea.
- *Propuestas:*
  - Bandas: `letter-spacing:.03em` o `font-size:15px`. Ojo: 15 px está bajo la regla de 16, así que mejor bajar solo el tracking.
  - Reseña: NBSP antes del «.” ».

**D-5 · Magnético solo con mouse.** En Cotiza, en táctil no hay ningún gesto propio, porque el sello y el despegue ocurren en Reseñas. *Propuesta:* troquel punteado que se cierra alrededor del botón WhatsApp al entrar (ya existe el componente `.troquel`).

## Desglose de los juegos (nv8)

| Juego | Funciona | Sensación | Nota |
|---|---|---|---|
| Carga + «la e se abre» | Sí, abre a ~4,7 s | Memorable | 10 |
| Barrido de tinta en h2 | Sí | Sutil | 8 |
| Troquel en servicios (grilla) | Sí | Ya no cansa: 7 filas | 8 |
| Brillo tornasol | Mouse en escritorio, scroll en celular | Vivo en ambos | 8 |
| Proceso sincronizado | Sí, 2,6 s / 7,3 s | Claro, AA | 9 |
| Pila de stickers junto al título | Sí | El mejor juego después de la carga | 9 |
| Tarjetas del equipo que giran | Sí | Mejor tamaño en escritorio | 8 |
| Team Mate / Café | Sí, 22 piezas + pop | Festivo; causa B-1 en celular | 8 |
| Sello 4,6 + reseñas que se despegan | Sí | Momento nuevo y de marca | 8 |
| Botones magnéticos | Solo mouse | Discreto | 7 |
| Menú del celular | Sí | Bien; hamburguesa cortada por B-1 | 7 |

## Archivos en `panelB/`
- `hoja_{m360,m412,t768,d1440}_*.jpg` y `*_NN.png`: recorrido completo.
- `sec_{d1440,t768}_{servicios,equipo,trabajos,resenas}.png`: secciones enteras. En las capturas largas de escritorio, el «Saltar al contenido» visible es un artefacto de la captura de elemento, no de la página.
- `portada_sin_texto_{d1440,m412}.png`: fondo usado para medir el contraste del titular.
- `m412_desborde_nav.png`, `m412_tras_pan_horizontal.png`, `m_team_mate.png`: evidencia de B-1.
- `m_sello_*ms.png`, `m_resena_despega.png`, `d_resena_despega.png`, `d_team_cafe.png`, `m_tornasol_scroll.png`, `m_proceso.png`, `hoja_juegos_movil.jpg` y los `d_*` y `m_*` del script de juegos: juegos.
- `rm_portada.png`, `rm_resenas.png`, `rm_servicios.png`: movimiento reducido.
- `carga_movil_412.webm`, `carga_cuadros.jpg`: carga cuadro a cuadro.
