"""Fase 7 — medios. Cortes elegidos en las hojas de hallazgos (_qa/medios/h_*.jpg, cuadros cada 0,5 s).
Videos: tramos sin rótulos, siempre hacia adelante, fundido final→inicio de 0,9 s (loop sin salto), sin audio.
Salida: assets/video/<id>.mp4 (h264 faststart) + .webm (VP9) + -poster.jpg ; manifiesto assets/video/media.json
Fotos: assets/img/<id>-<ancho>.webp + LQIP ; manifiesto assets/img/media.json
Uso: python3 tools/medios.py [video|foto|todo] [ids…]  (con ids solo rehace esos; SIN ids rehace todos y pisa los congelados)"""
import subprocess, json, os, sys, base64, io
from PIL import Image
RAW='assets/raw/ig/'
def R(n): return {'16':'IG-16_DXPvxs2kU24_1','24':'IG-24_DXuqkTokgD__1','25':'IG-25_DX63ggCxhyU_1','29':'IG-29_DYpb7QIRnPD_1','30':'IG-30_DY0Rwq1xJZG_1',
 '31':'IG-31_DZYzBtaRnwH_1','33':'IG-33_DZ0Kx3dRySk_1','34':'IG-34_DZ-3uhCPyk__1','35':'IG-35_Daf4nbhx4W1_1','37':'IG-37_Dan21cqR1DU_1','38':'IG-38_DarE53aRVmM_1',
 '40':'IG-40_Db6wz2vxhxn_1','42':'IG-42_DcmkKIpxx0k_1','44':'IG-44_Dcyy4aURnBo_1','45':'IG-45_Dc_c_IHxcJf_1','46':'IG-46_DdHdaazxdD3_1','47':'IG-47_Dd11g3fCY7m_1'}[n]
