# Dossier-brochure · Edel Impresiones (Bergerac, oct 2026)
# Genera dossier/edel-dossier-diseno.html (autocontenido). La carta de regalo de Bergerac va aparte (build_carta.py).
# Adaptado de chiloe_magico_tours/dossier/build_dossier.py. Cifras calculadas desde los archivos.
import base64, html, io, json, pathlib, re
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = ROOT / 'dossier'
SH = D / 'shots'
FT = D / 'fotos'
RAW = ROOT / 'assets/raw/ig'
E = html.escape

# ---------- fuentes citables y cifras (desde los archivos) ----------
MESES = 'ene feb mar abr may jun jul ago sep oct nov dic'.split()
IGJ = json.loads((ROOT / 'content/ig_posts.json').read_text(encoding='utf-8'))
POSTS = {p['id']: p for p in IGJ['posts']}
def fecha(iso): y, m, d = iso.split('-'); return f'{int(d)} {MESES[int(m) - 1]} {y}'
def IG(n): return f'Instagram · {fecha(POSTS[f"IG-{n}"]["fecha"])}'
CORPUS = [p for p in IGJ['posts'] if p['fecha'] >= '2026' and p['id'] != 'IG-27']
N_POSTS = len(CORPUS); N_REELS = sum(p['tipo'] == 'reel' for p in CORPUS)
DESDE, HASTA = fecha(min(p['fecha'] for p in CORPUS)), fecha(max(p['fecha'] for p in CORPUS))
PAGE = (ROOT / 'index.html').read_text(encoding='utf-8')
VID = json.loads((ROOT / 'assets/video/media.json').read_text(encoding='utf-8'))
FOT = json.loads((ROOT / 'assets/img/media.json').read_text(encoding='utf-8'))
vids = sorted({v for v in re.findall(r'assets/video/([a-z0-9-]+)\.mp4', PAGE) if not v.endswith('-540b')})
fots = sorted(set(re.findall(r'assets/img/([a-z0-9-]+?)-\d+\.webp', PAGE)))
N_VIDEOS = len(vids)
N_REELS_USADOS = len({t[0] for v in vids for t in VID[v]['tramos']})
N_FOTOS = len(fots); N_POSTS_FOTOS = len({FOT[f]['fuente'] for f in fots})
N_SERV = len(re.findall(r'<article class="serv', PAGE))
N_TRAB = len(re.findall(r'<li class="sticker"', PAGE))
N_RES = len(re.findall(r'<figure class="resena"', PAGE))
N_RES_G = len(re.findall(r'vía</span> Google', PAGE)); N_RES_F = N_RES - N_RES_G
CLIENTES = [html.unescape(c) for c in re.findall(r'<li class="sticker">.*?<b>(.*?)</b>', PAGE)]
assert N_SERV == 13 and N_TRAB == 13 and N_RES == 8, (N_SERV, N_TRAB, N_RES)
NOTA_G, N_G, FB_PCT, N_FB = '4,6', 10, '100 %', 6     # content/brand-voice.md · Datos verificables (2026-10-28)

# ---------- imágenes ----------
def b64img(img, w, q=80):
    img = ImageOps.exif_transpose(img).convert('RGB')
    if img.width > w:
        img = img.resize((w, round(img.height * w / img.width)), Image.LANCZOS)
    buf = io.BytesIO(); img.save(buf, 'JPEG', quality=q, optimize=True, progressive=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()
def shot(name, w=1500): return b64img(Image.open(SH / f'{name}.jpg'), w)
def raw(f, w=1500, q=82): return b64img(Image.open(RAW / f), w, q)
def fot(f, w=1500, q=82): return b64img(Image.open(FT / f), w, q)
def font(name): return 'data:font/woff2;base64,' + base64.b64encode((ROOT / 'assets/fonts' / f'{name}.woff2').read_bytes()).decode()
def png_file(rel, w=900):
    im = Image.open(ROOT / rel).convert('RGBA')
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True)
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()

# originales de Instagram usados como fotos
R = dict(llaveros='IG-17_DXW7rwCkbUs_1.jpg', disenamos='IG-19_DXfC6kjkQaU_1.jpg', troquelados='IG-21_DXh__qBkTB-_1.jpg',
         cocina='IG-22_DXjt3eCkQj1_1.jpg', tarjetas='IG-23_DXnJhAjkako_1.jpg', sigma='IG-28_DYfXezbxOP2_1.jpg',
         auspicio='IG-41_DcJb-cfu29x_1.jpg', equipo1='IG-18_DXZ39nRkXCt_1.jpg', equipo3='IG-18_DXZ39nRkXCt_3.jpg',
         equipo4='IG-18_DXZ39nRkXCt_4.jpg', van='IG-39_Da52kcUERCq_1.jpg', miel='IG-43_DctSvfaEZz3_1.jpg',
         xs='IG-26_DX9jQqLRBD8_1.jpg', reiver='IG-32_DZnUOscxYBm_1.jpg', pilates='IG-34_DZ-3uhCPyk__1.jpg')

# ---------- paleta (css/tokens.css) ----------
C = dict(tinta='#05263f', azul='#0358a5', cian='#0195ca', cianluz='#3bb6e6', naranja='#fa621f', banda='#ce4204',
         uv='#2e279f', uvluz='#545fe0', madera='#d3a03c', papel='#f3f0eb', gris='#5f6062')
