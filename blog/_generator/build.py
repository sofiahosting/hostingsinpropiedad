#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build.py — Generador del blog SEO de Sofía Retif (sin dependencias externas).

Lee los datos de blog/_generator/data/*.json y las plantillas de
blog/_generator/templates/, y escribe HTML estático en /blog/ + un sitemap.xml
en la raíz del repo. Idempotente: se puede correr las veces que quieras.

Uso:
    python3 blog/_generator/build.py

Sitio estático (GitHub Pages). Nada de esto corre en el servidor: el output es
HTML plano que se commitea al repo.
"""

import json
import os
import re
import html
from datetime import date

# ------------------------------------------------------------------ config
SITE = "https://sofiaretif.com"
GA4_ID = "G-XXXXXXXXXX"          # <-- Sofía: reemplaza por tu Measurement ID de GA4
OG_IMAGE = SITE + "/og-image.jpg"
BUILD_DATE = date.today().isoformat()

# Favicon (mismo de las landings: casa con corazón, degradado azul)
FAVICON = ("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9"
           "IjAgMCA2NCA2NCI+PGRlZnM+PGxpbmVhckdyYWRpZW50IGlkPSJnIiB4MT0iMCIgeTE9IjAiIHgyPSIxIiB5Mj0iMSI+"
           "PHN0b3Agb2Zmc2V0PSIwIiBzdG9wLWNvbG9yPSIjM0E2RTk2Ii8+PHN0b3Agb2Zmc2V0PSIxIiBzdG9wLWNvbG9yPSIj"
           "MjI0OTZBIi8+PC9saW5lYXJHcmFkaWVudD48L2RlZnM+PHJlY3Qgd2lkdGg9IjY0IiBoZWlnaHQ9IjY0IiByeD0iMTUi"
           "IGZpbGw9InVybCgjZykiLz48cG9seWdvbiBwb2ludHM9IjMyLDEzIDU0LDMzIDEwLDMzIiBmaWxsPSIjRkRGQUY1Ii8+"
           "PHJlY3QgeD0iMTciIHk9IjMxIiB3aWR0aD0iMzAiIGhlaWdodD0iMjIiIHJ4PSIzIiBmaWxsPSIjRkRGQUY1Ii8+PHBh"
           "dGggZD0iTTMyIDQxLjVjLTEuOC0zLTctMi03IDEuNiAwIDMgMy42IDUgNyA2LjkgMy40LTEuOSA3LTMuOSA3LTYuOSAw"
           "LTMuNi01LjItNC42LTctMS42eiIgZmlsbD0iI0M4N0Q4NyIvPjwvc3ZnPgo=")

# Enlaces oficiales a productos (NO inventar otros)
LINKS = {
    "curso":       "https://pay.hotmart.com/N101179190K",
    "masterclass": "/masterclass.html",
    "bootcamp":    "/curso-en-vivo.html",
    "asesoria":    "/asesoria.html",
    "aprende":     "/aprende-conmigo.html",
}

# Bloques de CTA reutilizables (hacia páginas de venta)
CTA = {
    "masterclass": {
        "h":   "Aprende el modelo completo en mi masterclass gratis",
        "p":   "Te muestro paso a paso cómo generar ingresos con Airbnb sin comprar propiedad, y cómo saber si es rentable en tu ciudad.",
        "btn": "Reservar mi lugar gratis",
        "href": LINKS["masterclass"],
        "small": "Clase en vivo · 100% gratis",
    },
    "curso": {
        "h":   "Da el primer paso con mi curso",
        "p":   "El sistema completo, del inmueble vacío al anuncio publicado, para montar tu primer Airbnb sin propiedad.",
        "btn": "Ver el curso",
        "href": LINKS["curso"],
        "small": "Acceso inmediato · aprende a tu ritmo",
    },
    "bootcamp": {
        "h":   "Hazlo acompañada en el Bootcamp en vivo",
        "p":   "6 clases en vivo para montar tu primer Airbnb paso a paso, con plantillas, contrato y acompañamiento cercano.",
        "btn": "Conocer el Bootcamp",
        "href": LINKS["bootcamp"],
        "small": "Cupos limitados · clases en vivo",
    },
    "asesoria": {
        "h":   "¿Quieres verlo para tu caso? Agenda una asesoría 1:1",
        "p":   "Revisamos juntos tu situación y armamos un plan personalizado para que empieces con claridad.",
        "btn": "Agendar asesoría",
        "href": LINKS["asesoria"],
        "small": "Sesión 1:1 con Sofía",
    },
}

CAT = {
    "ciudades": {"nombre": "Ciudades", "desc": "Cuánto se gana y cómo empezar un Airbnb en cada ciudad."},
    "guias":    {"nombre": "Guías",    "desc": "El paso a paso para montar y operar tu Airbnb sin propiedad."},
    "glosario": {"nombre": "Glosario", "desc": "Los términos del negocio de rentas cortas, explicados fácil."},
}

# ------------------------------------------------------------------ rutas
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(HERE, "..", ".."))   # raíz del repo
BLOG_DIR = os.path.join(ROOT_DIR, "blog")
DATA_DIR = os.path.join(HERE, "data")
TPL_DIR = os.path.join(HERE, "templates")

with open(os.path.join(TPL_DIR, "base.html"), encoding="utf-8") as f:
    BASE = f.read()

# Registro de URLs generadas para el sitemap
SITEMAP_URLS = []


# ------------------------------------------------------------------ helpers
def load(name):
    with open(os.path.join(DATA_DIR, name), encoding="utf-8") as f:
        return json.load(f)


def esc(s):
    return html.escape(str(s), quote=True)


def write_page(rel_path, title, description, og_title, canonical_path,
               content, jsonld, add_to_sitemap=True, priority="0.7"):
    """Renderiza la plantilla base y escribe el archivo."""
    canonical = SITE + canonical_path
    page = BASE
    repl = {
        "TITLE": esc(title),
        "DESCRIPTION": esc(description),
        "OG_TITLE": esc(og_title or title),
        "CANONICAL": canonical,
        "OG_IMAGE": OG_IMAGE,
        "FAVICON": FAVICON,
        "CSS": "/assets/blog.css",
        "GA4_ID": GA4_ID,
        "ROOT": "/",
        "JSONLD": jsonld,
        "CONTENT": content,
    }
    for k, v in repl.items():
        page = page.replace("{{" + k + "}}", v)

    out = os.path.join(ROOT_DIR, rel_path.lstrip("/"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    if add_to_sitemap:
        SITEMAP_URLS.append((canonical, BUILD_DATE, priority))


def breadcrumbs(items):
    """items = lista de (label, href|None). El último sin enlace."""
    parts = []
    for label, href in items:
        if href:
            parts.append('<a href="%s">%s</a>' % (href, esc(label)))
        else:
            parts.append('<span>%s</span>' % esc(label))
    return '<nav class="breadcrumbs" aria-label="Ruta de navegación">' + ' › '.join(parts) + '</nav>'


def breadcrumb_jsonld(items):
    elems = []
    for i, (label, href) in enumerate(items, 1):
        el = {"@type": "ListItem", "position": i, "name": label}
        if href:
            el["item"] = SITE + href if href.startswith("/") else href
        elems.append(el)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": elems}


def article_jsonld(headline, description, url, breadcrumb_items):
    art = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": headline,
        "description": description,
        "inLanguage": "es",
        "datePublished": BUILD_DATE,
        "dateModified": BUILD_DATE,
        "mainEntityOfPage": {"@type": "WebPage", "@id": SITE + url},
        "author": {"@type": "Person", "name": "Sofía Retif", "url": SITE + "/"},
        "publisher": {
            "@type": "Organization",
            "name": "Sofía Retif · Hosting Sin Propiedad",
            "logo": {"@type": "ImageObject", "url": OG_IMAGE},
        },
        "image": OG_IMAGE,
    }
    return json_block([art, breadcrumb_jsonld(breadcrumb_items)])


def json_block(objs):
    if not isinstance(objs, list):
        objs = [objs]
    out = []
    for o in objs:
        out.append('<script type="application/ld+json">\n'
                   + json.dumps(o, ensure_ascii=False, indent=2)
                   + '\n</script>')
    return "\n".join(out)


def cta_box(key):
    c = CTA[key]
    return ('<div class="cta-box">'
            '<h3>%s</h3><p>%s</p>'
            '<a class="btn" href="%s">%s</a>'
            '<p class="small">%s</p>'
            '</div>') % (esc(c["h"]), esc(c["p"]), c["href"], esc(c["btn"]), esc(c["small"]))


def related_box(items):
    """items = lista de (label, href)."""
    lis = "".join('<li><a href="%s">%s</a></li>' % (href, esc(label)) for label, href in items)
    return ('<div class="related"><h3>Sigue leyendo</h3><ul>%s</ul></div>') % lis


def para(text):
    return "<p>%s</p>" % text


def wrap_article(kicker, h1, lede, sections_html, cta_key, related):
    return (
        '<div class="wrap">' + sections_html["crumbs"] + '</div>'
        '<div class="wrap"><article>'
        '<span class="kicker">%s</span>'
        '<h1>%s</h1>'
        '<p class="lede">%s</p>'
        '<p class="meta">Por Sofía Retif · Actualizado el %s</p>'
        '%s'
        '%s'
        '%s'
        '</article></div>'
    ) % (esc(kicker), esc(h1), esc(lede), _fecha_es(BUILD_DATE),
         sections_html["body"], cta_box(cta_key), related_box(related))


MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
         "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def _fecha_es(iso):
    y, m, d = iso.split("-")
    return "%d de %s de %s" % (int(d), MESES[int(m) - 1], y)


def money(n):
    return "{:,}".format(int(round(n))).replace(",", ",")


# ------------------------------------------------------------------ ciudades
def render_ciudades(data):
    ciudades = data["ciudades"]
    by_country = {}
    for c in ciudades:
        by_country.setdefault(c["pais"], []).append(c)
    cards = []

    for c in ciudades:
        nombre = c["nombre"]
        slug = c["slug"]
        occ = int(str(c["ocupacion"]).replace("%", ""))
        adr_mid = (c["adr_low"] + c["adr_high"]) / 2
        noches = round(30 * occ / 100)
        renta_mid = (c["renta_low"] + c["renta_high"]) / 2
        ingreso = adr_mid * noches
        costos = renta_mid + 120 + 150 + ingreso * 0.10
        ganancia = ingreso - costos

        zonas_li = "".join("<li>%s</li>" % esc(z) for z in c["zonas"])
        tabla = (
            '<table class="data-table"><tbody>'
            '<tr><th>Población</th><td>%s</td></tr>'
            '<tr><th>Tarifa por noche (estimada)</th><td>%d – %d USD</td></tr>'
            '<tr><th>Ocupación típica (estimada)</th><td>%s</td></tr>'
            '<tr><th>Renta mensual de un depto turístico</th><td>%d – %d USD</td></tr>'
            '<tr><th>Temporada alta</th><td>%s</td></tr>'
            '</tbody></table>'
        ) % (esc(c["poblacion"]), c["adr_low"], c["adr_high"], esc(c["ocupacion"]),
             c["renta_low"], c["renta_high"], esc(c["temporada"]))

        # otras ciudades del mismo país (para enlace interno)
        otras = [x for x in by_country[c["pais"]] if x["slug"] != slug][:2]

        # ---- Ángulo 1: cuánto se gana ----
        slug1 = "cuanto-se-gana-airbnb-%s" % slug
        path1 = "/blog/ciudades/%s.html" % slug1
        title1 = "¿Cuánto se gana con un Airbnb en %s? (2026)" % nombre
        desc1 = ("Cuánto se puede ganar con un Airbnb en %s: tarifas por noche, ocupación y una "
                 "estimación de ganancia mensual. Datos y zonas para arrancar." % nombre)
        crumbs1 = [("Inicio", "/"), ("Blog", "/blog/"), ("Ciudades", "/blog/ciudades/"), (nombre, None)]
        body1 = (
            para("¿Te preguntas cuánto se puede ganar con un Airbnb en <strong>%s</strong>? "
                 "Aquí te dejo una estimación realista con las tarifas y la ocupación de la ciudad, "
                 "para que decidas con números y no con corazonadas." % esc(nombre))
            + '<h2>¿Cuánto se gana con un Airbnb en %s?</h2>' % esc(nombre)
            + para("Con una tarifa promedio de alrededor de <strong>%d USD por noche</strong> y una "
                   "ocupación cercana al <strong>%d%%</strong> (unas %d noches al mes), un departamento "
                   "en %s podría generar cerca de <strong>%s USD de ingreso mensual</strong>. Al restar "
                   "renta, servicios, limpieza y comisiones, la ganancia neta estimada ronda los "
                   "<strong>%s USD al mes</strong>." % (
                       round(adr_mid), occ, noches, esc(nombre), money(ingreso), money(ganancia)))
            + '<div class="callout gold">Son cifras <strong>orientativas</strong>: cambian según la '
              'zona exacta, la calidad del inmueble y la época del año. Siempre corre tus propios '
              'números antes de firmar.</div>'
            + '<h2>Los datos de %s de un vistazo</h2>' % esc(nombre) + tabla
            + '<h2>¿Por qué %s funciona para rentas cortas?</h2>' % esc(nombre)
            + para("%s es %s. Esa demanda constante es justo lo que hace atractivo el modelo de "
                   "hospedaje corto aquí." % (esc(nombre), esc(c["turismo"])))
            + '<h2>Mejores zonas para Airbnb en %s</h2>' % esc(nombre)
            + para("Estas son de las zonas con más demanda para hospedaje en %s:" % esc(nombre))
            + '<ul>%s</ul>' % zonas_li
            + '<h2>Regulación en %s</h2>' % esc(nombre)
            + para("Antes de operar: %s" % esc(c["regulacion"]))
        )
        related1 = [
            ("Cómo poner un Airbnb en %s sin ser dueño" % nombre,
             "/blog/ciudades/airbnb-en-%s-sin-ser-dueno.html" % slug),
            ("Cómo calcular la rentabilidad de un Airbnb",
             "/blog/guias/como-calcular-la-rentabilidad-de-un-airbnb.html"),
            ("Cómo empezar un Airbnb sin propiedad",
             "/blog/guias/como-empezar-airbnb-sin-propiedad.html"),
        ] + [("¿Cuánto se gana con un Airbnb en %s?" % o["nombre"],
              "/blog/ciudades/cuanto-se-gana-airbnb-%s.html" % o["slug"]) for o in otras]

        write_page(path1, title1, desc1, title1,
                   path1, wrap_article("Ciudades · %s" % c["pais"], title1,
                                       "Estimación de ganancias, tarifas y zonas para un Airbnb en %s." % nombre,
                                       {"crumbs": breadcrumbs(crumbs1), "body": body1},
                                       "masterclass", related1),
                   article_jsonld(title1, desc1, path1, crumbs1), priority="0.7")

        # ---- Ángulo 2: sin ser dueño (arbitraje) ----
        slug2 = "airbnb-en-%s-sin-ser-dueno" % slug
        path2 = "/blog/ciudades/%s.html" % slug2
        title2 = "Cómo poner un Airbnb en %s sin ser dueño (arbitraje)" % nombre
        desc2 = ("Cómo montar un Airbnb en %s sin comprar propiedad: el modelo de arbitraje aplicado a "
                 "la ciudad, los números, las zonas y la regulación." % nombre)
        crumbs2 = [("Inicio", "/"), ("Blog", "/blog/"), ("Ciudades", "/blog/ciudades/"), (nombre, None)]
        body2 = (
            para("Sí se puede tener un Airbnb en <strong>%s</strong> sin comprar propiedad. El modelo "
                 "se llama arbitraje: rentas un departamento con contrato normal, lo amueblas y lo "
                 "rentas por noche con permiso del propietario." % esc(nombre))
            + '<h2>Cómo hacer Airbnb en %s sin comprar propiedad</h2>' % esc(nombre)
            + para("En %s puedes rentar un departamento por alrededor de <strong>%d – %d USD al mes</strong> "
                   "en zona turística, amueblarlo y rentarlo por noche. Tu ganancia es la diferencia entre "
                   "esa renta fija y lo que genera el inmueble en Airbnb." % (
                       esc(nombre), c["renta_low"], c["renta_high"]))
            + '<h2>Los números en %s</h2>' % esc(nombre)
            + para("Con una tarifa cercana a <strong>%d USD por noche</strong> y ocupación del %d%%, el "
                   "ingreso mensual estimado ronda los <strong>%s USD</strong>, con una ganancia neta "
                   "aproximada de <strong>%s USD</strong> tras cubrir renta y gastos. Cifras orientativas: "
                   "valida siempre tu caso." % (round(adr_mid), occ, money(ingreso), money(ganancia)))
            + tabla
            + '<h2>Mejores zonas para arbitraje en %s</h2>' % esc(nombre)
            + '<ul>%s</ul>' % zonas_li
            + '<h2>Regulación y contrato en %s</h2>' % esc(nombre)
            + para("Hazlo en regla: %s Y sobre todo, firma un contrato que autorice por escrito la renta "
                   "corta." % esc(c["regulacion"]))
        )
        related2 = [
            ("¿Cuánto se gana con un Airbnb en %s?" % nombre,
             "/blog/ciudades/cuanto-se-gana-airbnb-%s.html" % slug),
            ("Qué es el arbitraje de Airbnb",
             "/blog/guias/que-es-el-arbitraje-de-airbnb.html"),
            ("Cómo convencer a un propietario de rentarte para Airbnb",
             "/blog/guias/como-conseguir-departamentos-para-airbnb.html"),
        ] + [("Cómo poner un Airbnb en %s sin ser dueño" % o["nombre"],
              "/blog/ciudades/airbnb-en-%s-sin-ser-dueno.html" % o["slug"]) for o in otras]

        write_page(path2, title2, desc2, title2,
                   path2, wrap_article("Ciudades · %s" % c["pais"], title2,
                                       "El modelo de arbitraje de Airbnb aplicado a %s, con números y zonas." % nombre,
                                       {"crumbs": breadcrumbs(crumbs2), "body": body2},
                                       "bootcamp", related2),
                   article_jsonld(title2, desc2, path2, crumbs2), priority="0.7")

        cards.append(('%s' % c["pais"], nombre,
                      "Ganancias, tarifas y cómo empezar un Airbnb en %s." % nombre,
                      path1))

    return cards


# ------------------------------------------------------------------ guías
def section_html(sec):
    if "h2" in sec and "p" in sec:
        return "<h2>%s</h2>" % esc(sec["h2"]) + "".join(para(esc(p)) for p in sec["p"])
    if "h2" in sec and "lista" in sec:
        lis = "".join("<li>%s</li>" % esc(x) for x in sec["lista"])
        return "<h2>%s</h2><ul>%s</ul>" % (esc(sec["h2"]), lis)
    if "h3" in sec and "p" in sec:
        return "<h3>%s</h3>" % esc(sec["h3"]) + "".join(para(esc(p)) for p in sec["p"])
    if "callout" in sec:
        return '<div class="callout">%s</div>' % esc(sec["callout"])
    return ""


def render_guias(data):
    guias = data["guias"]
    cards = []
    n = len(guias)
    for i, g in enumerate(guias):
        slug = g["slug"]
        path = "/blog/guias/%s.html" % slug
        crumbs = [("Inicio", "/"), ("Blog", "/blog/"), ("Guías", "/blog/guias/"), (g["titulo"], None)]
        body = "".join(section_html(s) for s in g["body"])
        # relacionados: 3 siguientes guías (rotando) + hub de ciudades
        rel = []
        for k in range(1, 4):
            o = guias[(i + k) % n]
            rel.append((o["titulo"], "/blog/guias/%s.html" % o["slug"]))
        rel.append(("Ver Airbnb por ciudad", "/blog/ciudades/"))
        write_page(path, g["titulo"], g["description"], g.get("og_title", g["titulo"]),
                   path, wrap_article("Guía · %s" % g["cluster"], g["titulo"], g["lede"],
                                      {"crumbs": breadcrumbs(crumbs), "body": body},
                                      g["cta"], rel),
                   article_jsonld(g["titulo"], g["description"], path, crumbs), priority="0.8")
        cards.append((g["cluster"], g["titulo"], g["description"], path))
    return cards


# ------------------------------------------------------------------ glosario
def render_glosario(data):
    terms = data["terminos"]
    cards = []
    n = len(terms)
    for i, t in enumerate(terms):
        slug = t["slug"]
        path = "/blog/glosario/%s.html" % slug
        titulo = "%s: qué es y para qué sirve" % t["termino"]
        crumbs = [("Inicio", "/"), ("Blog", "/blog/"), ("Glosario", "/blog/glosario/"), (t["termino"], None)]
        body = ('<div class="callout"><strong>%s.</strong> %s</div>'
                % (esc(t["termino"]), esc(t["definicion"]))
                + "".join(para(esc(p)) for p in t["body"]))
        rel = []
        for k in range(1, 3):
            o = terms[(i + k) % n]
            rel.append(("Qué es %s" % o["termino"], "/blog/glosario/%s.html" % o["slug"]))
        rel.append(("Cómo empezar un Airbnb sin propiedad",
                    "/blog/guias/como-empezar-airbnb-sin-propiedad.html"))
        write_page(path, titulo, t["description"], titulo,
                   path, wrap_article("Glosario", t["termino"], t["definicion"],
                                      {"crumbs": breadcrumbs(crumbs), "body": body},
                                      t.get("cta", "masterclass"), rel),
                   article_jsonld(titulo, t["description"], path, crumbs), priority="0.6")
        cards.append(("Glosario", t["termino"], t["definicion"][:120] + "…", path))
    return cards


# ------------------------------------------------------------------ hubs
def card_html(tag, titulo, desc, href):
    return ('<div class="card"><span class="tag">%s</span>'
            '<h3><a href="%s">%s</a></h3><p>%s</p></div>') % (esc(tag), href, esc(titulo), esc(desc))


def render_hub(rel_path, canonical_path, kicker, h1, intro, groups, crumbs, title, desc):
    """groups = lista de (titulo_seccion|None, [cards])."""
    blocks = ['<div class="hub-hero"><div class="wrap-wide"><h1>%s</h1><p>%s</p></div></div>'
              % (esc(h1), esc(intro))]
    blocks.append('<div class="wrap-wide">' + breadcrumbs(crumbs))
    for gtitle, cards in groups:
        if gtitle:
            blocks.append('<h2 class="section-title">%s</h2>' % esc(gtitle))
        blocks.append('<div class="card-grid">' + "".join(
            card_html(*c) for c in cards) + '</div>')
    blocks.append('</div>')
    content = "".join(blocks)
    jsonld = json_block([
        {"@context": "https://schema.org", "@type": "CollectionPage",
         "name": title, "description": desc, "url": SITE + canonical_path, "inLanguage": "es"},
        breadcrumb_jsonld(crumbs),
    ])
    write_page(rel_path, title, desc, h1, canonical_path, content, jsonld, priority="0.6")


# ------------------------------------------------------------------ sitemap
CORE_PAGES = [
    ("/", "1.0"),
    ("/masterclass.html", "0.9"),
    ("/aprende-conmigo.html", "0.9"),
    ("/curso-en-vivo.html", "0.9"),
    ("/asesoria.html", "0.8"),
    ("/estudio-factibilidad.html", "0.7"),
    ("/portafolio", "0.6"),
    ("/faq.html", "0.6"),
    ("/contacto.html", "0.5"),
]


def write_sitemap():
    urls = []
    seen = set()
    for path, prio in CORE_PAGES:
        loc = SITE + path
        if loc in seen:
            continue
        seen.add(loc)
        urls.append((loc, BUILD_DATE, prio))
    for loc, lastmod, prio in SITEMAP_URLS:
        if loc in seen:
            continue
        seen.add(loc)
        urls.append((loc, lastmod, prio))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod, prio in urls:
        lines.append("  <url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>"
                     % (esc(loc), lastmod, prio))
    lines.append("</urlset>")
    with open(os.path.join(ROOT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return len(urls)


# ------------------------------------------------------------------ main
def main():
    ciudades = load("ciudades.json")
    guias = load("guias.json")
    glosario = load("glosario.json")

    city_cards = render_ciudades(ciudades)
    guide_cards = render_guias(guias)
    gloss_cards = render_glosario(glosario)

    # Hub de ciudades (agrupado por país)
    by_country = {}
    for tag, titulo, desc, href in city_cards:
        by_country.setdefault(tag, []).append((tag, titulo, desc, href))
    city_groups = [(pais, cards) for pais, cards in by_country.items()]
    render_hub("/blog/ciudades/index.html", "/blog/ciudades/", "Ciudades",
               "Airbnb por ciudad", "Cuánto se gana y cómo empezar un Airbnb sin ser dueño, ciudad por ciudad.",
               city_groups,
               [("Inicio", "/"), ("Blog", "/blog/"), ("Ciudades", None)],
               "Airbnb por ciudad · Sofía Retif",
               "Guías por ciudad: cuánto se gana y cómo montar un Airbnb sin comprar propiedad en México, Latinoamérica y EE.UU.")

    # Hub de guías (agrupado por cluster)
    by_cluster = {}
    for tag, titulo, desc, href in guide_cards:
        by_cluster.setdefault(tag, []).append((tag, titulo, desc, href))
    guide_groups = [(cl, cards) for cl, cards in by_cluster.items()]
    render_hub("/blog/guias/index.html", "/blog/guias/", "Guías",
               "Guías para tu primer Airbnb", "Todo lo que necesitas para montar y operar tu Airbnb sin propiedad, paso a paso.",
               guide_groups,
               [("Inicio", "/"), ("Blog", "/blog/"), ("Guías", None)],
               "Guías de Airbnb sin propiedad · Sofía Retif",
               "Guías paso a paso para empezar y operar un Airbnb sin comprar propiedad: arbitraje, contratos, muebles, precios y más.")

    # Hub de glosario
    render_hub("/blog/glosario/index.html", "/blog/glosario/", "Glosario",
               "Glosario del negocio de rentas cortas", "Los términos clave del mundo Airbnb, explicados en simple.",
               [(None, gloss_cards)],
               [("Inicio", "/"), ("Blog", "/blog/"), ("Glosario", None)],
               "Glosario de Airbnb y rentas cortas · Sofía Retif",
               "Diccionario del negocio de rentas cortas: arbitraje, rent-to-rent, ADR, ocupación, cohost y más términos explicados.")

    # Hub principal del blog
    top_guides = guide_cards[:6]
    top_cities = city_cards[:6]
    top_terms = gloss_cards[:6]
    render_hub("/blog/index.html", "/blog/", "Blog",
               "Blog de Sofía Retif", "Aprende a generar ingresos con Airbnb sin comprar propiedad. Guías, datos por ciudad y los términos del negocio.",
               [("Guías para empezar", top_guides),
                ("Airbnb por ciudad", top_cities),
                ("Glosario", top_terms)],
               [("Inicio", "/"), ("Blog", None)],
               "Blog · Airbnb sin propiedad · Sofía Retif",
               "Guías, datos por ciudad y glosario para generar ingresos con Airbnb sin comprar propiedad. Aprende con Sofía Retif.")

    total = write_sitemap()
    print("OK · %d ciudades ×2 + %d guías + %d términos + hubs" %
          (len(ciudades["ciudades"]), len(guias["guias"]), len(glosario["terminos"])))
    print("Sitemap: %d URLs → sitemap.xml" % total)


if __name__ == "__main__":
    main()
