# Panel fase 19: voz de marca e imágenes/video (nueva_v7)

Evaluado el 2026-10-28 sobre http://localhost:8787/nueva_v7/. Celular 412×915 (DPR 2,6) y escritorio 1440×900, en ES y EN (botón del pie). Antes de puntuar se leyó entera la bitácora `_plan/edel/justificacion.md`: lo decidido ahí no resta puntos.
Material de respaldo en `_qa/fase19/panelA/`: 39 capturas, texto visible extraído del DOM (`*_texto_ES.txt`, `*_texto_EN.txt`), `recorrido.json` (estado de cada video y relación de aspecto de cada caja) y `frames/` (hojas de 10 cuadros por video, uniones del loop, cabezas cuadro a cuadro y pasos del proceso).

| Dimensión | Nota | Meta |
|---|---|---|
| A) Voz de marca | **15,5 / 20** | ≥ 17: no llega |
| B) Imágenes y video | **12,5 / 20** | ≥ 17: no llega |

---

## A) Voz de marca (15,5/20)

### Fidelidad: 6/8
- Comparé uno a uno contra `ig_posts.json`, `fb.md` y la bio todos los textos de marca: H1 (IG-16), los H2 (IG-22, IG-20, IG-30, IG-21, IG-18, IG-38), las bajadas (IG-22, IG-40, IG-43), las 13 tarjetas de servicio, los 3 pasos (IG-30 partida, aprobada), el cierre (IG-44), el juego de equipo (IG-35), el pie (BIO) y «Pendones, Rollers, Adhesivos» (FB-INTRO). Todos son literales y conservan la ortografía original. No encontré @ personales en el texto, promociones vencidas («Se acerca fin de año…» de IG-47 está bien excluido) ni teléfono antiguo.
- Las reseñas de Facebook (Fernando, Marta) son literales de `fb.md`.
- **Error 1: «Dulce Enlatta · Vasos grabados»** (EN «Engraved mugs»). El post de origen (IG-46) dice «imprimir tus stickers transparente en blanco», y el `aria-label` del mismo video dice «Sticker transparente impreso en blanco». Es un dato falso sobre el servicio, y además contradice la tarjeta «Transparentes».
- **Error 2: el chip «1º Pioneros en Chiloé»**. El «1º» no está en ninguna fuente; la bio dice «🚀 Pioneros en Chiloé». «+20 años de experiencia» es una adaptación aceptable del dato de la bio.
- **Error 3: Medallas empieza con un fragmento**, «…nosotros podemos realizarlas…». Es literal, pero «realizarlas» queda sin antecedente.
- **Falta de trazabilidad:** las 6 reseñas de Google (Silvana, Andrés, Cristian, Chilwe Gourmet, Alan y Luis) y el «4,6» solo constan en `brand-voice.md` y `copy.md`. No hay captura de origen en `content/`, como sí la hay para Facebook (`fb.md`).
- **Errores solo de documentación:** `copy.md` y `brand-voice.md` dicen «Berries & Miel Chiloé», pero la pieza dice «BERRIES & HIELO CHILOÉ» (la página está bien). `brand-voice.md` cataloga IG-46 como «Vasos grabados», y de ahí viene el error 1.

### Voz y tono: 5/6
- La voz se parece a su Instagram: tuteo, ✨ 💫 🙂‍↔️ como acentos, el humor de taller (Team Mate / Team Café, IG-38 en Cotiza) y los CTA propios («Háblanos al DM», «cotiza»).
- Resta lo siguiente:
  - La tarjeta Medallas, incompleta.
  - La tarjeta Diplomas es solo un llamado («Háblanos al DM…») mientras las demás describen el servicio. Además manda al DM, pero el botón de la web lleva a WhatsApp.
  - El H2 de Equipo (una oración de 20 palabras con ✨) pesa en escritorio y en celular ocupa 4 líneas en mayúsculas condensadas. Es literal y elegido, así que no resta por fidelidad, solo por ritmo de lectura.

### Interfaz y microcopias ES/EN: 4,5/6
- **Lo que está bien:**
  - Las microcopias ES no suenan a venta: «Ver trabajos», «Despega el sticker para ver el siguiente», «Toca las fotos para darlas vuelta».
  - En EN, la glosa del H1 («Your brand starts with a good impression») conserva el doble sentido, y «Our people», «Peel the sticker…» y «Skip to content» son correctos.
  - Funciona el cambio de `alt`, `aria` y `meta` (`data-meta-en`).
