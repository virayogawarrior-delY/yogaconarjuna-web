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

NAV = [
    ('Home', '/'),
    ('Sobre mí', '/sobre-mi-creador-de-virayoga/'),
    ('Mi libro', '/mi-libro/'),
    ('Formación Virayoga', '/virayoga/'),
    ('Actividades', '/servicios-de-virayoga/'),
    ('Agenda', '/agenda/'),
    ('Prensa', '/prensa/'),
    ('Blog', '/blog/'),
    ('Productos', '/productos/'),
    ('Contacta', '/contacta/'),
]

def _ver(rel):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', rel), 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()[:8]
CSS_V, JS_V = _ver('css/style.css'), _ver('js/main.js')

ICON = {
 'fb': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.2H7.8v3h2.6V21h3.1z"/></svg>',
 'ig': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 7.3A4.7 4.7 0 1 0 12 16.7 4.7 4.7 0 0 0 12 7.3zm0 7.7a3 3 0 1 1 0-6 3 3 0 0 1 0 6zm6-7.9a1.1 1.1 0 1 1-2.2 0 1.1 1.1 0 0 1 2.2 0zM21.9 8.2c-.1-1.5-.4-2.8-1.5-3.9S18 2.9 16.5 2.8C15 2.7 9 2.7 7.5 2.8 6 2.9 4.7 3.2 3.6 4.3S2.2 6.7 2.1 8.2C2 9.7 2 14.3 2.1 15.8c.1 1.5.4 2.8 1.5 3.9s2.4 1.4 3.9 1.5c1.5.1 7.5.1 9 0 1.5-.1 2.8-.4 3.9-1.5s1.4-2.4 1.5-3.9c.1-1.5.1-6.1 0-7.6zM19.9 17.6a3 3 0 0 1-1.7 1.7c-1.2.5-4 .4-5.2.4s-4.1.1-5.2-.4a3 3 0 0 1-1.7-1.7c-.5-1.2-.4-4-.4-5.3s-.1-4.1.4-5.3a3 3 0 0 1 1.7-1.7c1.2-.5 4-.4 5.2-.4s4.1-.1 5.2.4a3 3 0 0 1 1.7 1.7c.5 1.2.4 4 .4 5.3s.1 4.1-.4 5.3z"/></svg>',
 'x': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.8 3h3.1l-6.8 7.7L22 21h-6.2l-4.9-6.4L5.3 21H2.2l7.2-8.3L1.8 3h6.4l4.4 5.8L17.8 3zm-1.1 16.2h1.7L7.4 4.7H5.6l11.1 14.5z"/></svg>',
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
          ('https://twitter.com/yogaconarjuna', 'X (Twitter)', 'x')]

TESTIMONIALS = ['DXdwQoNDMti', 'Dc8JLtGR493', 'DX8rQTyMKCm', 'DX6EL_mMEZm', 'DXwejItMblf']

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

def testimonials_html(title='Lo que dicen mis alumnos', soft=True):
    items = ''
    for n, c in enumerate(TESTIMONIALS, 1):
        # Si existe src/video/<codigo>.mp4 se usa el vídeo propio (mejor); si no, el reproductor de Instagram dentro de la web
        if os.path.exists(os.path.join(HERE, 'video', c + '.mp4')):
            items += f'''
      <div class="t"><video controls playsinline preload="none" poster="/video/{c}.jpg" src="/video/{c}.mp4" title="Testimonio {n}"></video></div>'''
        else:
            items += f'''
      <div class="t"><blockquote class="instagram-media" data-instgrm-permalink="https://www.instagram.com/reel/{c}/" data-instgrm-version="14"><div class="t-placeholder"><a href="https://www.instagram.com/reel/{c}/" target="_blank" rel="noopener">Ver testimonio</a></div></blockquote></div>'''
    return f'''
<section class="section{' soft' if soft else ''}" id="testimonios">
  <div class="wrap">
    <div class="center reveal">
      <h2 class="section-title">{title}</h2>
      <p class="lead">Experiencias reales de personas que practican Virayoga.</p>
    </div>
    <div class="testimonials" data-instagram>{items}
    </div>
  </div>
</section>'''

