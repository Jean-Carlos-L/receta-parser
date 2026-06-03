from core.tokenizer import tokenize_receta
from core.pcfg_bestfirst import parse_1best


def _find_first(n, etiqueta):
    if n.etiqueta == etiqueta:
        return n
    for h in n.hijos:
        got = _find_first(h, etiqueta)
        if got is not None:
            return got
    return None


def _assert(cond, msg):
    if not cond:
        raise AssertionError(msg)


def test_param_over_pp_durante():
    tokens = tokenize_receta("cocina durante cuarenta minutos\n")
    arbol, pos = parse_1best("S", tokens)
    _assert(arbol is not None, "No se genero arbol")
    _assert(pos == len(tokens), f"No consumio todo: {pos}/{len(tokens)}")
    _assert(_find_first(arbol, "PARAM") is not None, "Se esperaba PARAM en el arbol")


def test_param_over_pp_en_aceite_caliente():
    # Nota: evitar sustantivos que no esten en el lexico actual.
    tokens = tokenize_receta("frie carne en aceite caliente\n")
    arbol, pos = parse_1best("S", tokens)
    _assert(arbol is not None, "No se genero arbol")
    _assert(pos == len(tokens), f"No consumio todo: {pos}/{len(tokens)}")
    _assert(_find_first(arbol, "PARAM") is not None, "Se esperaba PARAM en el arbol")


def test_pp_redundancy_still_parses():
    tokens = tokenize_receta("agrega con la cebolla\n")
    arbol, pos = parse_1best("S", tokens)
    _assert(arbol is not None, "No se genero arbol")
    _assert(pos == len(tokens), f"No consumio todo: {pos}/{len(tokens)}")
    _assert(_find_first(arbol, "PP") is not None, "Se esperaba PP en el arbol")


def test_concordance_is_hard_constraint():
    # "la gallina cortado" no es parseable como S con la gramatica actual.
    # Verificamos la poda por concordancia a nivel NP.
    tokens = tokenize_receta("la gallina cortado\n")
    arbol, pos = parse_1best("NP", tokens)
    _assert(arbol is not None, "No se genero NP")
    _assert(pos == 2, f"Se esperaba fallback a DET N (2 tokens), obtuvo {pos}")


def run():
    tests = [
        test_param_over_pp_durante,
        test_param_over_pp_en_aceite_caliente,
        test_pp_redundancy_still_parses,
        test_concordance_is_hard_constraint,
    ]
    ok = 0
    for t in tests:
        t()
        ok += 1
    print(f"PCFG 1-best: {ok}/{len(tests)}")


if __name__ == "__main__":
    run()
