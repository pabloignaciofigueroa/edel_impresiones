# Fase 19b · Panel A (voz de marca, imágenes y video) y juez dueño (nueva_v8)

Evaluado el 2026-10-28 en http://localhost:8787/nueva_v8/, en celular 412×915 (DPR 2,6, táctil) y escritorio 1440×900, en ES y EN (EN forzado con `localStorage edel-lang=en`). Antes de puntuar leí entera la bitácora `_plan/edel/justificacion.md` y las decisiones nuevas del BRIEF; esas decisiones no restan puntos. Usé las mismas rúbricas de la ronda 1 (`_qa/fase19/panel_voz_imagen.md` y `juez_dueno.md`).

**Respaldo en `_qa/fase19b/panelA/`:**
- Recorridos: `movil_es_*`, `movil_en_*`, `escritorio_es_*` y `escritorio_en_*` (cada pantalla, desde la portada a los 8 s).
- Texto visible extraído del DOM: `*_texto.txt`.
- `recorrido.json`: alto de cada sección, estado de los 23 videos y errores de JS.
- Interacciones: `i_*` (pila 4/13 y 13/13, Team Mate, giro de foto, reseña que se despega, recortes de Letreros).
- `frames/`: hojas de 12 cuadros por video v8, cabeza y cola de cada loop, `proceso8_pasos.jpg` con marcas de tiempo, `diplomas8_fullres.jpg` (6 cuadros a 540×960 para revisar privacidad) y `nav_movil_recorte.png` (botón de menú cortado).

Los 23 videos quedan en readyState 4 y reproduciéndose, sin errores de JS en ninguna de las 4 combinaciones. El mapa sale vacío porque el entorno de prueba no tiene red hacia Google; según la bitácora, en línea sí carga.

## Notas

| Dimensión | Ronda 1 (nv7) | Ronda 2 (nv8) | Meta |
|---|---|---|---|
| A) Voz de marca | 15,5 | **18,5 / 20** | ≥ 17 ✔ |
| B) Imágenes y video | 12,5 | **16,5 / 20** | ≥ 17 ✘ (le falta medio punto) |
| Juez dueño | 17 | **18,5 / 20** | ≥ 17 ✔ |

**¿Se la mostraría mañana al dueño?** Sí, una vez corregido el desborde horizontal del celular (bloqueante 1, que se arregla con una línea de CSS ya verificada). Lo demás son mejoras.

---

## Qué quedó resuelto de la ronda 1

