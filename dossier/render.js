// PDF y PNG por lámina, más chequeo de desbordes de los bloques de texto.
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1248, height: 816 } });
  for (const name of ['edel-dossier-diseno', 'edel-carta-regalo']) {
    await p.goto('file://' + __dirname + '/' + name + '.html', { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    const over = await p.evaluate(() => [...document.querySelectorAll('.lam')].map((l, i) => {
      const L = l.getBoundingClientRect(); const bad = [];
      l.querySelectorAll('.tx').forEach(t => { const r = t.getBoundingClientRect();
        if (r.bottom > L.bottom - 18 || r.right > L.right - 10) bad.push((t.innerText || '').slice(0, 30)); });
      return bad.length ? i + ':' + bad.join(' | ') : null; }).filter(Boolean));
    console.log(name, 'overflow', JSON.stringify(over));
    await p.pdf({ path: __dirname + '/' + name + '.pdf', width: '13in', height: '8.5in', printBackground: true });
    if (name === 'edel-dossier-diseno') {
      const lams = await p.$$('.lam');
      for (let i = 0; i < lams.length; i++) await lams[i].screenshot({ path: `${__dirname}/pages/p-${String(i).padStart(2, '0')}.png` });
    }
  }
  await b.close();
})();
