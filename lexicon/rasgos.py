from lexicon.adjetivos import adjetivos
from lexicon.cuantificador import cuantificadores
from lexicon.determinantes import determinantes
from lexicon.level import level
from lexicon.numeros import numeros
from lexicon.orden import orden
from lexicon.preposiciones import preposiciones
from lexicon.sustantivos import sustantivos
from lexicon.verbos import verbos


# ==================== GÉNERO Y NÚMERO ====================

DET_GEN_NUM = {
    "el":   {"gen": "masc", "num": "sing"},
    "la":   {"gen": "fem",  "num": "sing"},
    "los":  {"gen": "masc", "num": "plur"},
    "las":  {"gen": "fem",  "num": "plur"},
    "un":   {"gen": "masc", "num": "sing"},
    "una":  {"gen": "fem",  "num": "sing"},
}

EXCEPCIONES_GENERO = {
    "carne": "fem",
    "sal":   "fem",
    "leche": "fem",
    "miel":  "fem",
    "mano":  "fem",
    "dia":   "masc",
    "agua":  "fem",
}


def _genero_numero(palabra):
    genero = EXCEPCIONES_GENERO.get(palabra)
    if genero is None:
        if palabra.endswith("a") or palabra.endswith("as"):
            genero = "fem"
        elif palabra.endswith("o") or palabra.endswith("os"):
            genero = "masc"
        else:
            genero = "masc"
    numero = "plur" if palabra.endswith("s") else "sing"
    return genero, numero


# ==================== BASE ====================

def _base(cat, **rasgos):
    data = {"cat": cat}
    data.update(rasgos)
    return data


LEXICO_RASGOS = {}

for t in determinantes:
    g_n = DET_GEN_NUM.get(t, {})
    LEXICO_RASGOS[t] = _base("det", **g_n)

for t in sustantivos:
    gen, num = _genero_numero(t)
    LEXICO_RASGOS[t] = _base("n", tipo="entidad", gen=gen, num=num)

for t in adjetivos:
    gen, num = _genero_numero(t)
    LEXICO_RASGOS[t] = _base("adj", tipo="estado", gen=gen, num=num)

for t in verbos:
    LEXICO_RASGOS[t] = _base("v", tipo="accion")

for t in preposiciones:
    LEXICO_RASGOS[t] = _base("prep")

for t in numeros:
    LEXICO_RASGOS[t] = _base("num")

for t in cuantificadores:
    LEXICO_RASGOS[t] = _base("quant")

for t in level:
    LEXICO_RASGOS[t] = _base("level")

for t in orden:
    LEXICO_RASGOS[t] = _base("orden")