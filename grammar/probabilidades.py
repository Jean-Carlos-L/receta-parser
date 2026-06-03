"""Tabla de probabilidades manuales para la PCFG.

Se define como un diccionario con claves `(lhs, rhs_tuple)`.

Notas:

- Por simplicidad inicial, se incluyen probabilidades solo para no terminales de alto nivel
  donde existe ambiguedad estructural relevante.
- Para el resto, el sistema puede usar fallback uniforme si se habilita.
"""

# Key: (lhs, rhs_tuple)
# Value: probability in (0, 1]

PROB_TABLE = {
    # Preferir PARAM sobre PP/NP cuando aplica, para resolver ambiguedades PP vs PARAM.
    ("COMP", ("NP",)): 0.10,
    ("COMP", ("PP",)): 0.30,
    ("COMP", ("PARAM",)): 0.60,

    # Preferir NPs mas "completos" cuando son validos.
    ("NP", ("DET", "N", "ADJ")): 0.35,
    ("NP", ("DET", "N")): 0.25,
    ("NP", ("N", "ADJ")): 0.20,
    ("NP", ("QUANT", "N")): 0.10,
    ("NP", ("N",)): 0.10,

    # Mantener PP redundante pero preferir la forma general PREP NP.
    ("PP", ("PREP", "NP")): 0.70,
    ("PP", ("PREP", "NUM", "N")): 0.10,
    ("PP", ("PREP", "DET", "N")): 0.10,
    ("PP", ("PREP", "DET", "N", "ADJ")): 0.10,

    # Estructura principal: sin sesgo fuerte.
    ("VP", ("V", "COMPS")): 0.70,
    ("VP", ("V",)): 0.30,

    ("COMPS", ("COMP", "COMPS")): 0.55,
    ("COMPS", ("COMP",)): 0.45,

    ("INS", ("VP",)): 0.60,
    ("INS", ("ORDEN", "VP")): 0.40,

    ("LISTA_INS", ("INS", "<EOS>")): 0.55,
    ("LISTA_INS", ("INS", "<EOS>", "LISTA_INS")): 0.45,

    ("S", ("LISTA_INS",)): 1.0,
}
