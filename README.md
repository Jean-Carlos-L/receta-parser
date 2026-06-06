
# Construcción de sistema de PLN para el análisis de recetas de cocina vallecaucanas

**Fecha:** 06/06/2026

**Curso:** Procesamiento del Lenguaje Natural

---

## Integrantes del Grupo

| Nombre Completo           | Código  | Rol           | Correo Electrónico                 |
| ------------------------- | ------- | ------------- | ---------------------------------- |
| Juan Camilo Garcia        | 2259416 | Colaborador   | [juan.garcia.saenz@correounivalle.edu.co] |
| Jhojan Serna Henao        | 2259504 | Colaborador   | [jhojan.serna@correounivalle.edu.co] |
| Jean Carlos Lerma         |  | Colaborador   | [jean.lerma@correounivalle.edu.co] |

---

# Receta Parser

Analizador sintáctico para recetas de cocina vallecaucanas basado en gramáticas libres de contexto, unificación de rasgos y parsing probabilístico.

## 1. Descripción general del proyecto

**Receta Parser** es un sistema de Procesamiento de Lenguaje Natural (PLN) diseñado para analizar sintácticamente recetas de cocina escritas en español. El proyecto toma como dominio las recetas tradicionales de la región del Valle del Cauca, Colombia, y produce árboles de derivación que revelan la estructura gramatical subyacente de cada instrucción culinaria.

### Problema que resuelve

Las recetas de cocina son un tipo de texto semi-estructurado con un vocabulario acotado y una sintaxis relativamente predecible, pero con ambigüedades estructurales que un analizador básico no puede resolver. Por ejemplo, la frase *"en aceite caliente"* puede interpretarse como un sintagma preposicional (PP) o como un parámetro de cocción (PARAM). El sistema utiliza mecanismos lingüísticos y probabilísticos para desambiguar y encontrar la interpretación más plausible.

### Objetivos principales

- Implementar un parser para un subconjunto del español restringido al dominio culinario.
- Validar concordancia de género y número entre determinantes, sustantivos y adjetivos mediante un sistema de unificación de rasgos.
- Resolver ambigüedades estructurales mediante una gramática probabilística (PCFG) con búsqueda del mejor análisis (*1-best*).
- Visualizar los árboles de derivación generados.

## 2. Arquitectura general

El sistema sigue un flujo secuencial de procesamiento en cinco etapas:

```
Entrada (receta en texto plano)
        │
        ▼
    ┌─────────┐
    │Tokenizer│  Divide el texto en tokens y normaliza (minúsculas, sin tildes)
    └────┬────┘
         │ lista de tokens
         ▼
    ┌──────────┐
    │  Parser  │  Aplica la gramática CFG + reglas DCG (unificación)
    │  (DCG)   │  usando búsqueda con PCFG (best-first)
    └────┬─────┘
         │ árbol sintáctico
         ▼
    ┌───────────┐
    │  Printer  │  Imprime la derivación completa en consola
    └─────┬─────┘
          │
          ▼
    ┌────────────┐
    │ Dibujador  │  Visualiza el árbol con matplotlib
    └────────────┘
```

### Componentes principales

- **Tokenizador**: Convierte el texto crudo en una secuencia de tokens normalizados.
- **Parser DCG**: Analiza la secuencia de tokens aplicando reglas gramaticales con restricciones de concordancia.
- **PCFG (best-first)**: Guía el proceso de parseo con probabilidades para seleccionar el árbol más probable.
- **Impresor**: Muestra la derivación completa en formato legible.
- **Dibujador**: Genera una visualización gráfica del árbol sintáctico.

## 3. Tecnologías utilizadas

- **Python 3**: Lenguaje de implementación. Se usa la biblioteca estándar para la lógica central.
- **matplotlib**: Generación de la representación visual del árbol de derivación.
- **heapq** (std lib): Cola de prioridad para la búsqueda best-first del PCFG.
- **dataclasses** (std lib): Modelado de reglas y estados de parseo.
- **typing** (std lib): Anotaciones de tipos para claridad y mantenibilidad del código.

