# Carta de envío (regalo) de Bergerac · Edel Impresiones
# Mismo formato que la de Chiloé Mágico (chiloemagico-carta-envio.pdf): 13 × 8,5 in, mitad crema y mitad grafito.
# Genera dossier/edel-carta-regalo.html; render.js la pasa a PDF y la antepone al dossier para el anillado.
import base64, io, pathlib
import qrcode
from PIL import Image

D = pathlib.Path(__file__).resolve().parent
K = D / 'carta'
URL = 'edelimpresiones.pages.dev'
MARCA = 'Edel Impresiones'
ROJO = '#fb0278'   # fucsia Bergerac (bergerac.cl), en la segunda línea del titular (Pablo)
AMARILLO, GRAFITO, CREMA = '#ffb701', '#282828', '#fdfcfa'

def b64(path, w=None, fmt='JPEG', q=84):
    im = Image.open(path)
    im = im.convert('RGBA' if fmt == 'PNG' else 'RGB')
    if w and im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, fmt, **({'quality': q} if fmt == 'JPEG' else {'optimize': True}))
    return f'data:image/{fmt.lower()};base64,' + base64.b64encode(buf.getvalue()).decode()
def font(f): return 'data:font/woff2;base64,' + base64.b64encode((K / f).read_bytes()).decode()
def qr(url):
    q = qrcode.QRCode(border=1, box_size=10, error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data(url); q.make(fit=True)
    buf = io.BytesIO(); q.make_image(fill_color='black', back_color='white').save(buf, 'PNG')
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()

# imagen: la portada del brochure (la impresora UV con su logo), no una captura con texto (Pablo)
LOGOV = D.parent / 'brand/png/logo-vertical-claro.png'  # misma portada del brochure: franja tinta + impresora UV

HTML = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{MARCA} · Carta de Bergerac</title><style>
@font-face{{font-family:"Alfa";src:url({font("alfa-slab-one-latin-400-normal.woff2")}) format("woff2")}}
@font-face{{font-family:"Alfa";src:url({font("alfa-slab-one-latin-ext-400-normal.woff2")}) format("woff2");unicode-range:U+0100-024F}}
@font-face{{font-family:"Mona";font-weight:300;src:url({font("mona-sans-latin-300-normal.woff2")}) format("woff2")}}
@font-face{{font-family:"Mona";font-weight:500;src:url({font("mona-sans-latin-500-normal.woff2")}) format("woff2")}}
@font-face{{font-family:"Mona";font-weight:600;src:url({font("mona-sans-latin-600-normal.woff2")}) format("woff2")}}
@font-face{{font-family:"Mona";font-weight:900;src:url({font("mona-sans-latin-900-normal.woff2")}) format("woff2")}}
@page{{size:13in 8.5in;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:"Mona",Arial,sans-serif;font-weight:500;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.hoja{{width:13in;height:8.5in;position:relative;overflow:hidden;display:flex}}
.izq{{width:6.5in;height:100%;background:{CREMA};color:{GRAFITO};position:relative;padding:.5in .54in}}
.der{{width:6.5in;height:100%;background:{GRAFITO};color:#e3e2e0;position:relative;padding:.58in .5in .5in .49in}}
.marca{{display:flex;align-items:center;gap:.09in}}
.marca img{{height:.31in}}
.marca span{{font-weight:600;font-size:13.5pt;letter-spacing:.02em}}
.fecha{{position:absolute;right:.54in;top:.62in;font-size:6.6pt;letter-spacing:.24em;text-transform:uppercase}}
h1{{font-family:"Alfa";font-weight:400;font-size:26pt;line-height:1;text-transform:uppercase;margin-top:.36in;letter-spacing:.005em}}
h1 em{{font-style:normal;color:{ROJO}}}
.foto{{margin-top:.3in;height:2.55in;border-radius:.2in;overflow:hidden}}
.foto img{{width:100%;height:100%;object-fit:cover;display:block}}
.pie-foto{{font-size:6.2pt;color:#8a8987;margin-top:.1in}}
.izq .p{{font-size:9.1pt;line-height:1.62;margin-top:.12in}}
.izq .p.hola{{margin-top:.34in}}
.base{{position:absolute;left:.54in;bottom:.36in;font-size:6.2pt;letter-spacing:.26em;color:#8a8987;text-transform:uppercase}}
.der .p{{font-size:9.1pt;line-height:1.62;margin-bottom:.14in}}
.der .y{{color:{AMARILLO};font-weight:600;font-size:18.2pt;line-height:1.25;margin-bottom:.16in}}
.captura{{border-radius:.16in;overflow:hidden;margin:0 0 .14in;height:1.95in;position:relative}}
.captura{{display:flex;background:#05263f}}
.captura .cm{{width:2.2in;flex:none;display:flex;align-items:center;justify-content:center}}
.captura .cm img{{height:1.5in;display:block}}
.captura .cf{{flex:1;min-width:0;height:100%;object-fit:cover;object-position:50% 22%;display:block}}
.captura .tab{{position:absolute;left:0;top:.2in;background:#fff;opacity:.85;padding:.08in .16in .08in .2in;border-radius:0 .1in .1in 0}}
.captura .tab img{{width:1.15in;display:block}}
.cap{{display:flex;justify-content:space-between;align-items:center;gap:.2in;margin-bottom:.16in}}
.cap p{{font-size:8pt;line-height:1.5;color:#cfcecc}}
.cap b{{display:block;color:#fff;font-weight:900;font-size:15pt;letter-spacing:.005em;margin-top:.05in}}
.cap img{{width:1.1in;height:1.1in;display:block;border-radius:3pt;flex:none}}
.firma{{position:absolute;left:.49in;right:.5in;bottom:.36in;border-top:.6pt solid #555;padding-top:.13in;display:flex;justify-content:space-between;align-items:flex-end}}
.firma .who{{font-family:"Alfa";font-size:11pt;color:#fff;letter-spacing:.02em}}
.firma .rol{{font-size:8pt;color:#cfcecc;margin-top:.03in}}
.firma a{{font-family:"Alfa";font-size:13pt;color:{AMARILLO};text-decoration:none;letter-spacing:.02em}}
</style></head><body><article class="hoja">
<section class="izq">
  <div class="marca"><img src="{b64(K / "bergerac-icon.png", 300, "PNG")}" alt=""><span>BERGERAC</span></div>
  <p class="fecha">Castro, octubre de 2026</p>
  <h1>Estudiando<br>marcas de Chiloé,<br><em>nos encontramos con<br>{MARCA}.</em></h1>
  <div class="foto"><img src="{b64(K / "putemun.jpg", 1600)}" alt=""></div>
  <p class="pie-foto">La vista desde nuestro estudio, en Putemún.</p>
  <p class="p hola">Hola, equipo de {MARCA}:</p>
  <p class="p">Somos Bergerac, un estudio digital de Castro. Hace un tiempo comenzamos a estudiar negocios y marcas de Chiloé que tienen una presencia especialmente atractiva en redes sociales. En ese recorrido, {MARCA} nos llamó la atención de inmediato. Sus reels muestran sus máquinas trabajando, sus piezas llevan una banda naranja que se reconoce al instante, y su propia frase ya lo dice todo: tu marca empieza por una buena impresión.</p>
  <p class="base">Bergerac · Estudio digital · Castro, Chiloé</p>
</section>
<section class="der">
  <p class="p">Nos gusta trabajar en proyectos que nos motivan, así que decidimos hacer algo con eso. Construimos un sitio web para {MARCA} usando únicamente lo que ya comparten: sus publicaciones, sus fotografías, sus videos y las reseñas públicas de sus clientes.</p>
  <p class="p y">Es un regalo. Si les gusta, es suyo.</p>
  <div class="captura"><div class="cm"><img src="{b64(LOGOV, 500, "PNG")}" alt="Edel Impresiones"></div><img class="cf" src="{b64(D / "fotos/portada-uv.jpg", 1440)}" alt=""></div>
  <div class="cap"><p>El sitio que hicimos para {MARCA}.<br>Escanea el código o entra a<b>{URL}</b></p><img src="{qr("https://" + URL)}" alt=""></div>
  <p class="p">Solo les pedimos una cosa a cambio, y únicamente si están de acuerdo: poder nombrar a {MARCA} en nuestra página, con su nombre y su logo, entre los trabajos que hemos realizado en la isla. Y si por cualquier motivo prefieren que no siga en línea, lo retiramos sin problema.</p>
  <p class="p">Junto a esta carta va también el dossier de decisiones de diseño, donde explicamos cada elección que tomamos a partir del material que encontramos.</p>
  <p class="p">Ante todo, muchas gracias por darse el tiempo de revisarlo. Lo hicimos con esmero y dedicación. Ojalá les guste.</p>
  <div class="firma"><div><p class="who">PABLO FIGUEROA G.</p><p class="rol">Director de estudio</p></div><a href="https://bergerac.cl">BERGERAC.CL</a></div>
</section>
</article></body></html>'''
(D / 'edel-carta-regalo.html').write_text(HTML, encoding='utf-8')
print('carta ok', round(len(HTML) / 1e6, 2), 'MB')
