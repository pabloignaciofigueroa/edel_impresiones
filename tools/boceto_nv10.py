#!/usr/bin/env python3
"""Genera nv10 en /nueva_v10/ (y con --final la raíz): segunda revisión de Pablo en computador (pila como baraja, «Y también» que llena su tarjeta, equipo en dos filas, reseñas en cinta sin fin).
Textos: content/copy.md (literal de la marca, fuente en cada línea). Medios: assets/video/media.json, assets/img/media.json.
Falla si un medio no tiene texto alternativo en inglés.
Uso: python3 tools/boceto_nv10.py [--final]  → escribe nueva_v10/index.html o index.html (css/nv10, js/nv10 son archivos fuente propios).
Congeladas: /nueva/ (nv1) = 7d4a298 · /nueva_v2/ (nv2) = 25f3c30 · /nueva_v3/ (nv3) = 9a09689 · /nueva_v4/ (nv4) = 0f490b1 · /nueva_v5/ (nv5) = f53b825 · /nueva_v6/ (nv6) = e30375d · /nueva_v7/ (nv7) = 9a5679f · nv8 = cfdfc83 · nv9 = la publicada el 29 oct antes de nv10."""
import json, html, pathlib, sys, re, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = 'https://edelimpresiones.pages.dev/'
FINAL = '--final' in sys.argv  # fase 20: versión definitiva en la raíz (rutas sin ../)
OUT = ROOT / ('index.html' if FINAL else 'nueva_v10/index.html')
V = json.load(open(ROOT / 'assets/video/media.json'))
F = json.load(open(ROOT / 'assets/img/media.json'))
L = json.load(open(ROOT / 'brand/_logo_paths.json'))
ROT = json.load(open(ROOT / 'brand/_iso_rotado.json'))  # vector limpio (agente vectorial), reordenado para partir en la punta (agente de diseño)
D_PATH_INV = 'M750 402A56 56 0 0 0 690 458A56 56 0 0 0 746 514A56 56 0 0 0 802 458V340'  # «d»: primero la panza, después el asta (no se lee «J»)
UP = '' if FINAL else '../'  # /nueva_v10/ → raíz
WA0 = 'https://wa.me/56982823772'
WA_ES = 'Hola Edel, quiero cotizar un trabajo'  # fase 19: mensaje prellenado (Pablo)
WA_EN = 'Hi Edel, I would like a quote for a job'
WA = WA0 + '?text=' + urllib.parse.quote(WA_ES)
WA_EN_URL = WA0 + '?text=' + urllib.parse.quote(WA_EN)
IG = 'https://www.instagram.com/edel.chiloe/'
FB = 'https://www.facebook.com/edel.chiloe/'
MAPS = 'https://www.google.com/maps/search/?api=1&query=Eduardo+Provasoli+619+Castro+Chile'
MAPS_EMBED = 'https://www.google.com/maps?q=Eduardo%20Provasoli%20619%2C%20Castro%2C%20Chile&output=embed'
e = html.escape
M8 = lambda k: k + '8' if k + '8' in V else k  # fase 19: cortes nuevos con id propio (las copias congeladas usan los anteriores)


def nb(s):
    """Emoji final pegado a la palabra anterior con espacio no separable (no cambia el texto literal)."""
    return re.sub(r' ([^\w\s]+)$', '\u00a0\\1', s)


def t(es, en, tag='span', cls='', attrs=''):
    """Texto de interfaz traducible: español en el DOM, inglés en data-en."""
    c = f' class="{cls}"' if cls else ''
    return f'<{tag}{c} data-en="{e(en)}"{attrs}>{es}</{tag}>'


def brand(es, gloss_en='', tag='span', cls='', lang='es'):
    """Frase literal de la marca: se muestra igual en ES y EN (lang="es"); en EN lleva una glosa pequeña."""
    c = f' class="{cls}"' if cls else ''
    g = f'<span class="glosa" lang="en" hidden>{e(gloss_en)}</span>' if gloss_en else ''
    return f'<{tag}{c} lang="{lang}">{es}{g}</{tag}>'


