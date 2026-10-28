"""Verifica contraste AA de los pares de color de la paleta (texto >=4.5, títulos grandes >=3)."""
import sys,json
def L(h):
    h=h.lstrip('#'); c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    c=[x/12.92 if x<=0.03928 else ((x+0.055)/1.055)**2.4 for x in c]; return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
def cr(a,b): A,B=sorted([L(a),L(b)],reverse=True); return (A+0.05)/(B+0.05)
T={'tinta':'#05263f','azul':'#0358a5','cian':'#0195ca','cian-luz':'#3bb6e6','naranja':'#fa621f','naranja-banda':'#ce4204','uv':'#2e279f','uv-luz':'#545fe0','madera':'#d3a03c','papel':'#f3f0eb','gris':'#5f6062','blanco':'#ffffff'}
# (texto, fondo, mínimo, uso)
P=[('blanco','tinta',4.5,'texto en portada y pie'),('naranja','tinta',3,'títulos y acentos grandes en portada'),
('azul','papel',4.5,'títulos y enlaces en secciones claras'),('tinta','papel',4.5,'texto corrido claro'),('gris','papel',4.5,'texto secundario'),
('blanco','azul',4.5,'servicios'),('blanco','naranja-banda',4.5,'rótulos Oswald sobre banda'),('blanco','naranja',3,'títulos grandes sobre naranja'),
('tinta','naranja',4.5,'reseñas'),('blanco','uv',4.5,'proceso'),('tinta','madera',4.5,'equipo'),('cian-luz','tinta',4.5,'cierre: acentos'),('cian','tinta',3,'cierre: formas y títulos grandes'),('blanco','gris',4.5,'chips')]
bad=0
for a,b,m,u in P:
    v=cr(T[a],T[b]); ok=v>=m; bad+=not ok
    print(f"{'OK ' if ok else 'MAL'} {a:13s} sobre {b:13s} {v:5.2f} (mín {m}) · {u}")
if __name__=='__main__': json.dump(T,open('brand/palette.json','w'),indent=1); sys.exit(1 if bad else 0)