No se utilizan frameworks externos de PLN (NLTK, spaCy, etc.). Todo el sistema está implementado desde cero como ejercicio académico.

## 4. Componentes del sistema

### 4.1 `core/` — Núcleo del parser

| Archivo | Responsabilidad |
|---------|----------------|
| `core/tokenizer.py` | Normaliza el texto (minúsculas, eliminación de tildes) y lo divide en tokens. Cada línea delimitada por salto de línea se considera una instrucción y recibe un marcador `<EOS>` al final. |
| `core/node.py` | Define la clase `Nodo`, la estructura base del árbol sintáctico. Cada nodo tiene una etiqueta, una lista de hijos, un valor (si es terminal) y un diccionario de rasgos. |
| `core/parser.py` | Parser recursivo descendente que implementa el DCG. Expande símbolos no terminales siguiendo las producciones de la gramática y aplica unificación de concordancia en los sintagmas nominales (`NP`). |
| `core/dcg.py` | Contiene el sistema de unificación (algoritmo de unificación de DAGs) y las funciones de validación de concordancia de género y número. Define qué símbolos requieren concordancia (`SIMBOLOS_CONCORDANCIA = {'NP'}`). |
| `core/pcfg_bestfirst.py` | Parser basado en búsqueda best-first con costo uniforme. Utiliza la PCFG para expandir producciones, priorizando las de mayor probabilidad (menor costo logarítmico). Retorna el mejor árbol (1-best). |
| `core/printer.py` | Recorre el árbol sintáctico en profundidad e imprime la derivación completa con sangría jerárquica. |
| `core/dibujador.py` | Dibuja el árbol sintáctico usando matplotlib, posicionando los nodos recursivamente según la cantidad de hojas de cada subárbol. |

### 4.2 `grammar/` — Gramática y probabilidades

| Archivo | Responsabilidad |
|---------|----------------|
| `grammar/gramatica.py` | Define la gramática libre de contexto como un diccionario. Las reglas léxicas (`V`, `N`, `DET`, etc.) se generan dinámicamente a partir del léxico con rasgos. |
| `grammar/pcfg.py` | Implementa la clase `PCFG` y la función `build_pcfg()`. Almacena reglas con probabilidades en escala logarítmica y permite *fallback* uniforme para producciones sin probabilidad explícita. |
| `grammar/probabilidades.py` | Tabla manual de probabilidades (`PROB_TABLE`) que asigna pesos a las producciones ambiguas para guiar la desambiguación. |

### 4.3 `lexicon/` — Léxico

Cada archivo define un conjunto de palabras de una categoría gramatical específica. El módulo `lexicon/rasgos.py` consolida todos los conjuntos en un único diccionario `LEXICO_RASGOS`, donde cada palabra tiene asociados su categoría y rasgos morfológicos (género, número, tipo).

| Archivo | Categoría | Cantidad |
|---------|-----------|----------|
| `lexicon/verbos.py` | Verbos en imperativo | ~37 |
| `lexicon/sustantivos.py` | Ingredientes y utensilios | ~75 |
| `lexicon/adjetivos.py` | Estados y tamaños | ~34 |
| `lexicon/determinantes.py` | Artículos | 7 |
| `lexicon/preposiciones.py` | Preposiciones | 8 |
| `lexicon/numeros.py` | Números en texto y dígitos | ~36 |
| `lexicon/cuantificador.py` | Cuantificadores | 5 |
| `lexicon/level.py` | Niveles de cocción | 3 |
| `lexicon/orden.py` | Marcadores de orden | 2 |

### 4.4 `recipes/` — Recetas

Define 13 recetas vallecaucanas en texto plano, cada una como una cadena multilínea. Cada línea es una instrucción independiente. Ejemplos: sancocho, empanadas, chuleta, pandebono, manjar blanco, champús, lulada, etc.

### 4.5 `test/` — Pruebas

