#!/usr/bin/env python3
"""Genera la web estática de Yoga con Arjuna en ../site
Uso: python3 build.py
Para cambiar enlaces de pago, edita PRODUCTS más abajo (campo 'stripe').
"""
import os, shutil, json, html, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'site')
DOMAIN = 'https://www.yogaconarjuna.com'
EMAIL = 'yogaconarjun@gmail.com'
WHATSAPP = '34619945481'
# Hoja de Google «Agenda web Yoga con Arjuna», publicada como CSV. La página de Agenda la lee al abrirse.
AGENDA_CSV = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRJKZHLZOl0yl4BaAz60Z0iUoo-PVH51euGlek8JwOeIxybudLqLMJQXEU8hMu9oIWf-VeLFlbEOc-s/pub?gid=984860236&single=true&output=csv'

# Menú acordado en la reunión del 21/11/2026: Home, Sobre mí (con las 3 ramas), Formación Virayoga,
# Agenda y actividades (juntas), Biblioteca (antes «Blog»), Prensa, Productos y Contacta.
# «Mi libro» y «Viajes a India» siguen existiendo como páginas y se enlazan desde Sobre mí y la Home.
NAV = [
    ('Home', '/'),
    ('Sobre mí', '/sobre-mi-creador-de-virayoga/'),
    ('Formación Virayoga', '/virayoga/'),
    ('Agenda y actividades', '/agenda/'),
    ('Biblioteca', '/blog/'),
    ('Prensa', '/prensa/'),
    ('Productos', '/productos/'),
    ('Contacta', '/contacta/'),
]
# Páginas que no están en el menú pero se marcan como parte de una sección
NAV_PARENT = {'/mi-libro/': '/sobre-mi-creador-de-virayoga/', '/viajes-india/': '/agenda/', '/servicios-de-virayoga/': '/agenda/'}

# Canción de fondo (Bhakti). El reproductor nunca arranca solo: la persona pulsa «play».
SONG = dict(src='/audio/jai-ganesha.mp3', title='Jai Ganesha', artist='Arjuna')
# Enlaces de la música de Arjuna (pendiente de que los envíe: dejar '' hasta tenerlos)
SPOTIFY = ''
YT_MUSIC = 'https://www.youtube.com/channel/UC9uWznLGx7_VeVcMQdMZblA'   # canal de YouTube de Bhakti

def _ver(rel):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', rel), 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()[:8]
CSS_V, JS_V = _ver('css/style.css'), _ver('js/main.js')

ICON = {
 'fb': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.2H7.8v3h2.6V21h3.1z"/></svg>',
 'ig': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 7.3A4.7 4.7 0 1 0 12 16.7 4.7 4.7 0 0 0 12 7.3zm0 7.7a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm6-7.9a1.1 1.1 0 1 1-2.2 0 1.1 1.1 0 0 1 2.2 0zM21.9 8.2c-.1-1.5-.4-2.8-1.5-3.9S18 2.9 16.5 2.8C15 2.7 9 2.7 7.5 2.8 6 2.9 4.7 3.2 3.6 4.3S2.2 6.7 2.1 8.2C2 9.7 2 14.3 2.1 15.8c.1 1.5.4 2.8 1.5 3.9s2.4 1.4 3.9 1.5c1.5.1 7.5.1 9 0 1.5-.1 2.8-.4 3.9-1.5s1.4-2.4 1.5-3.9c.1-1.5.1-6.1 0-7.6zM19.9 17.6a3 3 0 0 1-1.7 1.7c-1.2.5-4 .4-5.2.4s-4.1.1-5.2-.4a3 3 0 0 1-1.7-1.7c-.5-1.2-.4-4-.4-5.3s-.1-4.1.4-5.3a3 3 0 0 1 1.7-1.7c1.2-.5 4-.4 5.2-.4s4.1-.1 5.2.4a3 3 0 0 1 1.7 1.7c.5 1.2.4 4 .4 5.3s.1 4.1-.4 5.3z"/></svg>',
 'tt': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.6 2h-3.3v13.2a2.9 2.9 0 1 1-2.9-2.9c.3 0 .6 0 .9.1V9a6.3 6.3 0 1 0 5.3 6.2V8.6a8 8 0 0 0 4.7 1.5V6.8a4.7 4.7 0 0 1-4.7-4.8z"/></svg>',
 'music': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v10.6A4 4 0 1 0 14 17V7h4V3h-6z"/></svg>',
 'pause': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg>',
 'spotify': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm4.6 14.4a.6.6 0 0 1-.9.2c-2.4-1.5-5.4-1.8-8.9-1a.6.6 0 1 1-.3-1.2c3.9-.9 7.2-.5 9.9 1.1.3.2.4.6.2.9zm1.2-2.7a.8.8 0 0 1-1.1.3c-2.7-1.7-6.9-2.2-10.1-1.2a.8.8 0 1 1-.5-1.5c3.7-1.1 8.3-.6 11.4 1.3.4.2.5.7.3 1.1zm.1-2.8C14.7 9 9.4 8.8 6.3 9.7a1 1 0 1 1-.6-1.8c3.5-1.1 9.4-.9 13.1 1.3a1 1 0 0 1-.9 1.7z"/></svg>',
 'yt': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12 31 31 0 0 0 1 16.8a3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1c.4-1.6.5-4.8.5-4.8s0-3.2-.5-4.8zM9.7 15V9l5.8 3-5.8 3z"/></svg>',
 'play': '<svg viewBox="0 0 24 24" width="30" height="30" aria-hidden="true"><path fill="#fff" d="M8 5v14l11-7z"/></svg>',
 'mail': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4-8 5-8-5V6l8 5 8-5v2z"/></svg>',
 'wa': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.8 14.2c-.2.7-1.4 1.3-1.9 1.4-.5.1-1.1.1-1.8-.1-.4-.1-1-.3-1.7-.6-3-1.3-5-4.3-5.1-4.5-.2-.2-1.2-1.6-1.2-3s.8-2.1 1-2.4c.3-.3.6-.4.8-.4h.6c.2 0 .4 0 .6.5l.9 2.1c.1.2.1.4 0 .5l-.3.5-.4.5c-.1.1-.3.3-.1.6.2.3.8 1.3 1.6 2.1 1.1 1 2.1 1.3 2.4 1.4.3.2.5.1.6-.1l.9-1.1c.2-.3.4-.2.7-.1l2 1c.3.1.5.2.5.3.1.1.1.7-.1 1.3z"/></svg>',
 'pin': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg>',
 'lock': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M18 8h-1V6a5 5 0 0 0-10 0v2H6a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V10a2 2 0 0 0-2-2zM9 6a3 3 0 0 1 6 0v2H9V6zm3 11a2 2 0 1 1 0-4 2 2 0 0 1 0 4z"/></svg>',
 'card': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 14H4v-6h16v6zm0-10H4V6h16v2z"/></svg>',
 'heart': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21.4 10.6 20C5.4 15.4 2 12.3 2 8.5 2 5.4 4.4 3 7.5 3c1.7 0 3.4.8 4.5 2.1C13.1 3.8 14.8 3 16.5 3 19.6 3 22 5.4 22 8.5c0 3.8-3.4 6.9-8.6 11.5L12 21.4z"/></svg>',
}

SOCIAL = [('https://www.facebook.com/arjunayogastudio', 'Facebook', 'fb'),
          ('https://www.instagram.com/yogaconarjuna/', 'Instagram', 'ig'),
          ('https://www.tiktok.com/@yogaconarjuna', 'TikTok', 'tt'),
          ('https://www.youtube.com/@yogaconarjuna', 'YouTube', 'yt')]

# Testimonios en vídeo: lista de YouTube «Testimonios Virayoga» (vídeos cortos verticales).
# (id de YouTube, nombre, tipo, frase corta). Tipos: 'formacion' (profes formadas), 'vida' (lo que les ha cambiado),
# 'taller' (talleres, clases y eventos). Para añadir uno nuevo, sube el vídeo a la lista y añade aquí una línea.
TESTIMONIOS = [
    ('vCTJyjKA4UU', 'Montse', 'formacion', 'Profesora de Virayoga, súper feliz de haberse formado.'),
    ('4wH96GqEznA', 'Elena', 'formacion', '«La recomiendo un montón, tanto si es tu primera formación como si ya has hecho otras.»'),
    ('2z3X9ca_QSw', 'Caterine', 'formacion', '«Me ha aportado algo diferente: seguridad en mí misma.»'),
    ('4icnmu1MR-o', 'Gema', 'formacion', '«Virayoga me ha enfocado a despertar mi poder interior, mi seguridad, mi confianza.»'),
    ('-UmMe4KWMbc', 'Astrid', 'vida', 'Llegó hundida y hoy enseña Virayoga: su historia.'),
    ('TX3XsXXL66I', 'Alumna de Virayoga', 'vida', '«Me ha dado herramientas para ser más fuerte y afrontar la vida.»'),
    ('x0fsqrGqNis', 'Profesora de yoga', 'vida', '«Después de la quimioterapia, me ha ayudado a sentirme más fuerte.»'),
    ('FZ3Z8ljJ4Yw', 'Laya', 'vida', 'Todo lo que le aporta Virayoga.'),
    ('ykG72D7uJRA', 'Alumna de taller', 'taller', '«Ha sido todo un regalo. Superrecomendable.»'),
    ('DKPZAiohsL8', 'Alumna del taller «Libérate»', 'taller', '«Me ha sorprendido ese trasfondo tan profundo de crecimiento personal.»'),
    ('TRIcS73HJA8', 'Alumno de taller', 'taller', '«Mi primer contacto con el yoga: he conectado conmigo mismo.»'),
    ('2ZPxGgELdgU', 'Alumno de taller', 'taller', '«Me voy muy contento y lleno de este taller.»'),
    ('SBTLdEzidsc', 'Alumna de taller', 'taller', '«Vine con miedos… y no solo pude, me ha llegado al alma.»'),
    ('QAmn2FAw9Jc', 'Alumna de las clases', 'taller', '«Una práctica que me da energía, muy dinámica y divertida.»'),
]
TESTIMONIOS_LIST = 'https://www.youtube.com/playlist?list=PLKHs8bw52nGk'

def social_html():
    return '<div class="social">' + ''.join(
        f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}">{ICON[i]}</a>' for u, n, i in SOCIAL) + '</div>'

def newsletter(form_name='newsletter'):
    return f'''
<section class="newsletter">
  <div class="wrap reveal">
    <h2>¿Quieres estar al día de los próximos eventos?<br>Déjanos tu correo y te informaremos de todo.</h2>
    <form name="{form_name}" method="POST" action="/gracias/" data-netlify="true" netlify-honeypot="bot-field">
      <input type="hidden" name="form-name" value="{form_name}">
      <p class="hidden"><label>No rellenar: <input name="bot-field"></label></p>
      <label class="skip" for="nl-email">Correo electrónico</label>
      <input id="nl-email" type="email" name="email" placeholder="Correo electrónico" required autocomplete="email">
      <label class="check"><input type="checkbox" name="acepto" required> <span>Acepto recibir información de Yoga con Arjuna y la <a href="/politica-de-privacidad/">política de privacidad</a>.</span></label>
      <button class="btn" type="submit">¡Quiero saber más!</button>
    </form>
  </div>
</section>'''

def testimonials_html(title='Lo que dicen de Virayoga', kinds=('vida', 'formacion', 'taller'), ids=None, soft=True,
                      lead='Experiencias reales de personas que practican Virayoga.'):
    if ids:
        items = [t for i in ids for t in TESTIMONIOS if t[0] == i]
    else:
        items = [t for k in kinds for t in TESTIMONIOS if t[2] == k]
    cards = ''.join(f'''
      <figure class="t yt-t reveal">
        <div class="video short" data-yt="{vid}" data-title="Testimonio de {html.escape(name)}" style="background-image:url(https://i.ytimg.com/vi/{vid}/hqdefault.jpg)"><button aria-label="Ver el testimonio de {html.escape(name)}">{ICON['play']}</button></div>
        <figcaption><strong>{html.escape(name)}</strong><span>{html.escape(q)}</span></figcaption>
      </figure>''' for vid, name, _, q in items)
    return f'''
<section class="section{' soft' if soft else ''}" id="testimonios">
  <div class="wrap">
    <div class="center reveal">
      <h2 class="section-title">{title}</h2>
      <p class="lead">{lead}</p>
    </div>
    <div class="testimonials">{cards}
    </div>
    <p class="center" style="margin-top:12px"><a class="btn ghost" href="{TESTIMONIOS_LIST}" target="_blank" rel="noopener">Ver todos en YouTube</a></p>
  </div>
</section>'''

