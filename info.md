# Informe del proyecto — DCG para recetas vallecaucanas

## Estructura final del proyecto

```
receta-parser/
│
├── core/
│   ├── dcg.py              # DCG: unificación + concordancia
│   ├── parser.py           # Parser recursivo descendente
│   ├── node.py             # Nodo del árbol sintáctico
│   ├── printer.py          # Impresión del árbol de derivación
│   └── tokenizer.py        # Tokenización de recetas
│
├── lexicon/
│   ├── rasgos.py           # Léxico completo con rasgos lingüísticos
│   ├── sustantivos.py      # Conjunto de sustantivos
│   ├── verbos.py           # Conjunto de verbos
│   ├── adjetivos.py        # Conjunto de adjetivos
│   ├── determinantes.py    # Conjunto de determinantes
│   ├── preposiciones.py    # Conjunto de preposiciones
│   ├── numeros.py          # Conjunto de números
│   ├── cuantificador.py    # Conjunto de cuantificadores
│   ├── conjunciones.py     # Conjunto de conjunciones
│   ├── level.py            # Niveles de cocción
│   └── orden.py            # Ordenadores (primero, despues)
│
├── grammar/
│   └── gramatica.py        # Reglas de producción gramatical
│
├── recipes/
│   └── recetas.py          # 13 recetas vallecaucanas
│
├── tests_recetas_dcg.py    # Pruebas: parseo de recetas completas (16 casos)
├── tests_concordancia.py   # Pruebas: concordancia género/número (42 casos)
├── main.py                 # Punto de entrada
├── info.md                 # Este documento

└── SIGUIENTE_PASO.md       # Extensiones futuras
```

---

## 1. ¿Qué es un DCG y cómo funciona aquí?

Un DCG (Definite Clause Grammar / Gramática de Cláusulas Definidas) extiende una gramática libre de contexto añadiendo **rasgos lingüísticos** y **unificación** para validar restricciones como concordancia de género y número.

En este proyecto, cada palabra del léxico tiene asociado un diccionario de rasgos:

```python
# El léxico con rasgos se ve así:
LEXICO_RASGOS = {
    "el":   {"cat": "det", "gen": "masc", "num": "sing"},
    "la":   {"cat": "det", "gen": "fem",  "num": "sing"},
    "los":  {"cat": "det", "gen": "masc", "num": "plur"},
    "las":  {"cat": "det", "gen": "fem",  "num": "plur"},
    "gallina": {"cat": "n", "tipo": "entidad", "gen": "fem", "num": "sing"},
    "pollo":   {"cat": "n", "tipo": "entidad", "gen": "masc", "num": "sing"},
    "trozos":  {"cat": "n", "tipo": "entidad", "gen": "masc", "num": "plur"},
    "picada":  {"cat": "adj", "tipo": "estado", "gen": "fem", "num": "sing"},
    "picado":  {"cat": "adj", "tipo": "estado", "gen": "masc", "num": "sing"},
}
```

---

## 2. Separación en archivos

Originalmente el DCG estaba mezclado en varios archivos. Se separó en módulos con responsabilidades claras.

### 2.1 `core/dcg.py` — núcleo del DCG

Contiene todo lo relacionado con el sistema de rasgos y unificación:

**Unificación:**

```python
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
                return None  # Conflicto
        else:
            resultado[rasgo] = valor
    return resultado
```

Ejemplos:

```python
>>> unificar({'gen': 'fem', 'num': 'sing'}, {'gen': 'fem', 'num': 'sing'})
{'gen': 'fem', 'num': 'sing'}  # Compatible ✅

>>> unificar({'gen': 'fem', 'num': 'sing'}, {'gen': 'masc', 'num': 'sing'})
None  # Conflicto de género ❌
```

**Concordancia:**

```python
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
```

### 2.2 `core/parser.py` — ahora más limpio

Antes contenía la lógica de unificación inline. Ahora solo importa lo que necesita:

```python
from core.dcg import TERMINALES_CATEGORIA, SIMBOLOS_CONCORDANCIA, unificar_concordancia
```

Y la validación de concordancia se reduce a:

```python
if simbolo in SIMBOLOS_CONCORDANCIA:
    concordancia = unificar_concordancia(hijos)
    if concordancia is None:
        continue  # Descartar producción por conflicto
```

### 2.3 Archivos eliminados

- `core/unification.py` → se fusionó dentro de `core/dcg.py`

---

## 3. Cómo se aplica la unificación en el parseo

### 3.1 Solo en NP

La unificación solo se aplica dentro de sintagmas nominales (`NP`). El resto de la gramática funciona por expansión normal.

