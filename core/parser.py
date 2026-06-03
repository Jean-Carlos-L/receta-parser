from grammar.gramatica import gramatica
from core.node import Nodo
from core.dgs import TERMINALES_CATEGORIA, SIMBOLOS_CONCORDANCIA, unificar_concordancia
from lexicon.rasgos import LEXICO_RASGOS
from core.tokenizer import normalize_token


# ==================== PARSER ====================

def parse(simbolo, tokens, pos=0):

    if simbolo in TERMINALES_CATEGORIA:
        if pos < len(tokens):
            token = normalize_token(tokens[pos])
            rasgos = LEXICO_RASGOS.get(token)
            if rasgos and rasgos.get('cat') == simbolo.lower():
                nodo = Nodo(simbolo, valor=token)
                nodo.rasgos = dict(rasgos)
                return nodo, pos + 1
        return None, pos

    # ==================== TERMINALES LITERALES ====================

    if simbolo not in gramatica:

        if pos < len(tokens) and normalize_token(tokens[pos]) == normalize_token(simbolo):
            nodo = Nodo(simbolo, valor=simbolo)
            nodo.rasgos = dict(LEXICO_RASGOS.get(simbolo, {}))
            return nodo, pos + 1

        return None, pos

    # ==================== NO TERMINALES ====================

    mejor_nodo = None
    mejor_pos = pos

    for produccion in gramatica[simbolo]:

        hijos = []
        pos_actual = pos
        exito = True

        for subsimbolo in produccion:

            hijo, nueva_pos = parse(subsimbolo, tokens, pos_actual)

            if hijo is None:
                exito = False
                break

            hijos.append(hijo)
            pos_actual = nueva_pos

        if exito and pos_actual > mejor_pos:
            nodo = Nodo(simbolo, hijos)
            if simbolo in SIMBOLOS_CONCORDANCIA:
                concordancia = unificar_concordancia(hijos)
                if concordancia is None:
                    continue
                nodo.rasgos = concordancia
            else:
                rasgos = {}
                for hijo in hijos:
                    if hijo.rasgos:
                        rasgos.update(hijo.rasgos)
                nodo.rasgos = rasgos
            mejor_nodo = nodo
            mejor_pos = pos_actual

    return mejor_nodo, mejor_pos
