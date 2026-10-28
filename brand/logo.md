# Logo — reconstrucción

Generador: `python3 tools/logo.py` (escribe `brand/*.svg`). Fuente de medidas: IG-01 (1080 px).

| Pieza | Método | Coincidencia con el original (IoU) |
|---|---|---|
| Isotipo azul | potrace a 4x sobre la mancha del original (`brand/_iso_trazado.json`) | 0,995 |
| Isotipo naranja | ídem | 0,993 |
| «edel» | trazos monolínea de 40 px, remates redondos; lóbulos r=56; diagonal de la «e» ajustada por búsqueda | 0,956 |
| GRÁFICA E / IMPRENTA | Montserrat 700 a trazos (fontTools), tracking hasta el ancho original | 0,74 / 0,66 (diferencias subpíxel de forma de letra) |

Primero se probó el isotipo geométrico (círculo menos círculo, error < 1 px en los arcos) y dio 0,93 / 0,90: las puntas del original son más largas que una medialuna de círculos. Se dejó el trazado.

Variantes: `isotipo`, `isotipo-blanco`, `logotipo`, `logo-horizontal`, `logo-horizontal-claro` (fondo tinta), `logo-vertical`, `logo-vertical-claro`, `favicon.svg` + `favicon.ico` + `png/favicon-16…512`.
Todos los trazos llevan `pathLength="1"` para dibujarlos en la carga (prueba: `_qa/logo/dibujo_logo.mp4`).

Imagen para compartir: `assets/og.jpg` 1200×630, 69 KB — logo claro sobre tinta + plotter de corte en acción (IG-30, segundo 2, sin rótulos).
