# Plan Tecnico: PCFG 1-best con Best-First (Optimo)

Este documento propone un plan para evolucionar el proyecto `receta-parser` para soportar desambiguacion mediante una PCFG (Probabilistic Context-Free Grammar) devolviendo unicamente el arbol **1-best** (el mas probable), usando un algoritmo **best-first optimo**. No se implementa la generacion/retorno de multiples arboles.

Restricciones asumidas (segun requisitos):

- La gramatica debe permanecer **ambigua** (redundancia intencional).
- Se puede usar PCFG con probabilidades **definidas a mano**.
- Se requiere el optimo **1-best** (no heuristico/avaro).
- La concordancia (DGS) se modela como **restriccion dura**: derivaciones que violen unificacion se descartan.

---

## 1. Arquitectura actual (resumen verificado)

### 1.1 Tokenizacion

- Archivo: `core/tokenizer.py`
- Normaliza a minusculas, elimina tildes, tokeniza por espacios.
- Inserta `'<EOS>'` al final de cada linea.
- `normalize_token()` aplica la misma normalizacion para comparaciones.
- Limitacion actual: el lexico contiene expresiones multipalabra (ej. `al gusto`) pero el tokenizer no las produce como un solo token.

### 1.2 Lexico con rasgos

- Archivo: `lexicon/rasgos.py` y modulos `lexicon/*.py`
- `LEXICO_RASGOS`: `token -> {cat, gen, num, ...}`.
- Genero y numero: heuristica por sufijo + excepciones.
- Terminales por categoria en DGS: `V, N, ADJ, DET, QUANT, PREP, LEVEL, NUM, CONJ, ORDEN` (`core/dgs.py`).
- Observacion verificada: no hay solapamientos lexicales (un token no pertenece a multiples categorias), lo cual simplifica desambiguacion (la ambiguedad es estructural, no lexical).

### 1.3 Gramatica

- Archivo: `grammar/gramatica.py`
- Representacion: `gramatica: dict[str, list[list[str]]]`.
- No terminales lexicos (`V`, `N`, etc.) se construyen dinamicamente desde `LEXICO_RASGOS`.
- Ambiguedad intencional: por ejemplo redundancias en `PP` y solapamientos `PP` vs `PARAM`.

### 1.4 Parser actual

- Archivo: `core/parser.py`
- Algoritmo: descendente recursivo con backtracking.
- Retorna un unico arbol: selecciona el analisis que consume mas tokens; en empates conserva el primero por orden de producciones.
- Punto donde se pierden alternativas: mantiene solo `mejor_nodo/mejor_pos`.
- Concordancia: se aplica solo en `NP` (`SIMBOLOS_CONCORDANCIA={'NP'}`) como filtro; si falla unificacion, se descarta esa produccion.

---

## 2. Diagnostico (ambiguedad y perdida de informacion)

1. El sistema actual explora alternativas, pero no conserva ni rankea derivaciones: el resultado es siempre un solo arbol.
2. La ambiguedad se pierde dentro del bucle de producciones del parser al escoger solo el parse con mayor avance.
3. La gramatica contiene ambiguedades estructurales reales (p. ej. `PP -> PREP NP` vs `PP -> PREP DET N` que pueden generar la misma cadena; `COMP -> PP` vs `COMP -> PARAM` para secuencias como `durante NUM minutos`).
4. Sin un mecanismo de ranking probabilistico, el comportamiento depende del orden de reglas y del criterio de "mayor consumo".

---

## 3. Objetivo de evolucion

Incorporar una PCFG y un algoritmo de busqueda que:

- Encuentre el arbol **1-best** globalmente mas probable bajo la PCFG.
- No requiera generar/retornar todos los arboles.
- Mantenga la gramatica ambigua (no se elimina redundancia).
- Respete la concordancia como restriccion dura (podando derivaciones invalidas).

---

## 4. Diseno: PCFG manual

### 4.1 Representacion de probabilidades

Agregar una tabla de probabilidades por produccion, separada de `grammar/gramatica.py`.

- Estructura recomendada:
  - clave: `(lhs: str, rhs: tuple[str, ...])`
  - valor: `prob: float` (internamente convertir a `log_prob`)

Reglas:

- Para cada `lhs`: `sum(prob(lhs -> *)) == 1`.
- Probabilidades estrictamente positivas.
- Politica si falta una regla en la tabla:
  - Opcion A (simple): asignar uniforme entre las producciones de ese `lhs`.
  - Opcion B (estricta): error de validacion (mas seguro, pero mas trabajo inicial).

### 4.2 Probabilidades lexicas

No se recomienda expandir `V -> token` como reglas probabilisticas individuales (seria enorme y no hay datos). Para mantener el 1-best estable:

- Tratar el match lexical por categoria como una transicion determinista (sin costo), o
- Asignar un costo constante por match lexical (equivalente entre alternativas si todas consumen el mismo numero de terminales).

---

## 5. Diseno: algoritmo 1-best (best-first optimo)

### 5.1 Por que no greedy

Una busqueda avara (tomar siempre la expansion local mas probable y descartar las demas) no garantiza el arbol 1-best global: una decision local puede bloquear o llevar a una derivacion final menos probable.

### 5.2 Busqueda de costo uniforme (Uniform-Cost / Dijkstra)

Modelar el parseo como un problema de busqueda en un espacio de estados.

#### Costo

- Para cada aplicacion de produccion `A -> rhs`: sumar costo `-log P(A->rhs)`.
- Los costos son no negativos y aditivos.

