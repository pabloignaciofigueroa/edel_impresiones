# Dirección de arte — Edel Impresiones

Nivel de movimiento: **intermedio-festivo** (Pablo). Su Instagram mezcla taller real (máquinas, manos, materiales) con humor (🙂‍↔️, «Team Mate o Team Café»). La web tiene que sentirse como estar en el taller viendo salir los trabajos.
Idea rectora: **la página se imprime frente a ti.** Cada sección «sale de la máquina»: tinta que entra, cortes de plotter, stickers que se despegan.

## Ritmo (alto de cada sección, fondo, densidad)
| # | Sección | Fondo | Alto | Densidad | Movimiento |
|---|---|---|---|---|---|
| 0 | Carga | Tinta | 100svh | mínima | logo a lápiz al ritmo del % real |
| 1 | Portada | Tinta + video | 100svh (nada asoma) | baja | **momento memorable** |
| 2 | Intro | Papel | ~80svh | media | titular «se imprime» línea a línea; cifras cuentan |
| 3 | Servicios | Azul | libre | alta | tarjetas con video que entran «troqueladas» |
| 4 | Proceso | Luz UV | 100svh, sticky | baja | un video, tres pasos que se encienden según su tiempo |
| 5 | Trabajos y clientes | Papel + tornasol | libre | alta | baraja de stickers que se despegan |
| 6 | Equipo | Madera | ~100svh | media | Team Mate / Team Café + fotos que giran |
| 7 | Reseñas | Naranja | ~70svh | media | etiquetas que avanzan solas y se arrastran |
| 8 | Cotiza | Tinta + cian | 100svh | baja | botón WhatsApp magnético, mapa siempre activo |
| 9 | Pie | Tinta | corto | baja | — |
Alternancia oscuro/claro: tinta → papel → azul → UV → papel → madera → naranja → tinta. Nunca dos claros ni dos oscuros seguidos.

## Momento memorable — «la e se abre»
1. La carga dibuja el logo a lápiz (contorno → relleno → «edel» → bajada), al ritmo del % real (mín. 3 s, tope 8 s).
2. Al 100 %, «edel» y la bajada se van; el isotipo queda solo y su **contraforma** (el hueco oscuro entre la medialuna azul y la naranja) se convierte en ventana: crece pegada al isotipo, mismo centro y misma curva, y a través de ella aparece el video de las máquinas, que arranca desde 0 en ese instante (oculto con `visibility:hidden` hasta entonces).
3. La ventana sigue creciendo hasta cubrir la pantalla; el isotipo se queda chico arriba a la izquierda como logo del menú.
4. Entra el titular «Tu marca empieza por una buena impresión» línea por línea con un barrido de tinta (izquierda → derecha), y la banda naranja «Pioneros en Chiloé · Más de 20 años…» se desliza.

## Sistema de movimiento
- Curva única: `cubic-bezier(.16,1,.3,1)` (expo-out). Duraciones: 0,5 s (UI), 0,8 s (titulares), 1,1 s (apertura). Escalonado 0,06 s.
- **Barrido de tinta** (titulares Anton): cada línea entra con `clip-path` de izquierda a derecha y un leve desplazamiento vertical; es la firma tipográfica.
- **Troquel** (tarjetas de servicios): entran con un contorno punteado que se dibuja (como la línea de corte del plotter) y luego aparece el contenido.
- **Despegar** (Trabajos): stickers apilados; se arrastran o se tocan y se despegan con una esquina que se curva, y vuelven al fondo de la pila. Es el gesto de su reel de depilado.
- **Tornasol**: la tarjeta de plateados y el subrayado de Trabajos llevan un brillo holográfico que se mueve con el puntero o la inclinación (solo decorativo).
- Banda de rótulos (Oswald sobre naranja) que entra deslizándose desde el borde.
- Contadores en la intro («Más de 20 años», «4,6») que suben al verse.
- Botones magnéticos, subrayados que crecen.
- Videos: autoplay, mute, loop; **nunca dependen del scroll** ni se pausan. El proceso marca el paso activo por `currentTime` del video, no por scroll.

## Reglas técnicas
- Lenis + GSAP/ScrollTrigger vendorizados; **sin `pin`**: fijaciones con contenedor de alto `recorrido + 100vh` y un hijo `position: sticky`.
- Parallax con `inset` negativo en el medio. Sin saltos de layout (CLS < 0,01).
- `prefers-reduced-motion`: todo aparece sin animación, los videos muestran el póster y se pueden reproducir. Sin JS se lee todo.
- Grillas de columnas independientes con desfase que se mantiene; en escritorio el video estrella a un lado y las fotos llenan el otro.

## Celular primero
- Portada: video vertical 540 px (1,4 MB), el mismo montaje en escritorio a 720 px recortado con cover.
- Servicios en una columna con tarjetas de video 4:5; Trabajos como pila de stickers a ancho completo; Reseñas a ancho completo.