def page(path, title, desc, body, hero=None, hero_title=None, crumb=None, image=None, schema=None):
    canonical = DOMAIN + path
    nav = ''.join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if h == path or NAV_PARENT.get(path) == h else ""}{" class=\"nav-shop\"" if h == "/productos/" else ""}>{n}</a></li>'
        for n, h in NAV)
    hero_html = ''
    if hero:
        hero_html = f'<header class="page-hero" style="background-image:url(/img/{hero})"><h1>{hero_title}</h1></header>'
    crumb_html = ''
    if crumb:
        crumb_html = f'<nav class="breadcrumb narrow" aria-label="Ruta">Estás aquí: <a href="/">Home</a> / {crumb}</nav>'
    og = image or 'hero-1.jpg'
    ld = ''
    if schema:
        ld = '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False) + '</script>'
    doc = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{DOMAIN}/img/{og}">
<meta property="og:locale" content="es_ES">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@1,400;1,500&family=Hind:wght@300;400;500;600&family=Kaushan+Script&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/style.css?v={CSS_V}">
{ld}
</head>
<body>
<a class="skip" href="#main">Saltar al contenido</a>
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="/">Yoga con Arjuna</a>
    <button class="menu-toggle" aria-label="Menú" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
    <nav class="nav" id="menu" aria-label="Principal"><ul>{nav}</ul></nav>
  </div>
</header>
<main id="main">
{hero_html}
{crumb_html}
{body}
</main>
<footer class="site-footer">
  © <span data-year>2026</span> · Yoga con Arjuna<span class="sep">·</span><a href="/aviso-legal/">Aviso legal</a><span class="sep">·</span><a href="/politica-de-privacidad/">Privacidad</a><span class="sep">·</span><a href="/politica-de-cookies/">Cookies</a><span class="sep">·</span><a href="/condiciones-de-compra/">Condiciones de compra</a><span class="sep">·</span><a href="/contacta/">Contacta</a>
</footer>
<div class="song" data-song data-src="{SONG['src']}" data-title="{SONG['title']}">
  <button class="song-btn" type="button" aria-pressed="false" aria-label="Escuchar «{SONG['title']}», de {SONG['artist']}" title="Música: «{SONG['title']}», de {SONG['artist']}">
    <span class="i-play">{ICON['music']}</span><span class="i-pause">{ICON['pause']}</span><span class="txt">Escucha «{SONG['title']}»</span><span class="eq" aria-hidden="true"><i></i><i></i><i></i></span>
  </button>
</div>
<a class="wa-float" href="https://wa.me/{WHATSAPP}?text=Hola%20Arjuna%2C%20quiero%20m%C3%A1s%20informaci%C3%B3n" target="_blank" rel="noopener" aria-label="Escríbeme por WhatsApp">{ICON['wa'].replace('<svg ', '<svg width="28" height="28" ', 1)}<span>¿Hablamos?</span></a>
<button class="to-top" aria-label="Volver arriba"><svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true"><path fill="#fff" d="M12 4l-8 8h5v8h6v-8h5z"/></svg></button>
<script src="/js/main.js?v={JS_V}" defer></script>
</body>
</html>'''
    d = os.path.join(OUT, path.strip('/'))
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(doc)
    return canonical

PERSON = {"@context": "https://schema.org", "@type": "Person", "name": "Alberto López «Arjuna»",
          "alternateName": "Arjuna, el canalla del yoga", "jobTitle": "Profesor y creador de Virayoga",
          "url": DOMAIN + "/", "email": EMAIL,
          "sameAs": [u for u, _, _ in SOCIAL]}

# ---------------------------------------------------------------- HOME
def buy_button(pid, label='Comprar'):
    """Botón de compra de un producto de PRODUCTS (Stripe). Si aún no hay enlace, sale desactivado."""
    p = next(x for x in PRODUCTS if x['id'] == pid)
    if p['stripe']:
        return f'<a class="btn" href="{p["stripe"]}" target="_blank" rel="noopener">{label}</a>'
    return f'<a class="btn" href="/productos/#{pid}">{label}</a>'

# Las tres ramas de Arjuna (acordado en la reunión: sustituyen a «formador adaptable»)
PILLARS = [
    ('virayoga', 'vira-salto.jpg', 'Virayoga', 'El método',
     'Yoga, artes marciales y psicología en un mismo sistema. Te mueves en los 360º de la esterilla y despiertas tu actitud Vira. Y si quieres enseñarlo, te formo.',
     '/virayoga/', 'Conoce la formación'),
    ('viajes', 'india-jaipur.jpg', 'Viajes a India', 'El origen',
     'Una vez al año me llevo a un grupo a la India de verdad: la que no sale en las postales. No es un retiro, es un viaje que te remueve por dentro.',
     '/viajes-india/', 'Quiero viajar'),
    ('bhakti', 'arjuna-templo.jpg', 'Bhakti', 'Música medicina',
     'Mantras, guitarra y voz. El Bhakti es el yoga de la devoción, y para mí es la forma más directa de soltar la cabeza y abrir el corazón.',
     '/sobre-mi-creador-de-virayoga/#bhakti', 'Escúchame'),
]

def pillars_html(title='Mis tres caminos', lead='Todo lo que hago sale de aquí.'):
    cards = ''.join(f'''
      <a class="pillar reveal" href="{href}" id="rama-{k}">
        <div class="img" style="background-image:url(/img/{img})" role="img" aria-label="{html.escape(t)}"></div>
        <div class="body"><span class="kicker">{kick}</span><h3>{t}</h3><p>{d}</p><span class="more">{cta} →</span></div>
      </a>''' for k, img, t, kick, d, href, cta in PILLARS)
    return f'''
<section class="section">
  <div class="wrap">
    <div class="center reveal"><h2 class="section-title">{title}</h2><p class="lead">{lead}</p></div>
    <div class="pillars">{cards}
    </div>
  </div>
</section>'''

def hire_html():
    return '''
<section class="hire">
  <div class="wrap reveal">
    <div>
      <span class="kicker">Escuelas · empresas · hoteles · eventos privados</span>
      <h2>¿Quieres Virayoga en tu escuela o en tu evento? Contrátame.</h2>
      <p>Masterclasses y talleres de Virayoga para escuelas de yoga, sesiones para equipos de empresa, workshops en hoteles y celebraciones privadas, como despedidas de soltera. Tú pones el sitio y las ganas; yo, el resto.</p>
    </div>
    <a class="btn light" href="/servicios-de-virayoga/">Contrátame</a>
  </div>
</section>'''

def home():
    slides = ''.join(f'<div class="slide{" on" if i == 1 else ""}" style="background-image:url(/img/hero-{i}.jpg)"></div>' for i in (1, 5, 2, 6, 3, 4))
    body = f'''
<section class="home-hero" aria-label="Presentación">
  {slides}
  <div class="inner">
    <h1>Arjuna, el canalla del yoga</h1>
    <p>Yoga, artes marciales y psicología para despertar tu fuerza interior. Sin postureo y con los pies en la tierra.</p>
    <div class="hero-btns"><a class="btn" href="/virayoga/">Descubre la formación</a> <a class="btn light" href="/servicios-de-virayoga/">Contrátame</a></div>
  </div>
  <div class="dots"></div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="media reveal"><img src="/img/arjuna-estudio.jpg" alt="Alberto López, Arjuna, creador de Virayoga" width="801" height="1200" loading="lazy" style="max-width:440px;margin:0 auto"></div>
    <div class="reveal">
      <h2 class="section-title"><a href="/sobre-mi-creador-de-virayoga/" style="color:inherit">Hola, soy Arjuna</a></h2>
      <p>Me llaman «el canalla del yoga». Llevo muchos años enseñando, pero no soy el típico yogui: no te voy a hablar de luz cósmica ni a vender milagros.</p>
      <p>El yoga y las artes marciales me cambiaron la vida. De esa mezcla, y de lo que me ha tocado vivir, nació el <strong>Virayoga</strong>. Hoy mi vida gira alrededor de tres cosas: el Virayoga, los viajes a India y la música Bhakti.</p>
      <a class="btn ghost" href="/sobre-mi-creador-de-virayoga/">Conóceme</a>
    </div>
  </div>
</section>

{pillars_html()}

<section class="parallax" style="background-image:url(/img/virayoga-fondo.jpg)">
  <div class="wrap cols">
    <div class="reveal">
      <h2 class="section-title" style="color:#fff">¿Y qué es el Virayoga?</h2>
      <p><strong>Yoga + artes marciales + psicología = Virayoga.</strong> Un sistema de yoga dinámico que une el Hatha Yoga tradicional con movimientos de artes marciales y te hace trabajar todo el cuerpo usando los 360º de la esterilla.</p>
      <p>Ganas fuerza, coordinación y presencia. Y, de paso, algo que no sale en ninguna foto: seguridad en ti. Porque cada sesión parte de una intención clara que te lleva hacia tu <strong>actitud Vira</strong>.</p>
      <p><em>Vira</em> significa «guerrero» en sánscrito y <em>yoga</em>, «unión». No hace falta ser flexible ni venir de las artes marciales: hace falta querer trabajarte.</p>
      <a class="btn light" href="/virayoga/">Descubre el Virayoga</a>
    </div>
    <div class="reveal">
      <div class="video" data-yt="lozwmWKLfSU" data-title="Virayoga con Arjuna" style="background-image:url(https://i.ytimg.com/vi/lozwmWKLfSU/hqdefault.jpg)">
        <button aria-label="Reproducir vídeo">{ICON['play']}</button>
        <div class="cap">Mira una práctica de Virayoga</div>
      </div>
    </div>
  </div>
</section>

<section class="section soft"><div class="wrap">{camino_html()}</div></section>

{hire_html()}

{testimonials_html(ids=['TX3XsXXL66I', '2z3X9ca_QSw', 'ykG72D7uJRA', 'x0fsqrGqNis', '-UmMe4KWMbc', 'SBTLdEzidsc'])}

<section class="section soft">
  <div class="wrap split r">
    <div class="media book reveal"><a href="/mi-libro/"><img src="/img/libro-portada.jpg" alt="Portada del libro Conoce el Virayoga con Arjuna, el canalla del yoga" width="645" height="972" loading="lazy"></a></div>
    <div class="reveal">
      <h2 class="section-title"><a href="/mi-libro/" style="color:inherit">Mi libro, en PDF</a></h2>
      <p><em>Conoce el Virayoga con Arjuna, el canalla del yoga</em> es mi historia: cómo un chaval de la calle encontró en el yoga y las artes marciales su forma de salir adelante, y cómo de ahí nació el Virayoga.</p>
      <p>Descárgalo en PDF y empieza a leerlo hoy.</p>
      {buy_button('libro-pdf', 'Comprar el PDF · 9,95 €')} <a class="btn ghost" href="/mi-libro/">Saber más</a>
    </div>
  </div>
</section>

<section class="section" style="padding:64px 0">
  <div class="wrap center reveal">
    <h2 class="section-title">Sígueme en</h2>
    {social_html()}
  </div>
</section>
{newsletter()}'''
    site = {"@context": "https://schema.org", "@type": "WebSite", "name": "Yoga con Arjuna", "url": DOMAIN + "/"}
    page('/', 'Yoga con Arjuna · Virayoga, viajes a India y Bhakti con el canalla del yoga',
         'Arjuna, el canalla del yoga: creador del Virayoga (yoga, artes marciales y psicología), viajes a India y música Bhakti. Formación, masterclasses y eventos.',
         body, image='hero-1.jpg', schema=[site, PERSON])

# ---------------------------------------------------------------- SOBRE MÍ
def song_block():
    links = ''
    if SPOTIFY:
        links += f'<a class="btn ghost" href="{SPOTIFY}" target="_blank" rel="noopener">Escúchame en Spotify</a> '
    if YT_MUSIC:
        links += f'<a class="btn ghost" href="{YT_MUSIC}" target="_blank" rel="noopener">Canal de Bhakti en YouTube</a>'
    return f'''
  <div class="song-card reveal">
    <button class="song-big" type="button" data-song-toggle aria-label="Escuchar «{SONG['title']}»">{ICON['music']}</button>
    <div><span class="kicker">Escucha</span><h3>«{SONG['title']}»</h3><p>Un canto a Ganesha, el que aparta los obstáculos del camino. Dale al play y sigue navegando: la música te acompaña.</p>{('<p>' + links + '</p>') if links else ''}</div>
  </div>'''

def sobre():
    body = f'''