- **Lo que falla:**
  - «Engraved mugs» (ver error 1).
  - **Glosas EN incompletas:** solo 4 de 7 H2 llevan subtítulo en inglés (Portada, Intro, Servicios, Trabajos). Proceso («Así nace cada etiqueta»), Equipo y Cotiza quedan sin glosa, aunque `copy.md` fija la regla para todas las frases de marca.
  - «Message on Instagram» debería ser «Message us on Instagram», para que sea paralelo a «Message us on WhatsApp».
  - «Holographic silver» como rótulo queda cojo: debería ser «Holographic silver stickers».
  - En EN se ve «1º Pioneers in Chiloé» (ordinal español en la versión inglesa).
  - En escritorio, con mouse, dice «Toca las fotos…» / «Tap the photos…».

---

## B) Imágenes y video (12,5/20)

Inventario: 16 videos en loop (9:16, 540×960; la portada de escritorio es 720×1280) y 10 fotos. Los 23 elementos en pantalla se reprodujeron (readyState 4) y no hubo errores de JS. No vi tarjetas negras ni vacías por falta de medio. El mapa salió en blanco en el navegador sin red de la prueba, así que no lo puntúo.

### Pertinencia: 5,5/8
- **Muy bien:**
  - **Portada:** UV con luz azul, diplomas Dekra, plotter cortando «RESERVADO», medallas en UV y depilado. Vende el taller trabajando.
  - Plateados (Despensa Chiloé), Transparentes (Dulce Enlatta), Bitácoras (Chiloé Náutica), Prendas (SSC Rental), Medallas (diseño, láser, medalla y entrega en escenario), Láser (mostrador IG-24), Gráfica vehicular (Puro Lomo) y Proceso.
- **Tarjetas de presentación (`tarjetas.mp4`):** en el tercer tramo (IG-45 8,0–9,4) aparece un cuaderno anillado «Reiver Chiloé · Chequeo de salud pre-post inmersión». Es cerca de un tercio del loop y no es una tarjeta.
- **Diseño (`diseno.mp4`):** casi todo el loop es una mano haciendo el gesto de «chiquitito» frente a una pantalla en blanco, con las persianas ocupando media toma. Viene del reel de humor IG-33. Lee más a broma que a diseño; solo el último segundo (medalla RevelArte en pantalla) muestra diseño.
- **Impresión UV:** la cabeza del loop es una impresora de rollo (eco-solvente), no UV (ver el hallazgo B-2).
- **Stickers y etiquetas:** abre con un corte a cuchilla y regla sobre un impreso grande (IG-37), no sobre stickers. Es aceptable, pero no es lo mejor del material.
- **Privacidad en Diplomas:** en la tarjeta del celular se lee la nota, el n.º de oportunidad, las fechas, un **código QR nítido y escaneable** del certificado y el nombre del firmante, y en otros cuadros se leen nombres completos de los alumnos (p. ej. «Elizabeth Margoth Morales Aedo», «Juan Carlos Vera Aguilar»). Son datos personales de terceros (captura `frames/movil_diplomas_crop.png`).
- **Letreros:** el póster lleva «@estudio.soluna x @lamariannecoello». Con el recorte 4:5 y 1:1 esa línea cae fuera del encuadre; lo verifiqué y no resta, pero no conviene cambiar el `object-position`.
- **Fotos:** cada foto muestra lo que dice su rótulo. «Berries & Hielo», «XS Joyas · Etiquetas» (respaldado por IG-26) y «Sigma · Señaléticas» (IG-28) coinciden. Las franjas de IG-18 están aprobadas.

### Calidad técnica de loops y cortes: 3/6
- **Destello en la unión del loop.** Verificado cuadro a cuadro en `frames/cabezas_hero_uv_proceso.jpg` y `frames/*-seam.jpg`:
  - `hero.mp4`, `hero-540b.mp4`, `uv.mp4` y `proceso.mp4` empiezan con **4 cuadros (0,13 s) de otra toma**: la impresora de rollo, que sale del inicio de IG-45 en 0,6 s. Después hay un corte seco a la UV (scdet: corte en 0,133 s).
  - El fundido final del loop desemboca en esa toma intrusa, así que en cada vuelta se ve un parpadeo seguido de un salto. En la portada se repite cada 9,8 s.
  - `letreros.mp4` tiene lo mismo con 3 cuadros (corte en 0,1 s).
  - `medallas.mp4` abre con 0,4 s de pantalla y corta en seco al láser: queda nervioso, pero es tolerable.
- **Duración bajo la regla de 8–10 s en 9 de 16 videos:**

  | Video | Duración |
  |---|---|
  | `team` | 3,7 s |
  | `tarjetas` | 3,8 s |
  | `diplomas` | 6,0 s |
  | `prendas` | 6,2 s |
  | `letreros` | 6,3 s |
  | `uv` | 6,6 s |
  | `stickers` | 6,9 s |
  | `medallas` | 7,0 s |
  | `laser` | 7,6 s |

  La bitácora solo aprueba el `proceso` de 12,8 s. Lo de «tramos limpios de 4 s» es un pedido al cliente, no una excepción.