def page(path, title, desc, body, hero=None, hero_title=None, crumb=None, image=None, schema=None):
    canonical = DOMAIN + path
    nav = ''.join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if h == path else ""}{" class=\"nav-shop\"" if h == "/productos/" else ""}>{n}</a></li>'
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
def home():
    slides = ''.join(f'<div class="slide{" on" if i == 1 else ""}" style="background-image:url(/img/hero-{i}.jpg)"></div>' for i in (1, 5, 2, 6, 3, 4))
    body = f'''
<section class="home-hero" aria-label="Presentación">
  {slides}
  <div class="inner">
    <h1>Arjuna, el canalla del yoga</h1>
    <p>Despierta tu poder interno con el Virayoga: yoga, artes marciales y crecimiento personal.</p>
    <div><a class="btn" href="/agenda/">¡Quiero practicar!</a></div>
  </div>
  <div class="dots"></div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="media reveal"><img src="/img/arjuna-estudio.jpg" alt="Alberto López, Arjuna, profesor de Virayoga" width="801" height="1200" loading="lazy" style="max-width:440px;margin:0 auto"></div>
    <div class="reveal">
      <h2 class="section-title"><a href="/sobre-mi-creador-de-virayoga/" style="color:inherit">Hola, soy Arjuna</a></h2>
      <p>También conocido como «El canalla del yoga». Soy profesor desde hace muchos años pero no soy el «típico yogui». Dicen que soy canalla por mi forma de ser, pero para entenderlo tendrás que conocerme.</p>
      <p>Hubo un momento en mi vida en que el yoga y las artes marciales lo cambiaron todo. Es por eso que decidí compartir mi experiencia y crear el <strong>Virayoga</strong>, historia y método que te cuento en mi libro.</p>
      <a class="btn ghost" href="/sobre-mi-creador-de-virayoga/">Conóceme</a>
    </div>
  </div>
</section>

<section class="section soft">
  <div class="wrap split r">
    <div class="media book reveal"><a href="/mi-libro/"><img src="/img/libro-portada.jpg" alt="Portada del libro Conoce el Virayoga por Arjuna, el canalla del yoga" width="645" height="972" loading="lazy"></a></div>
    <div class="reveal">
      <h2 class="section-title"><a href="/mi-libro/" style="color:inherit">Un libro de superación</a></h2>
      <p><em>Conoce el Virayoga por Arjuna, el canalla del yoga</em> es un libro de vivencias que cuenta la historia de cómo un niño de la calle se supera a sí mismo y consigue tener éxito en la vida.</p>
      <p>Es una historia real que explica cómo puedes integrar la actitud Vira en tu vida. Una actitud de superación que me ha llevado a desarrollar el Virayoga, un sistema de yoga diferente.</p>
      <a class="btn" href="/mi-libro/">Comprar libro</a>
    </div>
  </div>
</section>

<section class="parallax" style="background-image:url(/img/virayoga-fondo.jpg)">
  <div class="wrap cols">
    <div class="reveal">
      <h2 class="section-title" style="color:#fff">Y ¿qué es el Virayoga?</h2>
      <p>Virayoga es un sistema holístico que nace de la unión del yoga y las artes marciales. Tiene como objetivo principal potenciar la inteligencia corporal y la fortaleza mental a través de los beneficios de sus disciplinas.</p>
      <p>Autoconfianza, seguridad, psicomotricidad y coordinación son algunas de las habilidades que se ven potenciadas gracias a la práctica de movimientos de artes marciales, mientras que la flexibilidad, el equilibrio y la presencia se ven aún más potenciadas por esta práctica.</p>
      <p>La principal diferencia con otros estilos de yoga son los movimientos marciales que, unidos a las asanas, generan una energía diferente. Esto lo convierte en una práctica dinámica que nos ayuda a potenciar los beneficios de cada asana.</p>
      <p>El objetivo final es despertar la <strong>actitud Vira</strong>, una actitud de guerrero. <em>Vira</em> en sánscrito significa «guerrero» y <em>yoga</em> «unión»: el Virayoga es «el yoga del guerrero». Despertando así nuestro guerrero interior.</p>
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

<section class="section">
  <div class="wrap">
    <div class="center reveal">
      <h2 class="section-title"><a href="/servicios-de-virayoga/" style="color:inherit">Servicios de Virayoga</a></h2>
      <p class="lead">Encuentra la mejor forma de practicar.</p>
    </div>
    <div class="services">
      <div class="service reveal"><img src="/img/ico-clases.jpg" alt="" width="70" height="70"><h3>Clases</h3><p>¿Quieres practicar un sistema de yoga que te aporte el equilibrio y la fuerza que necesitas?</p><a class="btn" href="/agenda/">¡Quiero practicar!</a></div>
      <div class="service reveal"><img src="/img/ico-retiros.jpg" alt="" width="70" height="70"><h3>Retiros</h3><p>¿Necesitas un respiro? ¿Estás cansado/a del día a día y no tienes un solo momento para cuidar de ti?</p><a class="btn" href="/agenda/">¡Quiero un retiro!</a></div>
      <div class="service reveal"><img src="/img/ico-india.jpg" alt="" width="70" height="70"><h3>Viaje a India</h3><p>¿Quieres tener una experiencia inolvidable que te cambie la percepción de tu vida?</p><a class="btn" href="/contacta/">¡Quiero viajar!</a></div>
      <div class="service reveal"><img src="/img/ico-formacion.png" alt="" width="70" height="70"><h3>Formación</h3><p>¿Buscas una formación profesional que te haga crecer personal y profesionalmente?</p><a class="btn" href="/virayoga/">¡Quiero formarme!</a></div>
    </div>
  </div>
</section>

{testimonials_html()}

<section class="section">
  <div class="wrap center reveal">
    <h2 class="section-title">Productos y recursos</h2>
    <p class="lead">Llévate el Virayoga a casa: el libro, cursos online y material de formación.</p>
    <a class="btn" href="/productos/">Ver productos</a>
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
    page('/', 'Yoga con Arjuna · Despierta tu poder interno con el Virayoga',
         'El Virayoga es un sistema de yoga holístico que fusiona las artes marciales, el yoga y el crecimiento personal. Conoce el Virayoga con Arjuna.',
         body, image='hero-1.jpg', schema=[site, PERSON])

# ---------------------------------------------------------------- SOBRE MÍ
def sobre():
    body = f'''