```
NP → DET N ADJ
     ├── DET:  rasgos = {gen: fem, num: sing}  (ej: "la")
     ├── N:    rasgos = {gen: fem, num: sing}  (ej: "gallina")
     └── ADJ:  rasgos = {gen: fem, num: sing}  (ej: "cortada")
     └── unificar() → {gen: fem, num: sing} ✅ → NP válido
```

### 3.2 Cuándo se rechaza un NP

| Frase | DET | N | Conflicto | Resultado |
|-------|-----|---|-----------|-----------|
| `el gallina` | masc, sing | fem, sing | género | ❌ Rechazado |
| `la pollo` | fem, sing | masc, sing | género | ❌ Rechazado |
| `los gallina` | masc, plur | fem, sing | número + género | ❌ Rechazado |
| `el trozos` | masc, sing | masc, plur | número | ❌ Rechazado |

### 3.3 Cuándo se acepta un NP

| Frase | DET | N | ADJ | Unificación | Resultado |
|-------|-----|---|-----|-------------|-----------|
| `la gallina cortada` | fem, sing | fem, sing | fem, sing | `{fem, sing}` | ✅ |
| `el pollo molido` | masc, sing | masc, sing | masc, sing | `{masc, sing}` | ✅ |
| `las papas grandes` | fem, plur | fem, plur | masc, plur | `{fem, plur}` | ✅ |
| `agua tibia` | _(sin DET)_ | fem, sing | fem, sing | `{fem, sing}` | ✅ |
| `carne molida` | _(sin DET)_ | fem, sing | fem, sing | `{fem, sing}` | ✅ |

### 3.4 Fallback a producción más corta

Si `DET + N + ADJ` falla por concordancia, el parser intenta `DET + N`:

```python
# "la gallina cortado"
# DET+N+ADJ → falla (gen fem ≠ masc en ADJ)
# DET+N     → funciona ("la gallina" es válido)
# Resultado: NP válido, ADJ descartado
```

---

## 4. Léxico con rasgos

### 4.1 Determinantes (hardcodeados)

```python
DET_GEN_NUM = {
    "el":   {"gen": "masc", "num": "sing"},
    "la":   {"gen": "fem",  "num": "sing"},
    "los":  {"gen": "masc", "num": "plur"},
    "las":  {"gen": "fem",  "num": "plur"},
    "un":   {"gen": "masc", "num": "sing"},
    "una":  {"gen": "fem",  "num": "sing"},
}
```

### 4.2 Sustantivos y adjetivos (heurística)

Se usa una heurística basada en la terminación de la palabra:

```python
def _genero_numero(palabra):
    genero = EXCEPCIONES_GENERO.get(palabra)
    if genero is None:
        if palabra.endswith("a") or palabra.endswith("as"):
            genero = "fem"
        elif palabra.endswith("o") or palabra.endswith("os"):
            genero = "masc"
        else:
            genero = "masc"
    numero = "plur" if palabra.endswith("s") else "sing"
    return genero, numero
```

| Terminación | Género | Ejemplos |
|-------------|--------|----------|
| `-a`, `-as` | femenino | `gallina`, `papas`, `cebolla`, `picada` |
| `-o`, `-os` | masculino | `pollo`, `trozos`, `picado`, `molido` |
| `-e`, consonante | masculino (default) | `aceite`, `tomate`, `sal`, `carne` |

### 4.3 Excepciones

Palabras que no siguen la regla general:

```python
EXCEPCIONES_GENERO = {
    "carne": "fem",   # termina en -e, pero es femenino
    "sal":   "fem",   # termina en consonante, pero es femenino
    "leche": "fem",
    "miel":  "fem",
    "mano":  "fem",   # termina en -o, pero es femenino
    "dia":   "masc",  # termina en -a, pero es masculino
}
```

---

## 5. Gramática actual

```
S        → LISTA_INS
LISTA_INS → INS '<EOS>' | INS '<EOS>' LISTA_INS
INS      → VP | ORDEN VP
VP       → V COMPS | V
COMPS    → COMP COMPS | COMP
COMP     → NP | PP | PARAM
NP       → DET N ADJ | DET N | N ADJ | QUANT N | N
PP       → PREP NP | PREP NUM N | PREP DET N | PREP DET N ADJ
PARAM    → 'durante' NUM 'minutos'
         | 'durante' NUM 'minutos' 'mas'
         | 'a' 'fuego' LEVEL
         | 'al' 'final'
         | 'en' 'aceite' 'caliente'
```

Las reglas léxicas (`V`, `N`, `DET`, etc.) se generan dinámicamente desde `LEXICO_RASGOS`:

```python
'V': [[t] for t, r in LEXICO_RASGOS.items() if r.get('cat') == 'v'],
'N': [[t] for t, r in LEXICO_RASGOS.items() if r.get('cat') == 'n'],
```

