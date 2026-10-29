# Evaluación independiente — Web de Edel Impresiones (fase 19, segunda ronda sobre nv8)

Eres un evaluador independiente: no construiste esta web. Evalúa con ojo crítico y honesto; no infles notas. Escribe en español.

## Qué es
Web "regalo" (prospección en frío) para Imprenta y Gráfica Edel, Castro, Chiloé (@edel.chiloe): imprenta y gráfica (stickers, impresión UV, corte láser, gráfica vehicular, letreros, bitácoras, diplomas, prendas, medallas, diseño). Se hizo SOLO con su material público (Instagram 2026, Facebook, Google). Regla de oro: todo texto visible es literal de la marca o un dato verificable (ghostwriter estricto); solo material real (sus fotos y videos), nada de stock.

## Dónde verla (local, servidor ya corriendo)
- Página: http://localhost:8787/nueva_v8/  (es la versión a evaluar; ignora /nueva/ … /nueva_v7/, son copias congeladas)
- Navegador: Playwright con Chromium ya instalado (`require('playwright')` desde node, `chromium.launch()` sin opciones). Usa celular 412×915 (deviceScaleFactor 2.6, isMobile, hasTouch) y escritorio 1440×900. La carga dura 3–8 s: espera ~7 s antes de evaluar la portada. Para recorrer: `lenis.scrollTo(y,{immediate:true})` o `scrollTo`.
- Puedes sacar capturas y grabar video (recordVideo) y mirarlos (lee las imágenes). ffmpeg está instalado.

## Fuentes para contrastar
- Guion con la fuente de cada texto: /home/claude/edel_impresiones/content/copy.md
- Voz de marca y corpus: /home/claude/edel_impresiones/content/brand-voice.md · captions originales: /home/claude/edel_impresiones/content/ig_posts.json · Facebook/reseñas: /home/claude/edel_impresiones/content/fb.md
- Paleta y tipografía: /home/claude/edel_impresiones/brand/palette.md, typography.md, art-direction.md
- Medios: /home/claude/edel_impresiones/assets/video/media.json (cortes y fuentes), /home/claude/edel_impresiones/assets/img/media.json; hojas de contacto del material original en /home/claude/edel_impresiones/_qa/hoja_fotos.jpg, hoja_reels_1.jpg, hoja_reels_2.jpg
- **Decisiones ya tomadas por el dueño del estudio (NO restan puntos):** /home/claude/edel_impresiones/_plan/edel/justificacion.md (léelo entero antes de puntuar). Entre ellas: nombre «Edel Impresiones»; se excluye lo de 2022–2023; titular «Tu marca empieza por una buena impresión»; equipo sin nombres; IG-35 se usa con su rótulo; fotos IG-18 con franja; galvanos fuera; textos con su ortografía original («stickers transparente», «de que Team eres»); sin crédito del estudio; idioma ES/EN solo en menú y pie; nivel de movimiento intermedio-festivo; pantalla de carga con dibujo del logo (aprobada).

## Reglas de la casa (para juzgar)
Ghostwriter estricto con fuente; nada inventado; nunca @ personales; contenido de origen en su idioma (interfaz traducida); diseño desde el sistema visual de la marca; solo material real; videos 8–10 s en loop sin rótulos (salvo decisiones); ningún texto < 16 px; contraste AA; CLS < 0,01; nada asoma bajo la portada; sin JS se lee todo; prefers-reduced-motion respetado.

## No hagas
No modifiques NINGÚN archivo del proyecto ni hagas commits. Escribe solo en tu carpeta de salida indicada.

## Segunda ronda
La primera ronda evaluó nv7: informes en /home/claude/edel_impresiones/_qa/fase19/ (juez_dueno.md, panel_voz_imagen.md, panel_servicios_entretencion.md, qa_tecnico.md) y el consolidado CONSOLIDADO.md. nv8 aplica sus arreglos. Decisiones nuevas del dueño (no restan): Servicios en celular en grilla de 2 columnas; escritorio en grilla pareja con pieza final «Y también: Pendones, Rollers, Adhesivos»; Trabajos con la pila junto al título; sello «4,6» y reseñas que se despegan; WhatsApp con mensaje prellenado («Hola Edel, quiero cotizar un trabajo»); el % de carga cuenta solo la portada; «IMPRESIÓN» en blanco sobre banda naranja (contraste); diplomas difuminados por privacidad (se ven desenfocados a propósito); Team 7,6 s y Prendas 6,2 s y los 3 videos propios de Trabajos (3,5–5,7 s) quedan cortos por falta de material (pedido al cliente en el dossier).
Verifica primero que los hallazgos de la primera ronda estén resueltos y luego busca problemas nuevos. Solo cuenta como bloqueante algo que realmente impida mostrarle la web al cliente mañana.