ALT = {  # texto alternativo ES / EN por medio (el build falla si falta el inglés)
    'hero': ('Máquinas de Edel imprimiendo y cortando: impresora UV, plotter de corte y depilado de stickers',
             'Edel machines printing and cutting: UV printer, cutting plotter and sticker weeding'),
    'plateados': ('Stickers plateados con efecto tornasol de Despensa Chiloé', 'Holographic silver stickers for Despensa Chiloé'),
    'transparentes': ('Sticker transparente impreso en blanco aplicado a un schop de Dulce Enlatta', 'Clear sticker printed in white applied to a Dulce Enlatta beer mug'),
    'uv': ('Impresora UV de Edel trabajando', 'Edel UV printer at work'),
    'diplomas': ('Diplomas de Dekra impresos en la impresora UV', 'Dekra diplomas printed on the UV printer'),
    'laser': ('Mostrador de madera cortado con láser, armado pieza por pieza', 'Laser-cut wooden display stand assembled piece by piece'),
    'bitacoras': ('Bitácoras de buceo de Chiloé Náutica: anillado y terminación', 'Chiloé Náutica dive logbooks: binding and finish'),
    'prendas': ('Estampado de prendas corporativas de SSC Rental', 'Heat-pressing SSC Rental corporate garments'),
    'medallas': ('Medallas de RevelArte: diseño, corte láser y entrega', 'RevelArte medals: design, laser cutting and delivery'),
    'letreros': ('Letrero de Pilates & Skincare cortado a mano', 'Pilates & Skincare sign being hand-trimmed'),
    'stickers': ('Corte y depilado de stickers troquelados', 'Cutting and weeding die-cut stickers'),
    'tarjetas': ('Tarjetas de presentación impresas por Edel', 'Business cards printed by Edel'),
    'diseno': ('Diseño en pantalla antes del corte', 'Design on screen before cutting'),
    'proceso': ('Así nace cada etiqueta: impresión, plotter de corte y depilado', 'How each label is made: printing, cutting plotter and weeding'),
    'team': ('Team Mate o Team Café en el escritorio de diseño', 'Team Mate or Team Coffee at the design desk'),
    'equipo': ('Integrante del equipo de Edel en el taller', 'A member of the Edel team in the workshop'),
    'equipo-2': ('Integrante del equipo de Edel en el taller', 'A member of the Edel team in the workshop'),
    'vehicular-1': ('Furgón de Puro Lomo rotulado por Edel', 'Puro Lomo van wrapped by Edel'),
    'vehicular-2': ('Parte trasera del furgón de Puro Lomo rotulado', 'Back of the wrapped Puro Lomo van'),
    'vehicular-3': ('Detalle del rotulado de Puro Lomo', 'Detail of the Puro Lomo wrap'),
    'vehicular-4': ('Lateral del furgón de Puro Lomo', 'Side of the Puro Lomo van'),
    'vehicular-5': ('Logo de Puro Lomo en el furgón', 'Puro Lomo logo on the van'),
    'etiquetas-miel': ('Etiquetas de Miel Chiloé', 'Miel Chiloé labels'),
    'etiquetas-naguara': ('Etiquetas de Naguara, galletas de membrillo', 'Naguara quince cookie labels'),
    'etiquetas-berries': ('Etiquetas de Berries & Hielo Chiloé', 'Berries & Hielo Chiloé labels'),
    'etiquetas-xs': ('Etiquetas de XS Joyas', 'XS Joyas labels'),
    'senaleticas-sigma': ('Señaléticas de Sigma en Trovicel', 'Sigma signs on PVC foam board'),
    'equipo-3': ('El equipo de Edel saludando en el taller', 'The Edel team waving in the workshop'),
    'equipo-4': ('El equipo de Edel junto a la impresora', 'The Edel team next to the printer'),
}
for k in list(V) + list(F):
    if (k.startswith('p') and k[1:2].isdigit()) or k.endswith('8'):
        continue
    if k not in ALT or not ALT[k][1]:
        sys.exit(f'ERROR: falta texto alternativo en inglés para {k}')


def video(vid, cls='', lazy=True, alt=None):
    a = ALT[alt or vid]; vid = M8(vid); m = V[vid]
    src = f'{UP}assets/video/{vid}'
    pre = 'none' if lazy else 'auto'
    ds = 'data-src' if lazy else 'src'
    pa = 'data-poster' if lazy else 'poster'  # fase 18: los pósters lejanos no se piden durante la carga
    return (f'<video class="vid {cls}" muted playsinline loop autoplay preload="{pre}" {pa}="{src}-poster.webp" '
            f'style="background-image:url({m["lqip"]})" aria-label="{e(a[0])}" data-aria-en="{e(a[1])}" {ds}="{src}.mp4"></video>')


def foto(fid, cls='', sizes='(min-width:900px) 33vw, 90vw', eager=False):
    m = F[fid]; a = ALT[fid]
    srcset = ', '.join(f'{UP}{p} {w}w' for w, p in m['srcset'])
    big = m['srcset'][-1][1]
    load = 'eager' if eager else 'lazy'
    return (f'<img class="{cls}" src="{UP}{big}" srcset="{srcset}" sizes="{sizes}" width="{m["ancho"]}" height="{m["alto"]}" '
            f'loading="{load}" decoding="async" style="background-image:url({m["lqip"]})" alt="{e(a[0])}" data-alt-en="{e(a[1])}">')