<article class="narrow content">
  <h2 class="quote-title">Hola, soy Arjuna,</h2>
  <p><strong>Alberto López en el DNI. Creador de Virayoga, viajero de India y músico de Bhakti.</strong></p>
  <p>Durante años caminé por dos caminos que parecían no tocarse: el Hatha Yoga, en la línea de Nil Hahoutoff, y las artes marciales. Hasta que un día, en un taxi, con una libreta y un bolígrafo, empecé a unirlos. Así nació el Virayoga, el 15 de noviembre de 2015.</p>
  <p>Soy una persona sencilla. Me gusta la gente de verdad, el humor y las cosas pequeñas del día a día. Por eso no me vas a ver de gurú: lo que te enseño lo he vivido antes en mi propio cuerpo.</p>
</article>

{pillars_html('Mis tres caminos', 'Lo que soy cabe en tres palabras: Virayoga, India y Bhakti.')}

<article class="narrow content">
  <h2 id="virayoga">Virayoga</h2>
  <p>Es mi método y mi forma de entender el yoga: Hatha Yoga, artes marciales y psicología aplicada en un mismo sistema de 9 sesiones. Ya hay 25 profesoras formadas y una comunidad que no para de crecer.</p>
  <p><a class="btn" href="/virayoga/">Conoce la formación</a></p>

  <h2 id="viajes">Viajes a India</h2>
  <p>Llevo más de 15 años viajando con grupos a India. Allí me impresionó la capacidad de servicio de su gente y descubrí que yo también la llevaba dentro: así empecé con el Karma Yoga. Cada año vuelvo para enseñarte la India profunda, la del origen del yoga.</p>
  <div class="gallery reveal"><img src="/img/india-jaipur.jpg" alt="Arjuna en Jaipur, India" loading="lazy"><img src="/img/india-arcos.jpg" alt="Postura de Virayoga en un palacio de India" loading="lazy"><img src="/img/arjuna-templo.jpg" alt="Arjuna meditando frente a un templo" loading="lazy"></div>
  <p><a class="btn" href="/viajes-india/">Ver el viaje a India</a></p>

  <h2 id="bhakti">Bhakti, música medicina</h2>
  <p>El Bhakti es el yoga de la devoción: cantar mantras hasta que la cabeza se calla y el corazón toma el mando. Lo vivo con la guitarra y la voz, en conciertos, en clase y en cada viaje. Si te apetece tenerlo en tu evento, también puedes <a href="/servicios-de-virayoga/">contratarme</a>.</p>
  {song_block()}

  <h2 id="libro">Mi libro</h2>
  <div class="mini-book reveal">
    <a href="/mi-libro/"><img src="/img/libro-portada.jpg" alt="Portada del libro Conoce el Virayoga" width="160" loading="lazy"></a>
    <div><p><em>Conoce el Virayoga con Arjuna, el canalla del yoga</em>: mi historia y la del método, contada sin filtros. Ahora en PDF.</p>{buy_button('libro-pdf', 'Comprar el PDF · 9,95 €')} <a class="btn ghost" href="/mi-libro/">Saber más</a></div>
  </div>

  <h3>Currículum</h3>
  <ul>
    <li>Certificado oficial de profesionalidad como Instructor de yoga.</li>
    <li>Profesor de yoga acreditado y habilitado por el Consell Català de l’Esport.</li>
    <li>Profesor de Hatha Yoga formado en la línea Nil Hahoutoff.</li>
    <li>Instructor de Defensa Personal (Totsival), Cinturón Negro 3er Dan.</li>
    <li>Instructor de Hapkido Jin Jung Kwan, Cinturón Negro 1er Dan.</li>
    <li>Maestrías de Reiki (Usui Tibetano, Karuna Gautama, Seichem-Sekhem).</li>
    <li>Formación en Ayurveda.</li>
    <li>Formación en Tantra tradicional hinduista en la línea de Osho y Mantak Chia.</li>
    <li>Organizador del Barcelona Yoga Day.</li>
    <li>Creador y formador de Virayoga.</li>
    <li>Autor del libro «Conoce el Virayoga con Arjuna, el canalla del yoga».</li>
  </ul>
  <p style="margin-top:2em"><a class="btn" href="/contacta/">Escríbeme</a></p>
</article>
{testimonials_html('Lo que Virayoga les ha cambiado', kinds=('vida',), lead='Personas que encontraron en la práctica algo más que ejercicio.')}
{newsletter()}'''
    page('/sobre-mi-creador-de-virayoga/', 'Sobre mí · Hola, soy Arjuna · Virayoga, viajes a India y Bhakti',
         'Soy Arjuna, el canalla del yoga: creador de Virayoga, viajero de India y músico de Bhakti. Te cuento quién soy y por qué hago lo que hago.',
         body, hero='cab-sobre-mi.jpg', hero_title='Sobre mí', crumb='Sobre mí', image='arjuna-estudio.jpg', schema=PERSON)

# ---------------------------------------------------------------- MI LIBRO
def libro():
    body = f'''
<div class="wrap content">
  <div class="layout-sidebar">
    <article>
      <h2 class="quote-title" style="margin-top:0">«Conoce el Virayoga con Arjuna,<br>el canalla del yoga»</h2>
      <p>Es un libro de superación. Te cuento cómo cambié mi vida gracias al yoga y las artes marciales, y cómo todo lo aprendido me llevó a crear el Virayoga.</p>
      <p>Es la historia de alguien normal y corriente que lucha por tener una vida mejor. Anécdotas, tropiezos y situaciones complicadas que me enseñaron que vale la pena vivir el día a día con pasión y con fuerza.</p>
      <p>Y es también tu puerta de entrada al Virayoga: el método que une yoga, artes marciales y psicología para que conectes con tu fuerza interior y la uses en tu vida, dentro y fuera de la esterilla.</p>
      <p>Es la historia de cómo cambié mi vida. Lo que hagas tú con ella ya es cosa tuya.</p>
      <div class="buy-box reveal">
        <h3>Llévatelo en PDF</h3>
        <p class="price-big">9,95 €</p>
        <p>Pago seguro y descarga inmediata. Lo lees en el móvil, en la tablet o en el ordenador.</p>
        {buy_button('libro-pdf', 'Comprar el PDF')}
      </div>
    </article>
    <aside class="sidebar">
      <div class="card"><img src="/img/libro-portada.jpg" alt="Portada del libro Conoce el Virayoga" width="645" height="972" loading="lazy"></div>
      <div class="card">
        <h3>¿Quieres enterarte de los próximos eventos? Déjanos tu correo y te informaremos de todo.</h3>
        <form name="newsletter-sidebar" method="POST" action="/gracias/" data-netlify="true" netlify-honeypot="bot-field">
          <input type="hidden" name="form-name" value="newsletter-sidebar">
          <p class="hidden"><label>No rellenar: <input name="bot-field"></label></p>
          <input type="email" name="email" placeholder="Correo electrónico" required aria-label="Correo electrónico">
          <label class="check"><input type="checkbox" name="acepto" required> <span>Acepto la <a href="/politica-de-privacidad/">política de privacidad</a>.</span></label>
          <button class="btn" type="submit" style="width:100%">¡Quiero saber más!</button>
        </form>
      </div>
    </aside>
  </div>
</div>
{newsletter()}'''
    book = {"@context": "https://schema.org", "@type": "Book", "name": "Conoce el Virayoga con Arjuna, el canalla del yoga",
            "author": {"@type": "Person", "name": "Alberto López «Arjuna»"}, "bookFormat": "https://schema.org/EBook",
            "inLanguage": "es", "image": DOMAIN + "/img/libro-portada.jpg",
            "offers": {"@type": "Offer", "price": "9.95", "priceCurrency": "EUR", "url": DOMAIN + "/mi-libro/"}}
    page('/mi-libro/', 'Mi libro en PDF · Conoce el Virayoga con Arjuna, el canalla del yoga',
         'Un libro de superación: cómo cambié mi vida gracias al yoga y las artes marciales y cómo nació el Virayoga. Cómpralo en PDF por 9,95 €.',
         body, hero='cab-libro.jpg', hero_title='Mi libro', crumb='<a href="/sobre-mi-creador-de-virayoga/">Sobre mí</a> / Mi libro', image='libro-portada.jpg', schema=book)

# ---------------------------------------------------------------- FORMACIÓN VIRAYOGA
# Una única formación (formulario de inicio, nov. 2026): las 9 sesiones son la estructura del método, no un curso aparte.
def virayoga():
    body = f'''
<article class="narrow content">
  <h2 class="quote-title">Formación de Virayoga</h2>
  <p class="lead">¿Qué pasaría si, en lugar de obsesionarte con tus debilidades, entrenaras tus fortalezas?</p>
  <p>El Virayoga es un sistema de yoga que une el <strong>Hatha Yoga</strong> tradicional, las <strong>artes marciales</strong> y la <strong>psicología aplicada</strong>. Trabajas todo el cuerpo en los 360º de la esterilla y, mientras tanto, la mente no tiene tiempo de irse a otra parte: estás presente sí o sí.</p>
  <p>La formación es una sola y completa: la <strong>formación total de Virayoga</strong>. Te da una base técnica y psicológica sólida para dominar tu práctica, crear tus propias clases y llevar la actitud Vira a tu día a día.</p>
  <div class="gallery reveal"><img src="/img/vira-salto.jpg" alt="Patada marcial de Virayoga junto al mar" loading="lazy"><img src="/img/vira-equilibrio.jpg" alt="Postura de equilibrio de Virayoga" loading="lazy"><img src="/img/india-arcos.jpg" alt="Postura de Virayoga en un palacio de India" loading="lazy"></div>

  <h2>¿Para quién es?</h2>
  <div class="profiles">
    <div class="profile reveal"><h4>Si ya das clases de yoga</h4><p>Sientes que repites siempre lo mismo y que a tus clases les falta fondo. Aquí encuentras un método con personalidad propia y herramientas reales para acompañar a tu alumnado.</p></div>
    <div class="profile reveal"><h4>Si quieres tu propia práctica</h4><p>Practicas yoga o artes marciales y quieres entender el porqué de cada movimiento. Te llevas un sistema completo, ordenado y fácil de seguir en tu día a día.</p></div>
    <div class="profile reveal"><h4>Si empiezas de cero</h4><p>Nunca has hecho yoga, o casi, pero quieres trabajarte: ganar fuerza física y mental, ordenar tus ideas y confiar más en ti. No necesitas ser flexible; necesitas ganas.</p></div>
  </div>
  <p><strong>No es para ti</strong> si buscas un yoga solo relajante, si para ti el yoga es únicamente hacer posturas o si quieres coleccionar un título rápido sin implicarte. Aquí hay trabajo, y del bueno.</p>

  <h2>Las 9 sesiones</h2>
  <p>El método se ordena en 9 sesiones. Cada una trabaja una cualidad psicológica con su <em>sankalpa</em> (intención) y su tipo de técnicas marciales: <strong>Proyección, Respeto, Fuerza, Anticipación, Resiliencia, Virtudes, Respuesta, Liberación y Fluir</strong>.</p>
