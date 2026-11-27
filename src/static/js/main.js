// Yoga con Arjuna — interacciones ligeras (sin dependencias)
(function () {
  // Menú móvil
  var t = document.querySelector('.menu-toggle'), n = document.querySelector('.nav');
  if (t && n) t.addEventListener('click', function () {
    var o = n.classList.toggle('open');
    t.setAttribute('aria-expanded', o ? 'true' : 'false');
    document.body.style.overflow = o ? 'hidden' : '';
  });

  // Slider de la portada
  var slides = document.querySelectorAll('.home-hero .slide');
  if (slides.length > 1) {
    var dots = document.querySelector('.dots'), i = 0, timer;
    slides.forEach(function (_, k) {
      var b = document.createElement('button');
      b.setAttribute('aria-label', 'Imagen ' + (k + 1));
      b.addEventListener('click', function () { go(k); restart(); });
      dots.appendChild(b);
    });
    function go(k) {
      slides[i].classList.remove('on'); dots.children[i].classList.remove('on');
      i = k; slides[i].classList.add('on'); dots.children[i].classList.add('on');
    }
    function restart() { clearInterval(timer); timer = setInterval(function () { go((i + 1) % slides.length); }, 6000); }
    dots.children[0].classList.add('on'); restart();
  }

  // Aparición suave al hacer scroll
  var els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: .12 });
    els.forEach(function (e) { io.observe(e); });
  } else els.forEach(function (e) { e.classList.add('in'); });

  // Botón volver arriba
  var up = document.querySelector('.to-top');
  if (up) {
    window.addEventListener('scroll', function () { up.classList.toggle('show', window.scrollY > 600); }, { passive: true });
    up.addEventListener('click', function () { window.scrollTo({ top: 0 }); });
  }

  // Vídeos de YouTube: solo se cargan al hacer clic (más rápido y sin cookies de terceros)
  document.querySelectorAll('.video[data-yt], .video[data-yt-list]').forEach(function (v) {
    v.addEventListener('click', function () {
      if (v.querySelector('iframe')) return;
      var f = document.createElement('iframe');
      f.src = v.dataset.ytList
        ? 'https://www.youtube-nocookie.com/embed/videoseries?list=' + v.dataset.ytList + '&autoplay=1&rel=0'
        : 'https://www.youtube-nocookie.com/embed/' + v.dataset.yt + '?autoplay=1&rel=0';
      f.allow = 'autoplay; encrypted-media; picture-in-picture'; f.allowFullscreen = true;
      f.title = v.dataset.title || 'Vídeo';
      v.innerHTML = ''; v.appendChild(f);
    });
  });

  // Testimonios de Instagram: se cargan cuando la sección entra en pantalla
  var tw = document.querySelector('[data-instagram]');
  if (tw) {
    var load = function () {
      if (window.instgrm) { window.instgrm.Embeds.process(); return; }
      var s = document.createElement('script'); s.async = true; s.src = 'https://www.instagram.com/embed.js';
      document.body.appendChild(s);
    };
    if ('IntersectionObserver' in window) {
      var io2 = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { load(); io2.disconnect(); } }, { rootMargin: '400px' });
      io2.observe(tw);
    } else load();
  }

  // Filtros del blog (Todo / Vídeos / Artículos)
  var fb = document.querySelectorAll('.blog .filters button');
  fb.forEach(function (b) {
    b.addEventListener('click', function () {
      fb.forEach(function (x) { x.classList.toggle('on', x === b); });
      document.querySelectorAll('.post').forEach(function (p) {
        p.classList.toggle('hide', b.dataset.f !== 'all' && p.dataset.type !== b.dataset.f);
      });
    });
  });

  // Testimonios en vídeo: solo suena uno a la vez
  var tv = document.querySelectorAll('.testimonials video');
  tv.forEach(function (v) { v.addEventListener('play', function () { tv.forEach(function (o) { if (o !== v) o.pause(); }); }); });

  // Test «¿Qué guerrero eres?»
  var qz = document.querySelector('[data-quiz]'), qd = document.getElementById('quiz-data');
  if (qz && qd) {
    var D = JSON.parse(qd.textContent), ans = [], cur = 0;
    var run = qz.querySelector('.q-run'), intro = qz.querySelector('.q-intro'), out = qz.querySelector('.q-result');
    var esc = function (t) { var d = document.createElement('div'); d.textContent = t; return d.innerHTML; };
    var show = function () {
      var q = D.q[cur];
      run.querySelector('.q-bar span').style.width = (cur / D.q.length * 100) + '%';
      run.querySelector('.q-step').textContent = 'Pregunta ' + (cur + 1) + ' de ' + D.q.length;
      run.querySelector('.q-title').textContent = q.t;
      var box = document.createElement('div'); box.className = 'q-opts'; run.replaceChild(box, run.querySelector('.q-opts'));
      if (document.activeElement) document.activeElement.blur();
      q.a.forEach(function (o, k) {
        var b = document.createElement('button'); b.type = 'button'; b.textContent = o.l;
        if (ans[cur] === k) b.className = 'sel';
        b.addEventListener('click', function () {
          ans[cur] = k; b.className = 'sel';
          setTimeout(function () { cur++; cur < D.q.length ? show() : result(); }, 220);
        });
        box.appendChild(b);
      });
      run.querySelector('.q-back').disabled = cur === 0;
    };
    var result = function () {
      var sc = {}, K = {};
      D.q.forEach(function (q, i) { var o = q.a[ans[i]]; (o.s || []).forEach(function (n) { sc[n] = (sc[n] || 0) + 1; }); if (o.g) K[o.g] = o.k; });
      var best = 1; for (var n = 1; n <= 9; n++) if ((sc[n] || 0) > (sc[best] || 0)) best = n; // empate: la etapa más temprana del camino
      var st = D.stages[best - 1];
      var porModo = function () { return K.modo === 'casa' ? (K.nivel === 'vira' ? 'manual' : 'curso') : K.modo; };
      var main, alt;
      if (K.obj === 'profesion' || K.pres === 'alto' || K.nivel === 'profe') {
        if (K.pres === 'bajo') { main = 'intro'; alt = 'formacion'; } else { main = 'formacion'; alt = 'intro'; }
      } else if (K.pres === 'bajo') {
        main = K.nivel === 'nuevo' ? 'libro' : (K.nivel === 'vira' ? 'manual' : 'curso');
        alt = porModo(); if (alt === main) alt = main === 'curso' ? 'libro' : 'curso';
      } else {
        main = porModo();
        alt = K.nivel === 'nuevo' ? 'libro' : (main === 'curso' ? 'manual' : 'curso');
      }
      var card = function (id, cls) {
        var r = D.res[id];
        return '<div class="rec ' + cls + '"><div class="img" style="background-image:url(/img/' + r.img + ')' + (id === 'libro' ? ';background-size:contain;background-color:#ebe7e4' : '') + '"></div><div class="body">' +
          '<div class="tag">' + (cls ? 'También te puede interesar' : 'Te recomendamos') + '</div><h4>' + esc(r.title) + '</h4>' +
          '<p>' + esc(r.why.replace('{n}', st.n).replace('{name}', st.name)) + '</p>' +
          '<a class="' + (cls ? '' : 'btn') + '" href="' + r.url + '">' + (cls ? 'Saber más →' : 'Ver recomendación') + '</a></div></div>';
      };
      var share = 'He hecho el test del guerrero de Yoga con Arjuna: mi etapa es ' + st.name + ' (' + st.sk + '). ¿Y la tuya? ' + location.origin + '/test-guerrero/';
      out.innerHTML = '<div class="badge">' + st.n + '</div><p class="kicker">Tu etapa: sesión ' + st.n + ' de 9</p>' +
        '<h3>El guerrero ' + st.de + ' ' + esc(st.name) + '</h3><p class="sk">«' + esc(st.sk) + '»</p><p class="txt">' + esc(st.txt) + '</p>' +
        card(main, '') + card(alt, 'alt') +
        '<div class="q-actions"><a class="btn ghost" target="_blank" rel="noopener" href="https://wa.me/?text=' + encodeURIComponent(share) + '">Compartir por WhatsApp</a>' +
        '<a class="btn' + (K.pres === 'hablar' ? '' : ' ghost') + '" target="_blank" rel="noopener" href="https://wa.me/' + D.wa + '?text=' + encodeURIComponent('Hola Arjuna, he hecho el test y mi etapa es ' + st.name + '. Me gustaría más información.') + '">Hablar con Arjuna</a>' +
        '<button class="btn ghost" type="button" data-again>Repetir el test</button></div>';
      run.hidden = true; out.hidden = false;
      var f = document.querySelector('.q-form'); if (f) { f.hidden = false; f.elements.resultado.value = st.n + ' · ' + st.name + ' · recomendación: ' + D.res[main].title + ' · busca: ' + K.obj + ' · nivel: ' + K.nivel + ' · modo: ' + K.modo + ' · inversión: ' + K.pres; }
      document.querySelectorAll('.steps li').forEach(function (li) { li.classList.toggle('me', +li.dataset.stage === st.n); });
      out.querySelector('[data-again]').addEventListener('click', function () { ans = []; cur = 0; out.hidden = true; if (f) f.hidden = true; run.hidden = false; show(); });
      qz.scrollIntoView({ behavior: 'smooth', block: 'start' });
    };
    qz.querySelector('[data-start]').addEventListener('click', function () { intro.hidden = true; run.hidden = false; show(); qz.scrollIntoView({ behavior: 'smooth', block: 'start' }); });
    run.querySelector('.q-back').addEventListener('click', function () { if (cur > 0) { cur--; show(); } });
  }

  // Agenda: lee la hoja de Google publicada como CSV. Si no hay eventos válidos, se queda la lista fija.
  var evBox = document.querySelector('.events[data-sheet]');
  if (evBox && window.fetch) {
    var MES = ['ene','feb','mar','abr','may','jun','jul','ago','sep','oct','nov','dic'];
    var parseCSV = function (txt) {
      var rows = [], row = [], f = '', q = false;
      for (var i = 0; i < txt.length; i++) {
        var c = txt[i];
        if (q) { if (c === '"') { if (txt[i+1] === '"') { f += '"'; i++; } else q = false; } else f += c; }
        else if (c === '"') q = true;
        else if (c === ',') { row.push(f); f = ''; }
        else if (c === '\n' || c === '\r') { if (c === '\r' && txt[i+1] === '\n') i++; row.push(f); rows.push(row); row = []; f = ''; }
        else f += c;
      }
      if (f !== '' || row.length) { row.push(f); rows.push(row); }
      return rows;
    };
    var toDate = function (v) {
      v = (v || '').trim(); var m;
      if ((m = v.match(/^(\d{4})-(\d{1,2})-(\d{1,2})/))) return new Date(+m[1], m[2]-1, +m[3]);
      if ((m = v.match(/^(\d{1,2})[\/.\-](\d{1,2})[\/.\-](\d{2,4})/))) { var y = +m[3]; if (y < 100) y += 2000; return new Date(y, m[2]-1, +m[1]); }
      return null;
    };
    var safeUrl = function (u) { u = (u || '').trim(); return /^(https?:|mailto:)/i.test(u) ? u : ''; };
    var el = function (tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text) e.textContent = text; return e; };
    fetch(evBox.getAttribute('data-sheet'), { cache: 'no-store' }).then(function (r) { return r.ok ? r.text() : ''; }).then(function (txt) {
      var rows = parseCSV(txt || ''); if (rows.length < 2) return;
      var today = new Date(); today.setHours(0,0,0,0);
      var evs = rows.slice(1).map(function (r) {
        return { ini: toDate(r[0]), fi: toDate(r[1]), t1: (r[0]||'').trim(), t2: (r[1]||'').trim(), act: (r[2]||'').trim(), lloc: (r[3]||'').trim(), desc: (r[4]||'').trim(), preu: (r[5]||'').trim(), foto: safeUrl(r[6]), link: safeUrl(r[7]) };
      }).filter(function (e) {
        if (!e.act || /^(EXEMPLE|EJEMPLO)/i.test(e.act)) return false;
        if (!e.ini) return !!e.t1;            // fecha escrita como texto («Por concretar», «Primavera 2027»…)
        return (e.fi || e.ini) >= today;
      }).sort(function (a, b) { return (a.ini ? 0 : 1) - (b.ini ? 0 : 1) || (a.ini && b.ini ? a.ini - b.ini : 0); });
      if (!evs.length) return;
      evBox.innerHTML = '';
      evs.forEach(function (e) {
        var row = el('div', 'event');
        var d = el('div', 'date');
        var top, sub;
        if (e.ini) {
          top = e.ini.getDate() + ' ' + MES[e.ini.getMonth()];
          if (e.fi && e.fi > e.ini) top = (e.fi.getMonth() === e.ini.getMonth() ? e.ini.getDate() : top) + '–' + e.fi.getDate() + ' ' + MES[e.fi.getMonth()];
          sub = String(e.ini.getFullYear());
        } else { top = e.t1; sub = e.fi ? '' : e.t2; }
        d.appendChild(document.createTextNode(top));
        if (sub) { d.appendChild(document.createElement('br')); var sm = el('small', '', sub); sm.style.fontSize = '.6em'; d.appendChild(sm); }
        var mid = el('div', e.foto ? 'ev-body has-img' : 'ev-body');
        if (e.foto) { var im = el('img', 'ev-img'); im.src = e.foto; im.alt = e.act; im.loading = 'lazy'; mid.appendChild(im); }
        if (e.preu) mid.appendChild(el('span', 'badge', e.preu));
        mid.appendChild(el('h3', '', e.act));
        if (e.lloc) mid.appendChild(el('p', 'ev-place', e.lloc));
        if (e.desc) mid.appendChild(el('p', '', e.desc));
        var a = el('a', 'btn', e.link ? 'Reservar' : 'Más info');
        a.href = e.link || '/contacta/'; if (e.link && !/^mailto:/i.test(e.link)) { a.target = '_blank'; a.rel = 'noopener'; }
        row.appendChild(d); row.appendChild(mid); row.appendChild(a); evBox.appendChild(row);
      });
    }).catch(function () {});
  }

  // Año del footer
  var y = document.querySelector('[data-year]'); if (y) y.textContent = new Date().getFullYear();

  // Formulario de contacto: «/contacta/?asunto=Viaje a India» deja elegido el asunto
  var sel = document.querySelector('#c-asunto'), q = new URLSearchParams(location.search).get('asunto');
  if (sel && q) {
    for (var k = 0; k < sel.options.length; k++) if (sel.options[k].text.indexOf(q) === 0) { sel.selectedIndex = k; break; }
  }

  // Música de fondo («Jai Ganesha»). Intenta sonar sola al entrar; si el navegador no lo deja
  // (casi siempre, hasta que la persona interactúa), arranca con el primer clic, toque o tecla.
  // Si la persona la pausa, no vuelve a sonar sola durante la visita. Sigue entre páginas desde el mismo punto.
  var sw = document.querySelector('[data-song]');
  if (sw) {
    var sb = sw.querySelector('.song-btn'), au = null, KEY = 'yca-song';
    var toggles = document.querySelectorAll('[data-song-toggle]');
    var saved = {};
    try { saved = JSON.parse(sessionStorage.getItem(KEY)) || {}; } catch (e) {}
    var stopped = !!saved.stopped;   // solo cuenta como «parada» si la persona la pausó con el botón
    function save(p) { try { sessionStorage.setItem(KEY, JSON.stringify({ playing: p, t: au ? au.currentTime : (saved.t || 0), stopped: stopped })); } catch (e) {} }
    function ui(p) {
      sw.classList.toggle('on', p); sw.classList.remove('resume');
      sb.setAttribute('aria-pressed', p ? 'true' : 'false');
      toggles.forEach(function (b) { b.classList.toggle('on', p); b.setAttribute('aria-pressed', p ? 'true' : 'false'); });
    }
    function audio() {
      if (!au) {
        au = new Audio(sw.dataset.src); au.loop = true; au.volume = .5; au.preload = 'auto';
        au.addEventListener('loadedmetadata', function () { if (saved.t) au.currentTime = saved.t; }, { once: true });
        au.addEventListener('play', function () { ui(true); save(true); });
        au.addEventListener('pause', function () { ui(false); });
      }
      return au;
    }
    var GESTURES = ['pointerdown', 'mousedown', 'touchend', 'click', 'keydown'];
    function unwait() { GESTURES.forEach(function (ev) { document.removeEventListener(ev, onGesture, true); }); }
    function onGesture(e) {
      // Si el gesto es sobre el propio botón, ya lo gestiona toggle()
      if (e.target.closest && (e.target.closest('.song-btn') || e.target.closest('[data-song-toggle]'))) { unwait(); return; }
      var a = audio();
      if (!a.paused) { unwait(); return; }
      // Solo dejamos de escuchar cuando de verdad ha empezado a sonar
      a.play().then(unwait).catch(function () {});
    }
    function toggle() {
      unwait(); var a = audio();
      if (a.paused) { stopped = false; a.play().catch(function () {}); }
      else { stopped = true; a.pause(); save(false); }
    }
    sb.addEventListener('click', toggle);
    toggles.forEach(function (b) { b.addEventListener('click', toggle); });
    if (!stopped) {
      audio().play().catch(function () {
        sw.classList.add('resume');
        GESTURES.forEach(function (ev) { document.addEventListener(ev, onGesture, true); });
      });
    }
    window.addEventListener('pagehide', function () { if (au) save(!au.paused); });
  }
})();
