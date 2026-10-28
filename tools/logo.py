"""Genera el logo de Edel Impresiones en SVG a partir de medidas tomadas del original (IG-01, 1080 px).
Isotipo: dos medialunas = círculo menos círculo (ajuste RANSAC, error medio < 1 px).
Logotipo «edel»: trazos monolínea de 40 px con remates redondos (stroke, pathLength=1).
Bajada «GRÁFICA E / IMPRENTA»: Montserrat 700 pasada a trazos con fontTools, tracking hasta el ancho original.
Uso: python3 tools/logo.py  → escribe brand/*.svg"""
import math, os
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.boundsPen import BoundsPen

AZUL_GRAD=[('0','#099ece'),('0.45','#0182b9'),('1','#035590')]
NAR_GRAD=[('0','#fa571c'),('1','#f97732')]
GRIS='#6d6e70'
# Círculos medidos (coordenadas del original 1080×1080)
BLUE_OUT=(263.3,533.8,210.9); BLUE_IN=(358.7,521.1,168.5)
OR_OUT=(345.1,483.8,108.9); OR_IN=(193.7,451.0,135.5)

def inter(c1,c2):
    (x0,y0,r0),(x1,y1,r1)=c1,c2; d=math.hypot(x1-x0,y1-y0)
    a=(r0*r0-r1*r1+d*d)/(2*d); h=math.sqrt(r0*r0-a*a)
    xm=x0+a*(x1-x0)/d; ym=y0+a*(y1-y0)/d
    return (xm+h*(y1-y0)/d, ym-h*(x1-x0)/d),(xm-h*(y1-y0)/d, ym+h*(x1-x0)/d)

def crescent(out,cut):
    """Área de 'out' fuera de 'cut'. Recorre el arco externo de out (el lado lejano a cut) y vuelve por el arco de cut."""
    p,q=inter(out,cut)
    f=lambda v:f'{v:.2f}'
    # arco de out entre p y q por el lado opuesto al centro de cut (large-arc si cut está más cerca)
    ro,rc=out[2],cut[2]
    # punto medio del arco externo: dirección opuesta a cut
    dx,dy=out[0]-cut[0],out[1]-cut[1]; n=math.hypot(dx,dy)
    # decidir large-arc: el arco externo es "grande" si el centro de out queda del lado externo de la cuerda
    mx,my=(p[0]+q[0])/2,(p[1]+q[1])/2
    side=(out[0]-mx)*dx+(out[1]-my)*dy
    large_out=1 if side>0 else 0
    side_c=(cut[0]-mx)*dx+(cut[1]-my)*dy
    large_cut=1 if side_c>0 else 0
    # sentido: p→q sobre out (sweep 0) y q→p sobre cut (sweep 1) → probar y validar por render
    return (f'M{f(p[0])} {f(p[1])}A{ro:.2f} {ro:.2f} 0 {large_out} 0 {f(q[0])} {f(q[1])}'
            f'A{rc:.2f} {rc:.2f} 0 {large_cut} 1 {f(p[0])} {f(p[1])}Z')

import json as _j
# Trazado final: potrace sobre las manchas del original a 4x (brand/_iso_trazado.json). Las medialunas geométricas
# (círculo menos círculo) daban IoU 0,93/0,90 y no reproducían las puntas largas; el trazado sí.
_T=_j.load(open('brand/_iso_trazado.json'))
BLUE=_T['blue']; ORANGE=_T['orange']

# «edel»: centro de lóbulo y=458, radio 56, trazo 40
def e_path(dx):
    # ajustado por búsqueda contra el original (IoU 0,956): diagonal a -45°, largo 60, cola hasta x=618
    cx=591+dx; a=math.radians(-45); ex,ey=cx+56*math.cos(a),458+56*math.sin(a); dd=60/math.sqrt(2)
    return (f'M{618+dx} 514H{cx}A56 56 0 0 1 {cx-56} 458A56 56 0 0 1 {cx} 402'
            f'A56 56 0 0 1 {ex:.2f} {ey:.2f}L{ex-dd:.2f} {ey+dd:.2f}')
D_PATH='M802 340V458A56 56 0 0 1 746 514A56 56 0 0 1 690 458A56 56 0 0 1 750 402'
L_PATH='M1013 340V514'
WORD=[e_path(0),D_PATH,e_path(325),L_PATH]