</article>
<div class="wrap">{camino_html('Las 9 sesiones del Virayoga', 'Cada sesión es una etapa del camino del guerrero, con su sankalpa.')}</div>
<article class="narrow content">
  <h2>Lo que te llevas</h2>
  <ul>
    <li><strong>Una estructura técnica muy clara.</strong> Cada sesión sigue un orden pensado (llaves, preparación vertebral, cardio, encadenamientos, fuerza, equilibrio, torsiones, invertidas…). Combinando sus partes tienes un abanico enorme de clases diferentes.</li>
    <li><strong>Criterio propio.</strong> Como has vivido todo el recorrido en tu cuerpo, sabes adaptar las secuencias a cada persona y crear las tuyas sin perder la esencia.</li>
    <li><strong>Herramientas para acompañar.</strong> La parte psicológica de las 9 sesiones te ayuda a guiar clases que van hacia dentro y a sostener a tu alumnado de forma natural.</li>
    <li><strong>Un cambio que se nota fuera de la esterilla.</strong> Más claridad, más seguridad y una actitud distinta ante lo que te pasa. Sin promesas mágicas: el método te da las herramientas y el resultado depende de tu práctica.</li>
  </ul>
  <h2>Cómo es</h2>
  <p>Formación online, por bloques y a tu ritmo, con autoevaluaciones y acompañamiento cercano de Arjuna y del equipo de Virayoga. Nos adaptamos a ti y a tu momento: mirar hacia dentro a veces remueve, y aquí tienes una mano amiga.</p>
  <div class="buy-box reveal">
    <h3>¿Damos el paso?</h3>
    <p>Escríbeme y te cuento fechas, precio y cómo empezar. Sin presiones: primero resolvemos tus dudas.</p>
    <p><a class="btn" href="/contacta/?asunto=Formación%20Virayoga">¡Quiero formarme!</a> &nbsp; <a class="btn ghost" href="/test-guerrero/">Haz el test: ¿qué guerrero eres?</a></p>
  </div>
  <h2 class="quote-title center">«Las asanas y el crecimiento personal encienden el fuego de la actitud Vira»<br><small style="font-size:.6em">Arjuna</small></h2>
</article>
{testimonials_html('Testimonios de la formación', kinds=('formacion',), lead='Profesoras formadas en Virayoga cuentan qué les ha aportado.')}
{testimonials_html('Y lo que dicen quienes practican', kinds=('vida',), soft=False, lead='Virayoga dentro y fuera de la esterilla.')}
{hire_html()}
{newsletter()}'''
    course = {"@context": "https://schema.org", "@type": "Course", "name": "Formación de Virayoga",
              "description": "Formación total de Virayoga: Hatha Yoga, artes marciales y psicología aplicada en 9 sesiones. Online, con acompañamiento cercano.",
              "provider": {"@type": "Person", "name": "Alberto López «Arjuna»", "url": DOMAIN + "/"}, "inLanguage": "es"}
    page('/virayoga/', 'Formación de Virayoga · Yoga, artes marciales y psicología · Yoga con Arjuna',
         'La formación total de Virayoga: Hatha Yoga, artes marciales y psicología en 9 sesiones. Para profes de yoga, practicantes y quien empieza de cero.',
         body, hero='cab-virayoga.jpg', hero_title='Virayoga', crumb='Formación Virayoga', image='vira-salto.jpg', schema=course)

# ---------------------------------------------------------------- CONTRÁTAME (antes «Actividades»; misma dirección)
def actividades():
    services = [
        ('studio-1.jpg', 'Escuelas de yoga', 'Masterclasses y talleres de Virayoga para tu escuela: tu alumnado prueba algo que no ha visto nunca y tú le das un empujón a tu centro.'),
        ('vira-equilibrio.jpg', 'Empresas', 'Sesiones para equipos que necesitan moverse, soltar tensión y ganar foco. Cuerpo y cabeza en la misma sala, por fin.'),
        ('arjuna-mar.jpg', 'Hoteles y eventos', 'Workshops de yoga y Virayoga para hoteles, encuentros y eventos en Barcelona y alrededores. También con música Bhakti en directo.'),
        ('ag-street.jpg', 'Celebraciones privadas', 'Despedidas de soltera, cumpleaños o un plan distinto con amigos: una clase de yoga con artes marciales que se recuerda (y se ríe).'),
    ]
    cards = ''.join(f'<div class="ag-card reveal"><div class="img" style="background-image:url(/img/{i})" role="img" aria-label="{html.escape(t)}"></div><div class="body"><h3>{t}</h3><p>{d}</p></div></div>' for i, t, d in services)
    body = f'''
<article class="narrow content">
  <p class="lead">¿Quieres que lleve el Virayoga a tu escuela, a tu empresa, a tu hotel o a tu celebración? Cuéntame qué tienes en mente y lo preparamos a medida.</p>
</article>
<div class="wrap content ag-cats" style="padding-top:0">
  <h2 class="cat">Contrata a Arjuna</h2>
  <div class="ag-cards">{cards}</div>

  <h2 class="cat">Masterclasses y talleres</h2>
  <div class="narrow" style="padding:0">
    <ul>
      <li><strong>Masterclass de Virayoga:</strong> yoga y artes marciales en los 360º de la esterilla. Para todos los niveles.</li>
      <li><strong>Taller de transiciones marciales:</strong> «Esquiva la bala», «La zarpa del tigre» y otros movimientos con nombre propio.</li>
      <li><strong>Taller de actitud Vira:</strong> la psicología de las 9 sesiones aplicada a la práctica y al día a día.</li>
      <li><strong>Bhakti en directo:</strong> mantras, guitarra y voz para cerrar la práctica o para tu evento.</li>
    </ul>
    <p>¿Te interesa algo distinto? Pregúntame: casi todo se puede adaptar.</p>
  </div>
</div>

<div class="wrap content" style="padding-top:0">
  <div class="contact-grid">
    <div class="contact-info reveal">
      <h2 class="quote-title" style="margin-top:0">Cuéntame tu idea</h2>
      <p>Dime qué tipo de evento es, dónde y cuántas personas seréis. Te contesto con una propuesta.</p>
      <div class="row">{ICON['wa']}<a href="https://wa.me/{WHATSAPP}?text=Hola%20Arjuna%2C%20quiero%20contratarte%20para%20un%20evento" target="_blank" rel="noopener">Escríbeme por WhatsApp</a></div>
      <div class="row">{ICON['mail']}<a href="mailto:{EMAIL}">{EMAIL}</a></div>
    </div>
    <form class="reveal" name="contratacion" method="POST" action="/gracias/" data-netlify="true" netlify-honeypot="bot-field">
      <input type="hidden" name="form-name" value="contratacion">
      <p class="hidden"><label>No rellenar: <input name="bot-field"></label></p>
      <label for="h-nombre">Nombre</label><input id="h-nombre" type="text" name="nombre" required autocomplete="name">
      <label for="h-email">Correo electrónico</label><input id="h-email" type="email" name="email" required autocomplete="email">
      <label for="h-tipo">Tipo de evento</label>
      <select id="h-tipo" name="tipo"><option>Escuela de yoga (masterclass o taller)</option><option>Empresa</option><option>Hotel o evento</option><option>Despedida o celebración privada</option><option>Bhakti / música en directo</option><option>Otro</option></select>
      <label for="h-mensaje">Fecha, lugar y número de personas</label><textarea id="h-mensaje" name="mensaje" required></textarea>
      <label class="check"><input type="checkbox" name="acepto" required> <span>He leído y acepto la <a href="/politica-de-privacidad/">política de privacidad</a>.</span></label>
      <button class="btn" type="submit">Enviar</button>
    </form>
  </div>
</div>
{testimonials_html('Ya han traído el Virayoga', ids=['x0fsqrGqNis', 'DKPZAiohsL8', 'ykG72D7uJRA', '2ZPxGgELdgU'], lead='Una profesora que contrató a Arjuna para su plataforma de clases y personas que vivieron sus talleres.')}'''
    svc = {"@context": "https://schema.org", "@type": "Service", "name": "Masterclasses, talleres y clases de Virayoga para escuelas, empresas, hoteles y eventos privados",
           "provider": {"@type": "Person", "name": "Alberto López «Arjuna»", "url": DOMAIN + "/"}, "areaServed": "Barcelona, España",
           "serviceType": "Yoga para eventos"}
    page('/servicios-de-virayoga/', 'Contrata a Arjuna · Yoga para escuelas, empresas, hoteles y despedidas en Barcelona',
         'Masterclasses y talleres de Virayoga para escuelas de yoga, yoga para empresas, workshops en hoteles y clases para despedidas de soltera y eventos privados en Barcelona.',
         body, hero='cab-actividades.jpg', hero_title='Contrátame', crumb='<a href="/agenda/">Agenda y actividades</a> / Contrátame', image='cab-actividades.jpg', schema=svc)

# ---------------------------------------------------------------- VIAJES A INDIA (nueva)
def viajes_india():
    faq = [
        ('¿Es un retiro de yoga?', 'No. Un retiro suele ser varias clases al día en un mismo sitio. Esto es un viaje: recorremos India, conocemos su gente y su cultura, y practicamos cuando el viaje lo pide.'),
        ('¿Cuánto dura?', 'Unos 15 días. Las fechas exactas del próximo viaje salen en la agenda.'),
        ('¿Cómo reservo mi plaza?', 'Escríbeme y te envío el programa, el precio y lo que incluye. Para asegurar la plaza se paga una señal.'),
        ('Tengo más dudas', 'Normal. Escríbeme por WhatsApp o por el formulario y lo hablamos.'),
    ]
    faq_html = ''.join(f'<details class="faq-item"><summary>{q}</summary><p>{a}</p></details>' for q, a in faq)
    body = f'''
<article class="narrow content">
  <h2 class="quote-title">Viaje al origen del yoga</h2>
  <p class="lead">Una vez al año me llevo a un grupo a India. No a la de las postales, sino a la India profunda: la que te remueve por dentro y te cambia la forma de mirar.</p>
  <p>Llevo más de 15 años guiando grupos por este país. Visitamos lo imprescindible, pero sobre todo vamos donde está la vida de verdad: su gente, sus templos, su comida y esa capacidad de darlo todo que te deja sin palabras.</p>
  <p>Yo voy a tu lado para cuidarte y enseñarte lo que he aprendido allí. Lo demás lo hace India.</p>
  <div class="gallery reveal"><img src="/img/india-jaipur.jpg" alt="Arjuna en Jaipur" loading="lazy"><img src="/img/india-arcos-2.jpg" alt="Virayoga en un palacio de India" loading="lazy"><img src="/img/india-arcos-3.jpg" alt="Postura marcial en India" loading="lazy"><img src="/img/india-jaipur-2.jpg" alt="Grupo de viaje en Jaipur" loading="lazy"><img src="/img/arjuna-templo.jpg" alt="Arjuna frente a un templo" loading="lazy"><img src="/img/india-arcos.jpg" alt="Arcos de un palacio en India" loading="lazy"></div>
  <div class="buy-box reveal">
    <h3>Próximo viaje</h3>
    <p>Fechas por concretar. Consulta la <a href="/agenda/">agenda</a> o escríbeme y te aviso en cuanto estén.</p>
    <p><a class="btn" href="/contacta/?asunto=Viaje%20a%20India">Quiero información</a> &nbsp; <a class="btn ghost" href="https://wa.me/{WHATSAPP}?text=Hola%20Arjuna%2C%20quiero%20informaci%C3%B3n%20del%20viaje%20a%20India" target="_blank" rel="noopener">WhatsApp</a></p>
  </div>
  <h2>Preguntas frecuentes</h2>
  <div class="faq">{faq_html}</div>
</article>
{newsletter()}'''
    trip = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    page('/viajes-india/', 'Viaje a India con Arjuna · Viaje al origen del yoga',
         'Viaja a la India profunda con Arjuna: unos 15 días con más de 15 años de experiencia guiando grupos. No es un retiro, es un viaje que te cambia por dentro.',
         body, hero='india-arcos-2.jpg', hero_title='Viajes a India', crumb='<a href="/agenda/">Agenda y actividades</a> / Viajes a India', image='india-jaipur.jpg', schema=trip)

# ---------------------------------------------------------------- AGENDA Y ACTIVIDADES
def agenda():
    def card(img, title, html_body):
        return f'<div class="ag-card reveal"><div class="img" style="background-image:url(/img/{img})" role="img" aria-label="{html.escape(title)}"></div><div class="body"><h3>{title}</h3>{html_body}</div></div>'
    mail = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
    body = f'''
