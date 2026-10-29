# Edel Impresiones: traspaso para el dossier

Web regalo terminada y publicada el 2026-10-28. Este documento es lo que necesita otra sesión para armar el dossier y entregarlo en la visita al cliente.

## Datos
| | |
|---|---|
| Web publicada | https://edelimpresiones.pages.dev/ |
| Visibilidad | Oculta para buscadores (`noindex`, `X-Robots-Tag` y `robots.txt`) hasta que el cliente la acepte |
| Repositorio | `pabloignaciofigueroa/edel_impresiones`, rama `main` (versión final); todas las versiones en `respaldo-versiones` |
| Hosting | Cloudflare Pages, proyecto `edelimpresiones`; cada push a `main` publica |
| Cliente | Imprenta y Gráfica Edel («Edel Impresiones»), Eduardo Provasoli 619, Castro, Chiloé |
| Contacto | WhatsApp +56 9 8282 3772 · edelimpresiones@hotmail.com |
| Redes | IG @edel.chiloe · FB facebook.com/edel.chiloe |

- **Skill para el dossier:** `dossier-brochure-web-regalo`: 14 láminas de 13×8,5 in, en PDF y HTML.
- **Material en el PC de Pablo:** `C:\Users\pfigug\Desktop\edel_impresiones`, con las carpetas 00_hojas, 01_imagenes, 02_videos y 03_textos.
- **Correo:** prohibido enviarlo. La entrega es en persona.

## Qué tiene la web, sección por sección (con su origen)
Todo texto visible es literal de la marca o un dato verificable. La fuente de cada texto está en `content/copy.md` y las decisiones en `_plan/edel/justificacion.md`. Solo se usa material real de sus redes: nada de stock.

0. **Carga:**
   - El isotipo se dibuja con una línea fina hacia adentro, en azul y naranjo, y se rellena sin salto de borde.
   - Después se escribe «edel» trazo a trazo y aparece la bajada.
   - El % es real: bytes de la portada, mínimo 3 s y tope 8 s.
   - Luego «la e se abre»: la contraforma del isotipo es la ventana al video de las máquinas.
   - Método marcado ★ para la skill.
1. **Portada:**
   - Titular «Tu marca empieza por una buena impresión» (IG-16).
   - Banda «Pioneros en Chiloé · Más de 20 años de experiencia nos respaldan» (bio).
   - Video de máquinas trabajando (UV, plotter, láser, depilado).
   - Botones «Cotiza por WhatsApp», con el mensaje prellenado «Hola Edel, quiero cotizar un trabajo», y «Ver trabajos».
2. **Intro:**
   - «Hacemos realidad tus proyectos» (IG-22).
   - Cifras: +20 años, 🚀 Pioneros en Chiloé, 4,6 en Google, 100 % recomendado en Facebook.
3. **Servicios:**
   - Título «Las ideas son infinitas… y nosotros tenemos cómo hacerlas realidad» (IG-20).
   - 13 tarjetas con rótulo, frase literal de su post y video o foto propia. Una línea de troquel punteada se dibuja alrededor de cada una, y la de plateados lleva brillo tornasol.
   - Cierra con «Y también: Pendones, Rollers, Adhesivos» (Facebook).
   - Celular: grilla de 2 columnas. Escritorio: grilla pareja de 3.
4. **Proceso:**
   - «Así nace cada etiqueta», con 3 pasos literales de IG-30.
   - El paso marcado sigue al video: imprimir, plotter, depilado.
5. **Trabajos:**
   - «El detalle hace la diferencia» (IG-21).
   - Pila de 13 stickers de clientes reales que se despegan con el dedo o con el botón.
   - Clientes: Puro Lomo, Miel Chiloé, Naguara, Berries & Hielo, XS Joyas, Sigma, Despensa Chiloé, Dulce Enlatta, Chiloé Náutica, SSC Rental, Dekra, RevelArte, Pilates & Skincare.