| Hallazgo ronda 1 | Estado en nv8 | Evidencia |
|---|---|---|
| B-1 «Vasos grabados / Engraved mugs» | ✔ Ahora «Dulce Enlatta · Stickers transparentes / Clear stickers», y `brand-voice.md` está corregido (l. 44) | `index.html` l. 134 |
| B-2 Destello en la unión del loop (hero, UV, proceso, letreros) | ✔ Los tramos parten en IG-45 1,62 s y la unión es un fundido limpio de UV a UV. No hay cuadros intrusos al inicio | `frames/cabeza_*`, `cola_*` |
| B-3 Libreta Reiver en Tarjetas; 3,8 s | ✔ Ya no hay Reiver, y `tarjetas8` dura 8,4 s. Queda un detalle de pertinencia (ver B-imagen) | `frames/hoja_tarjetas8.jpg` |
| B-4 QR y nombres de Dekra legibles | ✔ Revisé 6 cuadros a resolución completa: nombres, notas y QR quedan ilegibles y no se pueden escanear. Desde la portada ya salió el tramo con diplomas legibles | `frames/diplomas8_fullres.jpg` |
| B-5 Videos de menos de 8 s | ✔ `uv8` 8,1 · `letreros8` 8,1 · `stickers8` 8,3 · `medallas8` 8,2 · `laser8` 9,6 · `diplomas8` 8,3 · `tarjetas8` 8,4. Team (7,6 s), Prendas (6,2 s) y los 3 videos propios de Trabajos (3,5–5,7 s) son decisión del dueño | ffprobe |
| D-1 Trabajos repite los videos de Servicios | ◐ Bajó de 7 a 4 repeticiones: plateados, transparentes, prendas y diplomas8. Bitácoras, medallas y letreros ya tienen tramo propio | `index.html` l. 134 |
| D-2 Medallas con la frase completa de IG-44 | ✔ | l. 107 |
| D-3 «1º» → 🚀 | ✔ (y en EN ya no aparece «1º Pioneers») | l. 95 |
| D-4 Glosas EN de Proceso, Equipo y Cotiza | ✔ | l. 116, 149, 187 |
| D-5 «Message us on Instagram» y «Holographic silver stickers» | ✔ | l. 107, 190 |
| D-6 «Haz clic» con mouse / «Toca» en táctil | ✔ | l. 150 |
| D-7 Tarjeta Team con bloque vacío en escritorio | ✔ La tarjeta se ajusta a su contenido. El hueco pasó a otro lugar (ver deseable 3) | `escritorio_es_09/10` |
| D-8 Marcas de los pasos del Proceso | ✔ Con el video nuevo, `data-p2=2.6` coincide con la entrada del plotter (2,5 s) y `data-p3=7.3` con el depilado (7,5 s) | `frames/proceso8_pasos.jpg` |
| D-9 Portada de escritorio blanda | ✘ Sigue el 9:16 de 720 p ampliado. El velo ayuda al titular, pero la imagen de fondo se lee como una mancha oscura. Pendiente del video horizontal | `escritorio_es_00` |
| D-10 Video de Diseño (gesto de «chiquitito») | ✘ Sin cambios: es el mismo `diseno.mp4` | `frames/hoja_diseno.jpg` |
| D-11 Fuente de las reseñas de Google y del 4,6 | ✘ No existe `content/google.md` | `content/` |
| D-12 «Berries & Hielo» en la documentación | ✔ | `copy.md` l. 61, `brand-voice.md` l. 49 |
| D-13 URL de Facebook | ✘ Sin verificar (no consta en `fb.md`) | l. 204 |
| Juez 1 · Servicios en escritorio desparejo | ✔ Grilla pareja de 3 columnas que cierra con «Y también: Pendones, Rollers, Adhesivos» | `escritorio_es_06` |
| Juez 2 · Trabajos en escritorio con la mitad vacía | ✔ La pila queda junto al título y el botón pegado a ella | `escritorio_es_08` |
| Juez 3 · Servicios en celular de 9.030 px | ✔ **3.353 px** en una grilla de 2 columnas, unas 3,7 pantallas | `recorrido.json` |
| Juez 4 · Mapa sin estado de reposo | ◐ Ahora es una caja tinta, sin dirección ni póster. En línea carga, así que pasa a deseable | `movil_es_12` |
| Juez 7 · WhatsApp con mensaje prellenado | ✔ ES «Hola Edel, quiero cotizar un trabajo», EN «Hi Edel, I would like a quote for a job», en los 4 enlaces | l. 61, 71, 83, 189 |
| Juez 10 · Destacar la mejor reseña | ✔ Sello 4,6 y «Los mejores de Castro!» como primera reseña | `movil_es_10` |
| Juez 11 · Estallido Mate/Café visible | ◐ El botón pasa a naranja con un pulso y aparecen 🧉 de fondo. Es más visible, pero agrandarlo **introdujo el desborde del bloqueante 1** | `i_movil_team_mate.png` |
| Juez 12 · Pendones sin pieza | ✔ Ahora es la pieza final «Y también» | |

---

## A) Voz de marca: 18,5 / 20

### Fidelidad: 7,5 / 8
- Volví a cotejar contra `ig_posts.json`, `fb.md`, `copy.md` y la bio el H1, los 7 H2, las bajadas, las 13 tarjetas, los 3 pasos, el juego Team (IG-35), las 8 reseñas, el pie y «Pendones, Rollers, Adhesivos». Todo es literal y conserva la ortografía original («stickers transparente», «de que Team eres»).
- No hay @ personales en el texto. La firma «@estudio.soluna x @lamariannecoello» del póster de Pilates queda fuera del recorte en Servicios (4:5) y en Trabajos (1:1); lo verifiqué cuadro a cuadro (`i_movil_letreros_trab.png`).
- Los tres errores de la ronda 1 (vasos grabados, «1º», Medallas a medias) están corregidos.
- Resta 0,5 por trazabilidad: las 6 reseñas de Google y el «4,6 · 10 reseñas» siguen sin una captura o transcripción fechada en `content/`.

### Voz y tono: 5,5 / 6
- La voz suena a su Instagram: tuteo, ✨ 🙂‍↔️ 💪, humor de taller (Team Mate / Team Café) y Cotiza con IG-38.
- Resta 0,5 por dos cosas que ya estaban:
  - La tarjeta Diplomas sigue siendo solo un llamado («Háblanos al DM…»), mientras que la web empuja a WhatsApp. Es literal y no lo cuento como error, solo como roce de voz.
  - El H2 de Equipo pesa en 4 líneas de mayúsculas en el celular.