| Archivo | Propósito |
|---------|-----------|
| `test/tests_recetas_dcg.py` | Verifica que las 13 recetas y 3 variantes adicionales se parseen completamente con el parser DCG. |
| `test/tests_concordancia.py` | 42 casos que validan la corrección del sistema de concordancia de género y número en NPs. |
| `test/tests_recetas_pcfg.py` | Verifica que las 13 recetas se parseen correctamente con el PCFG 1-best. |
| `test/tests_pcfg_1best.py` | Pruebas específicas del parser PCFG: preferencia de PARAM sobre PP, respeto de la concordancia como restricción dura. |

## 5. Fundamentos teóricos implementados

### 5.1 CFG (Context Free Grammar / Gramática Libre de Contexto)

La columna vertebral del sistema es una gramática libre de contexto definida en `grammar/gramatica.py`. Las reglas de producción tienen la forma `A → α`, donde `A` es un símbolo no terminal y `α` es una secuencia de símbolos terminales y no terminales.

**Papel dentro del sistema**: Define la estructura sintáctica válida de las recetas: una receta es una lista de instrucciones (`LISTA_INS`), cada instrucción es un sintagma verbal (`VP`) opcionalmente precedido por un marcador de orden (`ORDEN`), el verbo puede tener complementos (`COMPS`), y estos pueden ser sintagmas nominales (`NP`), preposicionales (`PP`) o parámetros (`PARAM`).

**Beneficio**: Permite modelar relaciones jerárquicas como "una receta contiene instrucciones, que contienen verbos y complementos" de forma natural y expresiva.

### 5.2 DCG (Definite Clause Grammar / Gramática de Cláusulas Definidas)

El sistema extiende la CFG añadiendo **rasgos lingüísticos** (como género y número) y un mecanismo de **unificación** para validar restricciones de concordancia. Esto convierte al parser en una implementación de DCG.

**Papel dentro del sistema**: Cada palabra del léxico tiene un diccionario de rasgos (ej: `"gallina": {"cat": "n", "gen": "fem", "num": "sing"}`). Cuando el parser construye un `NP`, unifica los rasgos de género y número de todos sus hijos (determinante, sustantivo, adjetivo). Si la unificación falla (ej: "la pollo": femenino vs masculino), la producción se descarta.

**Beneficio**: Permite rechazar frases agramaticales como *"el gallina"* o *"los gallina"* que una CFG pura aceptaría, mejorando la precisión del análisis sin necesidad de reglas separadas para cada combinación.

### 5.3 PCFG (Probabilistic Context Free Grammar / Gramática Libre de Contexto Probabilística)

Cada regla de producción tiene asociada una probabilidad (en `grammar/probabilidades.py`), de modo que la gramática asigna un peso a cada posible derivación.

**Papel dentro del sistema**: Cuando existen múltiples análisis válidos para una misma frase (ambigüedad estructural), la PCFG permite seleccionar el más probable. Por ejemplo, la producción `PARAM` tiene probabilidad 0.6 frente a `PP` con 0.3 en el contexto de `COMP`, lo que hace que el sistema prefiera interpretar *"en aceite caliente"* como un parámetro de cocción en lugar de un sintagma preposicional genérico.

**Beneficio**: Resuelve ambigüedades de forma cuantitativa y fundamentada, emulando el conocimiento de dominio de un hablante nativo.

### 5.4 Parser (Analizador Sintáctico)

El sistema cuenta con dos implementaciones de parser:

1. **Parser recursivo descendente** (`core/parser.py`): Explora las producciones en profundidad, intentando cada alternativa en orden hasta encontrar una que consuma todos los tokens. Es simple e ilustrativo.

2. **Parser best-first con PCFG** (`core/pcfg_bestfirst.py`): Utiliza una cola de prioridad (algoritmo de costo uniforme) para expandir las producciones en orden de probabilidad decreciente. Implementa el concepto de "estado" de parseo (posición actual, símbolos pendientes, pila de nodos) y marcadores de reducción (`@REDUCE`) para reconstruir el árbol. Retorna el árbol más probable que consume la mayor cantidad de tokens.

**Beneficio**: La combinación de ambos permite contrastar un enfoque determinista puro con uno probabilístico, demostrando cómo las probabilidades mejoran la calidad de la desambiguación.

## 6. Justificación de diseño: uso y descarte de DFA

