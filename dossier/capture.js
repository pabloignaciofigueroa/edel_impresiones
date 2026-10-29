// Capturas del sitio para el dossier. Sirve public/ en :8765 antes de ejecutar.
// Uso: NODE_PATH=$(npm root -g) node dossier/capture.js
const { chromium } = require('playwright');
const OUT = __dirname + '/shots/';
const B = 'http://localhost:8765/';
// [clave, selector, modo, x]  modos: top · center · offset (fracción de la altura) · bottom
const S = [
  ['hero', '#portada', 'top'],
  ['intro', '#intro', 'center'],
  ['serv', '#servicios', 'offset', 0.0],
  ['serv2', '#servicios', 'offset', 0.22],
  ['serv3', '#servicios', 'offset', 0.5],
  ['serv-fin', '#servicios', 'bottom'],
  ['proc', '#proceso', 'top'],
  ['trab', '#trabajos', 'top'],
  ['equipo', '#equipo', 'top'],
  ['equipo2', '#equipo', 'offset', 0.45],
  ['res', '#resenas', 'center'],
  ['cot', '#cotiza', 'top'],
  ['pie', '.pie', 'bottom'],
];
const go = (p, y) => p.evaluate(y => window.lenis ? lenis.scrollTo(y, { immediate: true }) : scrollTo(0, y), y);
async function abrir(p) {
  await p.goto(B, { waitUntil: 'load' });
  await p.waitForFunction(() => document.documentElement.classList.contains('abierto'), null, { timeout: 15000 });
  await p.waitForTimeout(2500);
  // recorrer una vez para que todo entre y los videos tengan fuente
  const H = await p.evaluate(() => document.body.scrollHeight);
  for (let y = 0; y < H; y += 600) { await go(p, y); await p.waitForTimeout(160); }
  await p.waitForTimeout(1500);
}
async function shoot(p, vh, prefix, list) {
  for (const [k, sel, mode, x] of list) {
    const y = await p.evaluate(([sel, mode, x, vh]) => {
      const e = document.querySelector(sel); if (!e) return -1;
      const top = e.getBoundingClientRect().top + scrollY, h = e.offsetHeight;
      if (mode === 'top') return top; if (mode === 'offset') return top + h * x;
      if (mode === 'bottom') return top + h - vh; return top + (h - vh) / 2;
    }, [sel, mode, x, vh]);
    if (y < 0) { console.log('falta', k, sel); continue; }
    await go(p, Math.max(0, y)); await p.waitForTimeout(400);
    await go(p, Math.max(0, y) + 1); await p.waitForTimeout(2600);
    await p.screenshot({ path: `${OUT}${prefix}-${k}.jpg`, type: 'jpeg', quality: 84 });
  }
}
(async () => {
  const b = await chromium.launch();
  // ---------- computador ----------
  const c = await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1.5, locale: 'es-CL' });
  let p = await c.newPage();
  // pantalla de carga: cuadros mientras se dibuja y mientras se abre
  await p.goto(B, { waitUntil: 'commit' });
  for (const [k, t] of [['carga1', 900], ['carga2', 1900], ['carga3', 2900]]) {
    await p.waitForFunction(t => performance.now() > t, t); await p.screenshot({ path: `${OUT}d-${k}.jpg`, type: 'jpeg', quality: 86 });
  }
  await p.waitForFunction(() => document.body.classList.contains('cargando') && +document.getElementById('pct').textContent >= 100, null, { timeout: 15000 }).catch(() => {});
  await p.waitForTimeout(700); await p.screenshot({ path: `${OUT}d-abre.jpg`, type: 'jpeg', quality: 86 });
  await p.close();
  p = await c.newPage(); await abrir(p); await shoot(p, 900, 'd', S);
  // reseñas con el sello y Team Mate con estallido
  await go(p, await p.evaluate(() => document.querySelector('.team').getBoundingClientRect().top + scrollY - 260)); await p.waitForTimeout(1200);
  await p.click('[data-team="mate"]'); await p.waitForTimeout(350);
  await p.screenshot({ path: `${OUT}d-team.jpg`, type: 'jpeg', quality: 84 });
  // tarjeta del equipo dada vuelta
  await go(p, await p.evaluate(() => document.querySelector('.flip').getBoundingClientRect().top + scrollY - 200)); await p.waitForTimeout(800);
  await p.click('.flip'); await p.waitForTimeout(1100);
  await p.screenshot({ path: `${OUT}d-flip.jpg`, type: 'jpeg', quality: 84 });
  // pila: despegando un sticker
  await go(p, await p.evaluate(() => document.querySelector('#trabajos').getBoundingClientRect().top + scrollY)); await p.waitForTimeout(1500);
  const t = await p.evaluate(() => { const r = document.querySelector('.pila-js .sticker[aria-hidden="false"]').getBoundingClientRect(); return { x: r.left + r.width / 2, y: r.top + r.height / 2 }; });
  await p.mouse.move(t.x, t.y); await p.mouse.down(); await p.mouse.move(t.x + 150, t.y + 10, { steps: 8 }); await p.waitForTimeout(250);
  await p.screenshot({ path: `${OUT}d-trab-peel.jpg`, type: 'jpeg', quality: 84 });
  await p.mouse.up(); await p.waitForTimeout(800);
  // versión en inglés
  await go(p, 99999); await p.waitForTimeout(800);
  await p.click('.pie .lang'); await p.waitForTimeout(800);
  await go(p, await p.evaluate(() => document.querySelector('#servicios').getBoundingClientRect().top + scrollY)); await p.waitForTimeout(2600);
  await p.screenshot({ path: `${OUT}d-en.jpg`, type: 'jpeg', quality: 84 });
  await p.click('.pie .lang').catch(() => {});
  await c.close();
  // ---------- celular ----------
  const m = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2.5, isMobile: true, hasTouch: true, locale: 'es-CL' });
  p = await m.newPage();
  await p.goto(B, { waitUntil: 'commit' });
  await p.waitForFunction(() => performance.now() > 2000); await p.screenshot({ path: `${OUT}m-carga.jpg`, type: 'jpeg', quality: 86 });
  await p.close();
  p = await m.newPage(); await abrir(p); await shoot(p, 844, 'm', S);
  // menú abierto
  await go(p, 0); await p.waitForTimeout(800);
  await p.click('.menu-b'); await p.waitForTimeout(1200);
  await p.screenshot({ path: `${OUT}m-menu.jpg`, type: 'jpeg', quality: 84 });
  await b.close();
})();
