#!/usr/bin/env python3
"""
Genera la web de César San Martín (www.cesarsanmartin.com) en la carpeta docs/.

Uso:
    python3 _fuente/build.py            # genera la web con los datos guardados
    python3 _fuente/build.py --redes    # antes, descarga lo último de YouTube e Instagram

Solo usa la biblioteca estándar de Python 3 (no hay que instalar nada).
Todo el contenido está en _fuente/datos/*.json; las páginas se crean a partir de ahí.
"""
import datetime as dt
import html
import json
import os
import re
import shutil
import sys
import urllib.request
import xml.etree.ElementTree as ET

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FUENTE = os.path.join(RAIZ, "_fuente")
DATOS = os.path.join(FUENTE, "datos")
SALIDA = os.path.join(RAIZ, "docs")


def leer(nombre):
    with open(os.path.join(DATOS, nombre), encoding="utf-8") as f:
        return json.load(f)


with open(os.path.join(FUENTE, "ajustes.json"), encoding="utf-8") as f:
    AJ = json.load(f)
DOM = AJ["dominio"].rstrip("/")
HOY = dt.date.today()
e = html.escape  # escapar texto externo (redes)

# ---------------------------------------------------------------- páginas
# clave: (ruta ES, ruta EN, menú ES, menú EN)
PAGINAS = {
    "inicio":   ("/", "/en/", "Inicio", "Home"),
    "bio":      ("/biografia/", "/en/biography/", "Mi historia", "My Story"),
    "agenda":   ("/agenda/", "/en/schedule/", "Agenda", "Schedule"),
    "videos":   ("/videos/", "/en/videos/", "Vídeos y fotos", "Videos & Photos"),
    "noticias": ("/noticias/", "/en/news/", "Noticias", "News"),
    "prensa":   ("/prensa/", "/en/press/", "Prensa", "Press"),
    "contacto": ("/contacto/", "/en/contact/", "Contacto", "Contact"),
}
METAS = {
    "inicio": ("César San Martín, barítono · Ópera y zarzuela",
               "Web oficial del barítono César San Martín: ópera y zarzuela. Agenda de actuaciones, vídeos, críticas de prensa y contacto para contratación.",
               "César San Martín, baritone · Opera and zarzuela",
               "Official website of baritone César San Martín: opera and Spanish zarzuela. Upcoming performances, videos, press reviews and booking contact."),
    "bio": ("Biografía · César San Martín, barítono",
            "La historia de César San Martín: del coro infantil y el piano a la Escuela Superior de Canto de Madrid, el Teatro Real, el Teatro de la Zarzuela y escenarios internacionales.",
            "Biography · César San Martín, baritone",
            "The story of César San Martín: from children's choir and piano to the Escuela Superior de Canto de Madrid, the Teatro Real, the Teatro de la Zarzuela and international stages."),
    "agenda": ("Agenda y próximas actuaciones · César San Martín, barítono",
               "Próximas funciones y conciertos del barítono César San Martín, y el archivo de actuaciones en ópera, zarzuela y concierto desde 2021.",
               "Schedule and upcoming performances · César San Martín, baritone",
               "Upcoming opera, zarzuela and concert performances by baritone César San Martín, plus an archive of past engagements since 2021."),
    "videos": ("Vídeos y fotos · César San Martín, barítono",
               "Vídeos de César San Martín en directo: arias de ópera, romanzas de zarzuela y conciertos (Rigoletto, Il barbiere di Siviglia, Luisa Fernanda, Carmina Burana…). Galería de fotos.",
               "Videos and photos · César San Martín, baritone",
               "Live videos of César San Martín: opera arias, zarzuela romanzas and concerts (Rigoletto, Il barbiere di Siviglia, Luisa Fernanda, Carmina Burana…). Photo gallery."),
    "noticias": ("Noticias · César San Martín, barítono",
                 "Lo último de César San Martín en YouTube e Instagram, entrevistas, nominaciones y noticias sobre sus actuaciones.",
                 "News · César San Martín, baritone",
                 "The latest from César San Martín on YouTube and Instagram, plus interviews, nominations and news about his performances."),
    "prensa": ("Críticas y prensa · César San Martín, barítono",
               "Qué dice la crítica de César San Martín: reseñas de Codalario, Bachtrack, Ópera Actual, Opera World, Scherzo, Pro Ópera y Platea Magazine.",
               "Press reviews · César San Martín, baritone",
               "What critics say about César San Martín: reviews from Codalario, Bachtrack, Ópera Actual, Opera World, Scherzo, Pro Ópera and Platea Magazine."),
    "contacto": ("Contacto y contratación · César San Martín, barítono",
                 "Contacta con César San Martín para contratación artística, prensa u otras consultas.",
                 "Contact and booking · César San Martín, baritone",
                 "Contact César San Martín for artist booking, press or other enquiries."),
}