### ¿Por qué no se utilizó DFA?

Durante la fase de planeación inicial del proyecto se contempló el uso de Autómatas Finitos Deterministas (DFA) como posible mecanismo de reconocimiento sintáctico. Sin embargo, esta aproximación fue descartada por las siguientes razones técnicas:

El objetivo principal del proyecto era el **análisis sintáctico de estructuras lingüísticas** con relaciones jerárquicas y de dependencia no local (como la concordancia entre un determinante al inicio de un sintagma nominal y un adjetivo al final). Las gramáticas libres de contexto (CFG, DCG y PCFG) ofrecen una representación natural y expresiva para modelar este tipo de relaciones, ya que permiten capturar la estructura de constituyentes anidados propia del lenguaje natural.

Los DFA son apropiados para reconocer **lenguajes regulares** y patrones secuenciales simples, pero carecen de la capacidad de mantener una memoria estructurada (como una pila) necesaria para verificar correspondencias a distancia, como la concordancia de género y número dentro de un sintagma nominal. En un DFA, verificar que *"las papas grandes"* sea válido mientras *"las papas grande"* sea inválido requeriría un número de estados proporcional a todas las combinaciones posibles de género y número, lo que resulta en una explosión combinatoria inviable.

Las construcciones lingüísticas abordadas por el proyecto —sintagmas nominales con concordancia, sintagmas preposicionales anidados, parámetros de cocción con estructura interna variable— requerían mecanismos más expresivos que los proporcionados por los autómatas finitos. Incorporar DFA habría añadido complejidad al sistema sin aportar beneficios significativos al alcance real del proyecto, dado que el dominio de las recetas, aunque acotado, presenta ambigüedades estructurales y dependencias que trascienden los lenguajes regulares.

Por esta razón se decidió centrar la implementación en gramáticas libres de contexto (CFG) como base, extendidas con un sistema de unificación de rasgos (DCG) para la concordancia, y con probabilidades (PCFG) para la desambiguación. Esta combinación ofrece un equilibrio adecuado entre poder expresivo, eficiencia computacional y simplicidad de implementación para un proyecto universitario de PLN básico.

## 7. Instalación

### Requisitos

- Python 3.8 o superior.
- pip (gestor de paquetes de Python).

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/receta-parser.git
cd receta-parser

# 2. Crear y activar un entorno virtual (opcional pero recomendado)
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install matplotlib
```

No existe archivo `requirements.txt` porque la única dependencia externa es matplotlib. El resto del sistema utiliza exclusivamente la biblioteca estándar de Python.

## 8. Ejecución del sistema

### 8.1 Preparación del entorno

Asegúrate de estar en el directorio raíz del proyecto con el entorno virtual activado (si lo usas).

### 8.2 Carga de recursos

El sistema carga automáticamente el léxico, la gramática y las recetas al importar los módulos correspondientes. No se requiere configuración manual.

### 8.3 Ejecución del sistema principal

```bash
python3 main.py [nombre_receta]
```

Si no se especifica un nombre de receta, se ejecuta con la receta por defecto: `"sancocho"`.

**Recetas disponibles**: sancocho, empanadas, chuleta, arroz_atollado, manjar_blanco, pandebono, aborrajados, marranitas, champus, lulada, ceviche_camaron, sopa_pata, pescado_frito.

```bash
# Ejemplo: analizar la receta de empanadas
python3 main.py empanadas
```

### 8.4 Salida esperada

El sistema imprime:
1. Los tokens generados.
2. La derivación completa con sangría jerárquica.
3. Una ventana gráfica con el árbol de derivación (si matplotlib está disponible).

### 8.5 Ejecución de pruebas

```bash
# Pruebas de parseo DCG (16 casos de recetas)
python3 test/tests_recetas_dcg.py

# Pruebas de concordancia (42 casos)
python3 test/tests_concordancia.py

# Pruebas de parseo PCFG (13 recetas completas)
python3 test/tests_recetas_pcfg.py