TI, AZ, CI, CL, NA, BA = C['tinta'], C['azul'], C['cian'], C['cianluz'], C['naranja'], C['banda']
UV, UL, MA, PA, GR = C['uv'], C['uvluz'], C['madera'], C['papel'], C['gris']
TORNA = 'linear-gradient(115deg,#6b9fd7 0%,#cc7c9c 38%,#5e5da8 70%,#6b9fd7 100%)'

# ---------- helpers de maqueta (pulgadas) ----------
L, n = [], 0
def nx():
    global n; n += 1; return n
def lam(bg, inner, nc='rgba(5,38,63,.45)', cls=''):
    k = nx()
    return f'<article class="lam free {cls}" style="background:{bg}">{inner}<span class="no" style="color:{nc}">{k:02d}</span></article>'
def box(x, y, w, inner, cls='', st=''): return f'<div class="tx {cls}" style="left:{x}in;top:{y}in;width:{w}in;{st}">{inner}</div>'
def fr(name, x, y, w, rot=0, z=2, crop=None):
    st = f'height:{crop}in;' if crop else ''
    return f'<div class="fr" style="left:{x}in;top:{y}in;width:{w}in;{st}transform:rotate({rot}deg);z-index:{z}"><img src="{shot(name, 1400)}" alt=""></div>'
def ph(name, x, y, w, rot=0, z=3, crop=None):
    st = f'height:{crop}in;' if crop else ''
    return f'<div class="ph" style="left:{x}in;top:{y}in;width:{w}in;{st}transform:rotate({rot}deg);z-index:{z}"><img src="{shot(name, 600)}" alt=""></div>'
def photo(srcuri, x, y, w, h, r=.24, pos='50% 50%', z=1, rot=0, cls=''):
    return f'<div class="pic {cls}" style="left:{x}in;top:{y}in;width:{w}in;height:{h}in;border-radius:{r}in;transform:rotate({rot}deg);z-index:{z}"><img src="{srcuri}" style="object-position:{pos}" alt=""></div>'
def sticker(srcuri, x, y, w, h, rot=0, z=2, cap='', pos='50% 50%'):
    c = f'<span>{cap}</span>' if cap else ''
    return f'<div class="stk" style="left:{x}in;top:{y}in;width:{w}in;transform:rotate({rot}deg);z-index:{z}"><img src="{srcuri}" style="height:{h}in;object-position:{pos}" alt="">{c}</div>'
def medal(x, y, d, bg, fg, html_, rot=0, fs=11, z=4):
    return f'<div class="md" style="left:{x}in;top:{y}in;width:{d}in;height:{d}in;background:{bg};color:{fg};transform:rotate({rot}deg);font-size:{fs}pt;z-index:{z}"><div>{html_}</div></div>'
def banda(t, bg=BA, fg='#fff'): return f'<span class="bnd" style="background:{bg};color:{fg}">{t}</span>'
def pill(t, bg, fg='#fff'): return f'<span class="pill" style="background:{bg};color:{fg}">{E(t)}</span>'
def Q(text, source, cls=''): return f'<blockquote class="q2 {cls}"><p>“{text}”</p><cite>{E(source)}</cite></blockquote>'
def iso(x, y, w, z=3, op=1): return f'<img class="abs" src="{png_file("brand/png/isotipo.png", 500)}" style="left:{x}in;top:{y}in;width:{w}in;z-index:{z};opacity:{op}" alt="">'
def troq(x, y, w, h, c='rgba(255,255,255,.7)', r=.3, z=1):
    return f'<div class="troq" style="left:{x}in;top:{y}in;width:{w}in;height:{h}in;border-color:{c};border-radius:{r}in;z-index:{z}"></div>'
def seal(x, y, d, rot=-8):
    ring = 'PARA EDEL IMPRESIONES ★ HECHO EN CASTRO ★ OCTUBRE 2026 ★ '
    return f'''<svg class="seal" viewBox="0 0 200 200" style="left:{x}in;top:{y}in;width:{d}in;height:{d}in;transform:rotate({rot}deg)">
  <defs><path id="sr" d="M100,100 m-74,0 a74,74 0 1,1 148,0 a74,74 0 1,1 -148,0"/></defs>
  <circle cx="100" cy="100" r="98" fill="{BA}"/>
  <circle cx="100" cy="100" r="91" fill="none" stroke="#fff" stroke-width="2"/>
  <circle cx="100" cy="100" r="58" fill="none" stroke="#fff" stroke-width="1.5"/>
  <text font-family="Montserrat" font-weight="700" font-size="10.4" fill="#fff"><textPath href="#sr" textLength="462" lengthAdjust="spacing">{ring}</textPath></text>
  <text x="100" y="97" text-anchor="middle" font-family="Anton" font-size="30" fill="#fff">UN</text>
  <text x="100" y="128" text-anchor="middle" font-family="Anton" font-size="30" fill="#fff">REGALO</text>
</svg>'''
LOGO_CLARO = png_file('brand/png/logo-horizontal-claro.png', 1000)
LOGO = png_file('brand/png/logo-horizontal.png', 1000)


# ======================= LÁMINAS DEL DOSSIER =======================
# 01 · PORTADA · la impresora UV a doble página, solo el logo
nx()
L.append(f'''<article class="lam spread">
  <img class="bleed" src="{fot("portada.jpg", 2600, 86)}" style="object-position:50% 50%" alt="">
  <div class="spread-tab"><img class="spread-logo" src="{LOGO}" alt="Edel Impresiones"></div>
</article>''')