T = {  # textos de la interfaz
    "es": {"barítono": "Barítono", "sigue": "Sigue leyendo", "agenda": "Agenda", "proximas": "Próximas actuaciones",
           "ver_agenda": "Ver agenda completa", "sin_proximas": "Pronto anunciaremos nuevas fechas.",
           "videos": "Vídeos", "en_escena": "En escena",
           "videos_txt": "Fragmentos de actuaciones en directo desde algunos de los principales escenarios líricos.",
           "ver_videos": "Ver todos los vídeos", "sigueme": "Sígueme",
           "insta_txt": "Últimos momentos en escena, ensayos y novedades de la carrera en tiempo real.",
           "ultimo": "Lo último en mis redes", "mas_noticias": "Más noticias", "ver_yt": "Ver en YouTube ↗",
           "ver_insta": "Ver en Instagram ↗", "reproducir": "Reproducir", "mas_canal": "Más vídeos en el canal de YouTube",
           "canal": "Ver canal completo ↗", "fotos": "Fotos", "galeria": "Galería", "retratos": "Retratos",
           "mas_retratos": "Ver más retratos", "menos_retratos": "Ver menos", "escena": "En escena", "foto_de": "Foto", "ampliar": "Ampliar foto", "cerrar": "Cerrar", "anterior": "Anterior", "siguiente": "Siguiente",
           "noticias": "Noticias", "entrevistas": "Entrevistas y prensa", "prensa": "Prensa",
           "criticas": "Críticas", "contacto": "Contacto", "nombre": "Nombre", "asunto": "Asunto",
           "mensaje": "Mensaje", "enviar": "Enviar mensaje", "motivo": "Selecciona el motivo",
           "contratacion": "Contratación artística", "otro": "Otro", "ph_nombre": "Tu nombre",
           "ph_email": "tu@email.com", "ph_msg": "Escribe tu mensaje aquí…",
           "encuentrame": "También puedes encontrarme en", "trayectoria": "Trayectoria",
           "historia": "Mi historia", "actuaciones": "Actuaciones", "archivo": "Actuaciones anteriores",
           "solista": "Barítono solista", "redes_vacio": "Sigue mis novedades en",
           "conciertos": "Conciertos", "opera": "Ópera", "zarzuela": "Zarzuela",
           "conciertos_txt": "Arias y obras sinfónico-corales en concierto.",
           "opera_txt": "Producciones escénicas de ópera.", "zarzuela_txt": "Producciones escénicas de zarzuela.",
           "insta_agenda": "Sigue <strong>@{u}</strong> en Instagram para ver las últimas novedades de la agenda en tiempo real.",
           "ver_instagram": "Ver Instagram ↗", "derechos": "César San Martín — Barítono",
           "no_encontrada": "Página no encontrada", "volver": "Volver al inicio",
           "idioma": "Idioma", "menu": "Menú", "papel": "Papel"},
    "en": {"barítono": "Baritone", "sigue": "Keep reading", "agenda": "Schedule", "proximas": "Upcoming performances",
           "ver_agenda": "Full schedule", "sin_proximas": "New dates will be announced soon.",
           "videos": "Videos", "en_escena": "On stage",
           "videos_txt": "Live performance highlights from some of the leading opera houses.",
           "ver_videos": "Watch all videos", "sigueme": "Follow me",
           "insta_txt": "Latest moments on stage, rehearsals and career news in real time.",
           "ultimo": "Latest on social media", "mas_noticias": "More news", "ver_yt": "Watch on YouTube ↗",
           "ver_insta": "View on Instagram ↗", "reproducir": "Play", "mas_canal": "More videos on the YouTube channel",
           "canal": "Full YouTube channel ↗", "fotos": "Photos", "galeria": "Gallery", "retratos": "Portraits",
           "mas_retratos": "More portraits", "menos_retratos": "Show less", "escena": "On stage", "foto_de": "Photo", "ampliar": "Enlarge photo", "cerrar": "Close", "anterior": "Previous", "siguiente": "Next",
           "noticias": "News", "entrevistas": "Interviews & press", "prensa": "Press",
           "criticas": "Reviews", "contacto": "Contact", "nombre": "Name", "asunto": "Subject",
           "mensaje": "Message", "enviar": "Send message", "motivo": "Select a reason",
           "contratacion": "Artist booking", "otro": "Other", "ph_nombre": "Your name",
           "ph_email": "your@email.com", "ph_msg": "Write your message here…",
           "encuentrame": "You can also find me at", "trayectoria": "Career highlights",
           "historia": "My Story", "actuaciones": "Performances", "archivo": "Past performances",
           "solista": "Baritone soloist", "redes_vacio": "Follow my news on",
           "conciertos": "Concerts", "opera": "Opera", "zarzuela": "Zarzuela",
           "conciertos_txt": "Arias and symphonic-choral works in concert.",
           "opera_txt": "Staged opera productions.", "zarzuela_txt": "Staged zarzuela productions.",
           "insta_agenda": "Follow <strong>@{u}</strong> on Instagram for the latest schedule news in real time.",
           "ver_instagram": "Instagram ↗", "derechos": "César San Martín — Baritone",
           "no_encontrada": "Page not found", "volver": "Back to home",
           "idioma": "Language", "menu": "Menu", "papel": "Role"},
}

MES_ES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
MES_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

PLAY_SVG = ('<svg viewBox="0 0 68 48" aria-hidden="true"><path d="M66.5 7.7a8.5 8.5 0 0 0-6-6C56 0 34 0 34 0S12 0 7.5 1.7a8.5 8.5 0 0 0-6 6C0 12.1 0 24 0 24s0 '
            '11.9 1.5 16.3a8.5 8.5 0 0 0 6 6C12 48 34 48 34 48s22 0 26.5-1.7a8.5 8.5 0 0 0 6-6C68 35.9 68 24 68 24s0-11.9-1.5-16.3z" fill="#fff" fill-opacity=".9"/>'
            '<path d="M27 34l18-10-18-10v20z" fill="#b07253"/></svg>')


def ruta(clave, lang):
    return PAGINAS[clave][0 if lang == "es" else 1]


def fecha_corta(iso, lang):
    d = dt.date.fromisoformat(iso[:10])
    return f"{d.day} {(MES_ES if lang == 'es' else MES_EN)[d.month - 1]} {d.year}"


def rango(a, lang):
    """Texto de fechas de una función de la agenda."""
    M = MES_ES if lang == "es" else MES_EN
    if not a.get("inicio"):
        ft = a["fecha_texto"]
        return f"{ft} {a['anio']}" if ft != str(a["anio"]) else ft
    i, f = dt.date.fromisoformat(a["inicio"]), dt.date.fromisoformat(a["fin"] or a["inicio"])
    if i == f:
        return f"{i.day} {M[i.month-1]} {i.year}"
    if i.month == f.month:
        return f"{i.day}–{f.day} {M[i.month-1]} {i.year}"
    return f"{i.day} {M[i.month-1]} – {f.day} {M[f.month-1]} {f.year}"


def jpeg_tam(ruta_img):
    """(ancho, alto) de un JPEG sin dependencias externas."""
    with open(ruta_img, "rb") as f:
        datos = f.read()
    i = 2
    while i < len(datos):
        if datos[i] != 0xFF:
            i += 1
            continue
        marca = datos[i + 1]
        if marca in (0xC0, 0xC1, 0xC2):
            alto = int.from_bytes(datos[i + 5:i + 7], "big")
            ancho = int.from_bytes(datos[i + 7:i + 9], "big")
            return ancho, alto
        largo = int.from_bytes(datos[i + 2:i + 4], "big")
        i += 2 + largo
    return None, None


