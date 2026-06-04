from core.parser import parse
from core.tokenizer import tokenize_receta
from core.printer import imprimir_derivacion
from recipes.recetas import recetas


CASOS = [
    {
        "nombre": "sancocho_base",
        "texto": recetas["sancocho"],
    },
    {
        "nombre": "empanadas_base",
        "texto": recetas["empanadas"],
    },
    {
        "nombre": "chuleta_base",
        "texto": recetas["chuleta"],
    },
    {
        "nombre": "variante_1",
        "texto": "corta la yuca en trozos grandes\nagrega suficiente agua\ncocina a fuego medio durante cuarenta minutos",
    },
    {
        "nombre": "variante_2",
        "texto": "mezcla la masa\nfrie las empanadas en aceite caliente\nsirve las empanadas",
    },
    {
        "nombre": "variante_3",
        "texto": "agrega cebolla picada\nagrega cilantro picado\nrectifica la sal",
    },
    {
        "nombre": "arroz_atollado",
        "texto": recetas["arroz_atollado"],
    },
    {
        "nombre": "manjar_blanco",
        "texto": recetas["manjar_blanco"],
    },
    {
        "nombre": "pandebono",
        "texto": recetas["pandebono"],
    },
    {
        "nombre": "aborrajados",
        "texto": recetas["aborrajados"],
    },
    {
        "nombre": "marranitas",
        "texto": recetas["marranitas"],
    },
    {
        "nombre": "champus",
        "texto": recetas["champus"],
    },
    {
        "nombre": "lulada",
        "texto": recetas["lulada"],
    },
    {
        "nombre": "ceviche_camaron",
        "texto": recetas["ceviche_camaron"],
    },
    {
        "nombre": "sopa_pata",
        "texto": recetas["sopa_pata"],
    },
    {
        "nombre": "pescado_frito",
        "texto": recetas["pescado_frito"],
    },
]

def probar_caso(nombre, texto):
    print("\n" + "=" * 70)
    print(nombre)
    print("=" * 70)
    tokens = tokenize_receta(texto)
    arbol, pos_final = parse('S', tokens)
    ok = arbol is not None and pos_final == len(tokens)
    print(f"tokens={tokens}")
    print(f"resultado={'OK' if ok else 'FALLO'} ({pos_final}/{len(tokens)})")
    if arbol:
        imprimir_derivacion(arbol)
    else:
        print("sin arbol")
    return ok


if __name__ == "__main__":
    exitos = 0
    for caso in CASOS:
        if probar_caso(caso["nombre"], caso["texto"]):
            exitos += 1
    print(f"\n{'#' * 70}")
    print(f"Recetas: {exitos}/{len(CASOS)}")