### Interfaz y microcopias ES/EN: 5,5 / 6
- Todo lo que faltaba en EN está: glosas en los 7 H2, «Clear stickers», «Message us…», «Tap / Click the photos…», mensaje de WhatsApp en inglés, `aria`, `alt` y `meta` traducidos.
- Resta 0,5 porque en EN las cifras siguen con formato español: el chip «**4,6** on Google» (l. 96), el sello «4,6» (l. 175) y el chip «100 %» (l. 97), mientras que la banda de reseñas sí dice «4.6 … 100%». Es incoherente dentro de la misma página.

---

## B) Imágenes y video: 16,5 / 20

### Pertinencia: 6,5 / 8
- **Mejoró:**
  - Diplomas difuminados, con un difuminado parejo y creíble.
  - Medallas cuenta la historia completa: láser, UV, medalla y entrega en el escenario.
  - Letreros cierra con el póster terminado.
  - Trabajos tiene tomas propias de bitácoras (tapas y en mano), medallas (escenario) y letrero.
- **Tarjetas (`tarjetas8`):** sacaron a Reiver, pero cerca del **40 % del loop no son tarjetas de presentación**:
  - unos 3 s son mazos amarillos «SIGMO · VENENO» (IG-40 9,3–11,05, señaléticas o etiquetas de cebo);
  - el cierre son volantes con precio «$10.000» (IG-40 0–1,08).

  Solo Hojalatería Erice y XS Joyas son tarjetas. No bloquea, porque se leen como impresos de papelería, pero el rótulo dice «Tarjetas».
- **Diseño:** sin cambios. Es el reel de humor IG-33 (mano haciendo el gesto frente a una pantalla en blanco y persianas).
- **Team (`team8`):** el loop dura 7,6 s, pero las tazas salen de cuadro hacia los 3 s y más de la mitad muestra un monitor vacío con el rótulo. La duración es decisión del dueño; lo que resta es la composición.

### Calidad técnica: 5,5 / 6
- Las uniones del loop quedaron limpias en hero, UV, proceso, letreros y tarjetas: son fundidos y no hay cuadros intrusos.
- `team8` (0,4× interpolado) no muestra artefactos visibles, y el rótulo ya no se superpone a sí mismo.
- Los pasos del Proceso coinciden con la toma.
- Resta 0,5 por la portada de escritorio: un 9:16 de 720 p ampliado y oscurecido, que no se reconoce como máquina (`escritorio_es_00`). Es un pedido pendiente al cliente; el montaje está aprobado.

### Selección y ritmo: 4,5 / 6
- La variedad mejoró: 4 repeticiones exactas en vez de 7. Servicios en el celular ahora se recorre rápido.
- Restan tres cosas:
  - Las etiquetas «RESERVADO» siguen apareciendo 3 veces: portada, stickers y proceso, que ocupa ~7 de sus 11,8 s.
  - Quedan 4 trabajos con el mismo archivo que su servicio.
  - En escritorio, Equipo deja un hueco mostaza de unos 540×600 px a la derecha del video del integrante (`escritorio_es_10`).

**Para llegar a 17 en Imagen:**
- Recortar en `tarjetas8` el tramo IG-40 (Sigmo y volantes): +0,5.
- Dar a Plateados, Transparentes, Prendas y Diplomas de Trabajos una foto fija o un tramo distinto: +0,5.
- Con eso queda en 17,5.

---

## Juez dueño: 18,5 / 20

| # | Ítem | Nota | Justificación |
|---|---|---|---|
| 1 | Me reconozco: voz, tono, nombre, logo, colores | **4/4** | Son nuestras frases y emojis, el 🚀 de la bio, el azul y el naranjo, y la carga con el logo. Ya no hay cifras que nunca dijimos. |
| 2 | Muestra lo que hacemos | **3,5/4** | Hay 13 servicios en una grilla compacta y «Y también: Pendones, Rollers, Adhesivos» dejó de ser una línea suelta. El proceso en 3 pasos coincide con el video. Los trabajos siguen viéndose de a uno (13 toques) y en el celular no hay pista del siguiente cliente. |
| 3 | Calidad visual y primera impresión | **3,5/4** | El escritorio ya no se ve a medio terminar en Servicios ni en Trabajos. Restan tres cosas: (a) en el celular, el botón de menú queda cortado en el borde derecho y la página se desliza 24 px hacia el lado (bloqueante 1); (b) en Reseñas, el borde inferior de las tarjetas giradas queda cortado en recto (`escritorio_es_11`, `movil_es_10`); (c) el hueco mostaza en Equipo en escritorio. |
| 4 | Cotizar y contactar desde el celular | **4/4** | «Cotiza» siempre a mano, WhatsApp con mensaje prellenado en ES y EN, Instagram, correo y Maps. El horario sigue pendiente con el cliente. |
| 5 | Confianza | **3,5/4** | El sello 4,6 y «Los mejores de Castro!» abren las reseñas, y aparecen clientes reconocibles. El equipo sigue sin nombres (es decisión, no la penalizo) y los clientes no se ven juntos de un vistazo. |
| | **Total** | **18,5/20** | |