<article class="narrow content">
  <h2 class="quote-title">Hola, soy Arjuna,</h2>
  <p><strong>Creador, formador y profesor de Virayoga.</strong></p>
  <p>Después de una larga trayectoria como profesor de Hatha Yoga en la línea de Nil Hahoutoff y como instructor de defensa personal, fusioné mis dos pasiones en una única práctica, el Virayoga.</p>
  <p>Pero esto ya te lo he explicado, así que mejor te cuento quién soy. Soy una persona sencilla, que busca la felicidad en las pequeñas cosas del día a día.</p>
  <div class="gallery reveal"><img src="/img/arjuna-templo.jpg" alt="Arjuna meditando frente a un templo" loading="lazy"><img src="/img/india-jaipur.jpg" alt="Arjuna en Jaipur, India" loading="lazy"><img src="/img/arjuna-mar.jpg" alt="Arjuna meditando junto al mar" loading="lazy"></div>
  <p>Durante mis viajes a India me quedé impresionado de la capacidad de servicio de su gente y me di cuenta de que en mi interior también tenía esa cualidad escondida. Así que cuando emprendí mi viaje espiritual empecé a hacer Karma Yoga, a ayudar a los demás de forma incondicional.</p>
  <p>Sin duda, el Karma Yoga fue un punto de inflexión en mi vida.</p>
  <p>Otro punto de inflexión en mi vida, y el que ha creado la persona que hoy soy, es el yoga y las artes marciales.</p>
  <p>Gracias a esas dos disciplinas milenarias he construido una persona con conciencia, principios y feliz.</p>
  <p>Por todo esto, decidí transmitir mis conocimientos a través del Virayoga, para que otras personas puedan encontrar su propio camino a la felicidad.</p>
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
    <li>Creador, formador y profesor de Virayoga.</li>
    <li>Autor del libro «Conoce el Virayoga por Arjuna, el canalla del yoga».</li>
  </ul>
  <p style="margin-top:2em"><a class="btn" href="/contacta/">Escríbeme</a></p>
</article>
{testimonials_html()}
{newsletter()}'''
    page('/sobre-mi-creador-de-virayoga/', 'Sobre mí · Hola, soy Arjuna · Creador de Virayoga · Yoga con Arjuna',
         'Creador, formador y profesor de Virayoga. Amante de la vida y los animales. Quiero difundir mi método para que tú también puedas despertar tu poder interno.',
         body, hero='cab-sobre-mi.jpg', hero_title='Sobre mí', crumb='Sobre mí', image='arjuna-estudio.jpg', schema=PERSON)

# ---------------------------------------------------------------- MI LIBRO
def libro():
    stores = [('https://www.casadellibro.com/busqueda-libros?busqueda=conoce+el+virayoga', 'Casa del Libro'),
              ('https://www.fnac.es/SearchResult/ResultList.aspx?Search=conoce+el+virayoga', 'Fnac'),
              ('https://www.amazon.es/CONOCE-VIRAYOGA-ARJUNA-CANALLA-YOGA/dp/847091443X', 'Amazon'),
              ('https://www.alibri.es/', 'Alibri Llibreria')]
    st = ''.join(f'<a class="store" href="{u}" target="_blank" rel="noopener">{n} ↗</a>' for u, n in stores)
    body = f'''
<div class="wrap content">
  <div class="layout-sidebar">
    <article>
      <h2 class="quote-title" style="margin-top:0">"Conoce el Virayoga por Arjuna,<br>el canalla del Yoga"</h2>
      <p>Es un libro de superación, que explica cómo cambié mi vida gracias al yoga y las artes marciales. Y cómo todo lo aprendido me ha llevado a desarrollar el Virayoga, una herramienta para crecer como persona.</p>
      <p>Es la historia de alguien normal y corriente que lucha por tener una vida mejor. El ejemplo de que cuando no te conformas con lo que tienes y persigues tu sueño, este se puede hacer realidad.</p>
      <p>Un relato de anécdotas y vivencias que han marcado mi vida y me han llevado a tomar un rumbo muy diferente. Situaciones problemáticas que me han enseñado que vale la pena vivir el día a día con pasión y fuerza.</p>
      <p>Con este libro, quiero compartir contigo mi experiencia pero también presentarte el Virayoga. El método que fusiona las artes marciales, el yoga y el crecimiento personal para ayudarte a afrontar la vida.</p>
      <p>Una herramienta de autoconocimiento y fortaleza que saca lo mejor de ti, dejando ver todo tu potencial y despertando el guerrero interno que hay dentro de ti.</p>
      <p>Es la historia de cómo cambié mi vida, pero sobre todo, de cómo el Virayoga puede cambiar la tuya.</p>
      <p><strong>¡Cómpralo ya!</strong></p>
      <div class="reveal" style="background:var(--soft);padding:32px;margin:32px 0;text-align:center">
        <h3 style="margin-top:0">¿Lo quieres firmado y dedicado por Arjuna?</h3>
        <p>Cómpralo directamente aquí y te lo enviamos a casa.</p>
        <a class="btn" href="/productos/#libro-firmado">Comprar libro firmado</a>
      </div>
      <p class="subtitle-center">Consigue tu libro ahora online en:</p>
      <div class="stores">{st}</div>
      <p class="subtitle-center">O pídelo en tu librería más cercana.</p>
    </article>
    <aside class="sidebar">
      <div class="card"><a href="/productos/#libro-firmado"><img src="/img/libro-portada.jpg" alt="Portada del libro Conoce el Virayoga" width="645" height="972" loading="lazy"></a></div>
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
    book = {"@context": "https://schema.org", "@type": "Book", "name": "Conoce el Virayoga por Arjuna, el canalla del yoga",
            "author": {"@type": "Person", "name": "Alberto López «Arjuna»"}, "isbn": "847091443X",
            "publisher": "Beta Editorial", "inLanguage": "es", "image": DOMAIN + "/img/libro-portada.jpg"}
    page('/mi-libro/', 'Mi libro · Conoce el Virayoga por Arjuna, el canalla del yoga',
         'Un libro de superación: cómo cambié mi vida gracias al yoga y las artes marciales y cómo nació el Virayoga. Cómpralo online o firmado por Arjuna.',
         body, hero='cab-libro.jpg', hero_title='Mi libro', crumb='Mi libro', image='libro-portada.jpg', schema=book)