# 02 · CARTA · papel, foto del equipo, sello
L.append(lam(PA,
  photo(raw(R['equipo3'], 1300), .5, .5, 5.4, 7.5, pos='50% 55%', z=2) +
  troq(.34, .34, 5.72, 7.82, 'rgba(5,38,63,.35)', .34) +
  seal(8.9, 5.75, 2.15) +
  box(6.45, .7, 6.0, f'''<p class="k" style="color:{BA}">Antes de empezar</p>
  <h2 class="t" style="color:{TI}">Un sitio hecho <em style="color:{BA}">con</em> lo que ustedes ya publican</h2>
  <div class="letter2">
  <p>Equipo de Edel Impresiones:</p>
  <p>Cada título del sitio viene de sus posts, de su bio o de lo que sus clientes escribieron en Google y Facebook. Ninguna frase de la marca es inventada y no hay fotos de banco: las imágenes y los videos son los de su Instagram.</p>
  <p>La letra, los colores y el logo salen de sus propias piezas. Estas páginas cuentan de dónde viene cada decisión.</p>
  <p>Ojalá lo disfruten tanto como nosotros disfrutamos haciéndolo.</p>
  <p class="sign2">Pablo Figueroa G.</p></div>''')))

# 03 · DE DÓNDE VIENE TODO · azul, sus piezas como stickers, cifras gigantes
pol = [(raw(R['llaveros'], 520), .5, .55, -7), (raw(R['tarjetas'], 520), 2.45, .4, 4), (fot('IG-29_f6.png', 420), 4.4, .75, -3),
       (raw(R['troquelados'], 520), .7, 3.05, 5), (fot('IG-35_f2.png', 420), 2.7, 2.9, -5), (raw(R['sigma'], 520), 4.55, 3.2, 6),
       (raw(R['disenamos'], 520), 1.0, 5.45, -4), (fot('IG-44_f9.png', 420), 3.05, 5.35, 3)]
polh = ''.join(f'<div class="pol" style="left:{x}in;top:{y}in;transform:rotate({r}deg)"><img src="{s}" alt=""></div>' for s, x, y, r in pol)
def big(nm, cap): return f'<div class="bign"><b>{nm}</b><span>{cap}</span></div>'
L.append(lam(AZ, polh +
  box(6.9, .65, 5.65, f'''<p class="k" style="color:{CL}">De dónde viene todo</p>
  <h2 class="t" style="color:#fff">Todo esto <em style="color:{NA}">ya</em> era suyo</h2>
  <div class="bigs">{big(N_POSTS, "publicaciones suyas de 2026, del 15 de abril al 28 de septiembre")}{big(N_REELS_USADOS, "de sus reels dan vida a los videos del sitio")}{big(N_SERV, "servicios, cada uno con su video o su foto")}{big(N_RES, "reseñas de sus clientes, al pie de la letra")}</div>
  <p class="p" style="color:#fff">Cada texto tiene su origen identificado: un post, su bio, su página de Facebook o una reseña. Lo que ustedes aún no publican, como el horario de atención, no se inventa: queda <b>por confirmar con ustedes</b>.</p>'''),
  nc='rgba(255,255,255,.7)'))

# 04 · LA MARCA · papel, rótulo de su pieza a tamaño cartel, paleta en franjas
stripes = [('papel', 'Papel', TI), ('madera', 'Madera del taller', TI), ('naranja', 'Naranja Edel', TI), ('banda', 'Banda naranja', '#fff'),
           ('cian', 'Cian del isotipo', TI), ('azul', 'Azul Edel', '#fff'), ('uv', 'Luz UV', '#fff'), ('tinta', 'Tinta', '#fff')]
sth = ''.join(f'<div class="stripe" style="background:{C[k]};color:{fg}"><span class="sn">{nm}</span><span class="sh">{C[k]}</span></div>' for k, nm, fg in stripes)
L.append(lam(PA, f'<div class="stripes">{sth}<div class="stripe torna" style="background:{TORNA};color:#fff"><span class="sn">Tornasol</span><span class="sh">plateados</span></div></div>' +
  box(.55, .55, 6.9, f'''<p class="k" style="color:{BA}">La marca · letra, color y logo</p>
  <p class="spa">TARJETAS</p><p class="spb">{banda("DE PRESENTACIÓN")}</p>
  <p class="cap2">Así rotulan sus piezas ({IG("23")}) · Anton para títulos, Oswald para las bandas, Montserrat para el resto</p>''') +
  box(.55, 4.05, 6.9, f'''<div class="cols3">
  <div><h4 style="color:{BA}">Letra</h4><p>Viene de sus piezas: un título pesado y angosto en mayúsculas, y debajo una banda naranja con letras espaciadas. En el sitio, cada servicio lleva esa misma banda.</p></div>
  <div><h4 style="color:{AZ}">Color</h4><p>Viene de su logo, de sus piezas y de su taller: el azul y el naranja del isotipo, la madera de sus muros, la luz de la impresora UV y el brillo de los stickers plateados.</p></div>
  <div><h4 style="color:{BA}">Logo</h4><p>Se redibujó siguiendo su logo original, curva por curva, para que se vea nítido a cualquier tamaño: del ícono de la pestaña a un letrero.</p></div></div>''') +
  f'<img class="abs" src="{LOGO}" style="left:.55in;top:6.75in;width:2.6in" alt="">' +
  box(3.6, 6.85, 3.8, '<p class="p sm">Estos códigos son de pantalla; para imprimir conviene llevarlos a CMYK o Pantone.</p>'), cls='no-izq'))