**Mirada del dueño:** «Ahora sí se ve terminada en el computador, y en el celular se recorre rápido. La mandaría. Solo arreglen que en mi teléfono la página se mueve hacia el lado y el botón del menú sale cortado».

---

## BLOQUEANTES

| # | Dónde | Hallazgo | Propuesta concreta |
|---|---|---|---|
| 1 | `css/nv8/site.css` l. 349–351 (`.team{overflow:visible}` + `.burst{inset:-120px -40px -40px}`) | **Desborde horizontal en todo celular.** El `.burst` sobresale 24 px a cada lado de la tarjeta Team. `overflow-x:clip` en `body` (l. 4) no lo contiene, porque se propaga al viewport. Medido: `scrollWidth` es 436 en 412, 414 en 390 y 385 en 360. El header se estira y **el botón de menú queda cortado 8 px** a la derecha en todas las pantallas (`frames/nav_movil_recorte.png`), y la página se puede arrastrar de lado. Es una regresión del arreglo «estallido sin recorte». | Agregar `.s-equipo{overflow-x:clip}`, que recorta solo en horizontal y deja que los 🧉/☕ suban. **Verificado inyectando el estilo:** `scrollWidth` queda en 412 = `innerWidth` y el menú termina en 396 px. Otra opción es `.burst{inset:-120px 0 -40px}`. Después hay que repetir la prueba de desborde de la fase 17 (360–2560 px). |

No encontré otros bloqueantes de voz ni de imagen.

## Deseables (por impacto)

1. **Tarjetas sin Sigmo ni volantes.** En `tools/medios.py` / `assets/video/media.json` → `tarjetas8`, quitar los tramos IG-40 9,3–11,05 y 0–1,08. Dejar Erice y XS Joyas a ~0,5× (≈ 7 s) o repetir Erice con otro encuadre. Si queda bajo 8 s, anotarlo como las demás excepciones por falta de material.
2. **Reseñas con el borde inferior cortado.** `site.css` l. 146 `.res-pista{padding:6px 2px 18px}`: las tarjetas giradas se recortan abajo. Subir a `padding:14px 8px 40px` o reducir la rotación, y revisar `movil_es_10` y `escritorio_es_11`.
3. **Hueco en Equipo en escritorio.** `site.css` l. 343–346: con `.eq` en 2 columnas, la tarjeta Team queda arriba a la derecha y debajo queda vacío (~540×600 px). Dos opciones: (a) que el video del integrante (`.eq-fotos > video`) ocupe la columna derecha bajo Team, con `grid-row: span 2` para Team y el video; o (b) mover Team debajo de las fotos, a todo el ancho y horizontal.
4. **Cifras en EN.** `index.html` l. 96–97 y l. 175: agregar `data-en` al número («4.6», «100%»), o un `<b data-cuenta>` que formatee según `data-lang`.
5. **Trabajos sin repetir archivos de Servicios.** `index.html` l. 134: Despensa Chiloé, Dulce Enlatta, SSC Rental y Dekra usan el mismo video que su tarjeta de servicio. Usar un cuadro fijo distinto (póster en `<img>`) o un tramo alternativo del mismo reel.
6. **Diseño.** `diseno.mp4`: abrir con IG-44 0–1,4 (diseño de la medalla en pantalla) y encuadrar el monitor, no las persianas. Es lo que más resta pertinencia a Servicios.
7. **«RESERVADO» 3 veces.** Que la portada abra y se quede más en UV, láser y medallas, y dejar el plotter de «RESERVADO» para Proceso.
8. **Mapa en reposo.** `.mapa` (l. 163): poner la dirección y un pin dibujado como fondo mientras carga el iframe, para que nunca se vea una caja vacía si Google tarda o está bloqueado.
9. **Trazabilidad.** Crear `content/google.md` con las reseñas y el 4,6 (fecha y URL de la ficha) y verificar la URL de Facebook del pie (l. 204).
10. **Trabajos en el celular.** Bajo el contador, una pista del siguiente cliente («Siguiente: Miel Chiloé») o una tira de nombres, para que se vea el volumen sin tocar 13 veces.