6. **Equipo:**
   - Título literal de IG-18.
   - Fotos que giran, con frases del post en el dorso.
   - Juego «Team Mate o Team Café» (IG-35): estallido de 🧉 o ☕.
7. **Reseñas:**
   - El «4,6» se estampa como sello.
   - 8 reseñas literales, de Google y Facebook, que avanzan solas y se despegan como stickers.
8. **Cotiza:**
   - Frase literal de IG-38.
   - WhatsApp, Instagram, correo, dirección y mapa.
9. **Pie:** logo, bio e idioma ES/EN. El idioma está en el menú y en el pie. Las frases de la marca quedan en español y llevan una glosa en inglés.

## Proceso y evaluación (para contar en el dossier)
- 20 fases: inventario de 47 posts IG, voz, tipografías (Anton, Oswald, Montserrat), paleta desde su logo y piezas, logo reconstruido como vector limpio, guion, medios, dirección de arte, construcción, QA y cierre.
- Pablo revisó cada fase desde el celular. Las versiones v1 a v8 quedaron respaldadas.
- **Evaluación independiente (fase 19):** 4 evaluadores que no construyeron la web. Informes en `_plan/edel/evaluaciones/ronda1` (sobre v7) y `ronda2` (sobre v8).

| Evaluación | Ronda 1 (v7) | Ronda 2 (v8) | Meta |
|---|---|---|---|
| Juez dueño («¿se la mostrarías mañana?») | 17 | 18,5 | 17 |
| Voz de marca | 15,5 | 18,5 | 17 |
| Imágenes y video | 12,5 | 16,5* | 17 |
| Servicios y color | 14 | 18 | 17 |
| Entretención | 16 (3/4) | 17 → 19 con el arreglo final (4/4) | 17 / 4 |
| QA técnico | 3 bloqueantes | 0 bloqueantes | 0 |

\* Después de esa nota se recortó el video de Tarjetas (sacaba volantes). El evaluador estimó que con eso y con tomas propias para Trabajos llega a ~17,5; no se volvió a medir.

**Medido en v8:**
- Abre en 4,8 s en 4G y en < 8 s en roaming.
- CLS 0,0002.
- Contraste AA en todos los textos.
- 0 errores.
- 23/23 videos funcionando en la web publicada.

## Decisiones que conviene contar (el porqué)
- **Privacidad:** el reel de diplomas (IG-47) mostraba nombres de alumnos y un QR escaneable. Se difuminó, aunque el video luce menos.
- **Corrección de un dato:** «Dulce Enlatta» eran stickers transparentes (IG-46), no vasos grabados.
- **«IMPRESIÓN»:** va en blanco sobre banda naranja, para que se lea sobre el video. Es la banda de sus propias piezas.
- **Sin crédito del estudio:** es la página de Edel, no de Bergerac.

## Preguntas y pedidos al cliente (van en el dossier)
- Horario de atención (no está publicado).
- Nombres del equipo (IG-18), si quieren aparecer.
- Confirmar como clientes a XS Joyas (IG-26), Sigma (IG-28) y Despensa Chiloé (IG-29).
- Confirmar la URL de Facebook. Captura o enlace de las reseñas de Google: el 4,6 se tomó el 2026-10-28.
- Originales sin rótulos de los reels IG-16 (impresora UV) e IG-36 (Buena Pizza Social Club).
- Fotos sin texto de: galvanos (IG-15), llaveros (IG-17), tarjetas (IG-22/23), stickers troquelados (IG-21) y pendones/rollers 2026.
- Tomas más largas (≥ 10 s, sin rótulos), hoy cortas por falta de material:
  - Team Mate/Café (7,6 s).
  - Prendas (6,2 s).
  - Medallas, letreros y bitácoras terminados.
  - Proceso.
  - Tarjetas.
- Diplomas con datos ficticios o con autorización, para no tener que difuminar.
- Videos de las máquinas en horizontal (escritorio) y vertical (celular), en alta.
- Si aceptan la web: dominio propio y permiso para que Google la indexe.