# 05 · RECORRIDO · tinta, 4 actos con medallones
actos = [('d-hero', 'Entrar', 'La carga, la apertura y sus máquinas en marcha.', -3),
         ('d-serv2', 'Elegir', f'Sus {N_SERV} servicios, con video o foto y su propia frase.', 2),
         ('d-trab', 'Confiar', 'Trabajos para sus clientes, el equipo y sus reseñas.', -2),
         ('d-cot', 'Cotizar', 'WhatsApp con el mensaje listo, Instagram y correo.', 3)]
ah = ''
for i, (s_, t_, p_, r_) in enumerate(actos):
    x = .5 + i * 3.1
    ah += fr(s_, x, 2.95, 2.85, r_) + medal(x + 2.1, 2.45, .95, NA, TI, f'<b class="mdn">{i + 1}</b>', rot=-r_ * 2, z=5)
    ah += box(x, 5.25, 2.8, f'<h3 class="t3" style="color:#fff">{t_}</h3><p class="p" style="color:rgba(255,255,255,.88)">{p_}</p>')
L.append(lam(TI, iso(11.25, .45, 1.25, 1, .9) +
  box(.5, .6, 9.5, f'''<p class="k" style="color:{CL}">El recorrido</p>
  <h2 class="t" style="color:#fff">Una visita al taller, <em style="color:{NA}">en</em> cuatro pasos</h2>''') + ah +
  box(.5, 7.45, 12, f'<p class="p" style="color:rgba(255,255,255,.7)">El orden sigue al de un cliente que llega por primera vez: ver qué hacen, ver cómo lo hacen, ver para quién lo han hecho y escribirles.</p>'),
  nc='rgba(255,255,255,.6)'))

# 06 · EL MOMENTO · la «e» se abre (cuadros de la carga)
L.append(f'<article class="lam free" style="background:{TI}"><img class="bleed abs0" src="{shot("d-abre-450", 2400)}" style="object-position:70% 50%" alt="">' +
  fr('d-carga1c', .6, 4.35, 2.3, -4, 5) + fr('d-carga2c', 3.15, 4.75, 2.3, 3, 4) + medal(5.05, 4.2, 1.15, NA, TI, 'Así<br>carga', rot=10, fs=12, z=6) +
  box(.55, .6, 5.3, f'''<p class="k" style="color:{CL}">La llegada</p>
  <h2 class="t" style="color:{TI}">Su letra e, <em style="color:{BA}">hecha</em> ventana</h2>
  <p class="p">Mientras el sitio carga, su logo se dibuja con una línea fina en sus propios colores, se rellena y escribe «edel» trazo a trazo. Al terminar, el hueco oscuro de la «e» se abre como una ventana y por ella entran sus máquinas trabajando.</p>
  <p class="p">El número avanza con lo que de verdad ya se descargó de la portada, y a los pocos segundos abre igual, aunque haya poca señal.</p>''', 'card', f'background:{PA};') +
  f'<span class="no" style="color:rgba(255,255,255,.7)">{nx():02d}</span></article>')

# 07 · PORTADA DEL SITIO · tinta + UV, navegador y celular
L.append(lam(UV,
  box(.55, .65, 4.3, f'''<p class="k" style="color:{CL}">La portada</p>
  <h2 class="t" style="color:#fff">Su frase <em style="color:{NA}">sobre</em> sus máquinas</h2>
  <p class="p" style="color:rgba(255,255,255,.92)">El título es su propio post: «Tu marca empieza por una buena impresión». Funciona en los dos sentidos, como ustedes lo escribieron. Detrás, un video armado con sus reels: la impresora UV, el plotter de corte y el depilado.</p>
  <p class="p" style="color:rgba(255,255,255,.92)">La banda naranja repite su bio: «Pioneros en Chiloé · Más de 20 años de experiencia nos respaldan». Dos botones: cotizar por WhatsApp o ver trabajos.</p>''') +
  box(.55, 5.35, 4.1, Q('Tu marca empieza por una buena impresión 🔥', IG('16')), 'card', f'background:{PA};') +
  fr('d-hero', 5.3, .65, 7.25, 1.5) + ph('m-hero', 11.15, 3.45, 1.6, 5) +
  box(6.85, 5.55, 4.1, f'<div class="pills">{pill("Pioneros en Chiloé", BA)}{pill("Más de 20 años", PA, TI)}{pill(f"{NOTA_G} en Google", NA, TI)}{pill(f"{FB_PCT} recomendado en Facebook", PA, TI)}</div><p class="p" style="color:rgba(255,255,255,.85);margin-top:.12in">Justo debajo, sus cuatro datos; los números se cuentan solos al aparecer.</p>'),
  nc='rgba(255,255,255,.7)'))