def img(src, alt, cls="", lazy=True, extra=""):
    w, h = jpeg_tam(os.path.join(FUENTE, src.lstrip("/")))
    tam = f' width="{w}" height="{h}"' if w else ""
    lz = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    c = f' class="{cls}"' if cls else ""
    return f'<img src="{src}" alt="{alt}"{tam}{lz}{c}{extra}>'


# ---------------------------------------------------------------- redes
def descargar(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (web cesarsanmartin.com)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def leer_youtube(xml_bytes):
    ns = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015",
          "media": "http://search.yahoo.com/mrss/"}
    raiz = ET.fromstring(xml_bytes)
    items = []
    for en in raiz.findall("a:entry", ns):
        vid = en.findtext("yt:videoId", default="", namespaces=ns)
        enlace = en.find("a:link[@rel='alternate']", ns)
        url = enlace.get("href") if enlace is not None else f"https://www.youtube.com/watch?v={vid}"
        items.append({
            "red": "youtube", "id": vid, "url": url,
            "titulo": en.findtext("a:title", default="", namespaces=ns).strip(),
            "fecha": en.findtext("a:published", default="", namespaces=ns),
            "imagen": f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",
            "short": "/shorts/" in url,
        })
    return items


def leer_behold(js):
    items = []
    for p in js.get("posts", []):
        tam = p.get("sizes") or {}
        imagen = (tam.get("medium") or tam.get("small") or {}).get("mediaUrl") or p.get("thumbnailUrl") or p.get("mediaUrl")
        texto = (p.get("prunedCaption") or p.get("caption") or "").strip()
        items.append({
            "red": "instagram", "id": p.get("id", ""), "url": p.get("permalink", ""),
            "titulo": texto, "fecha": p.get("timestamp", ""), "imagen": imagen or "",
            "alt": p.get("altText") or "", "reel": bool(p.get("isReel")),
        })
    return items


def actualizar_redes():
    """Descarga las novedades. Si una red falla, se conservan los datos anteriores de esa red."""
    cache_f = os.path.join(DATOS, "redes.json")
    cache = json.load(open(cache_f, encoding="utf-8")) if os.path.exists(cache_f) else {}
    try:
        yt = leer_youtube(descargar(f"https://www.youtube.com/feeds/videos.xml?channel_id={AJ['youtube_canal_id']}"))
        if yt:
            cache["youtube"] = yt
            print(f"YouTube: {len(yt)} vídeos")
    except Exception as ex:  # noqa: BLE001
        print("AVISO: no se pudo leer YouTube:", ex)
    if AJ.get("behold_feed"):
        try:
            ig = leer_behold(json.loads(descargar(AJ["behold_feed"])))
            if ig:
                cache["instagram"] = ig
                print(f"Instagram: {len(ig)} publicaciones")
        except Exception as ex:  # noqa: BLE001
            print("AVISO: no se pudo leer Instagram:", ex)
    with open(cache_f, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=1)


def redes():
    f = os.path.join(DATOS, "redes.json")
    c = json.load(open(f, encoding="utf-8")) if os.path.exists(f) else {}
    yt = c.get("youtube", [])[: AJ["max_youtube"]]
    ig = c.get("instagram", [])[: AJ["max_instagram"]] if AJ.get("behold_feed") else []
    todo = sorted(yt + ig, key=lambda x: x.get("fecha", ""), reverse=True)
    return todo, {i["id"]: i["fecha"] for i in c.get("youtube", [])}


def recortar(t, n=150):
    t = re.sub(r"\s+", " ", t).strip()
    return t if len(t) <= n else t[: n - 1].rsplit(" ", 1)[0] + "…"


def tarjeta_red(it, lang):
    tx = T[lang]
    es_yt = it["red"] == "youtube"
    etiqueta = "YouTube" + (" Shorts" if it.get("short") else "") if es_yt else "Instagram" + (" · Reel" if it.get("reel") else "")
    alt = e(it.get("alt") or recortar(it["titulo"], 120) or etiqueta)
    fecha = fecha_corta(it["fecha"], lang) if it.get("fecha") else ""
    imgtag = (f'<img src="{e(it["imagen"])}" alt="{alt}" loading="lazy" decoding="async">' if it.get("imagen") else "")
    return (f'<article class="feed-card feed-{it["red"]}">'
            f'<a class="feed-media" href="{e(it["url"])}" target="_blank" rel="noopener">{imgtag}'
            f'{"<span class=feed-play>" + PLAY_SVG + "</span>" if es_yt else ""}</a>'
            f'<div class="feed-body"><div class="feed-meta"><span class="feed-red">{etiqueta}</span>'
            f'{"<time datetime=" + e(it["fecha"][:10]) + ">" + fecha + "</time>" if fecha else ""}</div>'
            f'<p class="feed-title">{e(recortar(it["titulo"]))}</p>'
            f'<a class="news-link" href="{e(it["url"])}" target="_blank" rel="noopener">{tx["ver_yt"] if es_yt else tx["ver_insta"]}</a>'
            f'</div></article>')


def bloque_redes(lang, n=None):
    items, _ = redes()
    tx = T[lang]
    if n:
        items = items[:n]
    if not items:
        return (f'<p class="feed-vacio">{tx["redes_vacio"]} <a href="{AJ["youtube_url"]}" target="_blank" rel="noopener">YouTube</a> · '
                f'<a href="{AJ["instagram_url"]}" target="_blank" rel="noopener">Instagram</a></p>')
    return '<div class="feed-grid">' + "".join(tarjeta_red(i, lang) for i in items) + "</div>"


# ---------------------------------------------------------------- datos
AGENDA = leer("agenda.json")
VIDEOS = leer("videos.json")["videos"]
PRENSA = leer("prensa.json")
NOTICIAS = leer("noticias.json")
BIO = leer("biografia.json")
FOTOS = leer("fotos.json")["fotos"] if os.path.exists(os.path.join(DATOS, "fotos.json")) else []


def proximas():
    fut = [a for a in AGENDA if a.get("fin") and dt.date.fromisoformat(a["fin"]) >= HOY]
    return sorted(fut, key=lambda a: a["inicio"])