# ---------- logo en línea (carga + apertura) ----------
def logo_overlay():
    word = [D_PATH_INV if i == 1 else p for i, p in enumerate(L['WORD'])]
    w = ''.join(f'<path d="{p}" pathLength="1"/>' for p in word)
    return f'''<svg id="ov" aria-hidden="true" preserveAspectRatio="none">
<defs>
 <clipPath id="co" clipPathUnits="userSpaceOnUse"><circle cx="263.3" cy="533.8" r="210.9"/></clipPath>
 <mask id="mkA" maskUnits="userSpaceOnUse" x="-2000" y="-2000" width="5000" height="5000"><path d="{ROT['BLUE']}"/><path class="cierre" d="{ROT['BLUE']}"/></mask>
 <mask id="mkN" maskUnits="userSpaceOnUse" x="-2000" y="-2000" width="5000" height="5000"><path d="{ROT['ORANGE']}"/><path class="cierre" d="{ROT['ORANGE']}"/></mask>
 <mask id="mk" maskUnits="userSpaceOnUse" x="-1e5" y="-1e5" width="2e5" height="2e5">
  <rect x="-1e5" y="-1e5" width="2e5" height="2e5" fill="#fff"/>
  <g class="ap"><circle id="hueco" cx="358.7" cy="521.1" r="0" fill="#000" clip-path="url(#co)"/></g>
 </mask>
</defs>
<rect id="velo" x="-1e5" y="-1e5" width="2e5" height="2e5" fill="#05263f" mask="url(#mk)"/>
<g class="ap">
 <path id="isoA" d="{ROT['BLUE']}" fill="url(#gaC)" mask="url(#mkA)"/>
 <path id="isoN" d="{ROT['ORANGE']}" fill="url(#gn)" mask="url(#mkN)"/>
 <g id="pal" transform="translate(-521.5 473)">
  <g id="edel" fill="none" stroke="#fff" stroke-width="40" stroke-linecap="round" stroke-linejoin="round">{w}</g>
  <path id="sub1" d="{L['SUB1']}" fill="#fa621f"/><path id="sub2" d="{L['SUB2']}" fill="#3bb6e6"/>
 </g>
</g>
</svg>'''


def logo_nav():
    return (f'<svg class="logo-nav" viewBox="40 300 1010 460" aria-hidden="true"><path d="{ROT["BLUE"]}" fill="url(#ga)"/>'
            f'<path d="{ROT["ORANGE"]}" fill="url(#gn)"/><g fill="none" stroke="currentColor" stroke-width="40" stroke-linecap="round">'
            + ''.join(f'<path d="{p}"/>' for p in L['WORD']) + '</g></svg>')


# ---------- servicios ----------
SERV = [  # (id video/foto, rótulo ES, rótulo EN, frase literal, fuente)
    ('stickers', 'Stickers y etiquetas', 'Stickers & labels', 'Nuestros stickers troquelados tienen cortes precisos y acabados profesionales que destacan tu marca en cualquier superficie.', 'IG-21'),
    ('plateados', 'Plateados tornasol', 'Holographic silver stickers', 'Los tan cotizados stickers plateados con efecto tornasol, ya están disponibles en nuestra gráfica ✨', 'IG-29'),
    ('transparentes', 'Transparentes', 'Clear stickers', '¿Sabías que podemos imprimir tus stickers transparente en blanco? 😏✨', 'IG-46'),
    ('uv', 'Impresión UV', 'UV printing', 'Impresión UV en acción', 'IG-16'),
    ('tarjetas', 'Tarjetas de presentación', 'Business cards', 'Tu carta de presentación habla por ti 🔥 Creamos tarjetas con acabados precisos y profesionales para que dejes una impresión inolvidable.', 'IG-23'),
    ('laser', 'Corte y grabado láser', 'Laser cutting & engraving', 'Podemos hacer realidad tu propuesta con nuestro servicio de corte y grabado láser; trabajamos en acrílico y madera 🪵', 'IG-17'),
    ('vehicular-1', 'Gráfica vehicular', 'Vehicle graphics', 'Tu vehículo también puede convertirse en una publicidad que trabaja por ti las 24 horas del día. 💪', 'IG-39'),
    ('letreros', 'Letreros y señaléticas', 'Signs & wayfinding', 'Un letrero bien pensado es una inversión para tu negocio.', 'IG-34'),
    ('bitacoras', 'Bitácoras', 'Logbooks', 'Porque no solo imprimimos… creamos piezas que cuentan historias 📖', 'IG-25'),
    ('diplomas', 'Diplomas', 'Diplomas', 'Háblanos al DM y cotiza la impresión de tus diplomas 📜', 'IG-47'),
    ('prendas', 'Prendas corporativas', 'Corporate apparel', 'Si necesitas estampar tus prendas corporativas, no te preocupes 🙂‍↔️✨ ¡Nosotros nos encargamos!', 'IG-42'),
    ('medallas', 'Medallas', 'Medals', 'Si tienes un evento y quieres entregar medallas personalizadas, nosotros podemos realizarlas 🙂‍↔️ desde el diseño hasta la entrega final 💪🏼🥇', 'IG-44'),
    ('diseno', 'Diseño', 'Design', 'Todo gran proyecto comienza con una idea… y nosotros la llevamos a diseño 🙌', 'IG-19'),
]


