# Bitácora de decisiones (para el dossier)

- 2026-10-28 · Nombre «Edel Impresiones» (Pablo). Respaldo: así firman en IG-16, IG-21, IG-25, IG-31.
- 2026-10-28 · Clientes visibles como portafolio (Pablo): son trabajos que la marca publicó.
- 2026-10-28 · Se deja fuera 2022–2023 y el teléfono antiguo (Pablo).
- 2026-10-28 · Se excluyen IG-27 y piezas de solo texto (Pablo).

## Pedidos pendientes al cliente
- Horario de atención (no está publicado).
- Nombres del equipo (IG-18) si quieren aparecer.
- Videos originales en horizontal y vertical de las máquinas (los de IG son 720p).
- 2026-10-28 · Titular de portada: «Tu marca empieza por una buena impresión» [IG-16] (Pablo). «Hacemos realidad tus proyectos» [IG-22] y «Las ideas son infinitas… y nosotros tenemos cómo hacerlas realidad» [IG-20] se usan dentro de la página (Pablo).
- 2026-10-28 · Movimiento: intermedio-festivo (Pablo). Se suma «Entretención» a la evaluación.
- 2026-10-28 · Equipo sin nombres (Pablo); se piden en el dossier.
- 2026-10-28 · XS Joyas (IG-26) y Sigma (IG-28) se muestran como clientes; en el dossier se pregunta si son reales (Pablo).
- 2026-10-28 · Imagen para compartir: plotter de corte cortando etiquetas «RESERVADO» (IG-30). En una imprenta, lo que vende es la máquina trabajando.
- 2026-10-28 · Prueba de carga con cabezal de impresión (`_qa/logo/cabezal_logo.mp4`): contorno a lápiz, cuatro pasadas de ida y vuelta que imprimen el isotipo, luego «edel» trazo a trazo. En celular se usa el logo vertical para que el isotipo se vea grande.
- 2026-10-28 · Carga: se descarta el cabezal; queda la versión de dibujo a lápiz (`_qa/logo/dibujo_logo.mp4`): contorno, relleno, «edel» trazo a trazo y bajada (Pablo).
- 2026-10-28 · Carga: se descarta el cabezal (Pablo: se veía feo y bajaba la calidad). Queda la versión de dibujo a lápiz (`_qa/logo/dibujo_logo.mp4`): contorno, relleno, «edel» trazo a trazo y bajada.
- 2026-10-28 · Guion (fase 6) en content/copy.md. Pendientes al cliente sumados: foto 2026 de pendones/rollers; confirmar Despensa Chiloé (IG-29) como cliente.
- 2026-10-28 · Guion cerrado (Pablo): rótulo portada «Pioneros en Chiloé · Más de 20 años…» [BIO]; bajada intro IG-22; proceso en tres pasos (IG-30 partida, autorizado); equipo con juego «Team Mate / Team Café» (IG-35); Cotiza con IG-38; pie sin crédito de Bergerac.
- 2026-10-28 · Medios (fase 7): 18 videos en loop sin rótulos y 12 fotos limpias (tools/medios.py, hojas en _qa/medios). Descartados por texto encima: reels IG-16 (IMPRESIÓN UV) e IG-36 (burbujas de chat); fotos IG-15, 17, 19, 20, 21, 22, 23, 32 y IG-18 #1/#2.
## Pedidos al cliente (medios)
- Originales sin rótulos de los reels IG-16 (impresora UV) e IG-36 (Buena Pizza Social Club).
- Fotos sin texto de: galvanos (IG-15), llaveros (IG-17), tarjetas (IG-22/23), stickers troquelados (IG-21).
- Tomas más largas del proceso (imprimir → plotter → depilado) y de tarjetas: hoy los tramos limpios duran 4 s.
- Videos de las máquinas en horizontal (escritorio) y vertical (celular), en alta.
- 2026-10-28 · Medios (Pablo): IG-35 se usa con su rótulo «Team Mate o Team Café»; fotos del equipo IG-18 #3/#4 aprobadas pese a la franja e isotipo; proceso en un solo video de 12,8 s con pasos marcados; tarjeta Galvanos fuera hasta tener foto; montaje de portada aprobado.
- 2026-10-28 · Fase 9: base en /nueva/ (tools/boceto_nv1.py, css/nv1, js/nv1). Carga con % real (fuentes, póster, primeros 3 s del video; mín 3 s, tope 8 s). Apertura «la e se abre»: la contraforma del isotipo es la ventana al video de las máquinas; zoom que acelera y desvanece primero el naranjo. publish.py adaptado de almud_bar y probado (falla con archivo faltante o interno).
- 2026-10-28 · Cloudflare Pages creado por la vía de Pages (no Workers): proyecto «edelimpresiones», rama main, sin framework ni build, salida public. Verificado en línea: / → /nueva/ (302), rutas internas 404 igual que una inventada, og.jpg 200, 0 imágenes rotas, mapa de Google activo.
- 2026-10-28 · nv2 (/nueva_v2/, fases 10–15). /nueva/ queda congelada en el commit 7d4a298. Servicios: línea de troquel punteada que se dibuja al entrar; tarjeta de plateados con brillo tornasol que sigue el dedo o la inclinación; en escritorio tres columnas independientes con desfase y el primer servicio grande a la izquierda. Trabajos: pila de stickers que se despegan (arrastrar o «Siguiente trabajo»), con esquina que se levanta. Equipo: fotos que giran (dorsos literales de IG-18), Team Mate / Team Café con estallido de 🧉/☕. Cotiza: botón magnético con mouse.
- 2026-10-28 · nv3 (/nueva_v3/, fases 16–17). /nueva_v2/ congelada en 25f3c30. Menú de celular a pantalla completa (role=dialog, aria-modal, Cerrar primero, foco atrapado, resto inert, Escape cierra, gsap.killTweensOf). Botones magnéticos en portada, nav y Cotiza. Títulos con text-wrap: balance. Nav inert mientras carga. Al girar el celular se vuelve a la sección que se veía.
- QA fase 17 (local, public/): 360, 390, 412, 768, 1024, 1280, 1440, 1920, 2560 px → 0 desborde, 0 textos < 16 px, 0 títulos con palabra sola, 0 líneas de título pisadas, 0 errores JS; menú OK en < 1000 px; movimiento reducido y sin JS: todo visible.
- 2026-10-28 · Fase 18 (QA, sobre public/ servido en local). Hallazgo: el primer pantallazo del celular pesaba 3,67 MB (4G medio) y 2,23 MB (roaming) porque durante la carga se pedían el video de Stickers y los pósters de todos los servicios. Corrección en nv4 (/nueva_v4/; /nueva_v3/ congelada en 9a09689): videos diferidos y sus pósters se piden recién al abrirse el logo; portada liviana re-codificada con id nuevo hero-540b (979 KB, antes 1,36 MB; la original queda para las copias congeladas). Resultado: 1,48 MB en roaming sin compresión (Cloudflare comprime el JS), abre en 5,7 s (4G) y 7,4 s (roaming).
- Resto del QA: 0 cuadros con video fuera de la boca del isotipo; CLS 0,0003 (celular) y 0,0009 (escritorio); 23/23 videos en play; contraste AA 0 fallas en 329 textos (ES y EN); 0 anclas o recursos rotos; 0 errores JS; sin vercel/github.io; cuentas solo @edel.chiloe.
- 2026-10-28 · nv5 (/nueva_v5/; /nueva_v4/ congelada en 0f490b1), revisión de Pablo:
  · Destello: el contorno del isotipo se veía 0,6–1,1 s en tamaño crudo antes de ubicarse (confirmado cuadro a cuadro). Ahora el logo y el % quedan ocultos hasta estar ubicados, y el fondo es tinta desde el primer byte (sin cuadro blanco).
  · Dibujo: el contorno se traza en los colores del logo (azul y naranjo), con una curva suavizada solo para la línea (potrace: 26 y 12 segmentos en vez de 110 y 41); el relleno sigue siendo el calco exacto. Sin puntos sueltos de los remates redondos.
  · Portada: la banda «Pioneros en Chiloé…» pasa debajo del título.
  · Idioma: sale de la barra; queda dentro del menú (celular) y en el pie (todas las pantallas). Las letras «edel» de la carga siguen en blanco (Pablo).