def pasadas():
    pas = [a for a in AGENDA if not (a.get("fin") and dt.date.fromisoformat(a["fin"]) >= HOY)]
    return sorted(pas, key=lambda a: (a["anio"], a.get("inicio") or "0"), reverse=True)


def papel(a, lang):
    return a["papel_es"] if lang == "es" else (a.get("papel_en") or a["papel_es"])


def lugar(a, lang):
    return a.get("lugar_en") if lang == "en" and a.get("lugar_en") else a["lugar"]


# ---------------------------------------------------------------- datos estructurados
def persona(lang):
    return {
        "@type": "Person", "@id": f"{DOM}/#cesar", "name": AJ["nombre"], "alternateName": AJ["nombre_corto"],
        "jobTitle": "Barítono" if lang == "es" else "Baritone",
        "description": METAS["inicio"][1 if lang == "es" else 3],
        "url": DOM + "/", "image": f"{DOM}/img/hero.jpg",
        "sameAs": [AJ["youtube_url"], AJ["instagram_url"]],
        "alumniOf": {"@type": "EducationalOrganization", "name": "Escuela Superior de Canto de Madrid"},
        "award": ["Premio Fin de Carrera Lola Rodríguez Aragón (Escuela Superior de Canto de Madrid)",
                  "Primer Premio, Concurso Internacional de Canto «Ciudad de Logroño»",
                  "Premio Especial, Concurso Internacional de Canto «Francisco Viñas»"],
    }


def evento(a, lang):
    partes = [p.strip() for p in lugar(a, lang).split(",")]
    sitio = {"@type": "Place", "name": partes[0],
             "address": {"@type": "PostalAddress", "addressLocality": partes[-1] if len(partes) > 1 else partes[0]}}
    nombre = a["obra"] + (f" — {papel(a, lang)}" if papel(a, lang) else "")
    ev = {"@type": "MusicEvent", "name": nombre, "startDate": a["inicio"], "endDate": a["fin"] or a["inicio"],
            "eventStatus": "https://schema.org/EventScheduled",
            "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
            "location": sitio, "image": f"{DOM}/img/hero.jpg",
            "description": descripcion_evento(a, lang),
            "performer": {"@id": f"{DOM}/#cesar"}}
    # Solo datos confirmados en agenda.json: si faltan, no se envían a Google.
    org = a.get("organizador")
    if org:
        ev["organizer"] = {"@type": "Organization", "name": org}
        if a.get("organizador_url"):
            ev["organizer"]["url"] = a["organizador_url"]
    if a.get("entradas_url"):
        of = {"@type": "Offer", "url": a["entradas_url"]}
        if a.get("precio_desde") is not None and a.get("moneda"):
            of["price"] = str(a["precio_desde"])
            of["priceCurrency"] = a["moneda"]
        if a.get("disponibilidad"):  # p. ej. "InStock", "SoldOut" (comprobado en la web de venta)
            of["availability"] = "https://schema.org/" + a["disponibilidad"]
        ev["offers"] = of
    return ev


def descripcion_evento(a, lang):
    p = papel(a, lang)
    if lang == "es":
        return f"César San Martín{' (' + p + ')' if p else ''} en «{a['obra']}». {lugar(a, lang)}."
    return f"César San Martín{' (' + p + ')' if p else ''} in {a['obra']}. {lugar(a, lang)}."


def video_ld(v, lang, subidas):
    fecha = v.get("subido") or subidas.get(v["id"], "")
    if not fecha:
        return None  # sin fecha de subida Google no acepta el vídeo; mejor no ponerlo que inventarla
    return {"@type": "VideoObject", "name": f'{v["obra"]} – {pieza(v, lang)} | César San Martín',
            "description": descripcion_video(v, lang), "thumbnailUrl": f"https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg",
            "uploadDate": fecha, "embedUrl": f"https://www.youtube.com/embed/{v['id']}",
            "contentUrl": f"https://www.youtube.com/watch?v={v['id']}"}


def ld_json(objs):
    if not objs:
        return ""
    datos = {"@context": "https://schema.org", "@graph": objs}
    return '<script type="application/ld+json">' + json.dumps(datos, ensure_ascii=False).replace("</", "<\\/") + "</script>"


# ---------------------------------------------------------------- plantilla
def cabecera(clave, lang, ld=None, titulo=None, desc=None, noindex=False):
    m = METAS.get(clave)
    titulo = titulo or (m[0] if lang == "es" else m[2])
    desc = desc or (m[1] if lang == "es" else m[3])
    es_url, en_url = PAGINAS[clave][0], PAGINAS[clave][1]
    canon = DOM + (es_url if lang == "es" else en_url)
    alternas = "" if noindex else (
        f'<link rel="canonical" href="{canon}">\n'
        f'<link rel="alternate" hreflang="es" href="{DOM}{es_url}">\n'
        f'<link rel="alternate" hreflang="en" href="{DOM}{en_url}">\n'
        f'<link rel="alternate" hreflang="x-default" href="{DOM}{es_url}">\n')
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    tx = T[lang]
    nav = "".join(
        f'<a href="{ruta(k, lang)}"{" class=active aria-current=page" if k == clave else ""}>{v[2] if lang == "es" else v[3]}</a>'
        for k, v in PAGINAS.items())
    graf = [persona(lang)] + (ld or [])
    if clave == "inicio":
        graf.append({"@type": "WebSite", "@id": f"{DOM}/#web", "url": DOM + "/", "name": AJ["nombre"],
                     "inLanguage": ["es", "en"], "about": {"@id": f"{DOM}/#cesar"}})
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{titulo}</title>
<meta name="description" content="{e(desc)}">
{robots}{alternas}<meta property="og:type" content="{'profile' if clave == 'inicio' else 'website'}">
<meta property="og:site_name" content="César San Martín">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{DOM}/img/hero.jpg">
<meta property="og:locale" content="{'es_ES' if lang == 'es' else 'en_GB'}">
<meta property="og:locale:alternate" content="{'en_GB' if lang == 'es' else 'es_ES'}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/estilos.css?v={VERSION_CSS}">
{ld_json(graf)}
</head>
<body>
<a class="saltar" href="#contenido">{'Saltar al contenido' if lang == 'es' else 'Skip to content'}</a>
<header>
<nav aria-label="{tx['menu']}">
  <div class="nav-inner">
    <a class="nav-brand" href="{ruta('inicio', lang)}">César San Martín</a>
    <div class="nav-scroll"><div class="nav-links">{nav}</div></div>
    <div class="lang-switcher" role="group" aria-label="{tx['idioma']}">
      <a class="lang-btn{' active' if lang == 'es' else ''}" href="{es_url}" hreflang="es" lang="es"{' aria-current=true' if lang == 'es' else ''}>ES</a>
      <a class="lang-btn{' active' if lang == 'en' else ''}" href="{en_url}" hreflang="en" lang="en"{' aria-current=true' if lang == 'en' else ''}>EN</a>
    </div>
  </div>
