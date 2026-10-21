# Web de César San Martín (www.cesarsanmartin.com)

Última actualización: 21-10-2026. **Al empezar una sesión nueva sobre la web, Claude lee primero este archivo.**

## 21-10-2026 — Agenda corregida (pendiente de publicar)

Se buscaron en internet (Operabase, programas, críticas) las fechas que faltaban en `datos/agenda.json`. Ahora todas las funciones tienen fecha exacta. Cambios aprobados por César:
- Años corregidos según las fuentes: Carmen → 2 y 4 feb 2024, Baluarte (Pamplona); Manon → 28-30 ene 2022; Bohème/Schaunard (Opus Lírica) → 2-4 mar 2018, Kursaal; Zauberflöte → 22-23 feb 2019, Kursaal; Barbiere → gira de Òpera Catalunya, 20 oct-14 nov 2021; María Moliner → 16 y 18 jun 2022; Bohème/Marcello (Luis Mariano) → 22-23 abr 2023, Irun; Barbieri 200 años → 29 jun 2024.
- Fechas añadidas: Policías y ladrones 18-27 nov 2022; Luisa Fernanda Santander 29-30 abr 2022; Butterfly Irun 30 nov-1 dic 2024.
- Novena: se dejan dos (OCNE, Auditorio Nacional, 3-4 feb 2023; Juan March, 18 abr 2024).
- Quitados: Pagliacci Málaga 2022 (cantó Carlos Daza), «Concierto de Zarzuela» Real Coliseo 29-6-2024 y Carmina Las Palmas 2022 (duplicados).
- «Real Coliseo de Carlos III, San Lorenzo de El Escorial» (nombre corregido).
- Copia anterior en `Web César/to delete/agenda_antes_21-10-2026.json`.
- **Sin datos oficiales**: sala del Oratorio de Navidad en Cracovia (18-19 dic 2026) y el concierto de Málaga del 16-10-2026 (no aparece en ninguna fuente pública). Esperando que César dé los datos.
- **Segunda revisión (coherencia web, mismo día)**, aprobada por César: agenda cotejada con Operabase 2018-2026, programas oficiales y prensa.
  - Corregido: Tabernera 2026 → Teatro Mayor (no el Colón); Goyescas 24 ene-1 feb 2026; El vizconde Bogotá 28 feb-1 mar 2026 (+ Medellín 5 mar); papeles: El vizconde = Don Alfonso / La Baronesa, Turandot = Un mandarín, Pericca e Varrone = Varrone.
  - Añadido: concierto de Málaga 16-10-2026 (datos de César en las notas de redes; sin fuente pública) y 33 funciones de Operabase que faltaban (Rigoletto/Marullo Teatro Real 2023-24, Verbena Zarzuela sep-oct 2026, Doña Francisquita, Las golondrinas, Pan y toros, The Magic Opal, Benamor 2021, Pagliacci A Coruña 2021, Los Gavilanes 2018-19, Pierre de Médicis 2025…). Luisa Fernanda Zarzuela 2021 (sustitución de Juan Jesús Rodríguez, dicho por César; sin fechas exactas).
  - Descartado: Misa de Rutter 2018 añadida después (César confirma que la cantó; Operabase le pone como director y sitúa el Riojafórum en Toledo: errores de Operabase), (Il viaggio a Reims Les Arts 2020: añadido después; César confirma que se hizo y solo se canceló la última función por la covid; sin fecha final exacta), Pagliacci Málaga 2022 (César confirma que no lo cantó).
  - Dudas que quedan: Los Gavilanes Bogotá 2018 (Operabase dice 29 oct-7 nov; un artículo de El Tiempo habla de estreno el 29 sep); Tabernera Zarzuela 2025 y Orlando furioso 2025 pueden tener más funciones (Operabase: 4-22 jun y 14-22 nov); no hay fuente pública de Carmina Getafe 3-7-2026 ni de la Verbena de Oviedo 16-5-2026.
  - Noticias: Policías y ladrones fechada «Noviembre 2022».
