# Edel Impresiones — web

Web de Imprenta y Gráfica Edel (Castro, Chiloé), hecha con su propio material público.
- Versión de trabajo: https://edelimpresiones.pages.dev/nueva/ (la raíz redirige ahí mientras se trabaja)
- Hosting: Cloudflare Pages, proyecto `edelimpresiones`, rama `main`, sin build, salida `public/`.

## Editar
1. Textos y estructura: `tools/boceto_nv1.py` (fuente de cada texto en `content/copy.md`). Estilos: `css/nv1/site.css`. Comportamiento: `js/nv1/site.js`.
2. `python3 tools/boceto_nv1.py` → genera `nueva/index.html`.
3. `python3 tools/publish.py` → regenera `public/` (lo único que se publica). Falla si se cuela algo interno o falta un archivo.
4. Commit y push a `main`: Cloudflare publica solo.

Medios: `python3 tools/medios.py` (cortes de video y fotos), logo: `python3 tools/logo.py`.