</nav>
</header>
<main id="contenido">
"""


def pie(lang):
    tx = T[lang]
    return f"""</main>
<footer>
  <div class="wrap">
    <div class="foot-inner">
      <div class="foot-brand">{AJ['nombre_corto']}</div>
      <div class="foot-links">
        <a href="{AJ['instagram_url']}" target="_blank" rel="noopener">Instagram</a>
        <a href="{AJ['youtube_url']}" target="_blank" rel="noopener">YouTube</a>
        <a href="{ruta('contacto', lang)}">{tx['contacto']}</a>
      </div>
    </div>
    <div class="foot-meta">© {HOY.year} {tx['derechos']}</div>
  </div>
</footer>
<script>
document.addEventListener('click',function(ev){{
  var b=ev.target.closest('.yt-btn');
  if(b){{
    var box=b.parentNode,id=box.getAttribute('data-id'),f=document.createElement('iframe');
    f.src='https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0';
    f.title=box.getAttribute('data-title');
    f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; fullscreen';
    f.allowFullscreen=true;f.setAttribute('loading','lazy');
    box.replaceChild(f,b);box.classList.add('yt-on');
  }}
  var g=ev.target.closest('.gallery-toggle-btn');
  if(g){{
    var x=document.getElementById('gallery-extra'),o=x.classList.toggle('open');
    g.classList.toggle('open',o);g.setAttribute('aria-expanded',o);
    g.querySelector('.txt').textContent=o?g.getAttribute('data-menos'):g.getAttribute('data-mas');
  }}
  var v=document.getElementById('visor');
  var l=ev.target.closest('.gal-link');
  if(l&&v&&v.showModal){{ev.preventDefault();verFoto(+l.getAttribute('data-i'));v.showModal();return;}}
  if(v&&v.open){{
    if(ev.target.closest('.visor-prev'))verFoto(vi-1);
    else if(ev.target.closest('.visor-next'))verFoto(vi+1);
    else if(ev.target.closest('.visor-x')||ev.target===v)v.close();
  }}
}});
var vi=0;
function verFoto(i){{
  var ls=document.querySelectorAll('.gal-link'),v=document.getElementById('visor');if(!ls.length)return;
  vi=(i+ls.length)%ls.length;var a=ls[vi],im=v.querySelector('img');
  im.src=a.getAttribute('href');im.alt=a.querySelector('img').alt;
  v.querySelector('figcaption').innerHTML=a.parentNode.querySelector('figcaption').innerHTML;
}}
document.addEventListener('keydown',function(ev){{
  var v=document.getElementById('visor');if(!v||!v.open)return;
  if(ev.key==='ArrowLeft')verFoto(vi-1);else if(ev.key==='ArrowRight')verFoto(vi+1);
}});
</script>
</body>
</html>
"""


# ---------------------------------------------------------------- piezas reutilizables
def pieza(v, lang):
    return v.get("pieza_en") if lang == "en" and v.get("pieza_en") else v["pieza"]


def descripcion_video(v, lang):
    partes = [v["compositor"]]
    if v.get("papel"):
        partes.append(v["papel"])
    sitio = ", ".join(x for x in (v.get("lugar"), v.get("anio")) if x)
    if sitio:
        partes.append(sitio)
    cred = v.get("creditos_es" if lang == "es" else "creditos_en")
    base = f'César San Martín, {"barítono" if lang == "es" else "baritone"} · ' + " · ".join(partes)
    return base + (f" · {cred}" if cred else "")


def video_html(v, lang, h="h3"):
    tx = T[lang]
    titulo = f'{v["obra"]} – {pieza(v, lang)}'
    thumb = f"https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg"
    sitio = ", ".join(x for x in (v.get("lugar"), v.get("anio")) if x)
    linea2 = " · ".join(x for x in (v["compositor"], v.get("papel"), sitio) if x)
    cred = v.get("creditos_es" if lang == "es" else "creditos_en")
    return f"""<div class="video-item">
  <div class="yt video-card" data-id="{v['id']}" data-title="{e(titulo)}">
    <button class="yt-btn" type="button" aria-label="{tx['reproducir']}: {e(titulo)}">
      <img src="{thumb}" alt="{e(titulo)} — César San Martín" width="480" height="360" loading="lazy" decoding="async">
      <span class="video-play">{PLAY_SVG}</span>
    </button>
  </div>
  <div class="video-caption"><{h} class="video-name">{titulo}</{h}><span>{linea2}</span>{f'<span class="video-cred">{cred}</span>' if cred else ''}
  <a class="video-yt" href="https://www.youtube.com/watch?v={v['id']}" target="_blank" rel="noopener">{tx['ver_yt']}</a></div>
</div>"""


def fila_agenda(a, lang):
    p = papel(a, lang)
    return (f'<div class="concert-row"><div class="concert-date">{rango(a, lang)}</div>'
            f'<div><div class="concert-title">{a["obra"]}</div>{f"<div class=concert-role>{p}</div>" if p else ""}</div>'
            f'<div class="concert-place">{lugar(a, lang)}</div></div>')


# ---------------------------------------------------------------- páginas
def pag_inicio(lang):
    tx = T[lang]
    prox = proximas()[:4]
    filas = "".join(
        f'<div class="mini-concert"><strong>{a["obra"]}{" · " + papel(a, lang) if papel(a, lang) else ""}</strong>{rango(a, lang)} · {lugar(a, lang)}</div>'
        for a in prox) or f'<p>{tx["sin_proximas"]}</p>'
    teatros = "".join(f'<span>{t}</span><span class="sep"> · </span>' for t in BIO["teatros"]) * 2
    citas = BIO["citas_es" if lang == "es" else "citas_en"]
    cit = "".join(f'<span class="cita">{c["cita"]} <em>— {c["medio"]}</em></span><span class="cita-sep">·</span>' for c in citas) * 2
    dest = VIDEOS[0]
    ld = [evento(a, lang) for a in prox]
    return cabecera("inicio", lang, ld) + f"""
