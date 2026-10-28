#!/usr/bin/env python3
"""Regenera public/: la carpeta que se publica en Cloudflare Pages.

Base: tools/publish.py de almud_bar. Copia solo lo que las páginas usan de verdad (se siguen las referencias desde los HTML
→ CSS/JS → fuentes, imágenes y videos), deja fuera todo lo interno y escribe public/_headers y public/_redirects.

Falla (código 1, sin dejar un public/ a medias) si:
  - se cuela algo interno (.md, .py, .csv, .json, assets/raw, nombres con "_"),
  - falta un archivo que index.html, css o js referencian,
  - algún archivo pesa más de 25 MB (límite por archivo de Cloudflare Pages).

Uso: python3 tools/publish.py
"""
import pathlib, re, shutil, sys, tempfile
from urllib.parse import unquote

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / 'public'

# Trabajo (fase 9): la versión en curso vive en /nueva/ (noindex). La raíz redirige ahí mientras se trabaja.
# Al cerrar (fase 20): la versión aprobada pasa a la raíz y las /nueva*/ quedan con 301 a /.
INCLUDE_FILES = ['nueva/index.html', 'nueva_v2/index.html', 'nueva_v3/index.html', 'nueva_v4/index.html', 'nueva_v5/index.html', 'nueva_v6/index.html', 'nueva_v7/index.html', '404.html', 'robots.txt']
INCLUDE_DIRS = ['vendor', 'assets/fonts', 'assets/video', 'assets/img', 'brand', 'css', 'js/nv1', 'js/nv2', 'js/nv3', 'js/nv4', 'js/nv5', 'js/nv6', 'js/nv7']
ALL_DIRS = []
BLOCKED_EXT = {'.md', '.py', '.csv', '.json', '.pyc', '.sh', '.ipynb'}
BLOCKED_DIRS = {'assets/raw'}
BLOCKED_NAMES = {'.DS_Store', 'Thumbs.db', '__pycache__', 'node_modules', '.git'}
MAX_BYTES = 25 * 1024 * 1024
EXTRA = ['assets/og.jpg']  # se referencia con URL absoluta (og:image); se publica siempre

# Caché (regla de la skill): assets una semana + swr un día; vendor 30 días immutable; brand una semana; css/js una hora + swr.
HEADERS = """\
/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin

/assets/*
  Cache-Control: public, max-age=604800, stale-while-revalidate=86400

/vendor/*
  Cache-Control: public, max-age=2592000, immutable

/brand/*
  Cache-Control: public, max-age=604800, stale-while-revalidate=86400

/css/*
  Cache-Control: public, max-age=3600, stale-while-revalidate=86400

/js/*
  Cache-Control: public, max-age=3600, stale-while-revalidate=86400
"""
REDIRECTS = """/ /nueva_v7/ 302
"""


def is_internal(rel: pathlib.PurePosixPath) -> str | None:
    """Devuelve el motivo si la ruta es interna; None si es publicable."""
    s = rel.as_posix()
    if any(s == d or s.startswith(d + '/') for d in BLOCKED_DIRS):
        return 'carpeta interna'
    for part in rel.parts:
        if part in BLOCKED_NAMES:
            return f'nombre bloqueado ({part})'
        if part.startswith('_') and s not in ('_headers', '_redirects'):
            return f'nombre interno ({part})'
        if part.startswith('.'):
            return f'archivo oculto ({part})'
    if rel.suffix.lower() in BLOCKED_EXT:
        return f'extensión interna ({rel.suffix})'
    return None


SITE = 'https://edelimpresiones.pages.dev/'


def used_files() -> set[str]:
    """Fase 16: lo que las páginas usan de verdad (HTML → CSS/JS → fuentes e imágenes), siguiendo las referencias.
    Lo que no se referencia no se publica (videos e imágenes viejas, vendor/ que la v2 no carga, brand/ de trabajo)."""
    seen, todo = set(EXTRA), list(INCLUDE_FILES)
    while todo:
        f = todo.pop()
        if f in seen or not (ROOT / f).is_file():
            continue
        seen.add(f)
        if pathlib.PurePosixPath(f).suffix not in ('.html', '.css', '.js', '.webmanifest'):
            continue
        text = (ROOT / f).read_text(errors='ignore').replace(SITE, '/')
        base = pathlib.PurePosixPath('.') if f.endswith('.js') else pathlib.PurePosixPath(f).parent
        todo += [r for r in references(text, base) if r not in seen]
    return seen