# ---------------------------------------------------------------- FORMACIÓN VIRAYOGA
def virayoga():
    body = f'''
<article class="narrow content">
  <h2 class="quote-title">El Virayoga, el yoga del guerrero</h2>
  <p>Virayoga significa el yoga del guerrero. Por esta razón, la práctica de Virayoga quiere despertar nuestro poder interno. Un poder que está íntegramente relacionado con la actitud con la que afrontamos la vida.</p>
  <p>Empoderamiento, presencia, lateralidad y autoconfianza son las principales palabras que definen este nuevo estilo de yoga. Del Hatha Yoga tradicional y de diferentes artes marciales nace una nueva forma de sentir el yoga.</p>
  <p>Su objetivo principal es poder aprovecharnos de los beneficios que nos aportan ambas disciplinas. Trabajando más profundamente nuestro cuerpo, potenciando como nunca nuestro sistema motriz y aportándole la salud necesaria para su buen funcionamiento.</p>
  <p>A nivel mental, es un yoga que nos fortalece el alma aportándonos autoconfianza, equilibrio y toma de conciencia. La integración de las artes marciales nos hace sentir más seguros de nosotros mismos, mejorando nuestra autoestima y actitud de superación.</p>
  <p>Todo esto sin olvidar que estamos practicando yoga y es únicamente en el movimiento donde se esconden las técnicas marciales. Es difícil de explicar pero fácil de experimentar. Así que te invito a probar el Virayoga, para que sientas en tu propia piel todo lo que te puede aportar. <a href="/servicios-de-virayoga/">Ver actividades aquí</a>.</p>
  <div class="gallery reveal"><img src="/img/vira-salto.jpg" alt="Patada marcial de Virayoga junto al mar" loading="lazy"><img src="/img/vira-equilibrio.jpg" alt="Postura de equilibrio de Virayoga" loading="lazy"><img src="/img/india-arcos.jpg" alt="Postura de Virayoga en un palacio de India" loading="lazy"></div>
  <h2>Las 9 sesiones</h2>
  <p>El Virayoga se estructura en 9 sesiones. Cada una de ellas tiene una tipología de técnicas marciales diferente y se relaciona con cada uno de los 9 estadios del camino del guerrero: <strong>Proyección, Respeto, Fuerza, Anticipación, Resiliencia, Virtudes, Respuesta, Liberación y Fluir</strong>.</p>
  <p>La práctica de Virayoga nos permite trabajar nuestro cuerpo y mente, aprendiendo técnicas marciales encubiertas. Es importante tener presente que en todo momento estamos practicando yoga. Únicamente nos daremos cuenta de las técnicas marciales durante el despiece de la postura. La diferencia con otros tipos de yoga está en el movimiento entre las asanas, momento en el que las técnicas marciales se encuentran encubiertas. Estos movimientos van a despertar en nuestro ser nuevos aspectos que desarrollarán nuestra fortaleza interior.</p>
</article>
<div class="wrap">{camino_html('Las 9 sesiones del Virayoga', 'Cada sesión trabaja una etapa del camino del guerrero, con su sankalpa (intención).')}</div>
<article class="narrow content">
  <h2>La psicología del Virayoga</h2>
  <p>La psicología del Virayoga es un proceso evolutivo mediante el cual vas conociendo y desarrollando nuevos aspectos para mejorar tu actitud y visión ante la vida.</p>
  <p>Es un proceso de autoconocimiento y fortalecimiento emocional. Después de esta experiencia y pasado el año de formación ya no vuelves a ser la misma persona. Aprendes de ti mismo, te autoconoces y te valoras de forma diferente. Esta evolución viene dada por los 9 estadios del camino del guerrero, momento en el que la persona se va enfrentando a sus dificultades, miedos y fortalezas para conseguir despertar su guerrero/a interno.</p>

  <div style="background:var(--soft);padding:40px;margin:3em 0" class="reveal">
    <h2 style="margin-top:0">¿Quieres ser profesor de Virayoga?</h2>
    <h3>Formación de Virayoga online</h3>
    <p>Esta formación de Virayoga está pensada para conocer las bases del Virayoga a través de sus 9 sesiones. Aprender las asanas de hatha y los movimientos de artes marciales que nos llevan a las asanas, construyendo así una práctica de yoga fluida y dinámica.</p>
    <p>La formación es de <strong>200 h</strong> y se estructura en seminarios mensuales, clases semanales en las que pones en práctica las sesiones de Virayoga y un retiro al final del curso en el que evidenciarás todos los cambios que la formación ha hecho en ti.</p>
    <h3>Objetivos de la formación</h3>
    <ul>
      <li>Profundizar en la práctica de Virayoga a través de la diseminación de movimientos y asanas para poder adaptar mejor la práctica a diferentes públicos.</li>
      <li>Adquirir conocimiento de diferentes pranayamas, meditaciones, técnicas de relajación y mantras que complementarán tu práctica de Virayoga.</li>
      <li>Aprender nuevos movimientos avanzados.</li>
      <li>Darte a conocer un nuevo estilo de yoga nacido del Hatha Yoga tradicional y de las artes marciales, permitiéndote vivir en primera persona los beneficios de estas dos disciplinas.</li>
      <li>Proporcionarte todo el conocimiento necesario para ser un buen instructor de Virayoga.</li>
      <li>Profundizar en tu autoconocimiento a través de la práctica para empoderarte y despertar tu guerrerx interior.</li>
      <li>Abrirte camino a una forma diferente de afrontar y vivir la vida. Entender qué es la actitud Vira.</li>
      <li>Mejorar la condición física a través del trabajo psicomotriz, el fortalecimiento del cuerpo, el equilibrio, la flexibilidad, etc.</li>
    </ul>
    <h4>¿A quién va dirigido?</h4>
    <p>Esta formación va dirigida a profesores de Virayoga que quieren conseguir la especialización en esta disciplina para complementar su formación inicial en Virayoga.</p>
    <h4>¿Qué aprenderás?</h4>
    <ul>
      <li>Los ajustes, adaptaciones, beneficios y contraindicaciones de las asanas y movimientos de Virayoga para adaptar mejor las clases a diferentes niveles.</li>
      <li>Los 9 pranayamas que se practican en cada sesión.</li>
      <li>Diferentes meditaciones y técnicas de relajación.</li>
      <li>Los movimientos avanzados de las sesiones de Virayoga.</li>
    </ul>
    <h4>Metodología</h4>
    <p>Formación teórico-práctica que incluye:</p>
    <ul><li>Manual didáctico.</li><li>Tutorías de acompañamiento y mejora.</li><li>Descuento en retiros y viajes.</li></ul>
    <p><strong>Online y presencial en Barcelona.</strong></p>
    <p><strong>Fechas:</strong> ¡formaciones ininterrumpidas! Escríbeme y te cuento: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <p><a class="btn" href="/contacta/">¡Quiero formarme!</a> &nbsp; <a class="btn ghost" href="/productos/">Ver material de formación</a></p>
  </div>
  <h2 class="quote-title center">"Las asanas y el crecimiento personal encienden el fuego de la actitud Vira"<br><small style="font-size:.6em">Arjuna</small></h2>
</article>
{testimonials_html('Testimonios de la formación')}
{newsletter()}'''
    course = {"@context": "https://schema.org", "@type": "Course", "name": "Formación de Virayoga (200 h)",
              "description": "Formación de 200 h para conocer las bases del Virayoga a través de sus 9 sesiones. Online y presencial en Barcelona.",
              "provider": {"@type": "Person", "name": "Alberto López «Arjuna»", "url": DOMAIN + "/"}, "inLanguage": "es"}
    page('/virayoga/', 'Formación Virayoga · El yoga del guerrero · Yoga con Arjuna',
         'Descubre el Virayoga, el yoga del guerrero que fusiona artes marciales, crecimiento personal y yoga tradicional. Formación de 200 h online y presencial en Barcelona.',
         body, hero='cab-virayoga.jpg', hero_title='Virayoga', crumb='Formación Virayoga', image='vira-salto.jpg', schema=course)