<div class="hero">
  {img('/img/hero.jpg', 'César San Martín, barítono', lazy=False)}
  <div class="hero-overlay"></div>
  <div class="hero-text">
    <h1 class="hero-name">{AJ['nombre_corto']}<span class="sr"> — {AJ['nombre']}, {tx['barítono'].lower()}</span></h1>
    <p class="hero-subtitle">&nbsp;&nbsp;{tx['barítono']}</p>
  </div>
</div>

<div class="marquee-wrap" aria-hidden="true"><div class="marquee-track">{teatros}</div></div>

<section class="home-section light">
  <div class="wrap"><div class="home-bio-grid">
    <div class="home-bio-img">{img('/img/retrato-06.jpg', 'Retrato de César San Martín' if lang == 'es' else 'Portrait of César San Martín')}</div>
    <div>
      <h2 class="section-label">{tx['historia']}</h2>
      <p class="home-bio-txt">{BIO['historia_es' if lang == 'es' else 'historia_en'][0].split('. ')[0]}. {'Años más tarde y después de muchas vueltas buscando, encontré el camino que siempre había estado esperándome.' if lang == 'es' else 'Years later, after many twists and turns, I found the path that had always been waiting for me.'}</p>
      <a class="read-more" href="{ruta('bio', lang)}">{tx['sigue']}</a>
    </div>
  </div></div>
</section>

<section class="home-section dark">
  <div class="wrap">
    <div class="section-label">{tx['agenda']}</div>
    <h2 class="section-title">{tx['proximas']}</h2>
    {filas}
    <a class="read-more" href="{ruta('agenda', lang)}">{tx['ver_agenda']}</a>
  </div>
</section>

<section class="home-section light">
  <div class="wrap"><div class="home-2col">
    <div>
      <div class="section-label">{tx['videos']}</div>
      <h2 class="section-title">{tx['en_escena']}</h2>
      <p class="home-bio-txt">{tx['videos_txt']}</p>
      <a class="read-more" href="{ruta('videos', lang)}">{tx['ver_videos']}</a>
    </div>
    <div>{video_html(dest, lang)}</div>
  </div></div>
</section>

<section class="home-section light feed-home">
  <div class="wrap">
    <div class="section-label">{tx['noticias']}</div>
    <h2 class="section-title">{tx['ultimo']}</h2>
    {bloque_redes(lang, 3)}
    <a class="read-more" href="{ruta('noticias', lang)}">{tx['mas_noticias']}</a>
  </div>
</section>

<section class="insta-cta">
  <div class="wrap insta-cta-inner">
    <div>
      <div class="section-label">Instagram</div>
      <h2 class="section-title">{tx['sigueme']}</h2>
      <p>{tx['insta_txt']}</p>
    </div>
    <a class="btn-outline-inv" href="{AJ['instagram_url']}" target="_blank" rel="noopener">@{AJ['instagram_usuario']} ↗</a>
  </div>
</section>

<div class="press-marquee" aria-hidden="true"><div class="marquee-track press-marquee-track">{cit}</div></div>
""" + pie(lang)


def pag_bio(lang):
    tx = T[lang]
    hist = "".join(f"<p>{p}</p>" for p in BIO["historia_es" if lang == "es" else "historia_en"])
    tr = BIO["trayectoria_es" if lang == "es" else "trayectoria_en"]
    mitad = (len(tr) + 1) // 2
    col = lambda ps: "".join(f"<p>{p}</p>" for p in ps)
    return cabecera("bio", lang) + f"""
<section class="inner-page">
  <div class="wrap">
    <div class="section-label">{tx['historia']}</div>
    <h1 class="section-title">{BIO['titulo_es' if lang == 'es' else 'titulo_en']}</h1>
    <div class="bio-personal">{hist}</div>
  </div>
</section>
<section class="inner-dark">
  <div class="wrap">
    <h2 class="section-label">{tx['trayectoria']}</h2>
    <div class="bio-cols bio-dark"><div>{col(tr[:mitad])}</div><div>{col(tr[mitad:])}</div></div>
  </div>
</section>
""" + pie(lang)


def pag_agenda(lang):
    tx = T[lang]
    prox = proximas()
    bloque_prox = "".join(fila_agenda(a, lang) for a in prox) or f'<p class="sin-fechas">{tx["sin_proximas"]}</p>'
    anios = {}
    for a in pasadas():
        anios.setdefault(a["anio"], []).append(a)
    grupos = "".join(
        f'<details class="year-group"{" open" if i == 0 else ""}><summary class="year-toggle"><h3 class="year-label">{anio}</h3>'
        f'<span class="year-arrow" aria-hidden="true">▼</span></summary><div class="year-body">'
        + "".join(fila_agenda(a, lang) for a in filas) + "</div></details>"
        for i, (anio, filas) in enumerate(sorted(anios.items(), reverse=True)))
    ld = [evento(a, lang) for a in prox]
    return cabecera("agenda", lang, ld) + f"""
<section class="inner-page">
  <div class="wrap">
    <div class="section-label">{tx['agenda']}</div>
    <h1 class="section-title">{tx['proximas']}</h1>
    <div class="agenda-prox">{bloque_prox}</div>
    <h2 class="section-label agenda-archivo">{tx['archivo']}</h2>
    {grupos}
    <div class="agenda-insta">
      <p>{tx['insta_agenda'].format(u=AJ['instagram_usuario'])}</p>
      <a class="btn-outline" href="{AJ['instagram_url']}" target="_blank" rel="noopener">{tx['ver_instagram']}</a>
    </div>
  </div>