def copy_tree(stage: pathlib.Path) -> list[str]:
    skipped = []
    used = used_files()
    for f in INCLUDE_FILES:
        src = ROOT / f
        if not src.is_file():
            sys.exit(f'ERROR: falta {f}')
        (stage / f).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, stage / f)
    for d in INCLUDE_DIRS:
        base = ROOT / d
        if not base.is_dir():
            sys.exit(f'ERROR: falta la carpeta {d}/')
        for src in sorted(base.rglob('*')):
            if not src.is_file():
                continue
            rel = pathlib.PurePosixPath(src.relative_to(ROOT).as_posix())
            if is_internal(rel):
                skipped.append(rel.as_posix())
                continue
            if rel.as_posix() not in used:
                skipped.append(rel.as_posix() + ' (sin uso)')
                continue
            dst = stage / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    for d in ALL_DIRS:  # v1b: medios de la v1 (sus rutas se arman en JS, el rastreo no las ve)
        for src in sorted((ROOT / d).rglob('*')):
            rel = pathlib.PurePosixPath(src.relative_to(ROOT).as_posix())
            if src.is_file() and not is_internal(rel):
                (stage / rel).parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, stage / rel)
    for f in EXTRA:
        (stage / f).parent.mkdir(parents=True, exist_ok=True); shutil.copy2(ROOT / f, stage / f)
    (stage / '_headers').write_text(HEADERS)
    (stage / '_redirects').write_text(REDIRECTS)
    return skipped


REF_PATTERNS = [
    re.compile(r'''(?:src|href|poster|data-[\w-]+)\s*=\s*["']([^"']+)["']'''),
    re.compile(r'''srcset\s*=\s*["']([^"']+)["']'''),
    re.compile(r'''url\(\s*["']?([^"')]+)["']?\s*\)'''),
    re.compile(r'''["'`]((?:\.{0,2}/)?(?:assets|brand|css|js|vendor)/[^"'`\s]+?)["'`]'''),
]


def references(text: str, base: pathlib.PurePosixPath) -> set[str]:
    refs = set()
    for pat in REF_PATTERNS:
        for m in pat.finditer(text):
            for piece in m.group(1).split(','):
                url = piece.strip().split(' ')[0].split('#')[0].split('?')[0]
                if not url or url.startswith('@') or re.match(r'^([a-z]+:|//|#|\{|\$)', url, re.I) or '${' in url:
                    continue
                if not re.search(r'\.[a-z][a-z0-9]{1,4}$', url, re.I):
                    continue
                p = (base / unquote(url)).as_posix() if not url.startswith('/') else url.lstrip('/')
                parts = []
                for seg in p.split('/'):
                    if seg in ('', '.'):
                        continue
                    if seg == '..':
                        if parts:
                            parts.pop()
                        continue
                    parts.append(seg)
                refs.add('/'.join(parts))
    return refs


def check(stage: pathlib.Path) -> list[str]:
    errors = []
    files = [p for p in stage.rglob('*') if p.is_file()]
    for p in files:
        rel = pathlib.PurePosixPath(p.relative_to(stage).as_posix())
        why = is_internal(rel)
        if why:
            errors.append(f'interno: {rel} ({why})')
        if p.stat().st_size > MAX_BYTES:
            errors.append(f'pesa más de 25 MB: {rel} ({p.stat().st_size / 1048576:.1f} MB)')
    sources = [stage / f for f in INCLUDE_FILES] + list((stage / 'css').rglob('*.css')) + list((stage / 'js').rglob('*.js'))
    missing = set()
    for src in sources:
        rel_dir = pathlib.PurePosixPath(src.relative_to(stage).as_posix()).parent
        # en JS las rutas son relativas al documento, no al archivo .js
        base = pathlib.PurePosixPath('.') if src.suffix == '.js' else rel_dir
        for ref in references(src.read_text(errors='ignore').replace(SITE, '/'), base):
            if not (stage / ref).is_file():
                missing.add(f'falta: {ref} (referenciado en {src.relative_to(stage)})')
    return errors + sorted(missing)


def main():
    with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
        stage = pathlib.Path(tmp) / 'public'
        stage.mkdir()
        skipped = copy_tree(stage)
        errors = check(stage)
        if errors:
            print('publish.py: ERROR, public/ no se modificó', file=sys.stderr)
            for e in errors:
                print('  ' + e, file=sys.stderr)
            sys.exit(1)
        if OUT.exists():
            shutil.rmtree(OUT)
        shutil.move(str(stage), OUT)
    files = [p for p in OUT.rglob('*') if p.is_file()]
    total = sum(p.stat().st_size for p in files)
    big = max(files, key=lambda p: p.stat().st_size)
    print(f'public/ listo: {len(files)} archivos, {total / 1048576:.1f} MB '
          f'(el mayor: {big.relative_to(OUT)}, {big.stat().st_size / 1048576:.1f} MB)')
    unused = [x for x in skipped if x.endswith('(sin uso)')]
    print(f'omitidos por internos: {len(skipped) - len(unused)} · sin uso (no se publican): {len(unused)}')
    if '-v' in sys.argv:
        for s in skipped:
            print('  - ' + s)


if __name__ == '__main__':
    main()