<div class="wrap content ag-cats">
  <h2 class="cat">Próximos eventos</h2>
  <div class="events" data-sheet="{html.escape(AGENDA_CSV)}">
    <div class="event reveal">
      <div class="date">12 dic<br><small style="font-size:.6em">2026 · 11 h</small><span class="badge price">Gratuito</span></div>
      <div><h3>Street Virayoga en Plaça Reial (Barcelona)</h3><p>Práctica de Virayoga al aire libre. ¡Solo trae tu esterilla!</p></div>
      <a class="btn" href="mailto:{EMAIL}?subject=Street%20Virayoga%2012%20diciembre">Apuntarme</a>
    </div>
    <div class="event reveal">
      <div class="date">19-20 feb<br><small style="font-size:.6em">2027</small></div>
      <div><h3>Taller de Virayoga en Murcia</h3><p>Dos días de Virayoga para conocer el método en persona.</p></div>
      <a class="btn ghost" href="/contacta/">Más info</a>
    </div>
    <div class="event reveal">
      <div class="date">Fechas<br><small style="font-size:.6em">a concretar</small></div>
      <div><h3>Viaje a India</h3><p>¡Volvemos a India! El viaje al origen del yoga, con más de 15 años de experiencia guiando grupos.</p></div>
      <a class="btn" href="/viajes-india/">Más info</a>
    </div>
    <div class="event reveal">
      <div class="date">2027<br><small style="font-size:.6em">próximamente</small></div>
      <div><h3>Tenerife Virayoga</h3><p>Volvemos como cada año a Tenerife, a nuestra escuela oficial MiYoga, con clases, talleres y concierto.</p></div>
      <a class="btn ghost" href="/contacta/">Avísame</a>
    </div>
  </div>

  <h2 class="cat">Eventos</h2>
  <div class="ag-cards">
    {card('ag-street.jpg', 'Street Virayoga', '<p>Práctica de Virayoga gratuita en la Plaça Reial de Barcelona, el primer sábado de cada mes. Al aire libre, con gente de todas partes y buen rollo. ¡Solo trae tu esterilla!</p>')}
    {card('ag-tenerife.jpg', 'Talleres y masterclasses', '<p>Talleres por toda España (Tenerife, Murcia…) y masterclasses en escuelas. Mira las fechas arriba o lleva el Virayoga a tu centro.</p><p><a class="btn ghost" href="/servicios-de-virayoga/">Contrátame</a></p>')}
  </div>

  <h2 class="cat">Formación y viajes</h2>
  <div class="ag-cards">
    {card('vira-salto.jpg', 'Formación de Virayoga', '<p>La formación total de Virayoga: yoga, artes marciales y psicología en 9 sesiones, online y con acompañamiento cercano.</p><p><a class="btn" href="/virayoga/">Conoce la formación</a></p>')}
    {card('india-jaipur-2.jpg', 'Viajes a India', '<p>Una vez al año, unos 15 días por la India profunda. No es un retiro: es un viaje que te cambia la forma de mirar.</p><p><a class="btn" href="/viajes-india/">Ver el viaje</a></p>')}
  </div>

  <h2 class="cat">Clases</h2>
  <div class="ag-cards">
    {card('ag-online.jpg', 'Virayoga online', f'<p>Clases por Zoom con la autenticidad de siempre. Se quedan grabadas por si no te va bien la hora. Escríbeme a {mail}.</p>')}
    {card('studio-2.jpg', 'Espai Kairos', '<p><strong>Los jueves en Terrassa a las 18:45 h</strong>: iniciación al Vinyasa con Arjuna.</p>')}
    {card('studio-1.jpg', 'Clases regulares', '<p><strong>Virayoga los miércoles a las 19 h</strong> en Martorelles.</p><p>¿Quieres venir o prefieres una clase privada? Escríbeme y lo hablamos.</p><p><a class="btn" href="/contacta/?asunto=Clases">Contáctame</a></p>')}
  </div>
</div>
{testimonials_html('Así se viven los talleres y las clases', kinds=('taller',), lead='Lo que cuentan al terminar un taller, un evento o una clase de Virayoga.')}
{hire_html()}
{newsletter()}'''
    ev = {"@context": "https://schema.org", "@type": "Event", "name": "Street Virayoga en Plaça Reial",
          "startDate": "2026-12-12T11:00:00+01:00", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
          "eventStatus": "https://schema.org/EventScheduled", "isAccessibleForFree": True,
          "location": {"@type": "Place", "name": "Plaça Reial", "address": "Plaça Reial, Barcelona"},
          "organizer": {"@type": "Person", "name": "Arjuna", "url": DOMAIN + "/"}, "image": DOMAIN + "/img/ag-street.jpg"}
    page('/agenda/', 'Agenda y actividades · Formación, viajes a India, talleres y Street Virayoga · Yoga con Arjuna',
         'Próximos eventos de Arjuna: talleres y masterclasses de Virayoga, Street Virayoga en Barcelona, viajes a India, formación y clases online y en Martorelles.',
         body, hero='cab-agenda.jpg', hero_title='Agenda y actividades', crumb='Agenda y actividades', image='ag-street.jpg', schema=ev)

# ---------------------------------------------------------------- PRENSA
PRESS = [
 ('p-elperiodico', 'Alberto López, «Arjuna»: Soy el canalla del yoga · El Periódico', 'Mi primera entrevista, en la contra de El Periódico, donde me bautizaron como «El canalla del yoga».', 'http://www.elperiodico.com/es/sociedad/20160312/albert-lopez-arjuna-soy-el-canalla-del-yoga-4971913', 'Leer entrevista'),
 ('p-tve', 'Entrevista para Ara i Aquí · TVE Catalunya', 'Entrañable entrevista sobre la transformación de un joven rebelde.', 'https://www.rtve.es/play/videos/ara-i-aqui/ara-aqui-els-joves-violents/4944539/', 'Ver vídeo'),
 ('p-sergio-marina', 'Entrevista con Sergio Marina', 'Conversación consciente con mi amigo Sergio Marina.', 'https://www.youtube.com/watch?v=KkWZLAjGwyo&t=1766s', 'Ver vídeo'),
 ('p-sprinter', 'Entrevista para la plataforma de Sprinter', 'Conoce a Arjuna, yoga trainer de Sprinter Pass.', 'https://blogsprinter.es/conoce-a-arjuna-yoga-trainer-de-sprinter-pass/', 'Leer entrevista'),
 ('p-amosdecasa', 'Revista Amos de Casa', 'Dos páginas con posturas de Virayoga para tu día a día.', None, 'Artículo solo en papel'),
 ('p-yoganimate', 'Podcast Yoganímate', 'Entrevista súper divertida con Lidia de Yoganímate.', 'https://www.ivoox.com/15-virayoga-arte-fusion-con-audios-mp3_rf_32308931_1.html', 'Escuchar'),
 ('p-quehacer', 'Qué hacer en Barcelona', 'Entrañable entrevista sobre Street Virayoga y el método.', 'https://www.quehacerenbcn.com/es/entrevistas/arjuna-quiero-conquistar-barcelona-con-el-virayoga', 'Leer entrevista'),
 ('p-25tv', '25tv · Tierra de sueños, con Pedro Riba', 'Con mi hermano espiritual Gundicha Dasa, hablando del #barcelonayogaday.', 'https://www.youtube.com/watch?v=dzqoQMBEaAU&t=2790s', 'Ver vídeo'),
 ('p-stylersmag', 'Stylersmag', 'Entrevista para la revista de moda y lifestyle Stylersmag.', 'https://stylersmag.com/conoces-el-virayoga-libro-arjuna/', 'Leer'),
 ('p-luces', 'Radio · Luces en la Oscuridad', 'Con Pedro Riba y Gundicha Dasa, hablando del Barcelona Yoga Day.', 'http://lucesenlaoscuridad.es/entradas_grabacion/los-hare-krishna-y-el-barcelona-yoga-day-gundicha-das-expresidente-del-templo-de-los-hare-krishna-en-barcelona-y-arjuna-creador-de-virayoga-ambos-organizadores-del-barcelona-yoga-day-en-reco/', 'Escuchar'),
 ('p-canalyoga', 'Canal Yoga TV, con Ángeles Shakti', 'Desde Chile presentan el Virayoga, «el yoga del guerrero, el yoga del héroe».', None, None),
 ('p-agentek', 'Agente K', 'Una entrevista muy centrada en el proyecto Virayoga y el libro «Conoce el Virayoga…».', 'https://www.agente-k.com/conoces-el-virayoga-libro-arjuna/', 'Leer'),
 ('p-alaultima', '«A la última» · Clickradiotv', 'Bonita entrevista con Lydia Bermejo.', 'http://www.ivoox.com/21993695', 'Escuchar'),
 ('p-elle', 'Revista ELLE', 'ELLE Belleza recomienda el libro de Virayoga en su sección de actividades saludables y fitness.', None, 'Artículo solo en papel'),
 ('p-bcndivina', 'Revista Barcelona Divina', 'Artículo sobre el libro «Conoce el Virayoga por Arjuna, el canalla del yoga».', None, 'Artículo solo en papel'),
 ('p-mundopranico', 'Mundo Pránico y Caja de Pandora', '28 minutos de entrevista muy divertidos y canallas.', 'https://www.youtube.com/watch?v=H1C0JCe6dJo', 'Ver vídeo'),
 ('p-panorama', 'De taxista a profe de yoga · El Panorama', 'Reportaje para el periódico venezolano El Panorama.', 'http://www.panorama.com.ve/experienciapanorama/REPORTAJE--De-taxista-a-profe-de-yoga-20170616-0068.html', 'Leer'),
 ('p-estetic', 'Virayoga, ¿en qué se basa este nuevo método? · Estetic', 'La revista digital Estetic quiso saber más sobre el método.', 'http://consalud.es/estetic/tendencias/virayoga-en-que-se-basa-este-nuevo-metodo-37059', 'Leer'),
 ('p-larazon', 'La Razón', 'Nos recomendó como principal actividad de bienestar para el verano.', None, 'Artículo solo en papel'),
 ('p-vichy', 'Balneari Vichy Catalán · The 19th Room', 'Presentación del libro en el Balneario Vichy Catalán.', 'https://the19throom.com/2017/09/03/presentacion-editorial-virayoga-en-el-hotel-balneari-vichy-catalan/', 'Ver'),
]
def prensa():
    items = ''
    for img, t, d, u, l in PRESS:
        contain = ' contain' if img in ('p-agentek', 'p-yoganimate', 'p-luces') else ''
        link = f'<a class="more" href="{u}" target="_blank" rel="noopener">{l} →</a>' if u else (f'<span class="paper">«{l}»</span>' if l else '')
        items += f'<div class="press-item reveal"><div class="thumb{contain}" style="background-image:url(/img/{img}.jpg)" role="img" aria-label="{html.escape(t)}"></div><h3>{t}</h3><p>{d}</p>{link}</div>'
    body = f'''
<div class="wrap content">
  <div class="narrow" style="padding:0">
    <h2 class="quote-title">Notas de prensa</h2>
    <p>Aquí te dejo algunas de las entrevistas y notas de prensa que me han ido haciendo hasta la fecha.</p>
  </div>
  <div class="press" style="margin-top:40px">{items}</div>