</section>
""" + pie(lang)


def foto_textos(f, lang):
    """(pie de foto, texto alternativo) de una foto de escena. Solo usa los datos confirmados de fotos.json."""
    es = lang == "es"
    lug = f["lugar_es"] if es else (f.get("lugar_en") or f["lugar_es"])
    lug_anio = lug + (f", {f['anio']}" if f.get("anio") else "")
    obra = f'<em>{f["obra"]}</em> ({f["compositor"]})' if f.get("compositor") else f'<em>{f["obra"]}</em>'
    pie_txt = obra + (f' · {f["papel"]}' if f.get("papel") else "") + f" · {lug_anio}"
    alt = (f'César San Martín en {f["obra"]}' + (f' de {f["compositor"]}' if f.get("compositor") else "")
           + (f', como {f["papel"]}' if f.get("papel") else "") + f", {lug_anio}") if es else \
          (f'César San Martín in {f["obra"]}' + (f' by {f["compositor"]}' if f.get("compositor") else "")
           + (f' as {f["papel"]}' if f.get("papel") else "") + f", {lug_anio}")
    return pie_txt, alt


def galeria_escena(lang):
    tx = T[lang]
    items = ""
    for i, f in enumerate(FOTOS):
        pie_txt, alt = foto_textos(f, lang)
        cred = f'<span class="gal-cred">{tx["foto_de"]}: © {f["credito"]}</span>' if f.get("credito") else ""
        items += (f'<figure class="gal-item"><a href="/img/escena/{f["archivo"]}" class="gal-link" data-i="{i}" '
                  f'aria-label="{tx["ampliar"]}: {alt}">{img("/img/escena/m/" + f["archivo"], alt)}</a>'
                  f'<figcaption>{pie_txt}{cred}</figcaption></figure>')
    return (f'<div class="gal-masonry">{items}</div>'
            f'<dialog class="visor" id="visor" aria-label="{tx["escena"]}">'
            f'<button type="button" class="visor-x" aria-label="{tx["cerrar"]}">×</button>'
            f'<button type="button" class="visor-nav visor-prev" aria-label="{tx["anterior"]}">‹</button>'
            f'<figure><img alt=""><figcaption></figcaption></figure>'
            f'<button type="button" class="visor-nav visor-next" aria-label="{tx["siguiente"]}">›</button></dialog>')


def foto_ld(f, lang):
    _, alt = foto_textos(f, lang)
    o = {"@type": "ImageObject", "contentUrl": f"{DOM}/img/escena/{f['archivo']}",
         "thumbnailUrl": f"{DOM}/img/escena/m/{f['archivo']}", "caption": alt}
    if f.get("credito"):
        o["creditText"] = f["credito"]
        o["copyrightNotice"] = "© " + f["credito"]
    return o


def pag_videos(lang):
    tx = T[lang]
    _, subidas = redes()
    secciones = ""
    for g in ("opera", "zarzuela", "concierto"):
        vs = [v for v in VIDEOS if v["grupo"] == g]
        nombre = tx["conciertos"] if g == "concierto" else tx[g]
        texto = tx["conciertos_txt"] if g == "concierto" else tx[g + "_txt"]
        secciones += (f'<section class="video-seccion" id="{g}"><h2 class="section-title video-h2">{nombre}</h2>'
                      f'<p class="video-intro">{texto}</p><div class="video-grid">'
                      + "".join(video_html(v, lang) for v in vs) + "</div></section>")
    ld = [x for x in (video_ld(v, lang, subidas) for v in VIDEOS) if x] + [foto_ld(f, lang) for f in FOTOS]
    alt_r = "Retrato de César San Martín, barítono" if lang == "es" else "Portrait of César San Martín, baritone"
    ret = lambda ns: "".join(f'<div class="p">{img(f"/img/retrato-0{n}.jpg", alt_r)}</div>' for n in ns)
    return cabecera("videos", lang, ld) + f"""
<section class="inner-page">
  <div class="wrap">
    <div class="section-label">{tx['videos']}</div>
    <h1 class="section-title">{'Vídeos de César San Martín en directo' if lang == 'es' else 'César San Martín live on stage'}</h1>
    {secciones}
    <div class="video-channel">
      <p>{tx['mas_canal']}</p>
      <a class="btn-outline" href="{AJ['youtube_url']}" target="_blank" rel="noopener">{tx['canal']}</a>
    </div>
  </div>
</section>
<section class="fotos-dark" id="fotos">
  <div class="wrap">
    <div class="section-label">{tx['fotos']}</div>
    <h2 class="section-title">{tx['galeria']}</h2>
    <h3 class="gallery-sub">{tx['retratos']}</h3>
    <div class="gallery-portraits">{ret((1, 2, 3))}</div>
    <div class="gallery-portraits gallery-more" id="gallery-extra">{ret((5, 6, 7))}</div>
    <button class="gallery-toggle-btn" type="button" aria-expanded="false" aria-controls="gallery-extra" data-mas="{tx['mas_retratos']}" data-menos="{tx['menos_retratos']}"><span class="txt">{tx['mas_retratos']}</span> <span class="arrow" aria-hidden="true">▼</span></button>
    <h3 class="gallery-sub gallery-sub2">{tx['escena']}</h3>
    {galeria_escena(lang)}
  </div>
</section>
""" + pie(lang)


def pag_noticias(lang):
    tx = T[lang]
    tarjetas = ""
    for n in NOTICIAS:
        et = n["etiqueta_es" if lang == "es" else "etiqueta_en"]
        tarjetas += (f'<article class="news-card">{f"<div class=news-tag>{et}</div>" if et else ""}'
                     f'<div class="news-date">{n["fecha"]}</div>'
                     f'<h3 class="news-title">{n["titulo_es" if lang == "es" else "titulo_en"]}</h3>'
                     f'<p class="news-excerpt">{n["texto_es" if lang == "es" else "texto_en"]}</p>'
                     f'<a class="news-link" href="{n["url"]}" target="_blank" rel="noopener">{n["enlace_es" if lang == "es" else "enlace_en"]}</a></article>')
    return cabecera("noticias", lang) + f"""
<section class="inner-page">
  <div class="wrap">
    <div class="section-label">{tx['noticias']}</div>
    <h1 class="section-title">{tx['ultimo']}</h1>
    {bloque_redes(lang)}
  </div>
</section>
<section class="inner-page">
  <div class="wrap">
    <h2 class="section-title">{tx['entrevistas']}</h2>
    <div class="news-grid">{tarjetas}</div>
  </div>