#### Estado (minimo viable)

- `pos`: indice en `tokens`.
- `pending`: secuencia (stack/cola) de simbolos aun por reconocer.
- `build`: informacion para reconstruir el arbol final (backpointer o acciones).
- `np_state`: estado de unificacion para concordancia cuando se este dentro de un `NP`.

#### Operadores

- Si `pending[0]` es terminal literal (p. ej. `'durante'`, `'<EOS>'`): consumir si coincide con `tokens[pos]`.
- Si `pending[0]` es terminal por categoria (p. ej. `N`, `V`, `PREP`): consumir si `LEXICO_RASGOS[tokens[pos]].cat == categoria`.
- Si `pending[0]` es no terminal (p. ej. `NP`, `PP`): expandir por cada produccion y agregar el costo correspondiente.

#### Condicion de exito

- `pending` vacio y `pos == len(tokens)`.

#### Garantia 1-best

Con uniform-cost, el primer estado de exito extraido de la cola de prioridad es el parse **mas probable** (1-best) segun la PCFG, sin enumerar todos los parses.

### 5.3 Poda segura (sin perder optimalidad)

Para controlar el espacio de busqueda sin perder el optimo:

- Dominancia/memoizacion:
  - mantener `best_cost_seen[key] = g_min`.
  - si un estado llega con el mismo `key` y `g >= g_min`, se descarta.
  - `key` debe incluir al menos: `(pos, pending_signature, np_signature)`.
- Concordancia como poda temprana:
  - durante la construccion de un `NP`, unificar rasgos incrementalmente.
  - si hay conflicto, descartar el estado.

Nota: el "descarte de menos probables" solo es correcto si esta fundamentado en estas podas seguras, no por mantener un beam fijo.

---

## 6. Modelado de concordancia y el "fallback" en 1-best

En un modelo 1-best, no existe un mecanismo especial de fallback.

- El "fallback" actual (p. ej. si `DET N ADJ` falla, entonces `DET N` funciona) se explica por la propia gramatica, que ya contiene ambas alternativas.
- En PCFG 1-best:
  - Derivaciones que violen concordancia (unificacion falla) se consideran **invalidas** y se podan.
  - El 1-best se elige entre las derivaciones restantes por probabilidad.

Ejemplo:

- Entrada: `la gallina cortado`
  - `NP -> DET N ADJ` se poda por conflicto de genero en `ADJ`.
  - `NP -> DET N` permanece y se selecciona (si es la mejor/valida).

---

## 7. Componentes a modificar / agregar (sin implementar)

### 7.1 Archivos nuevos sugeridos

- `grammar/probabilidades.py` (o `grammar/probabilidades.json`): tabla PCFG manual.
- `core/pcfg_bestfirst.py`: parser 1-best con uniform-cost.

### 7.2 Archivos existentes impactados (minimo)

- `core/parser.py`: mantener como baseline; opcional agregar wrapper `parse_1best_pcfg()`.
- `core/printer.py`: opcional imprimir `prob`/`logp` del arbol elegido.
- `test/`: agregar pruebas nuevas enfocadas a ambiguedad y seleccion 1-best.

---

## 8. Plan de implementacion (etapas)

### Etapa 1: Identificacion de ambiguedades objetivo

- Objetivo: listar frases tokenizables que produzcan 2+ derivaciones validas.
- Archivos: nuevos tests en `test/`.
- Validacion: cada caso debe tener al menos dos derivaciones posibles (verificable con instrumentacion temporal durante desarrollo).
- Riesgo: algunas ambiguedades teoricas pueden no aparecer por cobertura lexical/tokenizacion.

### Etapa 2: Modelo de PCFG (probabilidades)

- Objetivo: definir formato y validador (normalizacion por LHS).
- Archivos: `grammar/probabilidades.*`.
- Validacion: chequeo de suma=1 por LHS; reglas faltantes manejadas segun politica.

### Etapa 3: Parser 1-best best-first

- Objetivo: implementar uniform-cost sobre estados de parseo con backpointers.
- Archivos: `core/pcfg_bestfirst.py`.
- Dependencias: `grammar/gramatica.py`, `lexicon/rasgos.py`, `core/tokenizer.py`.
- Validacion:
  - Debe parsear los casos que hoy pasan (al menos los de `test/tests_recetas_dgs.py`) con probabilidades uniformes o razonables.
  - Debe seleccionar consistentemente el 1-best en casos ambiguos segun probabilidades manuales.

### Etapa 4: Poda segura + concordancia incremental

- Objetivo: eficiencia sin perder optimalidad.
- Implementar memoizacion por estado y poda por unificacion.
- Validacion: mismas salidas 1-best; mejoras observables en tiempo/estados explorados.

### Etapa 5: Integracion y ergonomia

- Objetivo: exponer una API clara:
  - `parse_best(simbolo, tokens, pcfg)`.
- Validacion: `main.py` puede escoger entre parser actual y PCFG 1-best.

---

## 9. Riesgos y consideraciones

- Greedy/beam no garantizan optimo 1-best; deben evitarse si el requisito es optimalidad.
- Sin una buena memoizacion, la busqueda puede crecer mucho en entradas largas.
- Tokenizacion multipalabra: si entra en alcance (ej. `al gusto`), habra que extender `tokenize_receta` (esto es independiente del 1-best, pero afecta cobertura).
- Probabilidades manuales: deben documentar el criterio (que ambiguedades se quieren favorecer) para que la desambiguacion sea justificable.
