from core.tokenizer import tokenize_receta
from core.parser import parse


# Cada caso: (frase, esperado, descripcion)
# esperado = True  → el NP debe parsear correctamente
# esperado = False → el NP debe ser RECHAZADO por conflicto de género/número

CONCORDANCIA = [
    # ========== GÉNERO ==========
    ("el pollo",       True,  "correcto: masc + masc"),
    ("la pollo",       False, "error: det fem + n masc"),
    ("la gallina",     True,  "correcto: fem + fem"),
    ("el gallina",     False, "error: det masc + n fem"),
    ("la carne",       True,  "correcto: fem + fem (excepción)"),
    ("el carne",       False, "error: det masc + n fem"),
    ("la sal",         True,  "correcto: fem + fem (excepción)"),
    ("el sal",         False, "error: det masc + n fem"),
    ("la cebolla",     True,  "correcto: fem + fem"),
    ("el cebolla",     False, "error: det masc + n fem"),
    ("un pollo",       True,  "correcto: masc + masc"),
    ("una pollo",      False, "error: det fem + n masc"),
    ("una gallina",    True,  "correcto: fem + fem"),
    ("un gallina",     False, "error: det masc + n fem"),

    # ========== NÚMERO ==========
    ("los pollos",     True,  "correcto: plur + plur"),
    ("los pollo",      False, "error: det plur + n sing"),
    ("la gallina",     True,  "correcto: sing + sing"),
    ("las gallina",    False, "error: det plur + n sing"),
    ("las gallinas",   True,  "correcto: plur + plur"),
    ("el trozos",      False, "error: det sing + n plur"),
    ("los trozos",     True,  "correcto: plur + plur"),
    ("la papas",       False, "error: det sing + n plur"),
    ("las papas",      True,  "correcto: plur + plur"),

    # ========== DET + N + ADJ ==========
    ("la gallina cortada",   True,  "correcto: fem sing completo"),
    ("el gallina cortada",   False, "error: det masc + n fem"),
    ("la gallina cortado",   True,  "valido: DET+N funciona, adj descartado"),
    ("el pollo molido",      True,  "correcto: masc sing completo"),
    ("la pollo molido",      False, "error: det fem + n masc"),
    ("las papas grandes",    True,  "correcto: fem plur completo"),
    ("la papas grandes",     False, "error: det sing + n plur"),
    ("los trozos medianos",  True,  "correcto: masc plur completo"),
    ("el trozos medianos",   False, "error: det sing + n plur"),
    ("la cebolla picada",    True,  "correcto: fem sing"),
    ("los cebolla picada",   False, "error: det plur + n sing"),
    ("el cilantro picado",   True,  "correcto: masc sing"),
    ("la cilantro picado",   False, "error: det fem + n masc"),

    # ========== SIN DET (N + ADJ) ==========
    ("agua tibia",        True,  "correcto: fem sing sin det"),
    ("pollo molido",      True,  "correcto: masc sing sin det"),
    ("carne molida",      True,  "correcto: fem sing sin det"),
    ("cebolla picada",    True,  "correcto: fem sing sin det"),

    # ========== CON QUANT ==========
    ("suficiente agua",   True,  "correcto: quant + n"),
    ("suficiente sal",    True,  "correcto: quant + n"),
]


def probar_concordancia():
    print("=" * 70)
    print("PRUEBAS DE CONCORDANCIA (NP individual)")
    print("=" * 70)
    exitos = 0
    for frase, esperado, descripcion in CONCORDANCIA:
        tokens = tokenize_receta(frase + "\n")
        arbol, _ = parse('NP', tokens)
        obtenido = arbol is not None
        ok = obtenido == esperado
        estado = "✓" if ok else "✗"
        print(f"  {estado} {frase:30s} → {'OK' if obtenido else 'RECHAZADO'}  (esperado: {'OK' if esperado else 'RECHAZADO'})  {descripcion}")
        if ok:
            exitos += 1
    print(f"\n  Concordancia: {exitos}/{len(CONCORDANCIA)}")
    return exitos


if __name__ == "__main__":
    exitos = probar_concordancia()
    print(f"\n{'#' * 70}")
    print(f"Total: {exitos}/{len(CONCORDANCIA)}")
