import matplotlib.pyplot as plt
import sys

from core.tokenizer import tokenize_receta
# from core.parser import parse
from core.printer import imprimir_derivacion
from core.dibujador import dibujar_arbol
from core.pcfg_bestfirst import parse_1best
from recipes.recetas import recetas


if __name__ == "__main__":

    receta_nombre = sys.argv[1] if len(sys.argv) > 1 else "sancocho"
    receta_texto = recetas.get(receta_nombre)
    if receta_texto is None:
        print(f"Receta '{receta_nombre}' no encontrada. Opciones: {', '.join(recetas)}")
        sys.exit(1)

    tokens = tokenize_receta(receta_texto)

    arbol, pos_final = parse_1best('S', tokens)

    print("\n" + "=" * 70)
    print(f"RECETA: {receta_nombre}")
    print("TOKENS:")
    print(tokens)

    print("\n" + "=" * 70)

    if arbol and pos_final == len(tokens):

        print("✅ RECETA PARSEADA CORRECTAMENTE")
        print("\nDERIVACIÓN COMPLETA:\n")

        imprimir_derivacion(arbol)

        print("\n🔷 ÁRBOL DE DERIVACIÓN (ventana gráfica)")
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.axis('off')
        dibujar_arbol(arbol, ax, 5, 5.5, 10)
        plt.title(f"Árbol de Derivación — {receta_nombre}", fontsize=12)
        plt.tight_layout()
        plt.show()

    else:

        print("❌ FALLÓ EL PARSEO")
        print(f"Progreso: {pos_final}/{len(tokens)} tokens")

        print("\nParte parseada:")
        print(' '.join(tokens[:pos_final]))

        print("\nFalla desde:")
        print(' '.join(tokens[pos_final:]))