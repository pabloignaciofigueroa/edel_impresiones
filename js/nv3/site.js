/* Edel Impresiones · nv1 (fase 9). Sin JS la página se lee completa; con movimiento reducido no hay carga ni apertura. */
(() => {
  'use strict';
  const D = document, H = D.documentElement, B = D.body;
  const $ = (s, c = D) => c.querySelector(s), $$ = (s, c = D) => [...c.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
  const EASE = 'expo.out';

  /* ---------- idioma ---------- */
  const store = { get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }, set(k, v) { try { localStorage.setItem(k, v); } catch (e) {} } };
  function setLang(l) {
    H.dataset.lang = l; H.lang = l;
    $$('[data-en]').forEach(el => { if (!el.dataset.es) el.dataset.es = el.textContent; el.textContent = l === 'en' ? el.dataset.en : el.dataset.es; });
    [['data-aria-en', 'aria-label'], ['data-alt-en', 'alt'], ['data-title-en', 'title'], ['data-meta-en', 'content']].forEach(([d, a]) => {
      $$(`[${d}]`).forEach(el => { const k = d + '-es'; if (!el.hasAttribute(k)) el.setAttribute(k, el.getAttribute(a) || ''); el.setAttribute(a, l === 'en' ? el.getAttribute(d) : el.getAttribute(k)); });
    });
    store.set('edel-lang', l);
  }
  const lb = $('.lang'); if (lb) lb.addEventListener('click', () => setLang(H.dataset.lang === 'en' ? 'es' : 'en'));
  if (H.dataset.lang === 'en') setLang('en');

  /* ---------- videos diferidos (nunca se pausan ni dependen del scroll) ---------- */
  const startVideo = v => { if (v.dataset.src && !v.src) { v.src = v.dataset.src; v.load(); } const p = v.play(); if (p) p.catch(() => {}); };
  const io = 'IntersectionObserver' in window ? new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { startVideo(en.target); io.unobserve(en.target); } }), { rootMargin: '150% 0px' }) : null;
  $$('video[data-src]').forEach(v => io ? io.observe(v) : startVideo(v));

  /* ---------- portada: video grande en pantallas anchas ---------- */
  const hv = $('.hero-video');
  if (hv && innerWidth >= 900 && hv.dataset.srcGrande) { hv.src = hv.dataset.srcGrande; }
  hv && hv.load();

  /* ---------- carga con % real y apertura «la e se abre» ---------- */
  const carga = $('#carga'), ov = $('#ov');
  const aps = $$('.ap', ov || D), hueco = $('#hueco'), isoA = $('#isoA'), isoN = $('#isoN'), pal = $('#pal');
  const edel = $$('#edel path'), sub = [$('#sub1'), $('#sub2')], pctEl = $('#pct');
  const A = { x: 265, y: 480 };           // ancla: contraforma oscura del isotipo (coordenadas del logo)
  const LOGO = { cx: 253, cy: 766, w: 520, h: 886 };
  let geo = null, state = { s: 1, tx: 0, ty: 0 };
  function layout() {
    const W = innerWidth, Hh = innerHeight; ov.setAttribute('viewBox', `0 0 ${W} ${Hh}`);
    const s0 = Math.min(W * 0.62 / LOGO.w, Hh * 0.56 / LOGO.h), cy = Hh * 0.45;
    geo = { W, H: Hh, s0, tx: W / 2 + s0 * (A.x - LOGO.cx), ty: cy + s0 * (A.y - LOGO.cy) };
    carga.style.setProperty('--pct-y', (cy + s0 * LOGO.h / 2 + 26) + 'px');
  }
  const apply = () => aps.forEach(g => g.setAttribute('transform', `translate(${state.tx} ${state.ty}) scale(${state.s}) translate(${-A.x} ${-A.y})`));
  function draw(p) {
    const L = [isoA, isoN].map(x => x.getTotalLength()), tot = L[0] + L[1], a = clamp(p / 0.55) * tot;
    [isoA, isoN].forEach((x, i) => { const before = i ? L[0] : 0, k = clamp((a - before) / L[i]); x.style.strokeDasharray = '1'; x.style.strokeDashoffset = 1 - k; x.style.fillOpacity = clamp((p - 0.5) / 0.15); });
    const Le = edel.map(x => x.getTotalLength()), te = Le.reduce((m, v) => m + v, 0); let acc = 0; const de = clamp((p - 0.62) / 0.3) * te;
    edel.forEach((x, i) => { x.style.strokeDashoffset = 1 - clamp((de - acc) / Le[i]); acc += Le[i]; });
    sub.forEach(x => x.style.opacity = clamp((p - 0.92) / 0.08));
    pctEl.textContent = Math.round(p * 100);
  }
  function finish() { if (!window.gsap) H.classList.add('hero-ok'); carga.classList.add('listo'); B.classList.remove('cargando'); H.classList.add('abierto'); D.dispatchEvent(new Event('edel:abierto')); if (window.lenis) lenis.start(); }

  if (!carga || reduce) { H.classList.add('hero-ok'); if (carga) carga.classList.add('listo'); B.classList.remove('cargando'); H.classList.add('abierto'); if (hv) hv.play().catch(() => {}); }
  else {
    layout(); state = { s: geo.s0, tx: geo.tx, ty: geo.ty }; apply(); draw(0);
    addEventListener('resize', () => { if (!H.classList.contains('abierto') && !opening) { layout(); state = { s: geo.s0, tx: geo.tx, ty: geo.ty }; apply(); } });
    // % real: fuentes (20), póster de portada (15), primeros 3 s del video de portada (65)
    let fonts = 0, poster = 0;
    Promise.allSettled([D.fonts.load('400 40px Anton'), D.fonts.load('500 18px Montserrat'), D.fonts.load('600 16px Oswald')]).then(() => fonts = 1);
    setTimeout(() => fonts = 1, 2500);
    const pi = new Image(); pi.onload = pi.onerror = () => poster = 1; pi.src = hv ? hv.getAttribute('poster') : '';
    const vidP = () => { if (!hv) return 1; try { if (hv.readyState >= 4) return 1; const b = hv.buffered; if (!b.length) return 0; return clamp(b.end(b.length - 1) / Math.min(3, hv.duration || 3)); } catch (e) { return 0; } };
    const real = () => 0.2 * fonts + 0.15 * poster + 0.65 * vidP();
    const t0 = performance.now(); let shown = 0, force = null, done = false, opening = false;
    const tick = () => {
      if (done) return; const el = performance.now() - t0;
      if (force === null && el >= 8000) force = { t: performance.now(), from: shown };
      if (force) shown = force.from + (1 - force.from) * clamp((performance.now() - force.t) / 350);
      else { const target = Math.min(real(), el / 3000); shown += (target - shown) * 0.18; if (target >= 0.999 && shown > 0.985) shown = 1; }
      draw(shown);
      if (shown >= 1 && el >= 3000) { done = true; clearInterval(iv); open(); }
    };
    const iv = setInterval(tick, 40); setTimeout(tick, 8000); setTimeout(tick, 8400);
    setTimeout(() => { if (!H.classList.contains('abierto')) { done = true; clearInterval(iv); finish(); } }, 13000); // red de seguridad

    function open() {
      opening = true;
      const W = geo.W, Hh = geo.H, s1 = Math.hypot(W / 2, Hh / 2) / 40 * 1.3;
      if (hv) { try { hv.currentTime = 0; } catch (e) {} }
      const go = () => { H.classList.add('abierto'); if (hv) hv.play().catch(() => {}); };
      if (window.gsap) {
        const tl = gsap.timeline({ onComplete: finish });
        tl.to([pal, '.pct'], { opacity: 0, duration: 0.35, ease: 'power2.out' })
          .to([isoA, isoN], { strokeOpacity: 0, duration: 0.3 }, 0)
          .add(() => { hueco.setAttribute('r', '168.5'); go(); }, 0.22)
          .to(state, { tx: W / 2, ty: Hh / 2, duration: 0.7, ease: 'power3.out', onUpdate: apply }, 0.3)
          .to(state, { s: s1, duration: 1.0, ease: 'power3.in', onUpdate: apply }, 0.3)
          .to(isoN, { opacity: 0, duration: 0.3, ease: 'power1.in' }, 0.7)
          .to(isoA, { opacity: 0, duration: 0.35, ease: 'power1.in' }, 0.9);
      } else { hueco.setAttribute('r', '168.5'); go(); setTimeout(finish, 300); }
    }
  }

  /* ---------- con GSAP: Lenis, barrido de tinta, contadores ---------- */
  function motion() {
    if (!window.gsap || reduce) return;
    gsap.registerPlugin(ScrollTrigger);
    if (window.Lenis) {
      window.lenis = new Lenis({ lerp: 0.1 });
      lenis.on('scroll', ScrollTrigger.update); gsap.ticker.add(t => lenis.raf(t * 1000)); gsap.ticker.lagSmoothing(0);
      if (B.classList.contains('cargando')) lenis.stop();
      $$('a[href^="#"]').forEach(a => a.addEventListener('click', ev => { const id = a.getAttribute('href'); if (id.length > 1 && $(id)) { ev.preventDefault(); lenis.scrollTo(id, { offset: -64 }); } }));
    }
    // portada
    const heroIn = () => {
      H.classList.add('hero-ok');
      const tl = gsap.timeline();
      tl.from('.s-portada .banda', { xPercent: -110, duration: 0.8, ease: EASE })
        .from('.h1 .ln>span', { yPercent: 108, clipPath: 'inset(0 100% 0 0)', duration: 0.9, stagger: 0.08, ease: EASE }, 0.1)
        .from('.hero-b .btn', { y: 24, opacity: 0, duration: 0.6, stagger: 0.06, ease: EASE }, 0.45)
        .from('.nav', { opacity: 0, duration: 0.6 }, 0.2);
    };
    if (H.classList.contains('abierto')) heroIn(); else D.addEventListener('edel:abierto', heroIn, { once: true });
    // títulos h2: barrido de tinta línea a línea
    $$('main section:not(.s-portada) .h2').forEach(h => {
      gsap.from($$('.ln>span', h), { yPercent: 100, clipPath: 'inset(0 100% 0 0)', duration: 0.9, stagger: 0.08, ease: EASE, scrollTrigger: { trigger: h, start: 'top 85%', once: true } });
    });
    $$('.banda').forEach(b => { if (b.closest('.s-portada')) return; gsap.from(b, { xPercent: -30, opacity: 0, duration: 0.7, ease: EASE, scrollTrigger: { trigger: b, start: 'top 90%', once: true } }); });
    // contadores
    $$('[data-cuenta]').forEach(b => {
      const end = parseFloat(b.dataset.cuenta), dec = end % 1 ? 1 : 0, txt = b.textContent, o = { v: 0 };
      gsap.to(o, { v: end, duration: 1.6, ease: 'power3.out', scrollTrigger: { trigger: b, start: 'top 90%', once: true },
        onUpdate: () => { b.textContent = txt.replace(/[\d.,]+/, o.v.toFixed(dec).replace('.', ',')); }, onComplete: () => b.textContent = txt });
    });
    // tarjetas de servicio y stickers
  }
  if (D.readyState === 'complete') motion(); else addEventListener('load', motion);

  /* ---------- nav sólida ---------- */
  const nav = $('#nav'); const onScroll = () => nav.classList.toggle('solido', scrollY > innerHeight * 0.6);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* ---------- proceso: paso activo según el tiempo del video ---------- */
  const pv = $('.proc-video'), pasos = $('.pasos');
  if (pv && pasos) {
    const p2 = +pasos.dataset.p2, p3 = +pasos.dataset.p3, li = $$('li', pasos);
    pv.addEventListener('timeupdate', () => { const t = pv.currentTime, k = t >= p3 ? 2 : t >= p2 ? 1 : 0; li.forEach((x, i) => x.classList.toggle('on', i === k)); });
  }

  /* ---------- Team Mate / Team Café ---------- */
  $$('.team-b button').forEach(b => b.addEventListener('click', () => { $$('.team-b button').forEach(x => x.setAttribute('aria-pressed', String(x === b))); }));

  /* ---------- reseñas: avanzan solas y se arrastran ---------- */
  const pista = $('.res-pista');
  if (pista) {
    let last = 0; const touch = () => last = performance.now();
    ['pointerdown', 'wheel', 'touchstart', 'focusin'].forEach(ev => pista.addEventListener(ev, touch, { passive: true }));
    const step = dir => { const c = pista.firstElementChild; const w = c.getBoundingClientRect().width + 18; let x = pista.scrollLeft + dir * w; if (x > pista.scrollWidth - pista.clientWidth + 4) x = 0; if (x < -4) x = pista.scrollWidth; pista.scrollTo({ left: x, behavior: reduce ? 'auto' : 'smooth' }); };
    $('.res-b .prev').addEventListener('click', () => { touch(); step(-1); }); $('.res-b .next').addEventListener('click', () => { touch(); step(1); });
    if (!reduce) setInterval(() => { if (performance.now() - last > 8000 && !D.hidden) step(1); }, 5000);
    let drag = null; pista.addEventListener('pointerdown', e => { if (e.pointerType !== 'mouse') return; drag = { x: e.clientX, s: pista.scrollLeft }; pista.setPointerCapture(e.pointerId); });
    pista.addEventListener('pointermove', e => { if (drag) pista.scrollLeft = drag.s - (e.clientX - drag.x); });
    pista.addEventListener('pointerup', () => drag = null);
  }

  /* ===================== nv2 · fases 10–15 ===================== */
  /* troquel: la línea de corte se dibuja al entrar la tarjeta */
  const servs = $$('.serv');
  if ('IntersectionObserver' in window && !reduce) {
    const tio = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { en.target.classList.add('cortado'); tio.unobserve(en.target); } }), { threshold: 0.22 });
    servs.forEach(c => tio.observe(c));
  } else servs.forEach(c => c.classList.add('cortado'));

  /* tornasol: el brillo sigue al puntero o la inclinación del celular */
  $$('.serv-torna').forEach(c => {
    const set = (x, y) => { c.style.setProperty('--tx', (x * 100).toFixed(1) + '%'); c.style.setProperty('--ty', (y * 100).toFixed(1) + '%'); };
    c.addEventListener('pointermove', e => { const r = c.getBoundingClientRect(); set((e.clientX - r.left) / r.width, (e.clientY - r.top) / r.height); });
    if (!reduce) addEventListener('deviceorientation', e => { if (e.gamma == null) return; set(clamp((e.gamma + 45) / 90), clamp((e.beta - 20) / 70)); }, { passive: true });
  });

  /* trabajos: pila de stickers que se despegan */
  const pila = $('.pila'), pui = $('.pila-ui');
  if (pila && pui) {
    pila.classList.add('pila-js'); pui.hidden = false;
    let order = $$('.sticker', pila); const N = order.length, rots = order.map((_, i) => [-3, 2.4, -1.2, 3.2, -2.2][i % 5]);
    const idx = $('.pila-i'); let shownN = 1, busy = false;
    const layout = () => order.forEach((c, i) => {
      c.style.zIndex = N - i; c.style.transition = 'transform .5s cubic-bezier(.16,1,.3,1), opacity .3s';
      c.style.transform = i < 4 ? `translateY(${i * 10}px) rotate(${rots[(i + shownN) % 5]}deg) scale(${1 - i * 0.035})` : 'translateY(30px) scale(.88)';
      c.style.opacity = i < 4 ? 1 : 0; c.style.setProperty('--peel', '0px');
      c.setAttribute('aria-hidden', i ? 'true' : 'false');
    });
    layout();
    const fly = dir => {
      if (busy) return; busy = true; const c = order[0];
      c.style.transition = 'transform .45s cubic-bezier(.5,0,.75,0), opacity .45s';
      c.style.transform = `translate(${dir * 120}vw, -40px) rotate(${dir * 28}deg)`; c.style.opacity = 0;
      setTimeout(() => { order.push(order.shift()); shownN = shownN % N + 1; idx.textContent = shownN; c.style.transition = 'none'; layout(); busy = false; }, reduce ? 0 : 460);
    };
    $('.pila-next').addEventListener('click', () => fly(1));
    let drag = null;
    pila.addEventListener('pointerdown', e => { const c = order[0]; if (busy || !c.contains(e.target)) return; drag = { x: e.clientX, y: e.clientY, t: performance.now(), c }; c.setPointerCapture(e.pointerId); c.style.transition = 'none'; });
    pila.addEventListener('pointermove', e => { if (!drag) return; const dx = e.clientX - drag.x, dy = (e.clientY - drag.y) * 0.4; drag.dx = dx;
      drag.c.style.transform = `translate(${dx}px, ${dy}px) rotate(${rots[shownN % 5] + dx * 0.06}deg)`; drag.c.style.setProperty('--peel', Math.min(80, Math.abs(dx) * 0.45) + 'px'); });
    const up = () => { if (!drag) return; const dx = drag.dx || 0, v = Math.abs(dx) / (performance.now() - drag.t); const c = drag.c; drag = null;
      if (Math.abs(dx) > 90 || (v > 0.6 && Math.abs(dx) > 30)) fly(Math.sign(dx)); else { c.style.transition = 'transform .5s cubic-bezier(.16,1,.3,1)'; layout(); } };
    pila.addEventListener('pointerup', up); pila.addEventListener('pointercancel', up);
  }

  /* equipo: tarjetas que giran (solo por aria-pressed) */
  $$('.flip').forEach(b => b.addEventListener('click', () => b.setAttribute('aria-pressed', String(b.getAttribute('aria-pressed') !== 'true'))));

  /* Team Mate / Team Café: estallido */
  const burst = $('.burst');
  $$('.team-b button').forEach(b => b.addEventListener('click', () => {
    if (reduce || !burst || !burst.animate) return;
    const r = b.getBoundingClientRect(), R = burst.getBoundingClientRect(), x0 = r.left + r.width / 2 - R.left, y0 = r.top - R.top;
    const em = b.dataset.team === 'mate' ? '🧉' : '☕';
    for (let i = 0; i < 14; i++) {
      const s = D.createElement('span'); s.textContent = em; s.style.left = x0 + 'px'; s.style.top = y0 + 'px'; burst.appendChild(s);
      const a = -Math.PI / 2 + (Math.random() - 0.5) * 1.9, d = 90 + Math.random() * 150;
      s.animate([{ transform: 'translate(-50%,0) scale(.4)', opacity: 1 }, { transform: `translate(calc(-50% + ${Math.cos(a) * d}px), ${Math.sin(a) * d}px) rotate(${(Math.random() - .5) * 120}deg) scale(1.1)`, opacity: 1, offset: 0.7 }, { transform: `translate(calc(-50% + ${Math.cos(a) * d * 1.1}px), ${Math.sin(a) * d + 60}px) scale(.9)`, opacity: 0 }],
        { duration: 1100 + Math.random() * 400, easing: 'cubic-bezier(.16,1,.3,1)' }).onfinish = () => s.remove();
    }
  }));

  /* cotiza: botón magnético (solo con mouse) */
  if (matchMedia('(pointer:fine)').matches && !reduce) $$('.mag').forEach(m => {
    m.addEventListener('pointermove', e => { const r = m.getBoundingClientRect(); m.style.transform = `translate(${(e.clientX - r.left - r.width / 2) * 0.22}px, ${(e.clientY - r.top - r.height / 2) * 0.3}px)`; });
    m.addEventListener('pointerleave', () => m.style.transform = '');
  });

  /* ===================== nv3 · fases 16–17 ===================== */
  /* menú del celular: diálogo modal, foco atrapado, resto inert */
  const menu = $('#menu'), mb = $('.menu-b');
  if (menu && mb) {
    const outside = [$('#nav'), $('main'), $('.pie')].filter(Boolean);
    const focusables = () => $$('a[href],button', menu);
    let last = null;
    const open = () => {
      last = D.activeElement; if (window.gsap) gsap.killTweensOf(menu);
      menu.hidden = false; mb.setAttribute('aria-expanded', 'true'); B.classList.add('menu-abierto'); outside.forEach(el => el.inert = true);
      if (window.lenis) lenis.stop();
      if (window.gsap && !reduce) { gsap.fromTo(menu, { clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0% 0)', duration: 0.6, ease: EASE }); gsap.fromTo($$('nav a', menu), { yPercent: 60, opacity: 0 }, { yPercent: 0, opacity: 1, duration: 0.6, stagger: 0.04, ease: EASE, delay: 0.1 }); }
      $('.menu-x', menu).focus();
    };
    const close = (go) => {
      if (window.gsap) gsap.killTweensOf([menu, ...$$('nav a', menu)]);
      const done = () => { menu.hidden = true; menu.style.clipPath = ''; mb.setAttribute('aria-expanded', 'false'); B.classList.remove('menu-abierto'); outside.forEach(el => el.inert = false); if (window.lenis) lenis.start();
        if (go && $(go)) { window.lenis ? lenis.scrollTo(go, { offset: -64, immediate: reduce }) : $(go).scrollIntoView(); } else if (last) last.focus(); };
      if (window.gsap && !reduce) gsap.to(menu, { clipPath: 'inset(0 0 100% 0)', duration: 0.45, ease: 'power3.in', onComplete: done }); else done();
    };
    mb.addEventListener('click', open);
    $('.menu-x', menu).addEventListener('click', () => close());
    $$('nav a', menu).forEach(a => a.addEventListener('click', ev => { ev.preventDefault(); ev.stopImmediatePropagation(); close(a.getAttribute('href')); }, true));
    menu.addEventListener('keydown', e => {
      if (e.key === 'Escape') { e.preventDefault(); close(); return; }
      if (e.key !== 'Tab') return; const f = focusables(), a = f[0], z = f[f.length - 1];
      if (e.shiftKey && D.activeElement === a) { e.preventDefault(); z.focus(); } else if (!e.shiftKey && D.activeElement === z) { e.preventDefault(); a.focus(); }
    });
    addEventListener('resize', () => { if (!menu.hidden && innerWidth >= 1000) close(); });
  }

  /* la nav no se puede enfocar mientras carga */
  const navEl = $('#nav'); if (navEl && B.classList.contains('cargando')) { navEl.inert = true; D.addEventListener('edel:abierto', () => navEl.inert = false, { once: true }); setTimeout(() => navEl.inert = false, 13500); }

  /* al girar el celular se conserva la sección que se estaba viendo */
  let anchor = null;
  const remember = () => { const secs = $$('main > section'); anchor = secs.find(s => s.getBoundingClientRect().bottom > innerHeight * 0.3) || null; };
  addEventListener('scroll', () => { clearTimeout(remember.t); remember.t = setTimeout(remember, 150); }, { passive: true });
  addEventListener('orientationchange', () => { const a = anchor; setTimeout(() => { if (a) { const y = a.getBoundingClientRect().top + scrollY; window.lenis ? lenis.scrollTo(y, { immediate: true }) : scrollTo(0, y); } if (window.ScrollTrigger) ScrollTrigger.refresh(); }, 350); });
})();
