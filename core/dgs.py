# ==================== UNIFICACIÓN ====================

def unificar(dag1, dag2):
    resultado = dict(dag1)

    for rasgo, valor in dag2.items():
        if rasgo in resultado:
            if isinstance(resultado[rasgo], dict) and isinstance(valor, dict):
                sub = unificar(resultado[rasgo], valor)
                if sub is None:
                    return None
                resultado[rasgo] = sub
            elif resultado[rasgo] != valor:
                return None
        else:
            resultado[rasgo] = valor

    return resultado


# ==================== CONCORDANCIA ====================

TERMINALES_CATEGORIA = {'V', 'N', 'ADJ', 'DET', 'QUANT', 'PREP', 'LEVEL', 'NUM', 'CONJ', 'ORDEN'}
SIMBOLOS_CONCORDANCIA = {'NP'}


def unificar_concordancia(hijos):
    unificado = None
    for hijo in hijos:
        if not hijo.rasgos:
            continue
        actual = {}
        for k in ('gen', 'num'):
            if k in hijo.rasgos:
                actual[k] = hijo.rasgos[k]
        if not actual:
            continue
        if unificado is None:
            unificado = actual
        else:
            unificado = unificar(unificado, actual)
            if unificado is None:
                return None
    return unificado or {}