</div>
{newsletter()}'''
    page('/prensa/', 'Notas de prensa · Yoga con Arjuna, el canalla del yoga',
         'Alberto López es «Arjuna, el canalla del yoga». Consulta todas las notas de prensa y entrevistas: El Periódico, TVE, ELLE, La Razón y más.',
         body, hero='cab-prensa.jpg', hero_title='Prensa', crumb='Prensa', image='p-elperiodico.jpg')

# ---------------------------------------------------------------- PRODUCTOS (nuevo)
# Sustituye 'stripe' por el Payment Link de cada producto (https://buy.stripe.com/...).
PRODUCTS = [
 dict(id='libro-pdf', tag='Libro en PDF', title='Libro «Conoce el Virayoga con Arjuna, el canalla del yoga» (PDF)', img='libro-portada.jpg', book=True,
      desc='Mi historia y la del Virayoga, contada sin filtros. Descarga inmediata para leer en el móvil, la tablet o el ordenador.', price='9,95 €', stripe=''),
 dict(id='formacion-virayoga', tag='Formación', title='Formación total de Virayoga', img='india-arcos-3.jpg',
      desc='Yoga, artes marciales y psicología en 9 sesiones. Online, por bloques, con autoevaluaciones y acompañamiento cercano.', price='XX €', stripe=''),
 dict(id='reserva-india', tag='Viaje', title='Reserva tu plaza: viaje a India', img='india-jaipur.jpg',
      desc='Paga la señal y asegura tu plaza en el próximo viaje al origen del yoga con Arjuna.', price='XX €', stripe=''),
]
def productos():
    cards = ''
    for p in PRODUCTS:
        if p['stripe']:
            btn = f'<a class="btn" href="{p["stripe"]}" target="_blank" rel="noopener">Comprar</a>'
            pend = ''
        else:
            btn = '<span class="btn disabled" aria-disabled="true">Comprar</span>'
            pend = '<div class="pending">Enlace de pago pendiente (Stripe Payment Link)</div>'
        cards += f'''
    <div class="product reveal" id="{p["id"]}">
      <div class="img{' book' if p.get('book') else ''}" style="background-image:url(/img/{p["img"]})" role="img" aria-label="{html.escape(p['title'])}"></div>
      <div class="body">
        <div class="tag">{p["tag"]}</div>
        <h3>{p["title"]}</h3>
        <p>{p["desc"]}</p>
        <div class="foot"><span class="price">{p["price"]}</span>{btn}</div>
        {pend}
      </div>
    </div>'''
    body = f'''
<div class="wrap content">
  <div class="narrow center" style="padding:0">
    <h2 class="quote-title">Lleva el Virayoga contigo</h2>
    <p class="lead">El libro en PDF, la formación de Virayoga y la reserva del viaje a India. Pago seguro con tarjeta, Apple Pay o Google Pay.</p>
  </div>
  <div class="products" style="margin-top:48px">{cards}
  </div>
  <div class="trust">
    <span>{ICON['lock']} Pago 100% seguro con Stripe</span>
    <span>{ICON['card']} Tarjeta, Apple Pay y Google Pay</span>
    <span>{ICON['heart']} ¿Dudas? <a href="/contacta/">Escríbeme</a></span>
  </div>
  <p class="center" style="font-size:.85rem;color:#777;margin-top:18px">Al comprar aceptas las <a href="/condiciones-de-compra/">condiciones de compra</a> y la <a href="/politica-de-privacidad/">política de privacidad</a>.</p>
</div>
{testimonials_html(kinds=('formacion', 'vida'))}
{newsletter()}'''
    items = [{"@type": "ListItem", "position": i + 1, "url": f"{DOMAIN}/productos/#{p['id']}", "name": p['title']} for i, p in enumerate(PRODUCTS)]
    page('/productos/', 'Productos · Libro en PDF, formación de Virayoga y viaje a India · Yoga con Arjuna',
         'Compra el libro «Conoce el Virayoga» en PDF, la formación total de Virayoga y reserva tu plaza en el viaje a India con Arjuna. Pago seguro.',
         body, hero='hero-6.jpg', hero_title='Productos', crumb='Productos', image='libro-portada.jpg',
         schema={"@context": "https://schema.org", "@type": "ItemList", "itemListElement": items})

# ---------------------------------------------------------------- CONTACTA
def contacta():
    body = f'''
<div class="wrap content">
  <div class="contact-grid">
    <div class="contact-info reveal">
      <h2 class="quote-title" style="margin-top:0">Contacta conmigo</h2>
      <p>¡Hola! Escríbeme para lo que necesites: la formación, el viaje a India, contratarme para un evento o una clase, o simplemente una duda.</p>
      <p>Te contesto en cuanto pueda. Si tienes prisa, el WhatsApp es más rápido.</p>
      <div style="margin-top:28px">
        <div class="row">{ICON['mail']}<a href="mailto:{EMAIL}">{EMAIL}</a></div>
        <div class="row">{ICON['wa']}<a href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener">WhatsApp 619 945 481</a></div>
        <div class="row">{ICON['pin']}<span>Martorelles · Terrassa · Barcelona · Online</span></div>
      </div>
      {social_html().replace('class="social"', 'class="social" style="justify-content:flex-start;margin-top:28px"')}
    </div>
    <form class="reveal" name="contacto" method="POST" action="/gracias/" data-netlify="true" netlify-honeypot="bot-field">
      <input type="hidden" name="form-name" value="contacto">
      <p class="hidden"><label>No rellenar: <input name="bot-field"></label></p>
      <label for="c-nombre">Nombre</label><input id="c-nombre" type="text" name="nombre" required autocomplete="name">
      <label for="c-email">Correo electrónico</label><input id="c-email" type="email" name="email" required autocomplete="email">
      <label for="c-asunto">Asunto</label>
      <select id="c-asunto" name="asunto">
        <option>Formación Virayoga</option><option>Viaje a India</option><option>Contratar a Arjuna (escuelas, empresas, eventos)</option><option>Clases</option><option>Bhakti / música</option><option>Libro y productos</option><option>Prensa</option><option>Otro</option>
      </select>
      <label for="c-mensaje">Mensaje</label><textarea id="c-mensaje" name="mensaje" required></textarea>
      <label class="check"><input type="checkbox" name="acepto" required> <span>He leído y acepto la <a href="/politica-de-privacidad/">política de privacidad</a>.</span></label>
      <button class="btn" type="submit">Enviar</button>
    </form>
  </div>
</div>'''
    page('/contacta/', 'Contacta conmigo · Yoga con Arjuna · Virayoga, despierta tu poder interno',
         'Contacta con Arjuna para recibir información de la formación de Virayoga, los viajes a India, masterclasses, eventos, clases y productos.',
         body, hero='cab-contacta.jpg', hero_title='Contacta', crumb='Contacta', image='cab-contacta.jpg')

# ---------------------------------------------------------------- CAMINO DEL GUERRERO (9 sesiones) Y TEST
# Fuente: Manual de formación de profesores de Virayoga (etapas y Sankalpas de cada sesión)
STAGES = [
    (1, 'Proyección', 'Proyecto mis objetivos con decisión y firmeza',
     'Tienes energía, pero te falta un rumbo claro. Tu paso ahora es tomar conciencia de dónde estás y hacia dónde quieres ir, y enfocar tus deseos en un camino concreto.'),
    (2, 'Respeto', 'Respeto mi espacio vital, mi libertad',
     'Tiendes a vivir según el «debo hacer» o lo que se espera de ti. Te toca escuchar lo que de verdad quieres, aprender a decir «no» y poner límites sanos.'),
    (3, 'Fuerza', 'La fuerza está dentro de mí',
     'La fuerza que buscas está dentro, en tu autoestima. Te toca aceptarte, creer en tus capacidades y crear un plan de acción para cambiar lo que no te gusta.'),
    (4, 'Anticipación', 'Me anticipo a mis acciones',
     'Mejor prevenir que curar. Te toca identificar tus puntos débiles antes de que lleguen los momentos difíciles y entrenar una actitud positiva ante lo que venga.'),
    (5, 'Resiliencia', 'Me levanto ante las adversidades',
     'Como se dice en artes marciales: «Me levanto». Has pasado por momentos duros y te toca recordar tu enorme poder de superación.'),
    (6, 'Virtudes', 'Utilizo mis armas internas para salir de las situaciones',
     'Te fijas más en tus errores que en tus aciertos. Te toca descubrir tus armas internas, tus puntos fuertes, y seguir desarrollándolos.'),
    (7, 'Respuesta', 'Cómo gestiono las situaciones que me ocurren',
     'Es el momento de la autenticidad: mostrarte al mundo tal como eres, con tus virtudes y tus defectos, sin miedo y con seguridad.'),
    (8, 'Liberación', 'Me libero de todo lo que no me deja avanzar',
     'Hay emociones que te pesan. Te toca afrontarlas, dejarlas sentir, conectar con ellas y aceptarlas para poder avanzar.'),
    (9, 'Fluir', 'Fluyo en cada situación',
     'Ya lo das todo, pero te cuesta soltar. Te toca el desapego: relajarte y dejar que la vida traiga cosas buenas hacia ti.'),
]

# Preguntas: las 5 primeras suman puntos a las etapas (s); las 4 últimas son prácticas y deciden el recurso (g = grupo, k = valor).
QUIZ = [
    ('¿Cómo describirías tu momento actual?', [
        ('Con ganas de cambios, pero sin un rumbo claro', [1]), ('Muy liado/a: acabo diciendo que sí a todo', [2]),
        ('Con ganas de sentirme más fuerte y seguro/a', [3]), ('Bien, pero me gustaría vivir con más calma', [9])]),
    ('Cuando algo no sale como esperabas…', [
        ('Me pilla desprevenido/a', [4]), ('Me cuesta un poco, pero me levanto', [5]),
        ('Reacciono rápido, a veces demasiado', [7]), ('Le doy vueltas por dentro', [8])]),
    ('¿Qué frase te pega más?', [
        ('«Tengo mil ideas y me cuesta elegir»', [1]), ('«Siempre pienso primero en los demás»', [2]),
        ('«Podría hacer mucho más si confiara en mí»', [3]), ('«Sé hacer muchas cosas, pero no sé en qué destaco»', [6])]),
    ('¿Qué te gustaría sentir al salir de una clase?', [
        ('Claridad y foco', [1]), ('Fuerza y energía', [3, 5]),
        ('Ligereza y calma', [8, 9]), ('Que me he mostrado tal como soy', [7])]),
    ('¿Qué parte del Virayoga te llama más?', [
        ('Las técnicas marciales: defensa y seguridad', [4, 6]), ('Las asanas y el trabajo físico', [3, 5]),
        ('La meditación y la respiración', [8, 9]), ('El crecimiento personal', [1, 7])]),
    ('¿Qué buscas principalmente?', [
        ('Ponerme en forma y ganar flexibilidad', ('obj', 'forma')), ('Desconectar del estrés', ('obj', 'estres')),
        ('Crecer como persona', ('obj', 'crecer')), ('Formarme y tener una salida profesional', ('obj', 'profesion'))]),
    ('¿Cuánto conoces el Virayoga?', [
        ('Nada, quiero empezar', ('nivel', 'nuevo')), ('Practico yoga, pero no Virayoga', ('nivel', 'yoga')),
        ('Ya practico Virayoga', ('nivel', 'vira')), ('Ya doy clases de yoga', ('nivel', 'profe'))]),
    ('¿Cómo te gustaría practicar?', [
        ('Desde casa, a mi ritmo', ('modo', 'casa')), ('En persona, en clase con Arjuna', ('modo', 'clase')),
        ('Con atención 100 % personal', ('modo', 'privada')), ('Viviendo una experiencia: un viaje a India', ('modo', 'viaje'))]),
    ('¿Qué inversión te encaja ahora mismo?', [
        ('Empezar con algo económico', ('pres', 'bajo')), ('Algunas clases o un taller', ('pres', 'medio')),
        ('Una formación completa', ('pres', 'alto')), ('Prefiero hablarlo antes con Arjuna', ('pres', 'hablar'))]),
]

# Recursos que puede recomendar el test (id de PRODUCTS o páginas de la web)
QUIZ_RES = {
    'curso': dict(title='Biblioteca: clases y prácticas gratuitas', img='vira-mar.jpg', url='/blog/',
                  why='Empieza desde casa con las prácticas gratuitas y pon el foco en la sesión {n}, {name}, que es la que más necesitas ahora.'),
    'manual': dict(title='Formación total de Virayoga', img='vira-salto.jpg', url='/virayoga/',
                   why='Ya conoces el Virayoga: la formación te lleva a fondo por las 9 sesiones, empezando por entender bien la de {name}.'),
    'formacion': dict(title='Formación total de Virayoga', img='india-arcos-3.jpg', url='/virayoga/',
                      why='Quieres enseñar: la formación te lleva por las 9 sesiones, también la de {name}, para vivirlas y transmitirlas.'),
    'intro': dict(title='Habla con Arjuna sobre la formación', img='india-arcos-3.jpg', url='/contacta/?asunto=Formación%20Virayoga',
                  why='Cuéntanos tu momento y te explicamos cómo empezar la formación, sin presiones.'),
    'clase': dict(title='Clases con Arjuna', img='studio-1.jpg', url='/agenda/',
                  why='Practica en grupo y en persona. Cuéntale a Arjuna que tu etapa es {name} y la trabajaréis juntos.'),
    'privada': dict(title='Clases privadas con Arjuna', img='clase-privada.jpg', url='/contacta/?asunto=Clases',
                    why='Escríbele y organizáis sesiones a tu medida, centradas en la etapa de {name}.'),
    'viaje': dict(title='Viaje a India con Arjuna', img='india-jaipur.jpg', url='/viajes-india/',
                  why='Vive el Virayoga fuera de la rutina: el viaje al origen del yoga es el mejor espacio para trabajar la etapa de {name}.'),
    'libro': dict(title='Libro «Conoce el Virayoga» en PDF', img='libro-portada.jpg', url='/mi-libro/',
                  why='La historia de Arjuna y la actitud Vira: el mejor punto de partida.'),
}

def camino_html(title='El camino del guerrero', intro='El Virayoga se estructura en 9 sesiones. Cada una es una etapa del camino para despertar tu guerrero interior.', cta=True):
    steps = ''.join(f'<li style="--i:{n}" data-stage="{n}"><span class="num">{n}</span><strong>{name}</strong><em>{html.escape(sk)}</em></li>' for n, name, sk, _ in STAGES)
    btn = '<p class="center" style="margin-top:36px"><a class="btn" href="/test-guerrero/">Haz el test: ¿qué guerrero eres?</a></p>' if cta else ''
    return f'''<section class="camino reveal" aria-label="Las 9 sesiones del Virayoga">
  <div class="center"><h2 class="section-title">{title}</h2><p class="lead">{intro}</p>
  <div class="count"><span data-count="9">9</span> sesiones · <span data-count="9">9</span> sankalpas · 1 guerrero</div></div>
  <ol class="steps">{steps}</ol>{btn}