# ---------------------------------------------------------------- ACTIVIDADES
def actividades():
    body = f'''
<article class="narrow content">
  <p class="lead">Yoga con Arjuna se adapta a tus necesidades. Es por eso que te ofrezco una gran variedad de servicios para que encuentres la mejor forma de practicar yoga.</p>
  <h2 class="quote-title">Clases</h2>
  <h4>Clases grupales</h4>
  <p>¿Quieres practicar un sistema de yoga que te aporte equilibrio, flexibilidad y fuerza? Te ofrezco clases de Hatha Yoga y clases de Virayoga.</p>
  <p>Son clases adaptadas a todos los niveles, donde además de la práctica de yoga/Virayoga realizaremos pranayamas, meditaciones y relajaciones. Todo esto para mejorar la actitud postural, desarrollar el sistema motriz y sentirte mejor contigo mism@.</p>
  <p><a class="btn ghost" href="/agenda/">Ver horarios</a></p>
  <h4>Clases privadas</h4>
  <p>¿No te van bien los horarios? ¿Quieres elegir la hora y el lugar para practicar y poder disfrutar de la máxima atención de un profesor?</p>
  <p>Lo que estás buscando son las clases particulares, donde te acompañaré a profundizar al máximo en la práctica y donde empezarás a notar todos los beneficios de una forma más rápida.</p>
  <p><a class="btn" href="/contacta/">¡Contáctame!</a></p>

  <div class="gallery two reveal"><img src="/img/studio-1.jpg" alt="Clase de Virayoga en el estudio" loading="lazy"><img src="/img/clase-privada.jpg" alt="Arjuna corrigiendo una postura en una clase privada" loading="lazy"></div>
  <h2 class="quote-title">Retiros</h2>
  <p>¿Necesitas un respiro? ¿Estás cansado/a del día a día y no tienes un momento para ti? Lo que necesitas es un retiro.</p>
  <p>Imagínate un fin de semana en el que solo pienses en ti. Donde puedes conectar contigo, cuidarte, sentirte bien, alimentar tu cuerpo y espíritu con una buena práctica y comida depurativa. ¿Suena bien, verdad?</p>
  <p><a class="btn" href="/contacta/">¡Apúntate aquí!</a></p>

  <div class="gallery two reveal"><img src="/img/meditacion-mar.jpg" alt="Meditación al amanecer junto al mar" loading="lazy"><img src="/img/playa.jpg" alt="Práctica de yoga en la playa" loading="lazy"></div>
  <h2 class="quote-title">Formaciones</h2>
  <h4>Formación de Virayoga</h4>
  <p>¿Buscas una formación de yoga que te aporte algo diferente y que cambie tu vida?</p>
  <p>Esta formación te proporciona las herramientas necesarias para convertirte en instructor/a de Virayoga, a la vez que despiertas tu guerrero/a interno gracias a un trabajo profundo de crecimiento personal. Formación de 200 h.</p>
  <p><a class="btn" href="/virayoga/">¡Quiero saber más!</a></p>

  <h2 class="quote-title">Viaje a India</h2>
  <p>¿Quieres tener una experiencia inolvidable?</p>
  <p>¿Quieres conocer las maravillas de la India? Un lugar donde incluso los más pobres te lo dan todo. Un país que no te deja indiferente. En nuestros viajes visitamos las zonas turísticas pero, sobre todo, vamos a ver la India profunda, donde su cultura y sus gentes te sorprenderán como nunca.</p>
  <div class="gallery reveal"><img src="/img/india-jaipur-2.jpg" alt="Arjuna en Jaipur" loading="lazy"><img src="/img/india-arcos-2.jpg" alt="Virayoga en un palacio de India" loading="lazy"><img src="/img/india-arcos-3.jpg" alt="Postura marcial en India" loading="lazy"></div>
  <p><a class="btn" href="/contacta/">¡Quiero ver más!</a></p>
</article>
{newsletter()}'''
    page('/servicios-de-virayoga/', 'Actividades de Virayoga · Clases, retiros, formación y viajes a India',
         'Yoga con Arjuna se adapta a tus necesidades: clases grupales y privadas de Virayoga y Hatha Yoga, retiros, formación de 200 h y viajes a India.',
         body, hero='cab-actividades.jpg', hero_title='Actividades', crumb='Actividades', image='cab-actividades.jpg')