# 08 · SERVICIOS · azul, troquel, banda naranja, celular en dos columnas
L.append(lam(AZ,
  box(.55, .55, 5.6, f'''<p class="k" style="color:{CL}">Los servicios</p>
  <h2 class="t" style="color:#fff">{N_SERV} servicios, <em style="color:{NA}">con</em> su línea de corte</h2>
  <p class="p" style="color:rgba(255,255,255,.92)">Cada tarjeta lleva el rótulo en la banda naranja de sus piezas, su video o foto, y la frase de su propio post: «Nuestros stickers troquelados tienen cortes precisos…», «Un letrero bien pensado es una inversión para tu negocio».</p>
  <p class="p" style="color:rgba(255,255,255,.92)">Al aparecer, cada tarjeta queda rodeada por una línea punteada que se traza sola, como el corte de sus stickers troquelados. La de los plateados brilla en tornasol al mover el mouse o al recorrer la página en el celular, como en su reel.</p>
  <p class="p" style="color:rgba(255,255,255,.92)">En el celular van de a dos, para que todo el catálogo se recorra de un vistazo. El último recuadro recoge lo que ofrecen en Facebook: pendones, rollers y adhesivos.</p>''') +
  fr('d-serv3', 6.45, .55, 6.1, 1.2) + ph('m-serv', 6.0, 4.1, 1.55, -5, 5) + ph('m-serv2', 7.75, 4.4, 1.55, 3, 4) +
  box(9.6, 4.55, 3.0, f'<div class="pills" style="flex-direction:column;align-items:flex-start">{banda("STICKERS Y ETIQUETAS")}{banda("IMPRESIÓN UV")}{banda("CORTE Y GRABADO LÁSER")}{banda("GRÁFICA VEHICULAR")}{banda("MEDALLAS")}</div>'),
  nc='rgba(255,255,255,.7)'))

# 09 · PROCESO · luz UV, sus tres pasos literales
pasos = [('1', 'primero imprimimos con alta calidad'), ('2', 'luego el plotter de corte da forma a cada detalle'), ('3', 'finalmente hacemos el depilado para dejarlas listas para usar 💫')]
pah = ''.join(f'<div class="paso"><b>{a}</b><span>{b}</span></div>' for a, b in pasos)
L.append(lam(UV,
  photo(fot('IG-30_f3.png', 900), .55, .55, 3.6, 6.4, pos='50% 50%', z=2) + troq(.4, .4, 3.9, 6.7, 'rgba(255,255,255,.55)') +
  box(4.75, .65, 4.2, f'''<p class="k" style="color:{CL}">El proceso</p>
  <h2 class="t" style="color:#fff">Así nace <em style="color:{NA}">cada</em> etiqueta</h2>
  <div class="pasos">{pah}</div>
  <p class="k" style="color:rgba(255,255,255,.7)">{IG("30")} · con sus mismas palabras</p>
  <p class="p" style="color:rgba(255,255,255,.92)">Su reel ya contaba el proceso en tres pasos. En el sitio, un solo video recorre las tres máquinas y el paso que se ve en pantalla se enciende en la lista. En el celular, primero el título y los pasos; después, el video.</p>''') +
  fr('d-proc', 9.3, .9, 3.3, 2.5) + ph('m-proc', 10.35, 3.85, 1.55, -4, 5),
  nc='rgba(255,255,255,.7)'))

# 10 · TRABAJOS · papel + tornasol, pila de stickers, clientes en cápsulas
cli = ''.join(pill(c_, [AZ, BA, TI, UV][i % 4]) for i, c_ in enumerate(CLIENTES))
L.append(lam(PA, cls='claro', inner=f'<div class="tornabar" style="background:{TORNA}"></div>' +
  box(.55, .75, 5.8, f'''<p class="k" style="color:{BA}">Los trabajos</p>
  <h2 class="t" style="color:{TI}">Sus clientes, <em style="color:{AZ}">en</em> una pila de stickers</h2>
  <p class="p">Ustedes hacen stickers, así que sus trabajos se muestran como una pila de stickers: se despegan con el dedo o con un botón, y se levanta la esquina como en una lámina real. Son {N_TRAB} trabajos que ustedes publicaron, cada uno con su cliente:</p>
  <div class="pills" style="margin:.1in 0 .16in">{cli}</div>
  <p class="p">La barra de colores viene de sus stickers plateados con efecto tornasol.</p>''') +
  box(.55, 5.45, 5.6, Q('En Edel Impresiones transformamos tus ideas en stickers que llevan la identidad de tu emprendimiento a todas partes. 💛', IG('43')) + '<p class="p">La frase que acompaña la pila es la de ese mismo post.</p>', 'card', f'background:#fff;') +
  sticker(raw(R['van'], 900), 6.7, .85, 2.75, 2.75, -6, 3, 'Puro Lomo · Gráfica vehicular', '50% 60%') +
  sticker(raw(R['miel'], 700), 9.55, .7, 2.6, 2.6, 5, 2, 'Miel Chiloé · Etiquetas') +
  fr('d-trab-peel', 7.05, 4.35, 5.5, -1.5, 4)))

# 11 · EQUIPO · madera, Team Mate o Team Café
L.append(lam(MA,
  box(.55, .55, 5.7, f'''<p class="k" style="color:{TI}">El equipo</p>
  <h2 class="t" style="color:{TI}">Las personas <em style="color:#fff">detrás</em> de cada trabajo</h2>
  <p class="p">Arriba va su post del equipo: «Detrás de cada negocio, existe un equipo humano que día a día lo da todo…». Sus fotos giran al tocarlas y, por detrás, muestran frases de ese mismo post. Van sin nombres hasta que ustedes digan si quieren aparecer.</p>''') +
  box(.55, 3.4, 5.4, f'''{Q("Y tú, de que Team eres?", IG("35"))}
  <p class="p">Su reel preguntaba «Team Mate o Team Café». En el sitio, la pregunta tiene dos botones: al elegir, saltan mates o tazas por la pantalla.</p>''', 'card', f'background:{PA};') +
  box(.55, 6.25, 5.4, Q('Los mejores de Castro! Personal super amables y el servicio excelente.', 'Silvana · Google'), '', '') +
  fr('d-team', 6.45, .6, 6.1, 1.5) + fr('d-flipc', 6.85, 4.55, 5.4, -2, 3),
  nc='rgba(5,38,63,.5)', cls='claro'))