def serv_cols():
    # Escritorio: tres columnas independientes con desfase (el primero, grande, a la izquierda).
    # Celular/tablet: las columnas son display:contents y cada tarjeta lleva su orden original.
    cols = [[0, 5, 7, 12], [1, 3, 6, 9, 11], [2, 4, 8, 10]]
    out = []
    for k, idxs in enumerate(cols):
        out.append(f'<div class="col col-{k + 1}">' + ''.join(serv_card(*SERV[i], order=i) for i in idxs) + '</div>')
    return ''.join(out)


def serv_card(sid, es, en, frase, src, order=0):
    media = video(sid) if sid in V else foto(sid, 'vid', '(min-width:900px) 30vw, 90vw')
    extra = ' serv-torna' if sid == 'plateados' else ''
    return (f'<article class="serv{extra}" style="order:{order}" data-src-ig="{src}"><span class="troquel" aria-hidden="true"></span><div class="serv-m">{media}</div>'
            f'<div class="serv-t">{t(es, en, "h3", "banda")}<p lang="es">{nb(frase)}</p></div></article>')


TRAB = [  # (cliente, trabajo ES, EN, medio)
    ('Puro Lomo', 'Gráfica vehicular', 'Vehicle graphics', 'vehicular-2'),
    ('Miel Chiloé', 'Etiquetas', 'Labels', 'etiquetas-miel'),
    ('Naguara', 'Etiquetas', 'Labels', 'etiquetas-naguara'),
    ('Berries & Hielo Chiloé', 'Etiquetas', 'Labels', 'etiquetas-berries'),
    ('XS Joyas', 'Etiquetas', 'Labels', 'etiquetas-xs'),
    ('Sigma', 'Señaléticas', 'Signs', 'senaleticas-sigma'),
    ('Despensa Chiloé', 'Stickers plateados', 'Silver stickers', 'plateados'),
    ('Dulce Enlatta', 'Stickers transparentes', 'Clear stickers', 'transparentes'),
    ('Chiloé Náutica', 'Bitácoras', 'Logbooks', 'bitacoras'),
    ('SSC Rental', 'Prendas', 'Apparel', 'prendas'),
    ('Dekra', 'Diplomas', 'Diplomas', 'diplomas'),
    ('RevelArte', 'Medallas', 'Medals', 'medallas'),
    ('Pilates & Skincare', 'Letrero', 'Sign', 'letreros'),
]


def trab_card(cli, es, en, mid):
    media = foto(mid, 'vid', '(min-width:900px) 25vw, 80vw') if mid in F else (video('trab-' + mid, alt=mid) if f'trab-{mid}8' in V else video(mid))
    return f'<li class="sticker"><div class="st-m">{media}</div><p><b>{e(cli)}</b> · {t(es, en)}</p></li>'


RESENAS = [
    ('Los mejores de Castro! Personal super amables y el servicio excelente.', 'Silvana', 'Google'),
    ('5 ESTRELLAS!! Excelente servicio. Super preocupados de hacer el trabajo que exactamente uno quiere. Atención personalizada. 100% RECOMENDABLE!', 'Fernando', 'Facebook'),
    ('Excelente atención. Se realizó una impresión de diploma y quedó en excelente calidad.', 'Andrés', 'Google'),
    ('Fue una experiencia grata, se destaca la responsabilidad y buen trato', 'Cristian', 'Google'),
    ('Muy responsables en la fecha de entrega.', 'Chilwe Gourmet', 'Google'),
    ('excelente , me encantaron como salieron mis fotos !!! totalmente recomendable , a estar siempre atentos a sus promos .', 'Marta', 'Facebook'),
    ('excelente calidad precio!', 'Alan', 'Google'),
    ('Buen servicio, 10/10', 'Luis', 'Google'),
]


def resena(txt, quien, fuente):
    return (f'<figure class="resena"><blockquote lang="es">“{e(txt).rstrip().replace(" .", "\u00a0.")}”</blockquote>'
            f'<figcaption>{e(quien)}, {t("Chile", "Chile")} · {t("vía", "via")} {fuente}</figcaption></figure>')