# ---------------------------------------------------------------- AGENDA
def agenda():
    def card(img, title, html_body):
        return f'<div class="ag-card reveal"><div class="img" style="background-image:url(/img/{img})" role="img" aria-label="{html.escape(title)}"></div><div class="body"><h3>{title}</h3>{html_body}</div></div>'
    mail = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
    wa = f'<a href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener">WhatsApp 619 945 481</a>'
    body = f'''
<div class="wrap content ag-cats">
  <h2 class="cat">Clases online</h2>
  <div class="ag-cards">
    {card('ag-online.jpg', 'Virayoga online', f'<p>Tenemos clases online vía Zoom, con la profesionalidad y la autenticidad de siempre: clases regulares y privadas.</p><p>Las clases se quedan guardadas por si no te va bien la hora. {mail}</p>')}
    {card('ag-cursos.jpg', 'Cursos online', '<p>Namaste warriors, puedes tener cursos online con una gran calidad audiovisual y muy económicos. Son para toda la vida y puedes practicarlos desde cualquier lugar.</p><p><a class="btn" href="/productos/">Ver cursos</a></p>')}
  </div>

  <h2 class="cat">Clases regulares</h2>
  <div class="ag-cards">
    {card('studio-1.jpg', 'Arjuna Yoga Studio', f'<p><strong>Virayoga los miércoles a las 19 h</strong> en Martorelles.</p><p>Reservas por {wa}.</p>')}
    {card('studio-2.jpg', 'Espai Kairos', '<p><strong>Los jueves en Terrassa a las 18:45 h</strong>: iniciación al Vinyasa con Arjuna.</p>')}
    {card('clase-privada.jpg', 'Yoga con Arjuna privadas', '<p>Virayoga, Hatha Yoga, meditación, Reiki y el masaje ayurveda son los pilares de la verdadera esencia de «Arjuna».</p><p>¿No te van bien los horarios? Las clases particulares te permiten elegir hora y lugar y disfrutar de la máxima atención.</p><p><a class="btn" href="/contacta/">Reservar</a></p>')}
  </div>

  <h2 class="cat">Viajes y retiros</h2>
  <div class="ag-cards">
    {card('india-jaipur-2.jpg', 'Viajes a India', f'<p>Tras 17 años de experiencia viajando con grupos, mi intención es mostrarte el verdadero néctar de este país.</p><p>Si India te llama, escríbeme y te cuento. {mail}</p>')}
    {card('ag-street.jpg', 'Street Virayoga', '<p>Práctica de Virayoga gratuita en la Plaça Reial de Barcelona, el primer sábado de cada mes. ¡Solo trae tu esterilla!</p>')}
  </div>

  <h2 class="cat">Próximos eventos</h2>
  <div class="events" data-sheet="{html.escape(AGENDA_CSV)}">
    <div class="event reveal">
      <div class="date">12 dic<br><small style="font-size:.6em">2026 · 11 h</small></div>
      <div><span class="badge">Gratuito</span><h3>Street Virayoga en Plaça Reial (Barcelona)</h3><p>Práctica de Virayoga al aire libre. ¡Solo trae tu esterilla!</p></div>
      <a class="btn" href="mailto:{EMAIL}?subject=Street%20Virayoga%2012%20diciembre">Apuntarme</a>
    </div>
    <div class="event reveal">
      <div class="date">Fechas<br><small style="font-size:.6em">a concretar</small></div>
      <div><h3>Viaje retiro India</h3><p>¡Volvemos a India! Con más de 15 años de experiencia sigo guiando a aventurerxs por este mágico país. ¿Te animas?</p></div>
      <a class="btn" href="/contacta/">Más info</a>
    </div>
    <div class="event reveal">
      <div class="date">2027<br><small style="font-size:.6em">próximamente</small></div>
      <div><h3>Tenerife Virayoga</h3><p>Volvemos como cada año a Tenerife, a nuestra escuela oficial MiYoga, con clases, talleres y concierto.</p></div>
      <a class="btn ghost" href="/contacta/">Avísame</a>
    </div>
  </div>
</div>
{newsletter()}'''
    ev = {"@context": "https://schema.org", "@type": "Event", "name": "Street Virayoga en Plaça Reial",
          "startDate": "2026-12-12T11:00:00+01:00", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
          "eventStatus": "https://schema.org/EventScheduled", "isAccessibleForFree": True,
          "location": {"@type": "Place", "name": "Plaça Reial", "address": "Plaça Reial, Barcelona"},
          "organizer": {"@type": "Person", "name": "Arjuna", "url": DOMAIN + "/"}, "image": DOMAIN + "/img/ag-street.jpg"}
    page('/agenda/', 'Agenda de eventos · Clases, retiros y viajes · Yoga con Arjuna',
         'Clases de Virayoga online y presenciales (Martorelles, Terrassa), Street Virayoga en Barcelona, retiros y viajes a India. Consulta la agenda de Arjuna.',
         body, hero='cab-agenda.jpg', hero_title='Agenda', crumb='Agenda', image='ag-street.jpg', schema=ev)

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
 dict(id='libro-firmado', tag='Libro', title='Libro «Conoce el Virayoga» firmado', img='libro-portada.jpg', book=True,
      desc='La historia de Arjuna y el método Virayoga, firmado y dedicado. Envío a domicilio en España.', price='XX €', stripe=''),
 dict(id='curso-online', tag='Curso online', title='Curso online de Virayoga: las 9 sesiones', img='india-arcos-2.jpg',
      desc='Practica las 9 sesiones del camino del guerrero desde casa, a tu ritmo y para siempre. Vídeos en alta calidad.', price='XX €', stripe=''),
 dict(id='formacion-introduccion', tag='Formación', title='Formación Virayoga · Introducción', img='india-arcos-3.jpg',
      desc='Manual de formación en PDF, vídeos de la sesión 1 (estiramientos, llaves y vaciados) y examen de certificación.', price='XX €', stripe=''),
 dict(id='manual-trabajo', tag='Recurso digital', title='Manual de trabajo Virayoga (PDF)', img='vira-mar.jpg',
      desc='El cuaderno de trabajo del alumno: posturas, pranayamas y meditaciones para acompañar tu práctica.', price='XX €', stripe=''),
 dict(id='bono-clases', tag='Clases', title='Bono de clases privadas', img='clase-privada.jpg',
      desc='Sesiones individuales de Virayoga, Hatha Yoga o meditación, online o presenciales. Tú eliges día y hora.', price='XX €', stripe=''),
 dict(id='reserva-india', tag='Viaje', title='Reserva tu plaza: viaje a India', img='india-jaipur.jpg',
      desc='Paga la señal y asegura tu plaza en el próximo viaje a la India auténtica con Arjuna.', price='XX €', stripe=''),
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
    <p class="lead">El libro, cursos online, material de formación y reservas. Pago seguro con tarjeta, Apple Pay o Google Pay.</p>
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
{testimonials_html()}
{newsletter()}'''
    items = [{"@type": "ListItem", "position": i + 1, "url": f"{DOMAIN}/productos/#{p['id']}", "name": p['title']} for i, p in enumerate(PRODUCTS)]
    page('/productos/', 'Productos y recursos · Libro, cursos online y formación · Yoga con Arjuna',
         'Compra el libro firmado «Conoce el Virayoga», cursos online, material de formación y bonos de clases con Arjuna. Pago seguro.',
         body, hero='hero-6.jpg', hero_title='Productos', crumb='Productos', image='libro-portada.jpg',
         schema={"@context": "https://schema.org", "@type": "ItemList", "itemListElement": items})

# ---------------------------------------------------------------- CONTACTA
def contacta():
    body = f'''
