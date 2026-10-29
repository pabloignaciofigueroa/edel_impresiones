# Edel Impresiones — web

Web de Imprenta y Gráfica Edel (Castro, Chiloé), hecha solo con su propio material público (Instagram 2026, Facebook, Google).

- **Web publicada:** https://edelimpresiones.pages.dev/ (versión final nv8, oculta para buscadores con `noindex` y `robots.txt` hasta que el cliente la acepte).
- **Hosting:** Cloudflare Pages, proyecto `edelimpresiones`, rama `main`, sin build, salida `public/`. Cada push a `main` publica.
- **Versiones anteriores:** /nueva/ … /nueva_v8/ redirigen con 301 a la raíz. Todas siguen en el repo y respaldadas en la rama `respaldo-versiones`.

## Editar
1. Textos y estructura: `tools/boceto_nv8.py`, con la fuente de cada texto en `content/copy.md`. Estilos: `css/nv8/site.css`. Comportamiento: `js/nv8/site.js`.
2. `python3 tools/boceto_nv8.py --final` genera `index.html`, la raíz publicada. Sin `--final` genera la copia de trabajo `nueva_v8/index.html`.
3. `python3 tools/publish.py` regenera `public/`, lo único que se publica. Copia solo lo que la página usa y falla si se cuela algo interno o falta un archivo.
4. Commit y push a `main`: Cloudflare publica solo.

## Medios y marca
- **Videos y fotos:** `python3 tools/medios.py video <id> [<id>…]`.
  - Siempre con ids: sin ids rehace todo y pisa los cortes que usan las versiones anteriores.
  - Los cortes de la versión final llevan el sufijo `8`.
  - Las fuentes de cada corte están en `assets/video/media.json`.
- **Logo:** `python3 tools/logo.py` genera `brand/*.svg` desde el vector limpio `brand/_iso_vector.json`.
  - Los PNG de `brand/png/` se renderizan desde esos SVG.
  - La imagen para compartir es `assets/og-edel.jpg`.
- **Contraste de la paleta:** `python3 tools/contraste.py`.

## Documentación
- **Decisiones y su porqué:** `_plan/edel/justificacion.md`.
- **Pedidos pendientes al cliente:** al final de ese mismo archivo.
- **Guion con la fuente de cada texto:** `content/copy.md`.
- **Voz de marca:** `content/brand-voice.md`.
- **Paleta, tipografía y dirección de arte:** `brand/`.
- **Evaluaciones independientes (fase 19):** `_qa/fase19/` (primera ronda, sobre nv7) y `_qa/fase19b/` (segunda ronda, sobre nv8).