- **`team.mp4` (3,7 s):**
  - Las tazas salen de cuadro al 1,6 s, así que más de la mitad del loop muestra un monitor vacío.
  - En el fundido, el rótulo animado se superpone a sí mismo («Te tem mate cafe» ilegible por un instante).
- **Portada en escritorio:**
  - Un 9:16 de 720 px en una caja de 1440×1008 se recorta al 39 % de la altura y se amplía ×2. Se nota blando y con bloques (`escritorio_01_portada.png`).
  - Detrás del H1 domina el texto «RESERVADO/Cliente/Fecha de entrega», que compite con el titular.
  - El montaje está aprobado y el video horizontal es un pedido pendiente, así que lo cuento solo como calidad, no como decisión.
- **Recortes:**
  - `equipo.mp4` en escritorio (caja 1,455) muestra solo cara y pecho del 9:16, un recorte forzado pero legible.
  - En las tarjetas, el 4:5 y el 1:1 sobre 9:16 respetan el sujeto.
  - Fotos 3:4 → 1:1: bien.
- **Proceso:** el paso activo se adelanta. En 2,9 s se marca «plotter», pero la imagen sigue en la impresora hasta ~3,3 s; en 7,8 s se marca «depilado», pero el plotter sigue hasta ~8,2 s (`frames/proceso_pasos.jpg`).

### Selección y ritmo visual: 4/6
- **A favor:** la portada vende, y hay variedad de técnicas, color y gente real (equipo, manos y escenario de RevelArte).
- **Repetición:**
  - **7 de los 13 trabajos de la pila reusan exactamente el mismo video de Servicios**: plateados, transparentes, bitácoras, prendas, diplomas, medallas y letreros. El furgón de Puro Lomo también sale dos veces.
  - El tramo IG-45 0,6–3,2 está en `hero`, `uv` y `proceso`.
  - El plotter de «RESERVADO» aparece en portada, stickers y proceso.
  - Quien recorre la página ve las mismas tomas 2 o 3 veces.
- **Equipo en escritorio:** la tarjeta Team Mate / Team Café deja un **bloque azul tinta vacío de ~600×200 px** sobre el video y otro debajo de los botones (`escritorio_12_y7920.png`, `escritorio_13_y8640.png`). Es una tarjeta medio vacía.

---

## Hallazgos priorizados

### BLOQUEANTES

| # | Sección | Dónde | Hallazgo | Propuesta |
|---|---|---|---|---|
| B-1 | Trabajos | `nueva_v7/index.html`, 8.ª tarjeta: «Dulce Enlatta · Vasos grabados» / `data-en="Engraved mugs"` | Dato falso: contradice IG-46 y el propio `aria-label` | Rótulo [UI] «Stickers transparentes» / EN «Clear stickers», respaldado por IG-46 «¿Sabías que podemos imprimir tus stickers transparente en blanco? 😏✨». Corregir también `brand-voice.md` («Vasos grabados (IG-46)») |
| B-2 | Portada, Servicios (UV), Proceso, Letreros | `assets/video/hero.mp4`, `hero-540b.mp4`, `uv.mp4`, `proceso.mp4` (4 cuadros intrusos) y `letreros.mp4` (3 cuadros) | Destello y salto en cada vuelta del loop | En `tools/medios.py`, mover el tramo IG-45 de 0,6 a **0,75 s** (pasado el corte interno) e IG-34 de 3,5 a **3,6 s**. Re-codificar y verificar con `ffmpeg -vf scdet=threshold=12` que no quede ningún corte antes de 0,5 s. `hero-540b` cambia de id para el caché, igual que en la fase 18 |
| B-3 | Servicios: Tarjetas de presentación | `tarjetas.mp4`, tramo IG-45 8,0–9,4 | Un tercio del loop muestra un cuaderno Reiver Chiloé, no tarjetas; el loop dura 3,8 s | Quitar el tramo 8,0–9,4. Dejar IG-45 5,5–8,0 (Hojalatería Erice) e IG-31 3,0–4,4 (XS Joyas) y llevarlo a ≥ 8 s con velocidad 0,6× (son tomas casi fijas, sin artefactos), o usar como tarjeta la foto limpia de XS Joyas (IG-26) con un empuje lento. Agregar al dossier el pedido de tomas más largas de tarjetas (ya está) |
| B-4 | Servicios y Trabajos: Diplomas; portada (tramo IG-47 4,0–6,5) | `diplomas.mp4`, `hero*.mp4` | QR escaneable, nota y nombres completos de alumnos de Dekra legibles | Desenfoque gaussiano con seguimiento sobre la línea del nombre y el QR (`ffmpeg boxblur` con máscara por tramo), o elegir tramos donde la UV tape el nombre. Volver a revisar a 2,6× DPR |
| B-5 | Varias | `team` 3,7 s, `tarjetas` 3,8 s, `diplomas` 6,0, `prendas` 6,2, `letreros` 6,3, `uv` 6,6, `stickers` 6,9, `medallas` 7,0, `laser` 7,6 | Incumplen la regla de 8–10 s; los de menos de 4 s se notan como tic | Prioridad `team` y `tarjetas`. `team`: IG-35 0–8 s si el reel lo permite (el rótulo ya está aprobado); si no, 0,75× y no fundir el rótulo sobre sí mismo (cortar el loop en una pose estable del texto). `laser`: IG-24 9,5→18,5. `diplomas`: IG-47 6,0–9,3 + 10,0–14,9. Los demás: sumar tramos limpios del mismo reel, nunca de otro servicio |