# 12 · RESEÑAS Y COTIZA · naranja, sello 4,6, WhatsApp
L.append(lam(NA,
  medal(.55, .55, 1.9, TI, '#fff', f'<b style="font-size:44pt;line-height:1">{NOTA_G}</b><br><small style="color:#ffd166">★★★★<span style="opacity:.35">★</span></small><br><small>Google</small>', rot=-8, z=5) +
  box(2.75, .6, 4.2, f'''<p class="k" style="color:{TI}">Lo que dicen sus clientes</p>
  <h2 class="t" style="color:{TI}">Una nota <em style="color:#fff">que</em> se estampa</h2>''') +
  box(.55, 2.85, 6.2, f'''<p class="p">{N_RES} reseñas en el sitio, al pie de la letra: {N_RES_G} de Google y {N_RES_F} de Facebook. Además de «excelente», hablan de responsabilidad, calidad y buen trato:</p>
  {Q("Muy responsables en la fecha de entrega.", "Chilwe Gourmet · Google")}
  {Q("…Super preocupados de hacer el trabajo que exactamente uno quiere. Atención personalizada…", "Fernando · Facebook")}
  <p class="p">Por eso su nota va como un sello que cae y se estampa, y cada reseña se despega como un sticker al pasar a la siguiente.</p>''') +
  fr('d-res', 7.15, .55, 5.4, 2) +
  box(7.15, 4.1, 5.4, f'''<p class="k" style="color:{CL}">Cotizar</p>
  <h3 class="t3" style="color:#fff">Un mensaje ya escrito</h3>
  <p class="p" style="color:rgba(255,255,255,.92)">Para cerrar, su frase: «No importa como expreses el tamaño del trabajo que necesitas, nosotros lo resolveremos y te entenderemos». El botón de WhatsApp abre la conversación con «Hola Edel, quiero cotizar un trabajo» ya escrito; también están su Instagram, su correo y su dirección en Castro.</p>''', 'card', f'background:{TI};'),
  nc='rgba(5,38,63,.55)'))

# 13 · DETALLES · papel, cinco celulares
phs = ''.join(ph(k, .65 + i * 2.45, .45 + (0, .3, 0, .3, 0)[i], 2.0, (-4, 3, -2, 4, -3)[i], crop=3.95) for i, k in enumerate(['m-carga', 'm-intro', 'm-serv2', 'm-menu', 'm-res']))
dots = ''.join(f'<div class="dot" style="left:{.45 + i * 2.45}in;top:{1.3 + (0, .3, 0, .3, 0)[i]}in;background:{c_}"></div>' for i, c_ in enumerate([TI, AZ, NA, UV, MA]))
det = [('Celular primero', 'Como su Instagram, se lee en el teléfono: botones grandes, el catálogo de a dos y un menú a pantalla completa con su azul y su letra.', AZ),
       ('Listo para compartir', 'Al mandar el enlace por WhatsApp aparece una imagen con su logo y su plotter cortando etiquetas, en vez de un enlace suelto.', BA),
       ('Cuidado con los datos', 'En su reel de diplomas se leían nombres de alumnos y un código QR: en el sitio van difuminados. Las publicaciones de 2022 y 2023 y el teléfono antiguo quedaron fuera.', UV),
       ('Sin tropiezos', 'La página no salta mientras carga, se lee bien incluso con sol y cada foto y video tiene su descripción para quien no puede verlos.', TI)]
deth = ''.join(box(.55 + i * 3.1, 5.55, 2.85, f'<div class="bar" style="background:{c_}"></div><h3 class="t4">{t_}</h3><p class="p">{p_}</p>') for i, (t_, p_, c_) in enumerate(det))
L.append(lam(PA, dots + phs + deth))

# 14 · CIERRE · foto a sangre del equipo y la tarjeta abajo, para que se vean sus caras
L.append(f'<article class="lam free" style="background:{TI}"><img class="bleed abs0" src="{raw(R["equipo4"], 2400)}" style="object-position:50% 22%" alt="">' +
  box(.5, 5.25, 12.0, f'''<div class="cierre3">
  <div><img src="{png_file("brand/png/isotipo.png", 300)}" class="mk" alt="">
  <p class="k" style="color:{BA}">Lo que sigue</p><h2 class="t" style="color:{TI};margin-bottom:.08in">Hacerlo <em style="color:{AZ}">suyo</em></h2>
  <p class="p">Este sitio se hizo solo con lo que ya estaba publicado. Con un par de conversaciones podría ir mucho más lejos:</p></div>
  <ul class="next2"><li>Fotos y videos propios del taller y de las máquinas, en alta resolución</li>
    <li>Horario de atención y nombres del equipo, contados por ustedes</li>
    <li>Dominio propio .cl y alojamiento a nombre de Edel Impresiones</li>
    <li>Cotizaciones que lleguen a su WhatsApp ordenadas por servicio, medida y fecha</li></ul>
  <div class="firma3"><p class="invite2">Cuando quieran, lo conversamos.</p>
  <p class="who2">Pablo Figueroa G.</p><p class="role2">Director de estudio</p>
  <p class="contact2"><a href="mailto:pablo@bergerac.cl">pablo@bergerac.cl</a> · <a href="tel:+56975892096">+56 9 7589 2096</a></p>
  <p class="link2"><a href="https://bergerac.cl">Bergerac.cl</a></p></div></div>''', 'card', f'background:{PA};padding:.3in .4in;') +
  f'<span class="no" style="color:rgba(255,255,255,.7)">{nx():02d}</span></article>')