# Pruebas específicas del parser 1-best
python3 test/tests_pcfg_1best.py
```

Todas las pruebas deben reportar el 100% de casos exitosos.

## 9. Ejemplos de uso

### Entrada

```bash
python3 main.py pandebono
```

### Salida (resumida)

```
======================================================================
RECETA: pandebono
TOKENS:
['mezcla', 'harina', 'con', 'queso', '<EOS>', 'agrega', 'huevo', '<EOS>', ...]

======================================================================
✅ RECETA PARSEADA CORRECTAMENTE

DERIVACIÓN COMPLETA:

S →
  LISTA_INS →
    INS →
      VP →
        V → 'mezcla'
        COMPS →
          COMP →
            NP →
              N → 'harina'
          COMP →
            PP →
              PREP → 'con'
              NP →
                N → 'queso'
    <EOS>
    LISTA_INS →
      ...
```

El sistema también abre una ventana con el árbol de derivación dibujado gráficamente.

### Prueba de concordancia

```bash
python3 test/tests_concordancia.py
```

```
======================================================================
PRUEBAS DE CONCORDANCIA (NP individual)
======================================================================
  ✓ el pollo                      → OK          (esperado: OK)          correcto: masc + masc
  ✓ la pollo                      → RECHAZADO   (esperado: RECHAZADO)   error: det fem + n masc
  ✓ la gallina                    → OK          (esperado: OK)          correcto: fem + fem
  ✓ el gallina                    → RECHAZADO   (esperado: RECHAZADO)   error: det masc + n fem
  ...

  Concordancia: 42/42

######################################################################
Total: 42/42
```

## 10. Limitaciones actuales

1. **Unificación limitada a NP**: La concordancia de género y número solo se verifica dentro de sintagmas nominales. No se valida concordancia verbo-sujeto ni entre argumentos del verbo.

2. **Heurística simple de género**: La asignación de género a sustantivos y adjetivos se basa en la terminación de la palabra (`-a` → femenino, `-o` → masculino). Palabras como *mano* (termina en `-o` pero es femenino) requieren excepciones explícitas.

3. **Sin soporte para expresiones multipalabra**: Frases como *"al gusto"* o *"a fuego medio"* se tokenizan como palabras separadas, no como unidades léxicas compuestas.

4. **Gramática fija y no recursiva**: No se manejan oraciones subordinadas, cláusulas relativas ni estructuras anidadas más allá de la recursión limitada de `LISTA_INS` y `COMPS`.

5. **Sin capa semántica**: El parser reconoce la estructura sintáctica pero no extrae significado (acciones, ingredientes, tiempos de cocción). No se genera una representación semántica ejecutable o interpretable.

6. **Cobertura léxica acotada**: El léxico está limitado a aproximadamente 200 palabras del dominio culinario vallecaucano. Palabras fuera de este vocabulario causan fallos de parseo.

7. **Dependencia de matplotlib**: La visualización gráfica del árbol requiere matplotlib. En entornos sin interfaz gráfica (servidores, SSH), esta funcionalidad no está disponible.


## Referencias

- Jurafsky, D., & Martin, J. H. (2023). *Speech and Language Processing* (3rd ed. draft). Stanford University. https://web.stanford.edu/~jurafsky/slp3/
  - Cap. 12: Formal Grammars of English (CFG, parsing)
  - Cap. 13: Constituency Parsing (CYK, Earley, probabilistic parsing)
  - Cap. 15: Transition-Based Parsing

- Gazdar, G., Klein, E., Pullum, G., & Sag, I. (1985). *Generalized Phrase Structure Grammar*. Harvard University Press.
  — Base teórica de los sistemas de rasgos y unificación.

- Shieber, S. M. (1986). *An Introduction to Unification-Based Approaches to Grammar*. CSLI Publications.
  — Fundamento del mecanismo de unificación de DAGs implementado en `core/dgs.py`.

- Manning, C., & Schütze, H. (1999). *Foundations of Statistical Natural Language Processing*. MIT Press.
  — Cap. 11: Probabilistic Context Free Grammars (PCFG).

- Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.). Pearson.
  — Cap. 3: Best-First Search, A\* — base del algoritmo implementado en `core/pcfg_bestfirst.py`.