# id: (tramos [(reel, desde, hasta)], fuente, uso)
VIDEOS={
 'hero':      ([('45',0.6,3.2),('47',4.0,6.5),('30',2.0,5.0),('44',5.0,7.0),('37',3.5,5.3)],'IG-45, IG-47, IG-30, IG-44, IG-37','portada: máquinas trabajando'),
 'plateados': ([('29',3.5,12.8)],'IG-29','servicio: plateados tornasol'),
 'transparentes':([('46',1.0,10.5)],'IG-46','servicio: transparentes (vaso Dulce Enlatta)'),
 'uv':        ([('45',0.6,3.2),('44',3.5,7.0),('47',4.0,6.0)],'IG-45, IG-44, IG-47','servicio: impresión UV'),
 'diplomas':  ([('47',6.0,9.3),('47',10.0,13.9)],'IG-47','servicio: diplomas (Dekra)'),
 'laser':     ([('24',9.5,18.0)],'IG-24','servicio: corte láser, mostrador'),
 'bitacoras': ([('25',5.0,14.5)],'IG-25','servicio: bitácoras (Chiloé Náutica)'),
 'prendas':   ([('42',1.0,3.8),('42',4.5,8.4),('42',9.0,10.0)],'IG-42','servicio: prendas (SSC Rental)'),
 'medallas':  ([('44',0.0,3.0),('44',7.5,12.7)],'IG-44','servicio: medallas (RevelArte)'),
 'letreros':  ([('34',3.5,7.0),('34',17.5,21.5)],'IG-34','servicio: letreros (Pilates & Skincare)'),
 'stickers':  ([('37',0.0,5.3),('31',12.0,14.8)],'IG-37, IG-31','servicio: stickers y etiquetas'),
 'tarjetas':  ([('45',5.5,8.0),('31',3.0,4.4),('45',8.0,9.4)],'IG-45, IG-31','servicio: tarjetas'),
 'diseno':    ([('44',0.0,1.4),('33',12.0,19.9)],'IG-44, IG-33','servicio: diseño'),
 'p1-imprimir':([('45',0.6,3.2),('30',0.0,1.8),('37',2.0,3.3)],'IG-45, IG-30, IG-37','proceso 1'),
 'p2-plotter':([('30',2.0,6.2),('31',12.0,13.3)],'IG-30, IG-31','proceso 2'),
 'p3-depilado':([('30',6.3,9.8),('37',3.5,5.3)],'IG-30, IG-37','proceso 3'),
 'proceso':   ([('45',0.6,3.2),('30',0.0,1.8),('30',2.0,6.2),('31',12.0,13.3),('30',6.3,9.8),('37',3.5,5.3)],'IG-45, IG-30, IG-31, IG-37','proceso: imprimir → plotter → depilado en un solo video (Pablo)'),
 'team':      ([('35',0.0,4.6)],'IG-35','equipo: Team Mate o Team Café (con su rótulo, decisión de Pablo)'),
 'equipo':    ([('33',0.0,11.5)],'IG-33','equipo'),
 'equipo-2':  ([('38',0.0,8.3)],'IG-38','equipo'),
 # Fase 19 — ids nuevos con sufijo 8 (los de arriba quedan intactos para las copias congeladas /nueva_v1..v7).
 # Cortes verificados cuadro a cuadro: IG-45 pasa de la impresora de rollo a la UV en 1,633 s (antes el loop arrastraba 4 cuadros de rollo);
 # IG-34 corta del póster a la mano en 4,5 s (y el barrido al póster termina en 17,9); IG-24 tiene un salto en 11,0 (se funde) y su último cuadro es 17,9; IG-37 corta en 2,133 / 3,6 / 5,667; IG-44 en 5,233; IG-30 en 1,967 / 6,5.
 'hero8':     ([('45',1.62,3.12,{}),('47',1.65,2.85,{}),('30',2.0,6.0,{}),('44',5.25,7.45,{}),('37',3.62,5.62,{})],'IG-45, IG-47, IG-30, IG-44, IG-37','portada: máquinas trabajando (sin cuadros intrusos ni diplomas legibles)'),
 'uv8':       ([('45',1.62,3.55,{'v':0.85}),('44',3.5,5.22,{'v':0.85}),('44',5.25,7.45,{'v':0.85}),('47',1.65,2.85,{'v':0.85}),('47',4.12,5.7,{'v':0.85,'cens':True})],'IG-45, IG-44, IG-47','servicio: impresión UV (diplomas con nombres y QR difuminados)'),
 'proceso8':  ([('45',1.62,3.55,{}),('30',0.0,1.8,{}),('30',2.0,6.2,{}),('31',12.0,13.28,{}),('30',6.52,9.8,{}),('37',3.62,5.3,{})],'IG-45, IG-30, IG-31, IG-37','proceso: imprimir → plotter → depilado en un solo video'),
 'p1-imprimir8':([('45',1.62,3.55,{}),('30',0.0,1.8,{}),('37',2.15,3.55,{})],'IG-45, IG-30, IG-37','proceso 1'),
 'letreros8': ([('34',4.52,7.3,{}),('37',8.05,11.03,{}),('34',17.9,21.7,{})],'IG-34, IG-37','servicio: letreros (Pilates & Skincare), sin rótulos ni póster intruso'),
 'diplomas8': ([('47',1.65,2.85,{'v':0.95}),('47',4.12,5.7,{'v':0.95,'cens':True}),('47',5.75,7.8,{'v':0.95,'cens':True}),('47',7.85,9.55,{'v':0.95,'cens':True}),('47',10.27,11.9,{'v':0.95,'cens':True}),('47',11.97,13.98,{'v':0.95,'cens':True})],'IG-47','servicio: diplomas (Dekra), nombres y QR difuminados'),
 'tarjetas8': ([('45',5.75,7.82,{'v':0.62,'interp':True}),('31',3.05,4.48,{'v':0.62,'interp':True}),('40',9.3,11.05,{'v':0.62,'interp':True}),('40',0.0,1.08,{'v':0.62,'interp':True})],'IG-45, IG-31, IG-40','servicio: tarjetas (Hojalatería Erice, XS Joyas, Sigma), sin el cuaderno Reiver'),
 'team8':     ([('35',1.12,4.5,{'v':0.4,'interp':True})],'IG-35','equipo: Team Mate o Team Café; el loop se funde con el rótulo ya quieto'),
 'medallas8': ([('44',1.32,3.0,{}),('44',3.5,5.22,{}),('44',5.25,7.45,{}),('44',7.52,10.2,{}),('44',10.52,12.58,{})],'IG-44','servicio: medallas (RevelArte): láser, UV, medalla y entrega'),
 'stickers8': ([('37',0.0,2.1,{'v':0.9}),('37',2.17,3.58,{'v':0.9}),('37',3.62,5.62,{'v':0.9}),('31',10.4,11.85,{'v':0.9}),('31',12.0,13.28,{'v':0.9}),('31',13.33,14.72,{'v':0.9})],'IG-37, IG-31','servicio: stickers y etiquetas'),
 # Trabajos (D-1): tomas distintas de las de Servicios
 'trab-medallas8':([('44',7.52,10.2,{}),('44',10.52,12.58,{})],'IG-44','trabajo: medallas RevelArte, medalla y entrega en escenario'),
 'trab-letreros8':([('34',17.9,24.5,{})],'IG-34','trabajo: letrero Pilates & Skincare terminado'),
 'trab-bitacoras8':([('25',2.25,4.8,{}),('25',15.3,17.13,{}),('25',17.2,18.8,{})],'IG-25','trabajo: bitácoras Chiloé Náutica (tapas y en mano)'),
 'laser8':    ([('24',7.0,10.97,{}),('24',11.03,17.88,{})],'IG-24','servicio: corte láser, mostrador'),
}
# segundos en que cambia el paso del proceso (revisados cuadro a cuadro a 5 fps)
PASOS={'proceso':{"1": 0.0, "2": 2.9, "3": 7.8},'proceso8':{'2':2.6,'3':7.3}}
XF=0.3   # fundido entre tramos
LOOP=0.9 # fundido final → inicio
def run(c): subprocess.run(c,check=True)
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
def _o(p): return p[3] if len(p)>3 else {}
def _len(p): return (p[2]-p[1])/_o(p).get('v',1)
def censurar(r,a,b):
    """Fase 19 (privacidad): difumina texto oscuro fino y QR (nombres de alumnos, códigos) cuadro a cuadro.
    Máscara = black-hat morfológico (trazos oscuros finos sobre papel claro) excepto verdes saturados (logos achs/DEKRA quedan nítidos),
    dilatada y suavizada; la zona se reemplaza por un mosaico desenfocado (ilegible y no escaneable). Devuelve un clip intermedio [a,b)."""
    import cv2, numpy as np
    out=f'/tmp/med_cens_{r}_{a}_{b}.mp4'
    if os.path.exists(out): return out
    W,H=720,1280
    dec=subprocess.Popen(['ffmpeg','-v','error','-i',RAW+R(r)+'.mp4','-vf',f'trim={a}:{b},setpts=PTS-STARTPTS,fps=30,scale={W}:{H}','-f','rawvideo','-pix_fmt','bgr24','-'],stdout=subprocess.PIPE)
    enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r','30','-i','-','-c:v','libx264','-preset','veryfast','-crf','8','-pix_fmt','yuv420p',out],stdin=subprocess.PIPE)
    k1=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(25,25)); k2=cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(45,45)); prev=None
    while True:
        buf=dec.stdout.read(W*H*3)
        if len(buf)<W*H*3: break
        f=np.frombuffer(buf,np.uint8).reshape(H,W,3)
        g=cv2.cvtColor(f,cv2.COLOR_BGR2GRAY); sat=cv2.cvtColor(f,cv2.COLOR_BGR2HSV)[...,1]
        bh=cv2.morphologyEx(g,cv2.MORPH_BLACKHAT,k1)
        hue=cv2.cvtColor(f,cv2.COLOR_BGR2HSV)[...,0]; verde=(hue>=30)&(hue<=95)&(sat>60)  # logos achs/DEKRA quedan nítidos
        m=cv2.dilate(((bh>24)&~verde).astype(np.uint8)*255,k2)
        m=cv2.GaussianBlur(m,(0,0),8).astype(np.float32)/255
        if prev is not None: m=np.maximum(m,prev*0.6)
        prev=m
        bl=cv2.GaussianBlur(cv2.resize(cv2.resize(f,(W//10,H//10),interpolation=cv2.INTER_AREA),(W,H),interpolation=cv2.INTER_LINEAR),(0,0),6)
        o=(f*(1-m[...,None])+bl*m[...,None]).astype(np.uint8)
        enc.stdin.write(o.tobytes())
    enc.stdin.close(); enc.wait(); dec.wait()
    return out
def build_video(vid,parts,w=720,crf=24,tag=''):
    """parts: (reel, desde, hasta[, opciones]). Con 4.º elemento (aunque sea {}) el tramo usa largo exacto. Opciones (fase 19, solo ids nuevos): v=velocidad (0,6 = más lento),
    interp=True interpola cuadros al ralentizar, cens=True difumina nombres/QR (censurar). Sin opciones el filtro es idéntico al original."""
    os.makedirs('assets/video',exist_ok=True); tmp=f'/tmp/med_{vid}{tag}.mp4'
    ins=[];fl=[];n=len(parts)
    for i,p in enumerate(parts):
        r,a,b=p[:3]; o=_o(p)
        if len(p)<=3:  # tramos originales: filtro idéntico al de siempre
            ins+=['-i',RAW+R(r)+'.mp4']
            fl.append(f'[{i}:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30,scale={w}:-2:flags=lanczos,setsar=1,format=yuv420p[s{i}]')
            continue
        src=censurar(r,a,b) if o.get('cens') else RAW+R(r)+'.mp4'
        ta,tb=(0,round(b-a,3)) if o.get('cens') else (a,b)
        v=o.get('v',1)
        sp=f'setpts=(PTS-STARTPTS)/{v},' if v!=1 else 'setpts=PTS-STARTPTS,'
        rate='minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:vsbmc=1,' if (v!=1 and o.get('interp')) else 'fps=30,'
        ins+=['-i',src]
        # largo exacto: se rellena con el último cuadro y se recorta a (b-a)/v, así cada fundido calza con su offset
        fl.append(f'[{i}:v]trim={ta}:{tb},{sp}{rate}tpad=stop_mode=clone:stop_duration=1,trim=duration={_len(p):.4f},scale={w}:-2:flags=lanczos,setsar=1,format=yuv420p[s{i}]')
    cur='s0'; L=_len(parts[0])
    for i in range(1,n):
        Li=_len(parts[i]); fl.append(f'[{cur}][s{i}]xfade=transition=fade:duration={XF}:offset={L-XF:.3f}[c{i}]'); cur=f'c{i}'; L=L+Li-XF
    # loop: cuerpo = [LOOP, L], cola = [0, LOOP] fundida sobre el final
    fl.append(f'[{cur}]split[x][y];[x]trim={LOOP}:{L:.3f},setpts=PTS-STARTPTS[body];[y]trim=0:{LOOP},setpts=PTS-STARTPTS[head];'
              f'[body][head]xfade=transition=fade:duration={LOOP}:offset={L-2*LOOP:.3f}[out]')
    run(['ffmpeg','-v','error','-y',*ins,'-filter_complex',';'.join(fl),'-map','[out]','-an','-c:v','libx264','-preset','veryfast','-crf',str(crf),'-pix_fmt','yuv420p','-movflags','+faststart',f'assets/video/{vid}{tag}.mp4'])
    return dur(f'assets/video/{vid}{tag}.mp4')
def webm(vid,tag=''):
    run(['ffmpeg','-v','error','-y','-i',f'assets/video/{vid}{tag}.mp4','-c:v','libvpx-vp9','-b:v','0','-crf','40','-row-mt','1','-deadline','good','-cpu-used','4','-an',f'assets/video/{vid}{tag}.webm'])
def poster(vid):
    run(['ffmpeg','-v','error','-y','-ss','0','-i',f'assets/video/{vid}.mp4','-frames:v','1','-q:v','4',f'assets/video/{vid}-poster.jpg'])
    im=Image.open(f'assets/video/{vid}-poster.jpg'); im.save(f'assets/video/{vid}-poster.webp',quality=72)
    t=im.copy(); t.thumbnail((16,16)); b=io.BytesIO(); t.save(b,'WEBP',quality=40); return 'data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
def videos():
    man={}
    only=sys.argv[2:] ; old=json.load(open('assets/video/media.json')) if only and os.path.exists('assets/video/media.json') else {}
    man.update({k:v for k,v in old.items() if k in VIDEOS})
    for vid,(parts,src,uso) in VIDEOS.items():
        if only and vid not in only: continue
        w,crf=(720,24) if vid in('hero','hero8') else (540,28)
        d=build_video(vid,parts,w=w,crf=crf); webm(vid); lq=poster(vid)
        if vid=='hero':  # versión liviana para celular
            build_video(vid,parts,w=540,crf=30,tag='-540'); webm(vid,'-540')
        ks=['.mp4','.webm','-poster.webp']
        if vid=='hero8':  # liviana (540, crf 30) y extra liviana para el primer pantallazo (540, crf 33, solo mp4; como hero-540b de la fase 18)
            build_video(vid,parts,w=540,crf=30,tag='-540'); webm(vid,'-540'); build_video(vid,parts,w=540,crf=33,tag='-540b')
            ks+=['-540.mp4','-540.webm','-540b.mp4']
        man[vid]=dict(fuente=src,uso=uso,duracion=round(d,2),tramos=parts,lqip=lq,
            kb={k:os.path.getsize(f'assets/video/{vid}{k}')//1024 for k in ks})
        if vid in PASOS: man[vid]['pasos']=PASOS[vid]
        print(vid,round(d,1),'s',man[vid]['kb'])
    json.dump(man,open('assets/video/media.json','w'),ensure_ascii=False,indent=1)
# Fotos limpias (sin texto encima). IG-18 #3/#4 llevan un isotipo chico en una esquina: pendiente de Pablo.
FOTOS={
 'vehicular-1':('IG-39_Da52kcUERCq_1.jpg','IG-39'),'vehicular-2':('IG-39_Da52kcUERCq_2.jpg','IG-39'),'vehicular-3':('IG-39_Da52kcUERCq_3.jpg','IG-39'),
 'vehicular-4':('IG-39_Da52kcUERCq_4.jpg','IG-39'),'vehicular-5':('IG-39_Da52kcUERCq_5.jpg','IG-39'),
 'etiquetas-miel':('IG-43_DctSvfaEZz3_1.jpg','IG-43'),'etiquetas-naguara':('IG-43_DctSvfaEZz3_2.jpg','IG-43'),'etiquetas-berries':('IG-43_DctSvfaEZz3_3.jpg','IG-43'),
 'etiquetas-xs':('IG-26_DX9jQqLRBD8_1.jpg','IG-26'),'senaleticas-sigma':('IG-28_DYfXezbxOP2_1.jpg','IG-28'),
 'equipo-3':('IG-18_DXZ39nRkXCt_3.jpg','IG-18'),'equipo-4':('IG-18_DXZ39nRkXCt_4.jpg','IG-18'),
}
def fotos():
    os.makedirs('assets/img',exist_ok=True); man={}
    for fid,(f,src) in FOTOS.items():
        im=Image.open(RAW+f).convert('RGB'); W,H=im.size; outs=[]
        for w in [480,800,1200,1600]:
            if w>W and outs: break
            ww=min(w,W); r=im.resize((ww,round(H*ww/W)),Image.LANCZOS); p=f'assets/img/{fid}-{ww}.webp'; r.save(p,quality=78,method=6); outs.append([ww,p])
        t=im.copy(); t.thumbnail((20,20)); b=io.BytesIO(); t.save(b,'WEBP',quality=40)
        man[fid]=dict(fuente=src,ancho=W,alto=H,srcset=outs,lqip='data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode())
        print(fid,W,H,len(outs))
    json.dump(man,open('assets/img/media.json','w'),ensure_ascii=False,indent=1)
if __name__=='__main__':
    m=sys.argv[1] if len(sys.argv)>1 else 'todo'
    if m in('foto','todo'): fotos()
    if m in('video','todo'): videos()
