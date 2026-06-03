# Significado de las siglas de la gramática

Esta gramática utiliza una combinación de convenciones estándar de Lingüística Computacional y símbolos específicos para el dominio de recetas o instrucciones culinarias.

## Tabla de símbolos

| Sigla       | Nombre completo               | Traducción             | Función                                                                      |
| ----------- | ----------------------------- | ---------------------- | ---------------------------------------------------------------------------- |
| `S`         | Sentence                      | Oración                | Símbolo inicial de la gramática.                                             |
| `LISTA_INS` | Lista de Instrucciones        | -                      | Conjunto de instrucciones encadenadas.                                       |
| `INS`       | Instruction                   | Instrucción            | Representa una acción individual.                                            |
| `VP`        | Verb Phrase                   | Sintagma Verbal        | Acción principal de la instrucción.                                          |
| `V`         | Verb                          | Verbo                  | Verbo principal como _mezclar_, _cortar_, _cocinar_, etc.                    |
| `COMPS`     | Complements                   | Complementos           | Lista de complementos asociados al verbo.                                    |
| `COMP`      | Complement                    | Complemento            | Complemento individual del verbo.                                            |
| `NP`        | Noun Phrase                   | Sintagma Nominal       | Objeto o entidad sobre la que actúa el verbo.                                |
| `PP`        | Prepositional Phrase          | Sintagma Preposicional | Complemento introducido por una preposición.                                 |
| `PARAM`     | Parameter                     | Parámetro              | Parámetros específicos de la acción (tiempo, temperatura, intensidad, etc.). |
| `DET`       | Determiner                    | Determinante           | Artículos y determinantes: _el_, _la_, _los_, _una_, etc.                    |
| `N`         | Noun                          | Sustantivo             | Ingrediente u objeto: _cebolla_, _carne_, _olla_, etc.                       |
| `ADJ`       | Adjective                     | Adjetivo               | Característica del sustantivo: _picada_, _caliente_, _fina_, etc.            |
| `QUANT`     | Quantifier                    | Cuantificador          | Cantidades: _dos_, _tres_, _medio kilo_, etc.                                |
| `PREP`      | Preposition                   | Preposición            | Palabras como _en_, _con_, _sobre_, _para_, etc.                             |
| `NUM`       | Number                        | Número                 | Valor numérico.                                                              |
| `ORDEN`     | Order Marker                  | Marcador de orden      | Indica secuencia temporal: _primero_, _después_, _luego_, etc.               |
| `LEVEL`     | Level                         | Nivel                  | Intensidad o nivel: _bajo_, _medio_, _alto_.                                 |
| `EOS`       | End Of Sentence / End Of Step | Fin de instrucción     | Marca el final de una instrucción o paso.                                    |

---

## Estructura general de la gramática

```text
S
└── LISTA_INS
    ├── INS
    ├── <EOS>
    └── LISTA_INS
```

La gramática permite una secuencia de instrucciones, donde cada instrucción puede contener:

```text
INS
├── VP
└── ORDEN VP
```

Es decir:

- Una acción simple.
- O una acción precedida por un marcador de orden.

---

## Sintagma verbal (VP)

```text
VP
├── V
└── COMPS
```

Ejemplos:

- `cortar`
- `mezclar la harina`
- `cocinar la cebolla durante 10 minutos`

---

## Sintagma nominal (NP)

Representa ingredientes u objetos.

```text
NP
├── DET N ADJ
├── DET N
├── N ADJ
├── QUANT N
└── N
```

Ejemplos:

| Producción | Ejemplo           |
| ---------- | ----------------- |
| DET N ADJ  | la cebolla picada |
| DET N      | el tomate         |
| N ADJ      | carne molida      |
| QUANT N    | dos cebollas      |
| N          | aceite            |

---

## Sintagma preposicional (PP)

Representa complementos introducidos por preposiciones.

```text
PP
├── PREP NP
├── PREP NUM N
├── PREP DET N
└── PREP DET N ADJ
```

Ejemplos:

- con la cebolla
- en 5 minutos
- sobre el plato
- con la salsa caliente

---

## Parámetros (PARAM)

Representan información contextual sobre la acción.

```text
PARAM
├── durante NUM minutos
├── durante NUM minutos mas
├── a fuego LEVEL
├── al final
└── en aceite caliente
```

Ejemplos:

- durante 10 minutos
- durante 5 minutos más
- a fuego medio
- al final
- en aceite caliente

---

## Ejemplo completo de derivación

Para la instrucción:

> cocinar la cebolla picada durante 10 minutos

La derivación sería:

```text
S
└── LISTA_INS
    ├── INS
    │   └── VP
    │       ├── V
    │       │   └── cocinar
    │       └── COMPS
    │           ├── COMP
    │           │   └── NP
    │           │       ├── DET
    │           │       │   └── la
    │           │       ├── N
    │           │       │   └── cebolla
    │           │       └── ADJ
    │           │           └── picada
    │           └── COMP
    │               └── PARAM
    │                   ├── durante
    │                   ├── NUM
    │                   │   └── 10
    │                   └── minutos
    └── <EOS>
```
