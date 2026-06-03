# receta-parser

# Gramática Formal — Receta de Cocina

## Símbolo Inicial

S

## Reglas de Producción

### Estructura Principal

S -> LISTA_INS

LISTA_INS -> INS '<EOS>'
           | INS '<EOS>' LISTA_INS

### Instrucciones

INS -> VP
     | ORDEN VP

### Frase Verbal

VP -> V COMPS
    | V

COMPS -> COMP COMPS
       | COMP

COMP -> NP
      | PP
      | PARAM

### Frase Nominal

NP -> DET N ADJ
    | DET N
    | N ADJ
    | QUANT N
    | N

### Frase Preposicional

PP -> PREP NP
    | PREP NUM N
    | PREP DET N
    | PREP DET N ADJ

### Parámetros

PARAM -> 'durante' NUM 'minutos'
       | 'durante' NUM 'minutos' 'mas'
       | 'a' 'fuego' LEVEL
       | 'al' 'final'
       | 'en' 'aceite' 'caliente'

## Léxico

V      -> 'pon' | 'agrega' | 'cocina' | 'corta' | 'sofreir' | 'mezcla'
        | 'prepara' | 'amasa' | 'frie' | 'añade' | 'rectifica'
        | 'sirve' | 'deja' | 'cubre'

N      -> 'gallina' | 'trozos' | 'agua' | 'carne' | 'olla' | 'yuca'
        | 'papa' | 'cebolla' | 'tomate' | 'cilantro' | 'masa' | 'harina'
        | 'maiz' | 'pollo' | 'aceite' | 'sal' | 'empanadas' | 'papas'
        | 'platano' | 'gusto' | 'minutos' | 'recipiente' | 'relleno'
        | 'queso' | 'ajo'

ADJ    -> 'grande' | 'grandes' | 'picado' | 'picada' | 'fresco'
        | 'molida' | 'molido' | 'machaca' | 'machacada' | 'cortada'
        | 'caliente' | 'tibia' | 'verde' | 'medianos' | 'mediano'

DET    -> 'una' | 'un' | 'la' | 'las' | 'los' | 'el'

QUANT  -> 'suficiente'

PREP   -> 'en' | 'con' | 'de' | 'para' | 'a'

LEVEL  -> 'medio'

NUM    -> 'cuarenta' | 'cincuenta' | 'treinta' | 'cinco' | 'ocho'

CONJ   -> 'y' | 'e' | 'luego'

ORDEN  -> 'primero' | 'despues'
