from core.tokenizer import tokenize_receta
from core.pcfg_bestfirst import parse_1best
from recipes.recetas import recetas


def run():
    exitos = 0
    total = len(recetas)

    print("=" * 70)
    print("PRUEBAS DE RECETAS COMPLETAS (PCFG 1-best)")
    print("=" * 70)

    for nombre, texto in recetas.items():
        tokens = tokenize_receta(texto)
        arbol, pos_final = parse_1best('S', tokens)
        ok = arbol is not None and pos_final == len(tokens)
        estado = "✓" if ok else "✗"
        print(f"  {estado} {nombre:25s} → {'OK' if ok else 'FALLO'} ({pos_final}/{len(tokens)})")
        if ok:
            exitos += 1

    print(f"\n  Recetas: {exitos}/{total} ✅")
    return exitos


if __name__ == "__main__":
    run()