- 2026-10-28 · nv6 (/nueva_v6/; /nueva_v5/ congelada en f53b825): % de carga real por bytes (Pablo: «que ese porcentaje sea real de carga»). Lista medida en el build: fuentes, portada completa, pósters de todos los videos y los primeros tres videos de Servicios (opción b de Pablo): 4,3 MB en celular, 7,3 MB en escritorio. Se descarga con fetch por partes y queda en memoria (objectURL): la portada se pide una sola vez y los videos de Servicios la reutilizan. Mínimo 3 s y tope 8 s contados desde el inicio de la carga (antes se contaban desde que corría el script: en roaming el tope caía a los ~10,5 s). Medido: wifi 100 % a los 3,4 s (limitado por el mínimo); 4G medio sube al ritmo de los bytes hasta 73 % a los 7,8 s y el tope completa a los 8,3 s; roaming 24 % a los 7,8 s y tope.
- 2026-10-28 · nv7 (/nueva_v7/; /nueva_v6/ congelada en e30375d). Dibujo del isotipo rehecho con dos agentes independientes (Pablo pidió «un agente de dibujo vectorial y un agente de diseño gráfico»):
  · Agente vectorial: isotipo como vector limpio (10 + 6 curvas Bézier, IoU 0,991/0,993, error medio 0,15 px, puntas agudas) → brand/_iso_vector.json. Se usa para relleno, dibujo y logo del menú.
  · Agente de diseño: cada medialuna es un solo elemento (el relleno real) y se anima su máscara con el mismo path: línea de 1 px hacia adentro (Pablo: «el contorno hacia adentro, para que cuando entre el real no exista diferencia»; 60 % más delgada), que luego se engrosa hacia adentro hasta llenar. Medido: 0 px de diferencia en el borde contra el logo final. Línea azul algo más clara al inicio (#1aa8d8→#0a6cb0) que vuelve al degradado del logo antes de engrosar (aprobado por Pablo). Especificación: _qa/agentes/diseno/especificacion.md.
  · «d» de «edel» dibujada primero la panza y luego el asta (antes se leía «J»).
- Pendiente: brand/*.svg y PNG del logo siguen con el calco potrace; pasar a brand/_iso_vector.json antes del cierre (fase 20).
