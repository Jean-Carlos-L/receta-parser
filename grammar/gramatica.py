from lexicon.rasgos import LEXICO_RASGOS

gramatica = {

    'S': [
        ['LISTA_INS']
    ],

    'LISTA_INS': [
        ['INS', '<EOS>'],
        ['INS', '<EOS>', 'LISTA_INS']
    ],

    'INS': [
        ['VP'],
        ['ORDEN', 'VP']
    ],

    'VP': [
        ['V', 'COMPS'],
        ['V']
    ],

    'COMPS': [
        ['COMP', 'COMPS'],
        ['COMP']
    ],

    'COMP': [
        ['NP'],
        ['PP'],
        ['PARAM']
    ],

    'NP': [
        ['DET', 'N', 'ADJ'],
        ['DET', 'N'],
        ['N', 'ADJ'],
        ['QUANT', 'N'],
        ['N']
    ],

    'PP': [
        ['PREP', 'NP'],
        ['PREP', 'NUM', 'N'],
        ['PREP', 'DET', 'N'],
        ['PREP', 'DET', 'N', 'ADJ']
    ],

    'PARAM': [
        ['durante', 'NUM', 'minutos'],
        ['durante', 'NUM', 'minutos', 'mas'],
        ['a', 'fuego', 'LEVEL'],
        ['al', 'final'],
        ['en', 'aceite', 'caliente']
    ],

    'V': [[t] for t, r in LEXICO_RASGOS.items() if r.get('cat') == 'v'],
    'N': [[t] for t, r in LEXICO_RASGOS.items() if r.get('cat') == 'n'],
    'ADJ': [[t] for t, r in LEXICO_RASGOS.items() if r.get('cat') == 'adj'],
    'DET': [[t] for t, r in LEXICO_RASGOS.items() if r.get('cat') == 'det'],
    'QUANT': [[t] for t, r in LEXICO_RASGOS.items() if r.get('cat') == 'quant'],
    'PREP': [[t] for t, r in LEXICO_RASGOS.items() if r.get('cat') == 'prep'],
    'LEVEL': [[t] for t, r in LEXICO_RASGOS.items() if r.get('cat') == 'level'],
    'NUM': [[t] for t, r in LEXICO_RASGOS.items() if r.get('cat') == 'num'],
    'ORDEN': [[t] for t, r in LEXICO_RASGOS.items() if r.get('cat') == 'orden']
}