# ======================= CSS =======================
CSS = f'''
@font-face{{font-family:"Anton";src:url({font("anton-latin-400-normal")}) format("woff2")}}
@font-face{{font-family:"Anton";src:url({font("anton-latin-ext-400-normal")}) format("woff2");unicode-range:U+0100-024F}}
@font-face{{font-family:"Oswald";font-weight:600;src:url({font("oswald-latin-600-normal")}) format("woff2")}}
@font-face{{font-family:"Montserrat";font-weight:400;src:url({font("montserrat-latin-400-normal")}) format("woff2")}}
@font-face{{font-family:"Montserrat";font-weight:500;src:url({font("montserrat-latin-500-normal")}) format("woff2")}}
@font-face{{font-family:"Montserrat";font-weight:700;src:url({font("montserrat-latin-700-normal")}) format("woff2")}}
@page{{size:13in 8.5in;margin:0}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{background:#8b8f8a}}
body{{font-family:"Montserrat",Arial,sans-serif;color:{TI};-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.lam{{width:13in;height:8.5in;overflow:hidden;margin:0 auto .3in;position:relative;page-break-after:always;break-after:page}}
@media print{{html,body{{background:none}}.lam{{margin:0}}}}
.bleed{{width:100%;height:100%;object-fit:cover;display:block}}
.abs0{{position:absolute;inset:0}}
.abs{{position:absolute;display:block}}
.spread .bleed{{position:absolute;inset:0}}
.spread-tab{{position:absolute;left:0;top:.45in;background:#fff;opacity:.75;padding:.2in .34in .2in .5in;border-radius:0 .18in .18in 0}}
.spread-logo{{width:2.3in;display:block}}
.no{{position:absolute;right:.4in;bottom:.28in;font-weight:700;font-size:7pt;letter-spacing:.2em;z-index:20}}
.tx{{position:absolute;z-index:4}}
.card{{border-radius:.22in;padding:.3in .34in;box-shadow:0 10pt 30pt rgba(0,0,0,.2)}}
.k{{font-family:"Oswald";font-weight:600;font-size:8.6pt;letter-spacing:.22em;text-transform:uppercase;margin-bottom:.1in}}
.t{{font-family:"Anton";font-weight:400;font-size:36pt;line-height:1.08;text-transform:uppercase;margin-bottom:.18in}}
.t em{{font-style:normal}}
.t3{{font-family:"Anton";font-weight:400;font-size:24pt;line-height:1.1;text-transform:uppercase;margin-bottom:.06in}}
.t4{{font-family:"Anton";font-weight:400;font-size:17pt;line-height:1.1;text-transform:uppercase;margin:.1in 0 .05in}}
.p{{font-size:9.8pt;line-height:1.5;margin-bottom:.08in}}
.p.sm{{font-size:8.4pt;color:{GR}}}
.q2{{margin:.04in 0 .1in}}
.q2 p{{font-style:italic;font-size:10.6pt;line-height:1.42;margin-bottom:3pt}}
.q2 cite{{font-family:"Oswald";font-style:normal;font-weight:600;font-size:7.4pt;letter-spacing:.16em;text-transform:uppercase;color:{GR}}}
.letter2 p{{font-size:13pt;line-height:1.5;margin-bottom:.12in}}
.seal{{position:absolute;z-index:6;filter:drop-shadow(0 8pt 18pt rgba(0,0,0,.25))}}
.sign2{{font-style:italic;color:{GR}}}
.pic{{position:absolute;overflow:hidden;box-shadow:0 12pt 34pt rgba(0,0,0,.22)}}
.pic img{{width:100%;height:100%;object-fit:cover;display:block}}
.troq{{position:absolute;border:2pt dashed;pointer-events:none}}
.fr{{position:absolute;border-radius:8pt;overflow:hidden;box-shadow:0 14pt 34pt rgba(0,0,0,.3);background:transparent;outline:1.8pt dashed rgba(255,255,255,.75);outline-offset:5pt}}
.claro .fr{{outline-color:rgba(5,38,63,.45)}}
.no-izq .no{{right:auto;left:7.5in}}
.cierre3{{display:grid;grid-template-columns:1.05fr 1.25fr .9fr;gap:.4in;align-items:start}}
.cierre3 .next2{{margin:.05in 0 0}}
.cierre3 .mk{{width:.42in;margin-bottom:.08in}}
.fr img{{width:100%;display:block}}
.ph{{position:absolute;border-radius:16pt;overflow:hidden;border:4pt solid #111;box-shadow:0 14pt 30pt rgba(0,0,0,.32);background:#111}}
.ph img{{width:100%;display:block;border-radius:12pt}}
.md{{position:absolute;border-radius:50%;display:flex;align-items:center;justify-content:center;text-align:center;font-family:"Anton";text-transform:uppercase;line-height:1.05;padding:.1in;box-shadow:0 8pt 20pt rgba(0,0,0,.22)}}
.md small{{font-size:.8em}}
.mdn{{font-size:30pt;font-weight:400}}
.pol{{position:absolute;width:1.85in;background:#fff;padding:.08in .08in .3in;border-radius:4pt;box-shadow:0 10pt 24pt rgba(0,0,0,.3)}}
.pol img{{width:100%;aspect-ratio:4/5;object-fit:cover;display:block;border-radius:2pt}}
.stk{{position:absolute;background:#fff;padding:.09in .09in .12in;border-radius:.2in;box-shadow:0 12pt 28pt rgba(5,38,63,.28)}}
.stk img{{width:100%;object-fit:cover;display:block;border-radius:.13in}}
.stk span{{display:block;font-weight:700;font-size:8pt;margin-top:.07in;color:{TI}}}
.bigs{{display:grid;grid-template-columns:1fr 1fr;gap:.12in .3in;margin:.06in 0 .2in}}
.bign b{{display:block;font-family:"Anton";font-weight:400;font-size:52pt;line-height:1.05;color:{PA}}}
.bign span{{display:block;font-size:8.8pt;line-height:1.35;color:#fff;margin-top:.02in}}
.stripes{{position:absolute;right:0;top:0;bottom:0;width:5.0in;display:flex}}
.stripe{{flex:1;position:relative}}
.stripe .sn{{position:absolute;left:50%;top:.55in;transform:translateX(-50%) rotate(180deg);writing-mode:vertical-rl;font-family:"Oswald";font-weight:600;font-size:8.6pt;letter-spacing:.2em;text-transform:uppercase;white-space:nowrap}}
.stripe .sh{{position:absolute;left:0;right:0;bottom:.55in;font-weight:700;font-size:7.6pt;letter-spacing:.06em;writing-mode:vertical-rl;transform:rotate(180deg);margin:0 auto;display:flex;align-items:center;justify-content:center}}
.spa{{font-family:"Anton";font-size:86pt;line-height:1.05;text-transform:uppercase;color:{TI}}}
.spb{{margin:.06in 0 0}}
.spb .bnd{{font-size:22pt;padding:.06in .18in .05in}}
.bnd{{display:inline-block;font-family:"Oswald";font-weight:600;font-size:9pt;letter-spacing:.18em;text-transform:uppercase;padding:5pt 10pt 4pt;line-height:1.2}}
.cap2{{font-family:"Oswald";font-weight:600;font-size:8pt;letter-spacing:.16em;text-transform:uppercase;color:{GR};margin-top:.2in}}
.cols3{{display:grid;grid-template-columns:repeat(3,1fr);gap:.28in}}
.cols3 h4{{font-family:"Anton";font-weight:400;font-size:17pt;text-transform:uppercase;margin-bottom:.06in}}
.cols3 p{{font-size:9.4pt;line-height:1.5}}
.pills{{display:flex;flex-wrap:wrap;gap:6pt}}
.pill{{display:inline-block;padding:5pt 11pt;border-radius:999px;font-weight:700;font-size:8.6pt}}
.paso{{display:flex;gap:.14in;align-items:flex-start;margin:.06in 0 .14in}}
.paso b{{flex:none;width:.5in;height:.5in;border-radius:50%;background:#fff;color:{UV};display:grid;place-items:center;font-family:"Anton";font-weight:400;font-size:20pt}}
.paso span{{font-size:13pt;line-height:1.35;color:#fff;padding-top:.06in}}
.tornabar{{position:absolute;left:0;right:0;top:0;height:.26in}}
.dot{{position:absolute;width:2.5in;height:2.5in;border-radius:50%;opacity:.92;z-index:1}}
.bar{{width:.6in;height:4pt;border-radius:2pt}}
.mk{{width:.55in;display:block;margin-bottom:.12in}}
.next2{{list-style:none;margin:.04in 0 .16in}}
.next2 li{{font-size:9.8pt;line-height:1.45;padding:5pt 0;border-bottom:.5pt solid #d6d0c6}}
.invite2{{font-size:13pt;font-style:italic;margin-bottom:.06in}}
.who2{{font-family:"Anton";font-size:12pt;letter-spacing:.14em;text-transform:uppercase}}
.role2{{font-size:9pt}}
.contact2{{font-size:8.4pt;color:{GR}}}
.card a,.regalo a{{color:inherit;text-decoration:none}}
.link2{{font-family:"Anton";font-size:17pt;letter-spacing:.16em;text-transform:uppercase;color:{BA};margin-top:.1in}}
/* carta de regalo */
.rg-col{{position:absolute;left:0;top:0;bottom:0;width:4.4in;padding:.7in .55in}}
.rg-logo{{width:2.9in;display:block}}
.rg-url{{position:absolute;left:.55in;bottom:.6in;font-family:"Oswald";font-weight:600;font-size:9pt;letter-spacing:.18em;text-transform:uppercase;color:{CL}}}
.regalo .letter2 p{{font-size:12.4pt;margin-bottom:.11in}}
.sign-r{{font-family:"Anton";font-size:13pt;letter-spacing:.14em;text-transform:uppercase;margin-top:.16in}}
.role-r{{font-size:9.6pt}}
.contact-r{{font-size:9pt;color:{GR};margin-top:.04in}}
'''

def doc(title, body):
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>'''
(D / 'edel-dossier-diseno.html').write_text(doc('Edel Impresiones · Decisiones de diseño del sitio web', ''.join(L)), encoding='utf-8')
# la carta de regalo de Bergerac se genera aparte (build_carta.py) y render.js la antepone en el PDF para anillar
print('láminas', n, '· MB', round(len(doc('', ''.join(L))) / 1e6, 1))
print('cifras', dict(posts=N_POSTS, reels=N_REELS, videos=N_VIDEOS, reels_usados=N_REELS_USADOS, fotos=N_FOTOS, posts_fotos=N_POSTS_FOTOS, res=(N_RES, N_RES_G, N_RES_F), clientes=CLIENTES, desde=DESDE, hasta=HASTA))
