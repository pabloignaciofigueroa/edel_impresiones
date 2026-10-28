"""Fase 7 — medios. Cortes elegidos en las hojas de hallazgos (_qa/medios/h_*.jpg, cuadros cada 0,5 s).
Videos: tramos sin rótulos, siempre hacia adelante, fundido final→inicio de 0,9 s (loop sin salto), sin audio.
Salida: assets/video/<id>.mp4 (h264 faststart) + .webm (VP9) + -poster.jpg ; manifiesto assets/video/media.json
Fotos: assets/img/<id>-<ancho>.webp + LQIP ; manifiesto assets/img/media.json
Uso: python3 tools/medios.py [video|foto|todo]"""
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
 'equipo':    ([('33',0.0,11.5)],'IG-33','equipo'),
 'equipo-2':  ([('38',0.0,8.3)],'IG-38','equipo'),
}
XF=0.3   # fundido entre tramos
LOOP=0.9 # fundido final → inicio
def run(c): subprocess.run(c,check=True)
def dur(f): return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f]))
def build_video(vid,parts,w=720,crf=24,tag=''):
    os.makedirs('assets/video',exist_ok=True); tmp=f'/tmp/med_{vid}{tag}.mp4'
    ins=[];fl=[];n=len(parts)
    for i,(r,a,b) in enumerate(parts):
        ins+=['-i',RAW+R(r)+'.mp4']
        fl.append(f'[{i}:v]trim={a}:{b},setpts=PTS-STARTPTS,fps=30,scale={w}:-2:flags=lanczos,setsar=1,format=yuv420p[s{i}]')
    cur='s0'; L=parts[0][2]-parts[0][1]
    for i in range(1,n):
        Li=parts[i][2]-parts[i][1]; fl.append(f'[{cur}][s{i}]xfade=transition=fade:duration={XF}:offset={L-XF:.3f}[c{i}]'); cur=f'c{i}'; L=L+Li-XF
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
    for vid,(parts,src,uso) in VIDEOS.items():
        w,crf=(720,24) if vid=='hero' else (540,28)
        d=build_video(vid,parts,w=w,crf=crf); webm(vid); lq=poster(vid)
        if vid=='hero':  # versión liviana para celular
            build_video(vid,parts,w=540,crf=30,tag='-540'); webm(vid,'-540')
        man[vid]=dict(fuente=src,uso=uso,duracion=round(d,2),tramos=parts,lqip=lq,
            kb={k:os.path.getsize(f'assets/video/{vid}{k}')//1024 for k in ['.mp4','.webm','-poster.webp']})
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
