def imprimir_derivacion(nodo, nivel=0):

    indent = "  " * nivel

    if nodo is None:
        return

    if nodo.valor:

        print(f"{indent}{nodo.etiqueta} → '{nodo.valor}'")

    else:

        if getattr(nodo, "rasgos", None):
            print(f"{indent}{nodo.etiqueta} → {nodo.rasgos}")
        else:
            print(f"{indent}{nodo.etiqueta} →")

        for hijo in nodo.hijos:
            imprimir_derivacion(hijo, nivel + 1)