def h2lines(*lines, cls='h2'):
    return f'<h2 class="{cls}" lang="es">' + ''.join(f'<span class="ln"><span>{l}</span></span>' for l in lines) + '</h2>'


P = V[M8('proceso')].get('pasos') or V['proceso']['pasos']
import os as _os
def _b(rel): return _os.path.getsize(ROOT / rel)
FUENTES = ['anton-latin-400-normal', 'montserrat-latin-400-normal', 'montserrat-latin-500-normal', 'montserrat-latin-700-normal', 'oswald-latin-600-normal']
HERO = M8('hero')
HERO_M = f'{HERO}-540b' if (ROOT / f'assets/video/{HERO}-540b.mp4').exists() else 'hero-540b'
# fase 19 (Pablo): el % cuenta solo lo de la portada (fuentes, póster y video de portada); Servicios y pósters bajan al abrir
def _lista(hero):
    g1 = [f'assets/fonts/{f}.woff2' for f in FUENTES] + [f'assets/video/{HERO}-poster.webp', f'assets/video/{hero}.mp4']
    return [[[UP + x, _b(x)] for x in g1]]
PRECARGA = {'movil': _lista(HERO_M), 'grande': _lista(HERO)}
SCHEMA = {
    "@context": "https://schema.org", "@type": "LocalBusiness", "name": "Edel Impresiones",
    "alternateName": "Imprenta y Gráfica Edel", "url": SITE, "image": SITE + "assets/og-edel.jpg", "logo": SITE + "brand/png/isotipo.png",
    "telephone": "+56982823772", "email": "edelimpresiones@hotmail.com",
    "address": {"@type": "PostalAddress", "streetAddress": "Eduardo Provasoli 619", "addressLocality": "Castro", "addressRegion": "Los Lagos", "addressCountry": "CL"},
    "sameAs": [IG, FB], "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.6", "reviewCount": "10"},
}

DESC_ES = 'Edel Impresiones, imprenta y gráfica en Castro, Chiloé: stickers y etiquetas, impresión UV, corte y grabado láser, gráfica vehicular, letreros y más. Cotiza por WhatsApp.'
DESC_EN = 'Edel Impresiones, print and graphics shop in Castro, Chiloé: stickers and labels, UV printing, laser cutting and engraving, vehicle graphics, signs and more. Get a quote on WhatsApp.'