- Dato útil: Operabase tiene la lista de funciones de César por año (operabase.com/cesar-san-martin-a3577/AAAA/performances), con algún error de sala.

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

## Estado al cerrar la sesión del 20-10-2026 (leer primero)

**Hecho hoy:**
- Web nueva enviada a GitHub (doble clic de César en `SUBIR_WEB_CESAR.command`).
- Tarea diaria `.github/workflows/publicar.yml` creada por Claude en la web de GitHub (el token de César solo tiene permiso «repo»; si algún día hay que cambiar ese archivo, hacerlo también desde la web de GitHub). Primera ejecución correcta: «YouTube: 15 vídeos». Avisos de GitHub sobre Node 20 y Ubuntu 26: informativos, sin efecto.
- GitHub → Settings → Pages: fuente «GitHub Actions» y dominio `www.cesarsanmartin.com`. «DNS check successful».
- DNS de IONOS cambiado (con el visto bueno de César). Quedan: TXT @ verificación de Google (sin tocar); A @ → 185.199.108.153, .109.153, .110.153, .111.153; CNAME www → 7ghtnfzys9-collab.github.io. IONOS desactivó al guardar los registros del alojamiento: A/AAAA @ y www (217.160.0.223 y 2001:8d8:100f:f000::2dc) y TXT _dep_ws_mutex. Para volver atrás: «Ajustar destino» → Webhosting en IONOS. No había registros de correo (MX).
- DNS público (Google) ya apunta a GitHub. A las 15:20 del 20-10 el certificado HTTPS de GitHub aún se estaba emitiendo y el Chrome de César mostraba error de seguridad: normal durante la transición.

**Pendiente (por orden):**
1. HECHO 21-10-2026: el certificado se había atascado; se quitó y volvió a poner el dominio en GitHub → Pages y salió al momento. «Enforce HTTPS» activado. Comprobado en el Chrome de César: portada, /videos/ (14 vídeos), /noticias/ (6 novedades), /en/, /sitemap.xml y robots.txt cargan bien; cesarsanmartin.com sin www lleva a https://www.
   - Ese día el feed RSS de YouTube daba error 404 (fallo temporal conocido de YouTube, suele durar horas). La web se publica con la última copia buena, así que el Short de Adriana del 20-10 aparecerá cuando YouTube vuelva a servir el feed.
   - La tarea programada de las 07:07 no se había ejecutado aún el 21-10 a las 08:30 (GitHub retrasa o salta a veces las tareas programadas, sobre todo las recién creadas). Se lanzó a mano (Actions → Publicar la web → Run workflow) y funcionó. Comprobar en los próximos días que aparecen ejecuciones «scheduled».
3. Google Search Console: dar de alta `https://www.cesarsanmartin.com` (ya hay un TXT de verificación de Google en el DNS; comprobar si es de Search Console) y enviar `sitemap.xml`.
4. Instagram automático (opcional): behold.so (ver abajo).
5. Cuando todo funcione: valorar dar de baja el alojamiento de IONOS si se paga aparte (el contrato que aparece es «IONOS Pack Dominio», n.º 63925398; comprobar qué incluye antes de decidir).
6. Preguntar a César si se añade a la agenda el concierto de Málaga del 16-10-2026.

## Instagram automático (opcional)

Crear cuenta gratuita en behold.so, conectar @cesarsanmartin.baritono, crear un feed tipo «JSON» y pegar su dirección en `_fuente/ajustes.json` → `behold_feed`. Plan gratuito: 6 publicaciones, se actualiza una vez al día, 1.200 consultas al mes (la web consulta una vez al día: unas 30).

## Avisos

- GitHub pausa las tareas diarias si el repositorio pasa 60 días sin ningún cambio; manda un correo antes. Basta con pulsar «Enable workflow» en la pestaña Actions o subir cualquier cambio.
- Si YouTube o Instagram fallan un día, la web se publica con la última copia buena (`redes.json`).
- **Dato pendiente de confirmar por César**: el concierto de Málaga del 16-10-2026 (Auditorio Edgar Neville, Filarmónica de Málaga) está en los vídeos pero no en la agenda; no se ha añadido sin su confirmación.