### Deseables

| # | Sección | Dónde | Propuesta |
|---|---|---|---|
| D-1 | Trabajos | Pila de 13 | Que los 7 trabajos repetidos no usen el mismo archivo de Servicios: tramos alternativos del mismo reel (bitácoras de IG-31; medallas solo con la entrega en escenario, IG-44 7,5–12,7; letreros solo con la toma del póster terminado; prendas con otro tramo de IG-42) o fotos fijas. También evita descargas dobles en la vista |
| D-2 | Servicios: Medallas | `<p>` de la tarjeta IG-44 | Frase completa literal de IG-44: «Si tienes un evento y quieres entregar medallas personalizadas, nosotros podemos realizarlas 🙂‍↔️ desde el diseño hasta la entrega final 💪🏼🥇» |
| D-3 | Intro, chips | `<b>1º</b>` | Reemplazar «1º» por 🚀, el emoji de la bio en «🚀 Pioneros en Chiloé» [BIO], o dejar el chip sin cifra. En EN desaparece así «1º Pioneers» |
| D-4 | EN | H2 de Proceso, Equipo y Cotiza | Agregar la glosa `<p lang="en" hidden>` como en las otras 4: «How each label is made» / «Behind every business there's a human team giving it their all every day to give you the best service ✨» / «However you describe the size of the job you need, we'll understand you and get it done» |
| D-5 | EN, interfaz | Cotiza; tarjeta Plateados | «Message on Instagram» → «Message us on Instagram»; «Holographic silver» → «Holographic silver stickers» |
| D-6 | Equipo (escritorio) | Texto de ayuda | Con `@media (hover:hover)`: «Haz clic en las fotos para darlas vuelta» / «Click the photos to flip them» |
| D-7 | Equipo (escritorio) | Tarjeta Team Mate / Team Café | Ajustar la caja a su contenido (video arriba y texto centrado verticalmente), sin los ~600×200 px vacíos |
| D-8 | Proceso | `<ol data-p2="2.9" data-p3="7.8">` | `data-p2="3.3"`, `data-p3="8.2"`, para que el paso marcado coincida con la toma |
| D-9 | Portada (escritorio) | `hero.mp4` en 1440×1008 | Mientras no llegue el video horizontal, evitar la ampliación ×2: el video a su tamaño nativo en una columna derecha con el titular a la izquierda, o un tope de `max-width` con fondo tinta. Evaluar también un tramo de arranque sin «RESERVADO» detrás del H1 (p. ej. la UV con luz azul) |
| D-10 | Servicios: Diseño | `diseno.mp4` | Encuadrar la pantalla (no las persianas) y abrir con IG-44 0–1,4 (diseño «FINAL / CORTE» de la medalla) en vez de cerrarlo; si se suma texto: «Creamos propuestas visuales pensadas en tu marca, tu estilo y lo que quieres comunicar.» [IG-19] |
| D-11 | Reseñas | `content/` | Guardar una captura o transcripción fechada de las reseñas de Google y del 4,6 (p. ej. `content/google.md`) para que el [DATO] sea verificable igual que `fb.md` |
| D-12 | Documentación | `content/copy.md` l. 61, `content/brand-voice.md` l. 49 | «Berries & Miel Chiloé» → «Berries & Hielo Chiloé» (así dice la pieza) |
| D-13 | Pie | Enlace `facebook.com/edel.chiloe/` | No consta en `fb.md`; verificar la URL real de la página «Imprenta y Gráfica Edel - Castro» y anotarla |

**Para llegar a ≥ 17:**
- **Voz:** con B-1, D-2, D-3, D-4 y D-5, Voz sube a unos 18.
- **Imagen:** con B-2 a B-5 y D-1, Imagen sube a unos 17. La portada de escritorio (D-9) y Diseño (D-10) dan el margen.