page = f'''<!doctype html>
<html lang="es" data-lang="es">
<head>
<meta charset="utf-8">
<style>html{{background:#05263f}}#ov{{visibility:hidden}}</style>
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Edel Impresiones · Imprenta y gráfica en Castro, Chiloé</title>
<meta name="description" content="{DESC_ES}" data-meta-en="{DESC_EN}">
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#05263f">
<link rel="canonical" href="{SITE}">
<meta property="og:type" content="website"><meta property="og:locale" content="es_CL">
<meta property="og:title" content="Edel Impresiones · Tu marca empieza por una buena impresión">
<meta property="og:description" content="{DESC_ES}">
<meta property="og:url" content="{SITE}"><meta property="og:image" content="{SITE}assets/og-edel.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{SITE}assets/og-edel.jpg">
<link rel="icon" href="{UP}brand/favicon.svg" type="image/svg+xml"><link rel="icon" href="{UP}brand/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="{UP}brand/png/favicon-180.png">
<link rel="preload" href="{UP}assets/fonts/anton-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{UP}assets/fonts/montserrat-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{UP}css/fonts.css"><link rel="stylesheet" href="{UP}css/tokens.css"><link rel="stylesheet" href="{UP}css/nv10/site.css">
<script>document.documentElement.classList.add('js');try{{if(localStorage.getItem('edel-lang')==='en')document.documentElement.dataset.lang='en'}}catch(e){{}}</script>
<script type="application/ld+json">{json.dumps(SCHEMA, ensure_ascii=False)}</script>
<script id="precarga" type="application/json">{json.dumps(PRECARGA)}</script>
</head>
<body class="cargando">
<svg class="defs" width="0" height="0" aria-hidden="true" focusable="false"><defs><linearGradient id="ga" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#099ece"/><stop offset=".45" stop-color="#0182b9"/><stop offset="1" stop-color="#035590"/></linearGradient><linearGradient id="gn" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fa571c"/><stop offset="1" stop-color="#f97732"/></linearGradient><linearGradient id="gaC" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1aa8d8"/><stop offset=".45" stop-color="#0b90c6"/><stop offset="1" stop-color="#0a6cb0"/></linearGradient></defs></svg>
<a class="saltar" href="#contenido">{t("Saltar al contenido", "Skip to content")}</a>
<div id="carga" role="status" aria-live="polite">
 {logo_overlay()}
 <p class="pct"><span id="pct">0</span> %<span class="sr" data-en="Loading Edel Impresiones">Cargando Edel Impresiones</span></p>
</div>

<header class="nav" id="nav">
 <a class="nav-logo" href="#portada" aria-label="Edel Impresiones">{logo_nav()}</a>
 <nav class="nav-links" aria-label="Secciones" data-aria-en="Sections">
  <a href="#servicios">{t("Servicios", "Services")}</a><a href="#proceso">{t("Proceso", "Process")}</a>
  <a href="#trabajos">{t("Trabajos", "Work")}</a><a href="#equipo">{t("Equipo", "Team")}</a><a href="#resenas">{t("Reseñas", "Reviews")}</a>
 </nav>
 <div class="nav-acc">
  <a class="btn btn-cot mag" href="{WA}" data-href-en="{WA_EN_URL}" target="_blank" rel="noopener">{t("Cotiza", "Get a quote")}</a>
  <button class="menu-b" type="button" aria-expanded="false" aria-controls="menu"><span class="menu-ico" aria-hidden="true"></span>{t("Menú", "Menu", "span", "sr")}</button>
 </div>
</header>
<div class="menu" id="menu" role="dialog" aria-modal="true" aria-label="Menú" data-aria-en="Menu" hidden>
 <button class="menu-x" type="button">{t("Cerrar", "Close")} <span aria-hidden="true">✕</span></button>
 <nav aria-label="Secciones" data-aria-en="Sections">
  <a href="#servicios">{t("Servicios", "Services")}</a><a href="#proceso">{t("Proceso", "Process")}</a><a href="#trabajos">{t("Trabajos", "Work")}</a>
  <a href="#equipo">{t("Equipo", "Team")}</a><a href="#resenas">{t("Reseñas", "Reviews")}</a><a href="#cotiza">{t("Cotiza", "Get a quote")}</a>
 </nav>
 <a class="btn btn-wa" href="{WA}" data-href-en="{WA_EN_URL}" target="_blank" rel="noopener">{t("Cotiza por WhatsApp", "Get a quote on WhatsApp")}<small>+56 9 8282 3772</small></a>
 <p class="menu-dir" lang="es">Eduardo Provasoli 619, Castro · @edel.chiloe</p>
 <p class="menu-lang"><button class="lang" type="button" aria-label="Cambiar idioma a inglés" data-aria-en="Switch language to Spanish"><span class="es">ES</span><span class="en">EN</span></button></p>
</div>

<main id="contenido">
<section class="s-portada" id="portada">
 <div class="hero-v">{video("hero", "hero-video", lazy=False).replace(f'src="{UP}assets/video/{HERO}.mp4"', f'data-src-movil="{UP}assets/video/{HERO_M}.mp4" data-src-grande="{UP}assets/video/{HERO}.mp4"').replace(' autoplay preload="auto"', ' preload="none"')}</div>
 <div class="hero-t">
  <h1 class="h1" lang="es"><span class="ln"><span>Tu marca</span></span><span class="ln"><span>empieza por una</span></span><span class="ln"><span>buena <em>impresión</em></span></span></h1>
  <p class="glosa-h" lang="en" hidden>Your brand starts with a good impression</p>
  <p class="banda b-nar" lang="es">Pioneros en Chiloé · Más de 20 años de experiencia nos respaldan</p>
  <div class="hero-b"><a class="btn btn-wa mag" href="{WA}" data-href-en="{WA_EN_URL}" target="_blank" rel="noopener">{t("Cotiza por WhatsApp", "Get a quote on WhatsApp")}</a>
  <a class="btn btn-l mag" href="#trabajos">{t("Ver trabajos", "See our work")}</a></div>
 </div>
</section>

<section class="s-intro" id="intro">
 <div class="w">
  {h2lines("Hacemos realidad", "tus proyectos")}
  <p class="glosa-h" lang="en" hidden>We make your projects happen</p>
  <p class="lead" lang="es">Desde tarjetas de presentación hasta piezas gráficas completas, cuidamos cada detalle para que tu marca destaque.</p>
  <ul class="cifras">
   <li><b data-cuenta="20">+20</b>{t("años de experiencia", "years of experience")}</li>
   <li><b class="cifra-iso" aria-hidden="true"><img src="{UP}brand/isotipo.svg" alt="" width="424" height="446"></b>{t("Pioneros en Chiloé", "Pioneers in Chiloé")}</li>
   <li><b data-cuenta="4.6" data-en="4.6">4,6</b>{t("en Google", "on Google")}</li>
   <li><b data-cuenta="100" data-en="100%">100 %</b>{t("recomendado en Facebook", "recommended on Facebook")}</li>
  </ul>
 </div>
</section>

<section class="s-serv" id="servicios">
 <div class="w">
  {h2lines("Las ideas son infinitas…", "y nosotros tenemos cómo", "hacerlas realidad")}
  <p class="glosa-h" lang="en" hidden>Ideas are endless… and we have what it takes to make them real</p>
  <p class="lead" lang="es">{nb("En nuestra gráfica encontrarás un sinfín de posibilidades para llevar adelante tus proyectos. 🖨️💫")}</p>
  <div class="serv-grid">{serv_cols()}<p class="serv-mas" style="order:99"><span class="mas-t">{t("Y también", "And also")}</span><span class="mas-s" lang="es"><span class="banda b-nar">Pendones,</span> <span class="banda b-nar">Rollers,</span> <span class="banda b-nar">Adhesivos</span></span></p></div>
 </div>
</section>

<section class="s-proc" id="proceso">
 <div class="proc-sticky w">
  <div class="proc-v">{video("proceso", "proc-video")}</div>
  <div class="proc-t">
   {h2lines("Así nace", "cada etiqueta")}
   <p class="glosa-h" lang="en" hidden>How each label is made</p>
   <ol class="pasos" data-p2="{P['2']}" data-p3="{P['3']}">
    <li class="on"><b>1</b><span lang="es">primero imprimimos con alta calidad</span></li>
    <li><b>2</b><span lang="es">luego el plotter de corte da forma a cada detalle</span></li>
    <li><b>3</b><span lang="es">{nb("finalmente hacemos el depilado para dejarlas listas para usar 💫")}</span></li>
   </ol>
   <p class="nota" lang="es">{nb("Detrás de cada proyecto hay mucho trabajo hecho con cariño ✨")}</p>
  </div>
 </div>
</section>

<section class="s-trab" id="trabajos">
 <div class="w">
  {h2lines("El detalle hace", "la diferencia")}
  <p class="glosa-h" lang="en" hidden>Detail makes the difference</p>
  <div class="tornasol" aria-hidden="true"></div>
  <p class="lead" lang="es">Estos son algunos de los trabajos que hemos realizado para emprendimientos locales, cuidando cada detalle para que sus productos, empaques y entregas tengan ese toque especial que los hace únicos. 🫶🏻</p>
  <div class="trab-w">
   <ul class="pila" aria-label="Trabajos" data-aria-en="Work">{"".join(trab_card(*x) for x in TRAB)}</ul>
   <div class="pila-ui" hidden>
    <p class="pila-tip">{t("Despega el sticker para ver el siguiente", "Peel the sticker to see the next one")}</p>
    <button type="button" class="btn btn-l pila-next">{t("Siguiente trabajo", "Next job")} →</button>
    <p class="pila-n" aria-live="polite"><span class="pila-i">1</span> / {len(TRAB)}</p>
   </div>
  </div>
 </div>
</section>

<section class="s-equipo" id="equipo">
 <div class="w eq">
  <p class="banda b-tinta eq-band">{t("Equipo humano", "Our people")}</p>
  <div class="eq-t">
   {h2lines(nb("Detrás de cada negocio, existe un equipo humano que día a día lo da todo para brindarles el mejor servicio ✨"), cls="h2 h2-m")}
   <p class="glosa-h" lang="en" hidden>Behind every business there's a human team giving it their all every day to give you the best service</p>
   <p class="lead eq-tip">{t("Toca las fotos para darlas vuelta", "Tap the photos to flip them", cls="tip-toca")}{t("Haz clic en las fotos para darlas vuelta", "Click the photos to flip them", cls="tip-clic")}</p>
  </div>
  <div class="eq-fotos">
   <button type="button" class="flip" aria-pressed="false"><span class="flip-in"><span class="flip-a">{foto("equipo-3", "", "(min-width:900px) 30vw, 50vw")}</span><span class="flip-b" lang="es">{nb("En Edel Impresiones nos preocupamos de siempre ser ese equipo que le trae soluciones y cumple los proyectos que necesitan 🧑‍💻👩‍💻")}</span></span><span class="sr">{t("Girar tarjeta", "Flip card")}</span></button>
   <button type="button" class="flip" aria-pressed="false"><span class="flip-in"><span class="flip-a">{foto("equipo-4", "", "(min-width:900px) 30vw, 50vw")}</span><span class="flip-b" lang="es">{nb("Gracias por siempre confiar en nosotros, seguiremos dando lo mejor ✨")}</span></span><span class="sr">{t("Girar tarjeta", "Flip card")}</span></button>
  </div>
  <div class="eq-vid">{video("equipo")}</div>
  <div class="team">
   <div class="team-v">{video("team")}</div>
   <div class="team-t">
    <p lang="es">{nb("No importa si eres Team Mate o Team Café, lo importante es que no te falte a la hora de trabajar 🙂‍↔️✨")}</p>
    <p class="team-q" lang="es">Y tú, de que Team eres?</p>
    <div class="team-b" role="group" aria-label="Elige tu equipo" data-aria-en="Pick your team">
     <button type="button" aria-pressed="false" data-team="mate">Team Mate</button><button type="button" aria-pressed="false" data-team="cafe">Team Café</button>
    </div>
    <div class="burst" aria-hidden="true"></div>
   </div>
  </div>
 </div>
</section>

<section class="s-res" id="resenas" aria-labelledby="res-h">
 <div class="w">
  <h2 class="sr" id="res-h">{t("Reseñas", "Reviews")}</h2>
  <div class="res-top">
   <p class="sello" aria-hidden="true"><b data-en="4.6">4,6</b><span>★★★★<i>★</i></span><small>Google</small></p>
   <p class="banda b-tinta">{t("4,6 en Google · 100 % recomendado en Facebook", "4.6 on Google · 100% recommended on Facebook")}</p>
  </div>
  <div class="res-pista" tabindex="0" role="region" aria-label="Reseñas" data-aria-en="Reviews">{"".join(resena(*r) for r in RESENAS)}</div>
  <div class="res-b"><button type="button" class="prev" aria-label="Reseña anterior" data-aria-en="Previous review">←</button><button type="button" class="next" aria-label="Reseña siguiente" data-aria-en="Next review">→</button></div>
 </div>
</section>

<section class="s-cot" id="cotiza">
 <div class="w cot">
  <div class="cot-t">
   {h2lines("No importa como expreses el tamaño del trabajo que necesitas, nosotros lo resolveremos y te entenderemos", cls="h2 h2-m")}
   <p class="glosa-h" lang="en" hidden>However you describe the size of the job you need, we'll understand you and get it done</p>
   <div class="cot-b">
    <a class="btn btn-wa mag" href="{WA}" data-href-en="{WA_EN_URL}" target="_blank" rel="noopener">{t("Escríbenos por WhatsApp", "Message us on WhatsApp")}<small>+56 9 8282 3772</small></a>
    <a class="btn btn-l" href="https://ig.me/m/edel.chiloe" target="_blank" rel="noopener">{t("Mensaje en Instagram", "Message us on Instagram")}</a>
    <a class="btn btn-l" href="mailto:edelimpresiones@hotmail.com">edelimpresiones@hotmail.com</a>
   </div>
   <address><a href="{MAPS}" target="_blank" rel="noopener">Eduardo Provasoli 619, Castro</a></address>
  </div>
  <div class="mapa"><iframe title="Mapa: Eduardo Provasoli 619, Castro" data-title-en="Map: Eduardo Provasoli 619, Castro" src="{MAPS_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
 </div>
</section>
</main>

<footer class="pie">
 <div class="w pie-w">
  <div class="pie-a"><img src="{UP}brand/logo-horizontal-claro.svg" alt="Edel Impresiones" width="1010" height="460" loading="lazy">
  <p lang="es">Imprenta y gráfica de Altos estándares · Pioneros en Chiloé · Más de 20 años de experiencia nos respaldan</p></div>
  <div class="pie-b"><p><a href="{IG}" target="_blank" rel="noopener">@edel.chiloe</a> · <a href="{FB}" target="_blank" rel="noopener">Facebook</a></p>
  <p class="pie-lang"><button class="lang" type="button" aria-label="Cambiar idioma a inglés" data-aria-en="Switch language to Spanish"><span class="es">ES</span><span class="en">EN</span></button></p></div>
 </div>
</footer>
<script src="{UP}vendor/gsap.min.js" defer></script><script src="{UP}vendor/ScrollTrigger.min.js" defer></script><script src="{UP}vendor/lenis.min.js" defer></script>
<script src="{UP}js/nv10/site.js" defer></script>
</body>
</html>
'''
EMOJI = re.compile('[\U0001F000-\U0001FAFF\u2194\u2300-\u23FF\u2600-\u2604\u2606-\u27BF\u2B00-\u2BFF\uFE0F\u200D]')
head, body = page.split('<body', 1)
body = re.sub(r'(?<=[^\s>]) {2,}(?=[^\s<])', ' ', EMOJI.sub('', body))
body = re.sub(r'[ \u00a0]+(</(?:p|span|h2|li|blockquote)>)', r'\1', body)
page = head + '<body' + body
assert not EMOJI.search(body), EMOJI.findall(body)[:5]
OUT.parent.mkdir(exist_ok=True)
OUT.write_text(page)
print(OUT.relative_to(ROOT), len(page) // 1024, 'KB')
