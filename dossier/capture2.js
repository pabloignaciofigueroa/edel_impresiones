// Apertura «la e se abre»: cuadros justo después del 100 %
const { chromium } = require('playwright');
const OUT = __dirname + '/shots/';
(async () => {
  const b = await chromium.launch();
  for (const [pre, vp, mob] of [['d', { width: 1440, height: 900 }, false], ['m', { width: 390, height: 844 }, true]]) {
    const c = await b.newContext({ viewport: vp, deviceScaleFactor: mob ? 2.5 : 1.5, isMobile: mob, hasTouch: mob });
    const p = await c.newPage(); await p.goto('http://localhost:8765/', { waitUntil: 'commit' });
    await p.waitForFunction(() => { const e = document.getElementById('pct'); return e && +e.textContent >= 100; }, null, { timeout: 15000, polling: 20 });
    const t0 = Date.now();
    for (const ms of [150, 450, 750, 1050]) { while (Date.now() - t0 < ms) await p.waitForTimeout(10); await p.screenshot({ path: `${OUT}${pre}-abre-${ms}.jpg`, type: 'jpeg', quality: 86 }); }
    await c.close();
  }
  await b.close();
})();