</section>
""" + pie(lang)


def pag_prensa(lang):
    tx = T[lang]
    items = "".join(
        f'<figure class="press-item"><figcaption><cite class="press-source">{p["medio"]}</cite><div class="press-meta">{p["detalle"]}</div></figcaption>'
        f'<blockquote lang="{lang if lang == "es" else "en"}">{p["es"] if lang == "es" else p["en"]}</blockquote></figure>'
        for p in PRENSA)
    nota = "" if lang == "es" else '<p class="press-nota">Reviews originally published in Spanish; English translations.</p>'
    return cabecera("prensa", lang) + f"""
<section class="inner-page">
  <div class="wrap">
    <div class="section-label">{tx['prensa']}</div>
    <h1 class="section-title">{'Críticas · Temporada 2025/26' if lang == 'es' else 'Reviews · Season 2025/26'}</h1>
    {nota}{items}
  </div>
</section>
""" + pie(lang)


def pag_contacto(lang):
    tx = T[lang]
    return cabecera("contacto", lang) + f"""
<section class="inner-page">
  <div class="wrap">
    <div class="section-label">{tx['contacto']}</div>
    <h1 class="section-title">{'Contratación, prensa y consultas' if lang == 'es' else 'Booking, press and enquiries'}</h1>
    <div class="contact-grid">
      <form action="{AJ['formspree']}" method="POST">
        <div class="form-field"><label for="f-nombre">{tx['nombre']}</label><input id="f-nombre" type="text" name="nombre" required placeholder="{tx['ph_nombre']}" autocomplete="name"></div>
        <div class="form-field"><label for="f-email">Email</label><input id="f-email" type="email" name="email" required placeholder="{tx['ph_email']}" autocomplete="email"></div>
        <div class="form-field"><label for="f-asunto">{tx['asunto']}</label><select id="f-asunto" name="asunto"><option value="">{tx['motivo']}</option><option value="contratacion">{tx['contratacion']}</option><option value="prensa">{tx['prensa']}</option><option value="otro">{tx['otro']}</option></select></div>
        <div class="form-field"><label for="f-msg">{tx['mensaje']}</label><textarea id="f-msg" name="mensaje" required placeholder="{tx['ph_msg']}"></textarea></div>
        <input type="hidden" name="idioma" value="{lang}">
        <button type="submit" class="form-submit">{tx['enviar']}</button>
      </form>
      <div class="contact-side">
        <h2 class="section-label">{tx['encuentrame']}</h2>
        <a class="contact-link" href="{AJ['instagram_url']}" target="_blank" rel="noopener">Instagram @{AJ['instagram_usuario']} ↗</a>
        <a class="contact-link" href="{AJ['youtube_url']}" target="_blank" rel="noopener">YouTube @cesarsanmartin.baritono ↗</a>
      </div>
    </div>
  </div>
</section>
""" + pie(lang)


def pag_404():
    PAGINAS["404"] = ("/404.html", "/404.html", "", "")
    h = cabecera("404", "es", titulo="Página no encontrada · César San Martín", desc="Página no encontrada.", noindex=True)
    del PAGINAS["404"]
    return h + f"""
<section class="inner-page"><div class="wrap">
  <h1 class="section-title">Página no encontrada <span class="dim">· Page not found</span></h1>
  <p><a class="read-more" href="/">Volver al inicio</a> &nbsp; <a class="read-more" href="/en/">Back to home</a></p>
</div></section>
""" + pie("es")


# ---------------------------------------------------------------- escribir
def escribir(rel, contenido):
    destino = os.path.join(SALIDA, rel.lstrip("/"))
    if destino.endswith("/") or rel.endswith("/"):
        destino = os.path.join(destino, "index.html")
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8") as f:
        f.write(contenido)


def sitemap():
    filas = []
    for clave, (es, en, *_ ) in PAGINAS.items():
        for url in (es, en):
            filas.append(f"""  <url><loc>{DOM}{url}</loc>
    <xhtml:link rel="alternate" hreflang="es" href="{DOM}{es}"/>
    <xhtml:link rel="alternate" hreflang="en" href="{DOM}{en}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{DOM}{es}"/>
  </url>""")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(filas) + "\n</urlset>\n")


FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="10" fill="#2e2e2e"/>'
           '<text x="32" y="44" font-family="Georgia,serif" font-size="30" font-style="italic" fill="#c98d6a" text-anchor="middle">CS</text></svg>')


def main():
    global VERSION_CSS
    if "--redes" in sys.argv:
        actualizar_redes()
    css = open(os.path.join(FUENTE, "estilos-base.css"), encoding="utf-8").read() + "\n" + \
        open(os.path.join(FUENTE, "estilos-extra.css"), encoding="utf-8").read()
    VERSION_CSS = format(abs(hash(css)) % 10**8, "08d") if False else str(sum(css.encode()) % 100000)
    if os.path.isdir(SALIDA):
        shutil.rmtree(SALIDA)
    os.makedirs(SALIDA)
    shutil.copytree(os.path.join(FUENTE, "img"), os.path.join(SALIDA, "img"))
    escribir("estilos.css", css)
    for lang in ("es", "en"):
        escribir(ruta("inicio", lang), pag_inicio(lang))
        escribir(ruta("bio", lang), pag_bio(lang))
        escribir(ruta("agenda", lang), pag_agenda(lang))
        escribir(ruta("videos", lang), pag_videos(lang))
        escribir(ruta("noticias", lang), pag_noticias(lang))
        escribir(ruta("prensa", lang), pag_prensa(lang))
        escribir(ruta("contacto", lang), pag_contacto(lang))
    escribir("404.html", pag_404())
    escribir("sitemap.xml", sitemap())
    escribir("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOM}/sitemap.xml\n")
    escribir("favicon.svg", FAVICON)
    escribir("CNAME", DOM.split("//", 1)[1] + "\n")
    escribir(".nojekyll", "")
    print(f"Web generada en docs/ ({HOY.isoformat()}): {len(PAGINAS) * 2} páginas, "
          f"{len(proximas())} próximas actuaciones, {len(redes()[0])} novedades de redes.")


VERSION_CSS = "1"
if __name__ == "__main__":
    main()
