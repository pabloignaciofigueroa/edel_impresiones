# Tipografía — Edel Impresiones

Método: recortes de sus piezas 2026 (IG-17, IG-18, IG-19, IG-23, IG-27) y del logo (IG-01), comparados contra candidatas de @fontsource renderizadas a igual tamaño (`_qa/tipo/comparacion.jpg`).

| Uso | Lo que usa la marca | Fuente web (libre) | Pesos | Por qué |
|---|---|---|---|---|
| Titulares (display) | Grotesca condensada muy pesada, mayúsculas («TARJETAS», «LLAVEROS», «DISEÑAMOS») | **Anton** | 400 | La más cercana en peso y compresión; League Gothic y Bebas quedan delgadas, Archivo Black es ancha. |
| Bajadas / rótulos | Condensada bold con tracking amplio, sobre banda naranja («TUS PROYECTOS», «EQUIPO HUMANO», «CORTE ACRÍLICO») | **Oswald** | 500, 600 | Igual forma y ritmo con `letter-spacing: .18em`. |
| Texto | Geométrica de lectura («La que siempre encuentra la forma…») | **Montserrat** | 400, 500, 700 | Coincide en «a», «g», «f» y proporción. También la más cercana a «GRÁFICA E IMPRENTA» del logo (700 con tracking). |
| Logotipo «edel» | Dibujo monolínea redondeado (no es una fuente) | — | — | Se reconstruye como SVG de trazos con remates redondos en la fase 5 (permite dibujarlo trazo a trazo en la carga). |

Los reels usan Poppins en sus rótulos (plantilla de edición del video): no se adopta para la web.

## Archivos
Autoalojados en `assets/fonts/` solo los woff2 usados (subconjuntos latin y latin-ext): Anton 400; Oswald 500/600; Montserrat 400/500/700. Declarados en `css/fonts.css` con `font-display: swap`. Se precargan Anton 400 latin y Montserrat 500 latin (arriba del pliegue).

## Reglas de uso
- Anton solo en mayúsculas, interlineado ≥ 1,22 (con 0,92, 1,02 y 1,12 las tildes de Ó, Í, É chocan con la línea de arriba: probado en `_qa/tipo`), nunca bajo 32 px.
- Oswald en mayúsculas con tracking .14–.2em, sobre banda de color (naranja o azul), como en sus piezas.
- Montserrat para todo texto corrido; mínimo 16 px (regla 10), cuerpo 17–18 px.
- Licencias: SIL Open Font License 1.1 (las tres).
- Comillas en Anton: sus «» se ven chicas (parecen "<<"); en citas se usan comillas “ ” o una comilla grande decorativa en Oswald.
