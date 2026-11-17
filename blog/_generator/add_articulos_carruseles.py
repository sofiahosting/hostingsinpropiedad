"""17-nov-2026 · Convierte los carruseles de IG (estilo viral) en artículos del blog.
- 4 guías nuevas (temas que el blog no tenía).
- 4 guías existentes reciben su carrusel (mismo tema → no se duplica keyword).
Idempotente: si el slug ya existe lo reemplaza; si el carrusel ya está, no lo repite.
Correr:  python3 blog/_generator/add_articulos_carruseles.py && python3 blog/_generator/build.py
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "data", "guias.json")
data = json.load(open(P, encoding="utf-8"))
G = data["guias"]
data["_nota"] = data["_nota"].replace("{h3, p:[...]}.", "{h3, p:[...]}, {carrusel:'/assets/blog/<slug>', n, alt, nota}.") if "carrusel" not in data["_nota"] else data["_nota"]


def car(slug, alt, nota="Este es el carrusel que subí a Instagram. Desliza para ver todas las láminas →"):
    return {"carrusel": "/assets/blog/%s" % slug, "n": 8, "alt": alt, "nota": nota}


NUEVAS = [
  {
    "slug": "como-saber-si-una-zona-sirve-para-airbnb",
    "titulo": "Cómo saber si una zona sirve para Airbnb (antes de firmar)",
    "og_title": "Así sé si una zona sirve para Airbnb",
    "description": "El método que uso para validar una zona para Airbnb en unos 20 minutos y gratis: buscar como huésped, revisar calendarios y hacer cuentas antes de firmar.",
    "keyword": "zona para airbnb",
    "cluster": "Empezar",
    "lede": "Puedes tener el mejor departamento, pero si no hay demanda en la zona se queda vacío. Así reviso una zona antes de firmar cualquier contrato, sin corazonadas.",
    "cta": "curso",
    "body": [
      {"h2": "La zona manda",
       "p": ["Es lo primero que aprendí en este negocio: la zona decide casi todo. Decide quién te reserva, cuánto puedes cobrar y qué tan lleno vas a estar.",
             "Por eso nunca elijo una zona porque me gusta a mí o porque me queda cerca. La elijo porque los datos dicen que ahí hay demanda."]},
      car("como-saber-si-una-zona-sirve-para-airbnb", "Carrusel: así sé si una zona sirve para Airbnb"),
      {"h2": "Paso 1: abre Airbnb como si fueras huésped",
       "p": ["Busca fechas reales en esa zona, por ejemplo un fin de semana del próximo mes y unos días entre semana. Fíjate cuántos departamentos hay, cómo se ven los mejores y qué tipo de lugar se parece al que tú quieres operar."]},
      {"h2": "Paso 2: revisa los calendarios",
       "p": ["Entra a los anuncios parecidos al tuyo y mira su calendario. Si están llenos, la demanda existe. Si están vacíos, esa no es tu zona, por bonita que sea.",
             "Los calendarios no mienten: son la mejor señal gratis que tienes de si la gente realmente se hospeda ahí."]},
      {"h2": "Paso 3: haz cuentas",
       "lista": ["Tarifa por noche de los anuncios que sí están llenos.",
                 "Por el número de noches que esperas ocupar al mes.",
                 "Menos tus gastos: limpieza, servicios, internet, comisión de la plataforma.",
                 "Contra lo que cuesta rentar un departamento en esa misma zona."]},
      {"callout": "Si los números no cierran en papel, no van a cerrar en la vida real. Mejor descartar una zona en una hoja de cálculo que con un contrato firmado."},
      {"h2": "Mi tip: piensa quién duerme ahí",
       "p": ["Turistas, viajes de negocio, familias que acompañan a alguien en un hospital, gente que viene a un evento. Tu huésped decide tu tarifa, lo que tiene que tener el departamento y hasta tus reseñas. Cuando sabes para quién es, todo lo demás se acomoda."]},
      {"h2": "¿Sí o no?",
       "p": ["Si los números cierran y los calendarios están llenos, sigue con buscar departamento ahí. Si no cierran o los calendarios están vacíos, siguiente zona. Cero corazonadas."]},
    ],
  },
  {
    "slug": "como-saber-si-un-departamento-sirve-para-airbnb",
    "titulo": "¿Este depa sirve para Airbnb? 4 señales para saberlo",
    "og_title": "¿Este depa sirve para Airbnb? Revisa estas 4 señales",
    "description": "Antes de rentar un departamento para Airbnb revisa 4 señales: ubicación, reglas del edificio, competencia y números. Un depa bonito no garantiza reservas.",
    "keyword": "departamento para airbnb",
    "cluster": "Empezar",
    "lede": "Un depa bonito no garantiza reservas. Antes de rentar uno para Airbnb reviso estas 4 señales, y si falla una, lo pienso dos veces.",
    "cta": "curso",
    "body": [
      {"h2": "Bonito no es lo mismo que rentable",
       "p": ["Es muy fácil enamorarse de un departamento por cómo se ve. Pero la decoración se arregla; la ubicación, las reglas del edificio y los números no. Por eso primero reviso lo que no se puede cambiar."]},
      car("como-saber-si-un-departamento-sirve-para-airbnb", "Carrusel: ¿este depa sirve para Airbnb? 4 señales"),
      {"h2": "Señal 1: la ubicación",
       "p": ["¿Qué hay cerca? Centro, hospitales, oficinas, universidades, atracciones, transporte. Eso define quién te reserva y a cuánto. Un departamento a dos cuadras de un hospital grande tiene un huésped muy distinto a uno junto a la playa, y los dos pueden funcionar si sabes para quién es."]},
      {"h2": "Señal 2: las reglas del edificio",
       "p": ["Confirma que el condominio permita renta corta. Muchos la prohíben en su reglamento, y ahí muere el negocio antes de empezar. Pregunta antes de firmar y, si se puede, pide verlo por escrito."]},
      {"h2": "Señal 3: la competencia",
       "p": ["Busca Airbnbs parecidos en la zona: mismo tamaño, mismo tipo de huésped. Si están llenos y tienen buenas reseñas recientes, hay demanda comprobada. Si no hay ninguno, o los que hay están vacíos, es una alerta."]},
      {"h2": "Señal 4: los números",
       "lista": ["Suma lo que entraría: tarifa por noche × noches ocupadas.",
                 "Resta la renta del departamento.",
                 "Resta limpieza y lavandería.",
                 "Resta luz, agua e internet.",
                 "Resta la comisión de la plataforma.",
                 "Lo que queda es tu margen."]},
      {"callout": "Si no deja margen, no es el depa. Por bonito que sea."},
      {"h2": "Antes de ir a verlo",
       "p": ["Haz este filtro desde tu casa. Te ahorra visitas, te da argumentos para negociar con el dueño y evita que firmes por emoción. Para elegir la zona primero, revisa mi guía de cómo saber si una zona sirve para Airbnb."]},
    ],
  },
  {
    "slug": "mitos-de-vivir-de-airbnb",
    "titulo": "5 mitos de vivir de Airbnb que mucha gente todavía cree",
    "og_title": "5 mitos de vivir de Airbnb",
    "description": "Que es dinero fácil, que necesitas comprar, que ya está saturado, que es ilegal o que tienes que saberlo todo. Los 5 mitos de vivir de Airbnb, explicados.",
    "keyword": "vivir de airbnb",
    "cluster": "Conceptos",
    "lede": "Hay ideas sobre Airbnb que frenan a mucha gente antes de empezar. Estos son los 5 mitos que más escucho, y lo que pasa en la vida real.",
    "cta": "curso",
    "body": [
      car("mitos-de-vivir-de-airbnb", "Carrusel: 5 mitos de vivir de Airbnb"),
      {"h2": "Mito 1: \"Es dinero fácil\"",
       "p": ["Falso. Es un negocio: requiere método y trabajo, sobre todo al inicio. Hay que elegir zona, negociar, amueblar, publicar y atender huéspedes. Bien hecho, sí deja ingresos cada mes, pero no es dinero que cae del cielo."]},
      {"h2": "Mito 2: \"Necesitas comprar un depa\"",
       "p": ["Falso. Con arbitraje (rentas y subarriendas con permiso del dueño) o con co-hosting (operas el Airbnb de alguien más) ganas sin comprar propiedad. Yo empecé así."]},
      {"h2": "Mito 3: \"Ya está saturado\"",
       "p": ["Siempre hay zonas con demanda sin cubrir. Lo que sí está saturado son los anuncios mediocres en zonas sin demanda. La clave es saber encontrar las zonas buenas y hacerlo mejor que la competencia."]},
      {"h2": "Mito 4: \"Es ilegal\"",
       "p": ["Con permiso del dueño por escrito y un edificio que permita renta corta, es un negocio legal. Lo que no se vale es subarrendar a escondidas o en un edificio que lo prohíbe. Si te interesa el detalle, tengo una guía sobre si el arbitraje de Airbnb es legal."]},
      {"h2": "Mito 5: \"Hay que saberlo todo desde el día uno\"",
       "p": ["Necesitas un método y dar el primer paso. Lo demás se aprende en el camino: nadie arranca sabiendo poner precios, contestar huéspedes o resolver una fuga a las 11 de la noche."]},
      {"callout": "Lo que sí necesitas: método, saber negociar y constancia. Más que suerte o millones."},
    ],
  },
  {
    "slug": "tengo-30-airbnbs-y-ninguno-es-mio",
    "titulo": "Tengo más de 30 Airbnbs y ninguno es mío: así funciona",
    "og_title": "Tengo +30 Airbnbs y ninguno es mío",
    "description": "No heredé nada ni compré un solo departamento. Así funcionan las 2 formas de tener Airbnbs sin ser dueño: arbitraje y co-hosting, y cuál te conviene.",
    "keyword": "airbnbs sin ser dueño",
    "cluster": "Mi experiencia",
    "lede": "Opero más de 30 Airbnbs y ninguno es mío. No heredé nada ni compré un solo depa. Te explico cómo funciona, para que veas que no es magia.",
    "cta": "curso",
    "body": [
      {"h2": "No necesitas comprar un depa",
       "p": ["Cuando cuento que tengo más de 30 Airbnbs, la gente asume que compré departamentos o que tengo mucho dinero. Ninguna de las dos. Hay 2 formas de entrar a este negocio sin hipoteca, y las dos son legales cuando se hacen con permiso del dueño."]},
      car("tengo-30-airbnbs-y-ninguno-es-mio", "Carrusel: tengo +30 Airbnbs y ninguno es mío"),
      {"h2": "Forma 1: arbitraje (así empecé yo)",
       "p": ["Rentas un departamento, lo amueblas y lo publicas en Airbnb con permiso del dueño por contrato. Pagas una renta fija al mes; lo que cobras en Airbnb arriba de eso, menos gastos, es tu ganancia.",
             "Es la forma que deja más margen por departamento, pero también la que pide algo de capital al inicio: depósito, primer mes y muebles."]},
      {"h2": "Forma 2: co-hosting",
       "p": ["El dueño pone el departamento y tú lo operas: anuncio, huéspedes, limpieza, precios. A cambio cobras un porcentaje de lo que genere. La inversión es casi cero, pero el ingreso por departamento es menor."]},
      {"h2": "¿Cuál te conviene?",
       "lista": ["Si tienes algo de capital y quieres más ganancia por depa: arbitraje.",
                 "Si arrancas en ceros o todavía no quieres arriesgar una renta: co-hosting.",
                 "No tienes que elegir para siempre: muchas personas empiezan con co-hosting y después pasan al arbitraje."]},
      {"callout": "No es una mejor que la otra. Depende de con qué arrancas. Lo importante es empezar con un método, no con una corazonada."},
      {"h2": "Lo que de verdad hace la diferencia",
       "p": ["Después de años en este negocio, lo que separa a quien le va bien de quien se rinde no es el dinero inicial. Es saber elegir la zona, saber negociar con el dueño y tratar esto como un negocio desde el primer día."]},
    ],
  },
]

# carruseles para guías existentes del mismo tema
EXTRA = {
  "como-conseguir-departamentos-para-airbnb": car("como-conseguir-departamentos-para-airbnb", "Carrusel: así convencí al dueño de rentarme su depa para Airbnb",
      "Así lo hice yo, en el carrusel que subí a Instagram. Desliza para verlo →"),
  "cuanto-dinero-necesito-para-empezar-airbnb": car("cuanto-dinero-necesito-para-empezar-airbnb", "Carrusel: ¿cuánto necesitas para empezar un Airbnb?",
      "Lo resumí en este carrusel de Instagram. Desliza para ver todas las láminas →"),
  "errores-comunes-al-empezar-airbnb": car("errores-comunes-al-empezar-airbnb", "Carrusel: 3 errores que me costaron dinero con Airbnb",
      "Los 3 que me costaron dinero a mí, en carrusel. Desliza para verlos →"),
  "cohost-vs-arbitraje-airbnb": car("cohost-vs-arbitraje-airbnb", "Carrusel: ¿co-hosting o arbitraje? Cuál te conviene",
      "La comparación en carrusel. Desliza para ver todas las láminas →"),
}

por_slug = {g["slug"]: i for i, g in enumerate(G)}
for g in NUEVAS:
    if g["slug"] in por_slug:
        G[por_slug[g["slug"]]] = g
    else:
        G.append(g)
for slug, sec in EXTRA.items():
    g = G[por_slug[slug]]
    if not any("carrusel" in b for b in g["body"]):
        g["body"].insert(1, sec)

# en la guía de conseguir departamento, además del carrusel, el resumen de cómo lo hice yo
g = G[por_slug["como-conseguir-departamentos-para-airbnb"]]
if not any(b.get("h2") == "Así lo hice yo: no le pedí un favor, le ofrecí un negocio" for b in g["body"]):
    g["body"].insert(2, {"h2": "Así lo hice yo: no le pedí un favor, le ofrecí un negocio",
                         "lista": ["Le dije la verdad de frente: que el departamento era para Airbnb. Si el dueño se entera después, pierdes el depa y su confianza.",
                                   "Le llevé una propuesta donde él gana: renta puntual cada mes (llene o no llene), su depa bien cuidado y un solo responsable para todo.",
                                   "Dejamos el sí por escrito: contrato con cláusula de subarriendo permitido y depósito. Nada de acuerdos de palabra.",
                                   "Empecé con alguien que ya me conocía: el primer sí es más fácil cuando ya hay confianza."]})

json.dump(data, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("guías:", len(G))