</section>'''

def test_guerrero():
    data = dict(
        stages=[dict(n=n, name=name, sk=sk, txt=txt, de={'Respeto': 'del', 'Fluir': 'del', 'Virtudes': 'de las'}.get(name, 'de la')) for n, name, sk, txt in STAGES],
        q=[dict(t=t, a=[dict(l=l, s=v) if isinstance(v, list) else dict(l=l, g=v[0], k=v[1]) for l, v in ans]) for t, ans in QUIZ],
        res=QUIZ_RES, wa=WHATSAPP)
    body = f'''
<section class="wrap content quiz-wrap">
  <div class="quiz" data-quiz>
    <div class="q-intro">
      <h2 class="script-title">¿Qué guerrero eres?</h2>
      <p class="lead">El Virayoga recorre 9 etapas: el camino del guerrero. Responde 9 preguntas rápidas y descubre en qué etapa estás, cuál es tu sankalpa y qué práctica te conviene ahora.</p>
      <p class="muted">2 minutos · sin registro</p>
      <button class="btn" data-start>Empezar el test</button>
    </div>
    <div class="q-run" hidden>
      <div class="q-bar"><span></span></div>
      <p class="q-step"></p>
      <h3 class="q-title"></h3>
      <div class="q-opts"></div>
      <button class="q-back" type="button">← Anterior</button>
    </div>
    <div class="q-result" hidden aria-live="polite"></div>
  </div>
  <form class="q-form" name="test-guerrero" method="POST" data-netlify="true" netlify-honeypot="bot-field" action="/gracias/" hidden>
    <input type="hidden" name="form-name" value="test-guerrero"><input type="hidden" name="resultado"><p hidden><input name="bot-field"></p>
    <h3>¿Quieres que Arjuna te oriente?</h3>
    <p>Déjanos tu correo y te escribiremos con una práctica para tu etapa.</p>
    <div class="row"><input type="text" name="nombre" placeholder="Nombre" required><input type="email" name="email" placeholder="Correo electrónico" required></div>
    <label class="check"><input type="checkbox" name="acepto" required> <span>Acepto la <a href="/politica-de-privacidad/">política de privacidad</a>.</span></label>
    <button class="btn" type="submit">Enviar</button>
  </form>
  {camino_html('Las 9 etapas del camino', 'Tu resultado aparece marcado en el camino.', cta=False)}
  <p class="center muted" style="font-size:.85rem;margin-top:40px">Este test es orientativo y no sustituye una valoración profesional.</p>
</section>
<script type="application/json" id="quiz-data">{json.dumps(data, ensure_ascii=False)}</script>'''
    page('/test-guerrero/', '¿Qué guerrero eres? Test de Virayoga · Yoga con Arjuna',
         'Descubre en qué etapa del camino del guerrero estás, tu sankalpa y la práctica de Virayoga que más te conviene. Test gratuito de 2 minutos.',
         body, hero='vira-salto.jpg', hero_title='¿Qué guerrero eres?', crumb='Test del guerrero', image='vira-salto.jpg')

# ---------------------------------------------------------------- BLOG (biblioteca de vídeos y artículos)
YT_CHANNEL = 'https://www.youtube.com/@yogaconarjuna'
YT_CHANNEL_ID = 'UCvABr1XkDwI3JPWX3LcYajw'   # la lista de subidas del canal es el mismo id empezando por «UU»
# Para añadir contenido, añade una línea a POSTS:
#   ('practica', 'ID_YOUTUBE', 'Título', 'Descripción corta')   → Clases y prácticas
#   ('directo',  'ID_YOUTUBE', 'Título', 'Descripción corta')   → Directos de Instagram (subidos a YouTube, aunque sea como «no listados»)
#   ('articulo', 'imagen.jpg', 'Título', 'Descripción corta', '/blog/slug/')   → Artículos
POSTS = [
    ('practica', 'lozwmWKLfSU', 'Una práctica de Virayoga', 'Yoga y artes marciales en movimiento: así es una sesión de Virayoga.'),
]
BLOG_CATS = [('practica', 'Clases y prácticas'), ('directo', 'Té con Arjuna (directos)'), ('articulo', 'Artículos')]

def blog():
    cards = ''
    for p in POSTS:
        t, ref, title, desc = p[:4]
        tag = dict(BLOG_CATS)[t]
        if t == 'articulo':
            cards += f'''<a class="post reveal" data-type="{t}" href="{p[4]}"><div class="img" style="background-image:url(/img/{ref})" role="img" aria-label="{html.escape(title)}"></div>
  <div class="body"><span class="tag">{tag}</span><h3>{title}</h3><p>{desc}</p><span class="more">Leer →</span></div></a>'''
        else:
            cards += f'''<article class="post reveal" data-type="{t}">
  <div class="video wide" data-yt="{ref}" data-title="{html.escape(title)}" style="background-image:url(https://i.ytimg.com/vi/{ref}/hqdefault.jpg)"><button aria-label="Reproducir: {html.escape(title)}">{ICON['play']}</button></div>
  <div class="body"><span class="tag">{tag}</span><h3>{title}</h3><p>{desc}</p></div>
</article>'''
    # Tarjetas «próximamente» para las categorías que aún no tienen contenido
    soon = {'practica': ('vira-equilibrio.jpg', 'Más prácticas en camino', 'Nuevas clases y prácticas guiadas para hacer en casa.'),
            'directo': ('arjuna-templo.jpg', 'Té con Arjuna', 'Los directos de Instagram, ahora guardados aquí para verlos cuando quieras.')}
    have = {p[0] for p in POSTS}
    for t, (img, title, desc) in soon.items():
        if t not in have or t == 'practica':
            cards += f'''<article class="post reveal soon-card" data-type="{t}"><div class="img" style="background-image:url(/img/{img})" role="img" aria-label="{html.escape(title)}"></div>
  <div class="body"><span class="tag">{dict(BLOG_CATS)[t]}</span><h3>{title}</h3><p>{desc}</p><span class="soon">Próximamente</span></div></article>'''
    # «Artículos» solo aparece cuando haya alguno (en la reunión se acordó que no es prioritario)
    cats = [(k, v) for k, v in BLOG_CATS if k != 'articulo' or 'articulo' in have]
    filters = '<button class="on" data-f="all">Todo</button>' + ''.join(f'<button data-f="{k}">{v}</button>' for k, v in cats)
    uploads = 'UU' + YT_CHANNEL_ID[2:]
    body = f'''
<section class="wrap content blog">
  <div class="narrow center">
    <h2 class="script-title">La biblioteca del guerrero</h2>
    <p class="lead">Recursos gratuitos para practicar Virayoga desde donde estés: clases, prácticas y los directos del Té con Arjuna.</p>
  </div>

  <div class="yt-block reveal">
    <div class="yt-text">
      <span class="yt-logo">{ICON['yt']}</span>
      <h3>Canal Yoga con Arjuna</h3>
      <p>Aquí tienes los últimos vídeos del canal. Suscríbete para no perderte ninguna práctica nueva.</p>
      <p><a class="btn yt-btn" href="{YT_CHANNEL}?sub_confirmation=1" target="_blank" rel="noopener">{ICON['yt']} Suscríbete</a> &nbsp; <a class="btn ghost" href="{YT_CHANNEL}/videos" target="_blank" rel="noopener">Ver todos los vídeos</a></p>
    </div>
    <div class="video wide" data-yt-list="{uploads}" data-title="Últimos vídeos de Yoga con Arjuna" style="background-image:url(/img/vira-mar.jpg)">
      <button aria-label="Ver los últimos vídeos del canal">{ICON['play']}</button><div class="cap">Últimos vídeos del canal</div>
    </div>
  </div>

  <div class="yt-block reveal">
    <div class="yt-text">
      <span class="yt-logo">{ICON['music']}</span>
      <h3>Bhakti, música medicina</h3>
      <p>Mantras, guitarra y voz: el canal de música de Arjuna. Dale al play y deja que la cabeza se calle un rato.</p>
      <p><a class="btn yt-btn" href="{YT_MUSIC}?sub_confirmation=1" target="_blank" rel="noopener">{ICON['yt']} Suscríbete</a> &nbsp; <a class="btn ghost" href="{YT_MUSIC}/videos" target="_blank" rel="noopener">Ver el canal</a></p>
    </div>
    <div class="video wide" data-yt-list="{'UU' + YT_MUSIC.rstrip('/').split('/')[-1][2:]}" data-title="Bhakti, música de Arjuna" style="background-image:url(/img/arjuna-templo.jpg)">
      <button aria-label="Escuchar la música de Arjuna">{ICON['play']}</button><div class="cap">Escucha la música Bhakti</div>
    </div>
  </div>

  <div class="filters" role="tablist">{filters}</div>
  <div class="posts">{cards}</div>