---

## 6. Recetas disponibles

### 6.1 Originales (3)

| Receta | Descripción |
|--------|-------------|
| Sancocho | Sancocho de gallina vallecaucano |
| Empanadas | Empanadas de carne y papa |
| Chuleta | Chuleta de pollo empanizada |

### 6.2 Nuevas (10)

| Receta | Ingredientes principales |
|--------|------------------------|
| Arroz atollado | Pollo, arroz, cebolla, tomate |
| Manjar blanco | Leche, arroz, panela, canela |
| Pandebono | Harina, queso, huevo |
| Aborrajados | Plátano, queso, harina |
| Marranitas | Plátano, cerdo |
| Champús | Maíz, piña, lulo, panela |
| Lulada | Lulo, agua, azúcar |
| Ceviche de camarón | Camarones, limón, cebolla, tomate |
| Sopa de pata | Res, yuca, papa, maíz |
| Pescado frito | Pescado, limón, sal |

---

## 7. Pruebas

### 7.1 `tests_recetas_dcg.py`

Prueba que las recetas completas se parseen correctamente:

```bash
python3 tests_recetas_dcg.py
# Recetas: 16/16 ✅
```

Cada caso tokeniza la receta completa y verifica que el parser consuma todos los tokens desde el símbolo inicial `S`.

### 7.2 `tests_concordancia.py`

Prueba la concordancia de género y número en NPs individuales:

```bash
python3 tests_concordancia.py
# Concordancia: 42/42 ✅
```

Cada caso verifica que un NP específico sea aceptado o rechazado según su concordancia:

```
  ✓ el pollo           → OK         (esperado: OK)         correcto: masc + masc
  ✓ la pollo           → RECHAZADO  (esperado: RECHAZADO)  error: det fem + n masc
  ✓ la gallina cortada → OK         (esperado: OK)         correcto: fem sing completo
  ✓ el gallina cortada → RECHAZADO  (esperado: RECHAZADO)  error: det masc + n fem
  ✓ los trozos         → OK         (esperado: OK)         correcto: plur + plur
  ✓ el trozos          → RECHAZADO  (esperado: RECHAZADO)  error: det sing + n plur
```

---

## 8. Cobertura léxica

| Categoría | Cantidad | Ejemplos |
|-----------|----------|----------|
| Verbos | 37 | corta, agrega, cocina, mezcla, frie, pela, machaca, sofrie, sirve |
| Sustantivos | 75 | gallina, pollo, cerdo, carne, yuca, papa, platano, arroz, maiz, lulo |
| Adjetivos | 34 | picado, molido, cortada, grande, mediano, caliente, tibio, machacado |
| Determinantes | 7 | el, la, los, las, un, una |
| Preposiciones | 8 | con, en, por, hasta, de, durante, para, a |
| Números | 36 | uno, dos, ..., treinta, cuarenta, cincuenta |
| Cuantificadores | 5 | al gusto, un poco, suficiente |
| Niveles | 3 | bajo, medio, alto |
| Ordenadores | 2 | primero, despues |
| Conjunciones | 3 | y, e, luego |

---

## 9. Limitaciones

1. **Unificación solo en NP**: no se valida concordancia verbo-sujeto ni argumentos del verbo
2. **Heurística simple**: palabras como `mano` (fem) o `agua` (fem con artículo `el`) necesitan excepciones explícitas
3. **Sin expresiones multipalabra**: tokens como `al gusto` o `a fuego medio` se tratan como tokens separados
4. **Gramática fija**: no maneja oraciones subordinadas ni estructuras complejas
5. **Sin semántica**: el parser reconoce estructura pero no extrae significado (acción, ingrediente, tiempo)

---

## 10. Cómo agregar una receta nueva

1. Agregar ingredientes nuevos a `lexicon/sustantivos.py` (si es necesario)
2. Agregar verbos nuevos a `lexicon/verbos.py` (si es necesario)
3. Agregar adjetivos nuevos a `lexicon/adjetivos.py` (si es necesario)
4. Escribir la receta en `recipes/recetas.py` en el mismo formato
5. Agregar el caso de prueba en `tests_recetas_dcg.py`
6. Ejecutar `python3 tests_recetas_dcg.py` para verificar

**Reglas para que una receta sea parseable:**
- Cada instrucción en una línea separada
- Usar verbos del léxico en imperativo (3ª persona singular)
- Los ingredientes deben ser sustantivos del léxico
- Los adjetivos deben concordar en género y número con el sustantivo
- Terminar cada instrucción con salto de línea (el tokenizer agrega `<EOS>` automáticamente)