def text_path(txt,x0,x1,cap_top,cap_h,font='assets/fonts/montserrat-latin-700-normal.woff2'):
    f=TTFont(font); gs=f.getGlyphSet(); cmap=f.getBestCmap(); upm=f['head'].unitsPerEm
    capH=f['OS/2'].sCapHeight or 700; s=cap_h/capH
    glyphs=[cmap[ord(c)] for c in txt]; adv=[gs[g].width for g in glyphs]
    # ancho de tinta sin tracking
    def ink(gn):
        bp=BoundsPen(gs); gs[gn].draw(bp); return bp.bounds
    first,last=ink(glyphs[0]),ink(glyphs[-1])
    base_w=sum(adv[:-1])*s - first[0]*s + last[2]*s
    track=((x1-x0)-base_w)/(len(txt)-1)
    out=[]; x=x0-first[0]*s; base=cap_top+cap_h
    for g,a,c in zip(glyphs,adv,txt):
        if c!=' ':
            sp=SVGPathPen(gs); tp=TransformPen(sp,(s,0,0,-s,x,base)); gs[g].draw(tp); out.append(sp.getCommands())
        x+=a*s+track
    return ' '.join(out)

SUB1=text_path('GRÁFICA E',516,1034,581,57)
SUB2=text_path('IMPRENTA',520,1033,679,57)

def grad_defs(idp):
    return (f'<defs><linearGradient id="{idp}a" x1="0" y1="0" x2="0" y2="1">'+''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o,c in AZUL_GRAD)+'</linearGradient>'
            f'<linearGradient id="{idp}n" x1="1" y1="0" x2="0" y2="1">'+''.join(f'<stop offset="{o}" stop-color="{c}"/>' for o,c in NAR_GRAD)+'</linearGradient></defs>')

def iso(idp='e',mono=None):
    fa=mono or f'url(#{idp}a)'; fn=mono or f'url(#{idp}n)'
    return f'<path class="iso-azul" d="{BLUE}" fill="{fa}" pathLength="1"/><path class="iso-naranja" d="{ORANGE}" fill="{fn}" pathLength="1"/>'
def word(col=GRIS):
    return f'<g class="edel" fill="none" stroke="{col}" stroke-width="40" stroke-linecap="round" stroke-linejoin="round">'+''.join(f'<path d="{p}" pathLength="1"/>' for p in WORD)+'</g>'
def sub(c1='#fa621f',c2='#0358a5'):
    return f'<path class="sub1" d="{SUB1}" fill="{c1}"/><path class="sub2" d="{SUB2}" fill="{c2}"/>'

def svg(vb,body,title='Edel Impresiones'):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-label="{title}"><title>{title}</title>{body}</svg>\n'

os.makedirs('brand',exist_ok=True)
W={
 'isotipo.svg':svg('40 312 424 446',grad_defs('i')+iso('i')),
 'isotipo-blanco.svg':svg('40 312 424 446',iso('w','#ffffff')),
 'logotipo.svg':svg('500 315 545 230',word()),
 'logo-horizontal.svg':svg('40 300 1010 460',grad_defs('h')+iso('h')+word()+sub()),
 'logo-horizontal-claro.svg':svg('40 300 1010 460',grad_defs('c')+iso('c')+word('#ffffff')+sub('#fa621f','#3bb6e6')),
}
# vertical: isotipo arriba, edel + bajada abajo (reubicando con transform)
# vertical: isotipo (bbox x51–455, y323–746) centrado arriba; «edel» + bajada (x515–1034, y320–736) debajo
VT='<g transform="translate(47 -297)">{i}</g><g transform="translate(-474.5 176)">{w}</g>'
W['logo-vertical.svg']=svg('0 0 600 932',grad_defs('v')+VT.format(i=iso('v'),w=word()+sub()))
W['logo-vertical-claro.svg']=svg('0 0 600 932',grad_defs('vc')+VT.format(i=iso('vc'),w=word('#ffffff')+sub('#fa621f','#3bb6e6')))
W['favicon.svg']=svg('40 312 424 446',grad_defs('f')+iso('f'))
for k,v in W.items(): open('brand/'+k,'w').write(v)
print('ok',list(W))