</section>
{newsletter('newsletter-blog')}'''
    page('/blog/', 'Biblioteca · Clases y prácticas gratuitas de Virayoga · Yoga con Arjuna',
         'Recursos gratuitos de Virayoga: clases y prácticas en vídeo, los directos del Té con Arjuna y el canal de YouTube de Arjuna.',
         body, hero='vira-mar.jpg', hero_title='Biblioteca', crumb='Biblioteca', image='vira-mar.jpg')

# ---------------------------------------------------------------- LEGALES Y GRACIAS
def legales():
    # Datos del titular pendientes: se marcan en amarillo para rellenarlos cuando el cliente los facilite
    def X(t): return f'<mark class="todo">[XXXX {t}]</mark>'
    TIT, NIF, DIR, CIUDAD = 'Alberto López Espín', X('NIF'), X('dirección completa'), X('ciudad')
    mail = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
    upd = 'Última actualización: noviembre de 2026.'
    def art(h1, inner):
        return f'<article class="narrow content legal" style="padding-top:56px"><h1>{h1}</h1><p class="upd">{upd}</p>{inner}</article>'

    page('/aviso-legal/', 'Aviso legal · Yoga con Arjuna', 'Aviso legal de la web yogaconarjuna.com.', art('Aviso legal', f"""
<h2>1. Datos identificativos</h2>
<p>En cumplimiento de la Ley 34/2002, de Servicios de la Sociedad de la Información y de Comercio Electrónico (LSSI-CE), se informa de los datos del titular de esta web:</p>
<ul><li><strong>Titular:</strong> {TIT} («Arjuna», Yoga con Arjuna)</li><li><strong>NIF:</strong> {NIF}</li><li><strong>Domicilio:</strong> {DIR}</li><li><strong>Correo electrónico:</strong> {mail}</li><li><strong>Teléfono / WhatsApp:</strong> +34 619 945 481</li><li><strong>Web:</strong> www.yogaconarjuna.com</li></ul>
<h2>2. Objeto</h2>
<p>Esta web ofrece información sobre las clases, formaciones, retiros, viajes y productos de Yoga con Arjuna y Virayoga, y permite contactar con el titular y adquirir algunos productos y servicios.</p>
<h2>3. Condiciones de uso</h2>
<p>El acceso a la web es gratuito y supone la aceptación de este aviso legal. La persona usuaria se compromete a hacer un uso adecuado de los contenidos y a no utilizarlos para actividades ilícitas o contrarias a la buena fe.</p>
<h2>4. Propiedad intelectual e industrial</h2>
<p>Los textos, fotografías, vídeos, logotipos, la marca Virayoga y el resto de contenidos de esta web pertenecen al titular o cuentan con la autorización correspondiente. Queda prohibida su reproducción, distribución o transformación sin autorización expresa por escrito.</p>
<h2>5. Responsabilidad</h2>
<p>El titular no se hace responsable de los daños derivados de un uso indebido de la web ni de los contenidos de sitios externos enlazados. La práctica de yoga, artes marciales y ejercicios de respiración requiere escuchar al propio cuerpo; ante cualquier duda de salud, consulta con un profesional sanitario antes de practicar.</p>
<h2>6. Enlaces externos</h2>
<p>La web contiene enlaces a redes sociales, tiendas de libros, YouTube, Instagram y la plataforma de pago Stripe. Cada uno de estos servicios tiene sus propias condiciones y políticas de privacidad.</p>
<h2>7. Legislación aplicable</h2>
<p>Este aviso legal se rige por la legislación española. Para cualquier controversia, las partes se someten a los juzgados y tribunales de {CIUDAD}, salvo que la normativa de consumidores establezca otro fuero.</p>
<p>Consulta también la <a href="/politica-de-privacidad/">política de privacidad</a>, la <a href="/politica-de-cookies/">política de cookies</a> y las <a href="/condiciones-de-compra/">condiciones de compra</a>.</p>"""))

    page('/politica-de-privacidad/', 'Política de privacidad · Yoga con Arjuna', 'Cómo trata Yoga con Arjuna tus datos personales.', art('Política de privacidad', f"""
<h2>1. Responsable del tratamiento</h2>
<p>{TIT}, NIF {NIF}, con domicilio en {DIR}. Contacto: {mail}.</p>
<h2>2. Qué datos tratamos y para qué</h2>
<ul>
<li><strong>Formulario de contacto:</strong> nombre, correo y mensaje, para responder a tu consulta.</li>
<li><strong>Newsletter y avisos de eventos:</strong> nombre y correo, para enviarte información sobre clases, formaciones, retiros y novedades, solo si lo has aceptado.</li>
<li><strong>Compras:</strong> nombre, correo, dirección de envío (si hay producto físico) y datos de la compra, para gestionar el pedido, emitir la factura y cumplir obligaciones fiscales. Los datos de la tarjeta los trata directamente Stripe; nosotros no tenemos acceso a ellos.</li>
<li><strong>WhatsApp y correo:</strong> los datos que nos envíes por estos canales, para atender tu consulta o reserva.</li>
</ul>
<h2>3. Base legal</h2>
<p>Tu consentimiento (formularios y newsletter), la ejecución de un contrato (compras y reservas) y el cumplimiento de obligaciones legales (facturación).</p>
<h2>4. Cuánto tiempo guardamos los datos</h2>
<p>Los datos de contacto, el tiempo necesario para responderte. Los de la newsletter, hasta que te des de baja. Los de compras, durante los plazos que exige la normativa fiscal y mercantil.</p>
<h2>5. Con quién se comparten</h2>
<p>No cedemos datos a terceros salvo obligación legal. Usamos proveedores que tratan datos por nuestra cuenta: Netlify (alojamiento web y formularios), Stripe (pagos) y Google (correo electrónico). Algunos de estos proveedores pueden estar fuera del Espacio Económico Europeo y aplican las garantías previstas en el RGPD.</p>
<h2>6. Tus derechos</h2>
<p>Puedes ejercer tus derechos de acceso, rectificación, supresión, oposición, limitación y portabilidad, y retirar tu consentimiento en cualquier momento, escribiendo a {mail}. Si consideras que no hemos atendido bien tu solicitud, puedes reclamar ante la Agencia Española de Protección de Datos (www.aepd.es).</p>
<h2>7. Menores</h2>
<p>Los menores de 14 años no pueden facilitarnos datos sin el consentimiento de sus padres o tutores.</p>"""))

    page('/politica-de-cookies/', 'Política de cookies · Yoga con Arjuna', 'Política de cookies de Yoga con Arjuna.', art('Política de cookies', """
<h2>¿Qué son las cookies?</h2>
<p>Son pequeños archivos que algunas webs guardan en tu navegador para recordar información sobre tu visita.</p>
<h2>¿Qué cookies usa esta web?</h2>
<p>Esta web <strong>no utiliza cookies propias de análisis ni de publicidad</strong>. Solo pueden aparecer cookies de terceros en estos casos:</p>
<ul>
<li><strong>Vídeos de YouTube:</strong> se cargan en modo de privacidad mejorada (youtube-nocookie.com) y solo cuando haces clic en el vídeo.</li>
<li><strong>Vídeos de YouTube:</strong> los vídeos (testimonios y prácticas) solo se cargan cuando pulsas «play», desde youtube-nocookie.com; a partir de ese momento YouTube (Google) puede instalar sus propias cookies.</li>
<li><strong>Pago con Stripe:</strong> al pulsar «Comprar» pasas a la página segura de Stripe, que usa cookies técnicas necesarias para el pago y la prevención del fraude.</li>
</ul>
<h2>Cómo gestionarlas</h2>
<p>Puedes ver, bloquear o borrar las cookies desde la configuración de tu navegador (Chrome, Safari, Firefox o Edge). Si las bloqueas, es posible que los vídeos insertados no se muestren.</p>
<p>Si en el futuro añadimos herramientas de analítica o publicidad, actualizaremos esta política y te pediremos el consentimiento antes de usarlas.</p>"""))

    page('/condiciones-de-compra/', 'Condiciones de compra · Yoga con Arjuna', 'Condiciones generales de contratación de productos y servicios de Yoga con Arjuna.', art('Condiciones de compra', f"""
<h2>1. Vendedor</h2>
<p>{TIT}, NIF {NIF}, {DIR}. Contacto: {mail}.</p>
<h2>2. Productos y precios</h2>
<p>Los precios de la sección <a href="/productos/">Productos</a> se muestran en euros e incluyen los impuestos aplicables. Los gastos de envío de productos físicos, si los hay, se indican antes de pagar.</p>
<h2>3. Proceso de compra y pago</h2>
<p>El pago se realiza a través de Stripe, con tarjeta u otros métodos que Stripe ofrezca. Al completar el pago recibirás un correo de confirmación. Si necesitas factura, solicítala en {mail}.</p>
<h2>4. Entrega</h2>
<ul>
<li><strong>Libro firmado y productos físicos:</strong> envío a la dirección indicada en un plazo aproximado de {X('X días laborables')}.</li>
<li><strong>Cursos y contenidos digitales:</strong> acceso por correo electrónico en un plazo máximo de 48 horas.</li>
<li><strong>Clases, formaciones, retiros y viajes:</strong> la compra reserva tu plaza en las fechas indicadas.</li>
</ul>
<h2>5. Derecho de desistimiento</h2>
<p>Dispones de 14 días naturales desde la recepción de un producto físico para devolverlo sin dar explicaciones, escribiendo a {mail}. Los gastos de devolución corren a tu cargo.</p>
<p>En los <strong>contenidos digitales</strong> (cursos online, descargas), al aceptar el acceso inmediato renuncias al derecho de desistimiento una vez iniciada la descarga o el visionado, según el artículo 103 de la Ley General para la Defensa de los Consumidores y Usuarios.</p>
<h2>6. Cancelaciones de clases, formaciones, retiros y viajes</h2>
<p>{X('política de cancelación: plazos y porcentaje de reembolso, a definir con Arjuna')}</p>
<h2>7. Reclamaciones</h2>
<p>Puedes enviarnos cualquier reclamación a {mail}.</p>"""))

    page('/gracias/', '¡Gracias! · Yoga con Arjuna', 'Mensaje recibido.',
         '<article class="narrow content center" style="padding-top:96px;padding-bottom:120px"><h1 class="quote-title">¡Gracias!</h1><p class="lead">Hemos recibido tu mensaje. Te contestaré lo antes posible.</p><p><a class="btn" href="/">Volver a la portada</a> &nbsp; <a class="btn ghost" href="/productos/">Ver productos</a></p></article>')
    # 404
    page('/404-tmp/', 'Página no encontrada · Yoga con Arjuna', 'Página no encontrada.',
         '<article class="narrow content center" style="padding-top:96px;padding-bottom:120px"><h1 class="quote-title">Ups, esta página no existe</h1><p class="lead">Puede que la hayamos movido al renovar la web.</p><p><a class="btn" href="/">Ir a la portada</a></p></article>')
    shutil.move(os.path.join(OUT, '404-tmp', 'index.html'), os.path.join(OUT, '404.html'))
    os.rmdir(os.path.join(OUT, '404-tmp'))

def extras(urls):
    with open(os.path.join(OUT, 'sitemap.xml'), 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for u in urls:
            f.write(f'  <url><loc>{u}</loc></url>\n')
        f.write('</urlset>\n')
    with open(os.path.join(OUT, 'robots.txt'), 'w') as f:
        f.write(f'User-agent: *\nAllow: /\nDisallow: /gracias/\nSitemap: {DOMAIN}/sitemap.xml\n')
    with open(os.path.join(OUT, 'favicon.svg'), 'w') as f:
        f.write('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#cb433c"/><text x="32" y="44" font-family="Georgia,serif" font-style="italic" font-size="36" text-anchor="middle" fill="#fff">A</text></svg>')
    # Redirecciones 301 de las URL antiguas de WordPress
    with open(os.path.join(OUT, '_redirects'), 'w') as f:
        f.write('''/sobre-mi/                 /sobre-mi-creador-de-virayoga/   301
/vira-yoga/                /virayoga/                       301
/formacion-de-virayoga/    /virayoga/                       301
/servicios/                /servicios-de-virayoga/          301
/tienda/                   /productos/                      301
/recursos/                 /productos/                      301
/feed/                     /                                301
/wp-admin/*                /                                301
/wp-login.php              /                                301
''')
    with open(os.path.join(OUT, '_headers'), 'w') as f:
        f.write('''/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
/img/*
  Cache-Control: public, max-age=31536000, immutable
/css/*
  Cache-Control: public, max-age=86400
/js/*
  Cache-Control: public, max-age=86400
/audio/*
  Cache-Control: public, max-age=2592000
''')

if __name__ == '__main__':
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(HERE, 'static'), OUT, dirs_exist_ok=True)
    shutil.copytree(os.path.join(HERE, 'img'), os.path.join(OUT, 'img'))
    for folder in ('video', 'audio'):
        if os.path.isdir(os.path.join(HERE, folder)):
            shutil.copytree(os.path.join(HERE, folder), os.path.join(OUT, folder))
    home(); sobre(); libro(); virayoga(); actividades(); viajes_india(); agenda(); prensa(); productos(); blog(); test_guerrero(); contacta(); legales()
    urls = [DOMAIN + p for p in ['/', '/sobre-mi-creador-de-virayoga/', '/mi-libro/', '/virayoga/', '/servicios-de-virayoga/', '/viajes-india/',
                                 '/agenda/', '/prensa/', '/productos/', '/blog/', '/test-guerrero/', '/contacta/', '/aviso-legal/', '/politica-de-privacidad/',
                                 '/politica-de-cookies/', '/condiciones-de-compra/']]
    extras(urls)
    print('OK ->', os.path.abspath(OUT))
