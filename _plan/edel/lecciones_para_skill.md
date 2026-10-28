# Lecciones para la skill web-regalo-cold-call (marcadas por Pablo)

## ★ Pantalla de carga: dibujo del logo sin salto + % real (Edel, nv7 · 2026-10-28)
Pablo: «Quedó increíble… márcalo con un asterisco, esto lo vas a replicar en la skill».

1. ★ **Logo como vector limpio, uno solo para todo.** No usar el calco (potrace) para el dibujo: rehacer el isotipo con un agente vectorial (Bézier por mínimos cuadrados sobre el borde subpíxel del original, G1 en uniones, puntas agudas; IoU ≥ 0,99, error medio < 0,6 px, pocos nodos). El mismo path sirve para relleno, dibujo y logo del menú.
2. ★ **Contorno hacia adentro con máscara (no trazo encima).** Cada forma es un solo elemento: el relleno real del logo con `mask` = el mismo path trazado en blanco. Máscara a 2 px → queda 1 px visible hacia adentro; al cerrar, la misma máscara pierde el guion y engrosa hacia adentro hasta `wMax`; al final se agrega la forma rellena a la máscara. Nunca se cambia de elemento → 0 px de diferencia en el borde (medido). No quitar la máscara al terminar. `clip-path` y trazos superpuestos fallan (bordes distintos).
   - Guion bidireccional desde una punta (`dasharray a gap b 0`) para que borde exterior e interior avancen juntos y se cierren en la otra punta. Path reordenado para partir en la punta.
   - Color del trazo = colores del logo (si el tono oscuro no se lee a 1 px, levantarlo y volver al tono del logo antes de engrosar). Nunca blanco puro.
   - Letras monolínea: ordenar los trazos para que se lean bien mientras se dibujan (la «d» con la panza primero, si no parece «J»).
   - Especificación completa: edel_impresiones/_qa/agentes/diseno/especificacion.md.
3. ★ **Sin destello al cargar.** El SVG de la carga oculto (`visibility:hidden`) hasta que el JS lo ubicó; el % también. Fondo de marca en `<style>` inline en el `<head>` (sin cuadro blanco). Remates redondos ocultos mientras su trazo mide 0 (si no, aparecen puntos sueltos). Verificar con screencast cuadro a cuadro de los primeros 2 s.
4. ★ **% real por bytes.** Lista con pesos medidos en el build (fuentes, portada completa, pósters de todos los videos, primeros videos de la sección siguiente); `fetch` por partes con `ReadableStream`, el % = bytes recibidos / total; lo descargado queda como objectURL y los `<video>` lo usan (la portada se pide una sola vez, sin `src` en el HTML). Mínimo 3 s y tope 8 s contados desde `performance.now() = 0` (inicio de la navegación), no desde que corre el script.
5. ★ **Método con Pablo:** cuando un detalle visual no resulta tras dos intentos, lanzar agentes especialistas independientes (vectorial + diseñador) con el código, las capturas y sus palabras textuales; entregar MP4 de prueba fuera del sitio antes de integrar.
