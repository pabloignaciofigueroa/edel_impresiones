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
