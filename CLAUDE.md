# Web de Yoga con Arjuna (yogaconarjuna.com)

Web estática generada con Python. No es WordPress.

## Cómo funciona
- Todo el contenido y las páginas están en `src/build.py` (listas PRODUCTS, PRESS, POSTS, QUIZ, STAGES… y una función por página).
- Estilos: `src/static/css/style.css`. Interacciones: `src/static/js/main.js`.
- Fotos: `src/img/`. Vídeos de testimonios: `src/video/`.
- `python3 src/build.py` genera la web en `site/` (no se sube a GitHub).
- Netlify construye y publica sola cada vez que hay un cambio en la rama principal de GitHub (`netlify.toml`).

## Cambios habituales
- **Producto o precio:** editar la lista `PRODUCTS` (campo `price` y `stripe` = enlace de pago de Stripe).
- **Vídeo o directo en el blog:** añadir una línea a `POSTS` (`'practica'` o `'directo'` + id de YouTube).
- **Nota de prensa:** añadir una línea a `PRESS`.
- **Textos legales:** función `legales()`; los datos pendientes están marcados como `[XXXX …]`.

## Reglas
- Antes de publicar, generar la web y revisar en móvil y escritorio.
- No cambiar las direcciones de las páginas (vienen de la web antigua y tienen redirecciones en `_redirects`).
- Textos de la web en español.

## Agenda desde Google Sheets
La sección «Próximos eventos» de /agenda/ se rellena sola desde la hoja «Agenda web Yoga con Arjuna» (publicada como CSV, constante `AGENDA_CSV` en `src/build.py`; el código está en `src/static/js/main.js`).
Columnas: fecha inicio, fecha fin, actividad, lugar, descripción, precio, foto (enlace), enlace de reserva. Si «fecha inicio» es un texto (p. ej. «Por concretar»), el evento sale al final de la lista con ese texto en lugar de la fecha. Las filas que empiezan por «EJEMPLO» y las fechas pasadas no se muestran. Si la hoja no tiene ningún evento válido, se ve la lista fija del código.