<div class="wrap content">
  <div class="contact-grid">
    <div class="contact-info reveal">
      <h2 class="quote-title" style="margin-top:0">Contacta conmigo</h2>
      <p>¡Hola! Ponte en contacto conmigo para saber más de cualquiera de mis servicios, dudas y comentarios.</p>
      <p>Te contestaré tan pronto como me sea posible. ¡Muchas gracias!</p>
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
        <option>Clases</option><option>Clases privadas</option><option>Formación Virayoga</option><option>Retiros</option><option>Viaje a India</option><option>Libro y productos</option><option>Prensa</option><option>Otro</option>
      </select>
      <label for="c-mensaje">Mensaje</label><textarea id="c-mensaje" name="mensaje" required></textarea>
      <label class="check"><input type="checkbox" name="acepto" required> <span>He leído y acepto la <a href="/politica-de-privacidad/">política de privacidad</a>.</span></label>
      <button class="btn" type="submit">Enviar</button>
    </form>
  </div>
</div>'''
    page('/contacta/', 'Contacta conmigo · Yoga con Arjuna · Virayoga, despierta tu poder interno',
         'Contacta con Arjuna para recibir información de clases de Virayoga, formación, retiros, viajes a India y productos.',
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
        ('Con atención 100 % personal', ('modo', 'privada')), ('Viviendo una experiencia: viaje o retiro', ('modo', 'viaje'))]),
    ('¿Qué inversión te encaja ahora mismo?', [
        ('Empezar con algo económico', ('pres', 'bajo')), ('Un curso o un bono de clases', ('pres', 'medio')),
        ('Una formación completa', ('pres', 'alto')), ('Prefiero hablarlo antes con Arjuna', ('pres', 'hablar'))]),
]

# Recursos que puede recomendar el test (id de PRODUCTS o páginas de la web)
QUIZ_RES = {
    'curso': dict(title='Curso online de Virayoga: las 9 sesiones', img='india-arcos-2.jpg', url='/productos/#curso-online',
                  why='Practica desde casa las 9 sesiones del camino del guerrero. Empieza por la sesión {n}, {name}, que es la que más necesitas ahora.'),
    'manual': dict(title='Manual de trabajo Virayoga (PDF)', img='vira-mar.jpg', url='/productos/#manual-trabajo',
                   why='Ya conoces el Virayoga: el manual te ayuda a profundizar en la sesión {n}, {name}, con sus posturas, pranayama y meditación.'),
    'formacion': dict(title='Formación de profesores de Virayoga', img='india-arcos-3.jpg', url='/virayoga/',
                      why='Quieres enseñar: la formación de 200 h te lleva por las 9 sesiones, también la de {name}, para vivirlas y transmitirlas.'),
    'intro': dict(title='Formación Virayoga · Introducción', img='india-arcos-3.jpg', url='/productos/#formacion-introduccion',
                  why='La forma más económica de empezar a formarte: manual en PDF, vídeos de la sesión 1 y examen de certificación.'),
    'clase': dict(title='Clases regulares con Arjuna', img='studio-1.jpg', url='/agenda/',
                  why='Practica en grupo y en persona. Cuéntale a Arjuna que tu etapa es {name} y la trabajaréis juntos.'),
    'privada': dict(title='Bono de clases privadas', img='clase-privada.jpg', url='/productos/#bono-clases',
                    why='Sesiones a tu medida, online o presenciales, centradas en la etapa de {name}.'),
    'viaje': dict(title='Viajes y retiros con Arjuna', img='india-jaipur.jpg', url='/agenda/',
                  why='Vive el Virayoga fuera de la rutina: un viaje o retiro es el mejor espacio para trabajar la etapa de {name}.'),
    'libro': dict(title='Libro «Conoce el Virayoga»', img='libro-portada.jpg', url='/mi-libro/',
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
BLOG_CATS = [('practica', 'Clases y prácticas'), ('directo', 'Directos'), ('articulo', 'Artículos')]

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
            'directo': ('arjuna-templo.jpg', 'Los directos de Instagram', 'Las clases y charlas en directo de Arjuna, ahora guardadas aquí para verlas cuando quieras.'),
            'articulo': ('meditacion-mar.jpg', 'Artículos', 'Textos sobre Virayoga, meditación, filosofía del yoga y viajes.')}
    have = {p[0] for p in POSTS}
    for t, (img, title, desc) in soon.items():
        if t not in have or t == 'practica':
            cards += f'''<article class="post reveal soon-card" data-type="{t}"><div class="img" style="background-image:url(/img/{img})" role="img" aria-label="{html.escape(title)}"></div>
  <div class="body"><span class="tag">{dict(BLOG_CATS)[t]}</span><h3>{title}</h3><p>{desc}</p><span class="soon">Próximamente</span></div></article>'''
    filters = '<button class="on" data-f="all">Todo</button>' + ''.join(f'<button data-f="{k}">{v}</button>' for k, v in BLOG_CATS)
    uploads = 'UU' + YT_CHANNEL_ID[2:]
    body = f'''
