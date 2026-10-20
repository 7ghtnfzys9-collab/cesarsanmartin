# Web de César San Martín (www.cesarsanmartin.com)

Última actualización: 20-10-2026. **Al empezar una sesión nueva sobre la web, Claude lee primero este archivo.**

## Qué cambió el 20-10-2026

Antes la web era un solo archivo (`index.html`) con todas las secciones escondidas y enlaces «#»: para Google era una única página. Ahora cada sección tiene su propia dirección, en español y en inglés:

| Sección | Español | Inglés |
|---|---|---|
| Inicio | `/` | `/en/` |
| Mi historia | `/biografia/` | `/en/biography/` |
| Agenda | `/agenda/` | `/en/schedule/` |
| Vídeos y fotos | `/videos/` | `/en/videos/` |
| Noticias | `/noticias/` | `/en/news/` |
| Prensa | `/prensa/` | `/en/press/` |
| Contacto | `/contacto/` | `/en/contact/` |

SEO incluido en cada página: título y descripción propios, dirección canónica, enlaces entre idiomas (hreflang), etiquetas para compartir en redes (Open Graph), datos estructurados para Google (persona, conciertos de la agenda, vídeos), `sitemap.xml` y `robots.txt`. El diseño es el mismo de antes (`estilos-base.css` es el CSS original sin tocar).

Vídeos: los 14 vídeos públicos del canal están en `/videos/`, agrupados en Ópera, Zarzuela y Conciertos. Se reproducen dentro de la web al pulsar (con youtube-nocookie, que no pone cookies hasta que se pulsa) y cada uno enlaza también a YouTube.

Novedades automáticas: la portada y `/noticias/` muestran lo último de YouTube (incluidos los Shorts) y, cuando se active, de Instagram. GitHub regenera la web **cada día a las 06:07 (hora peninsular de invierno)** y cada vez que se suben cambios.

## Estructura de la carpeta

```
cesarsanmartin/                 ← repositorio de GitHub (7ghtnfzys9-collab/cesarsanmartin)
├─ SUBIR_WEB_CESAR.command      ← doble clic para publicar
├─ LEEME_web.md                 ← este archivo
├─ _fuente/
│  ├─ build.py                  ← genera la web (solo Python 3 de serie)
│  ├─ ajustes.json              ← dominio, canal, Instagram, formulario…
│  ├─ estilos-base.css / estilos-extra.css
│  ├─ img/                      ← fotos de la web
│  └─ datos/                    ← TODO el contenido, en JSON
│     ├─ agenda.json  biografia.json  noticias.json  prensa.json  videos.json
│     └─ redes.json             ← copia de lo último de YouTube/Instagram (se rehace sola)
└─ .github/workflows/publicar.yml ← la tarea diaria de GitHub
```

`docs/` es la web ya generada; no se sube (GitHub la genera él mismo).

## Cómo se cambia algo

- **Una función nueva en la agenda**: añadir un bloque en `datos/agenda.json` con `inicio` y `fin` (AAAA-MM-DD). Pasa sola de «Próximas» a «Anteriores» cuando acaba.
- **Un vídeo nuevo**: añadir un bloque en `datos/videos.json` arriba de su grupo (`opera`, `zarzuela` o `concierto`). En las novedades de redes aparece solo, sin hacer nada.
- **Una crítica o noticia**: `datos/prensa.json` o `datos/noticias.json`.
- Luego doble clic en `SUBIR_WEB_CESAR.command`.

## Puesta en marcha (una sola vez) — PENDIENTE

1. **Primer envío** con `SUBIR_WEB_CESAR.command` (sin la tarea diaria: el token de César solo tiene el permiso «repo»). La tarea diaria `.github/workflows/publicar.yml` la crea Claude en la web de GitHub desde el Chrome de César; después, el `.command` la trae al Mac con cada envío.
2. **GitHub → repositorio cesarsanmartin → Settings → Pages** (el repositorio debe ser público: GitHub Pages es gratis solo en repositorios públicos) **→ Source: «GitHub Actions»**. En «Custom domain» poner `www.cesarsanmartin.com` y, cuando lo permita, marcar «Enforce HTTPS».
3. **IONOS → Dominios → cesarsanmartin.com → DNS**. Comprobado el 20-10-2026: el DNS es de IONOS y el dominio (con y sin www) apunta a 217.160.0.223, un servidor web de IONOS (red «ionos-inf») que sigue sirviendo la web antigua (archivo del 22-7-2026). GitHub Pages ya estaba activado en el repositorio con el dominio `cesarsanmartin.com`, pero no recibe visitas porque el DNS no apunta a GitHub. Cambios a hacer:
   - `www` → registro CNAME a `7ghtnfzys9-collab.github.io`
   - `@` (dominio sin www) → cuatro registros A: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153 (sustituyen al A actual de IONOS)
   - No tocar los registros MX (correo) si los hay.
4. **Google Search Console**: dar de alta `https://www.cesarsanmartin.com`, verificar y enviar `sitemap.xml`.
5. **Instagram automático (opcional)**: crear cuenta gratuita en behold.so, conectar @cesarsanmartin.baritono, crear un feed tipo «JSON» y pegar su dirección en `ajustes.json` → `behold_feed`. Plan gratuito: 6 publicaciones, se actualiza una vez al día, 1.200 consultas al mes (la web consulta una vez al día: unas 30).

## Avisos

- GitHub pausa las tareas diarias si el repositorio pasa 60 días sin ningún cambio; manda un correo antes. Basta con pulsar «Enable workflow» en la pestaña Actions o subir cualquier cambio.
- Si YouTube o Instagram fallan un día, la web se publica con la última copia buena (`redes.json`).
- **Dato pendiente de confirmar por César**: el concierto de Málaga del 16-10-2026 (Auditorio Edgar Neville, Filarmónica de Málaga) está en los vídeos pero no en la agenda; no se ha añadido sin su confirmación.