<section class="wrap content blog">
  <div class="narrow center">
    <h2 class="script-title">La biblioteca del guerrero</h2>
    <p class="lead">Clases, prácticas, directos y artículos de Arjuna para practicar Virayoga desde donde estés.</p>
  </div>

  <div class="yt-block reveal">
    <div class="yt-text">
      <span class="yt-logo">{ICON['yt']}</span>
      <h3>Mi canal de YouTube</h3>
      <p>Aquí tienes los últimos vídeos del canal. Suscríbete para no perderte ninguna práctica nueva.</p>
      <p><a class="btn yt-btn" href="{YT_CHANNEL}?sub_confirmation=1" target="_blank" rel="noopener">{ICON['yt']} Suscríbete</a> &nbsp; <a class="btn ghost" href="{YT_CHANNEL}/videos" target="_blank" rel="noopener">Ver todos los vídeos</a></p>
    </div>
    <div class="video wide" data-yt-list="{uploads}" data-title="Últimos vídeos de Yoga con Arjuna" style="background-image:url(/img/vira-mar.jpg)">
      <button aria-label="Ver los últimos vídeos del canal">{ICON['play']}</button><div class="cap">Últimos vídeos del canal</div>
    </div>
  </div>

  <div class="filters" role="tablist">{filters}</div>
  <div class="posts">{cards}</div>
</section>
{newsletter('newsletter-blog')}'''
    page('/blog/', 'Blog y videoteca · Yoga con Arjuna · Clases, directos y artículos de Virayoga',
         'Clases y prácticas de Virayoga en vídeo, directos de Instagram y artículos de Arjuna sobre yoga, meditación y filosofía.',
         body, hero='vira-mar.jpg', hero_title='Blog', crumb='Blog', image='vira-mar.jpg')

# ---------------------------------------------------------------- LEGALES Y GRACIAS
def legales():
    # Datos del titular pendientes: se marcan en amarillo para rellenarlos cuando el cliente los facilite
    def X(t): return f'<mark class="todo">[XXXX {t}]</mark>'
    TIT, NIF, DIR, CIUDAD = X('nombre y apellidos del titular'), X('NIF'), X('dirección completa'), X('ciudad')
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
<li><strong>Testimonios de Instagram:</strong> el servicio de inserción de Instagram (Meta) puede instalar sus propias cookies al cargar los vídeos.</li>
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
''')

if __name__ == '__main__':
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(HERE, 'static'), OUT, dirs_exist_ok=True)
    shutil.copytree(os.path.join(HERE, 'img'), os.path.join(OUT, 'img'))
    if os.path.isdir(os.path.join(HERE, 'video')):
        shutil.copytree(os.path.join(HERE, 'video'), os.path.join(OUT, 'video'))
    home(); sobre(); libro(); virayoga(); actividades(); agenda(); prensa(); productos(); blog(); test_guerrero(); contacta(); legales()
    urls = [DOMAIN + p for p in ['/', '/sobre-mi-creador-de-virayoga/', '/mi-libro/', '/virayoga/', '/servicios-de-virayoga/',
                                 '/agenda/', '/prensa/', '/productos/', '/blog/', '/test-guerrero/', '/contacta/', '/aviso-legal/', '/politica-de-privacidad/',
                                 '/politica-de-cookies/', '/condiciones-de-compra/']]
    extras(urls)
    print('OK ->', os.path.abspath(OUT))
