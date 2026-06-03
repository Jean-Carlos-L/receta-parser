# SPEC: Soporte de Ambigüedad y Desambiguación mediante PCFG

## Objetivo

Analizar completamente el proyecto actual del parser de recetas vallecaucanas y elaborar un plan técnico detallado para incorporar soporte de ambigüedad sintáctica mediante gramáticas probabilísticas (PCFG).

La implementación NO debe realizarse todavía. El objetivo de esta tarea es comprender el estado actual del sistema y proponer una estrategia de evolución técnicamente sólida.

---

## Contexto del proyecto

El proyecto consiste en un parser de recetas vallecaucanas basado en una gramática libre de contexto (CFG).

La gramática ha sido diseñada para contener ambigüedades de forma intencional. Estas ambigüedades serán posteriormente resueltas mediante un modelo probabilístico basado en PCFG (Probabilistic Context-Free Grammar).

Actualmente el parser genera un único árbol sintáctico para cada entrada.

La evolución deseada es:

1. Permitir que el parser genere múltiples árboles válidos cuando una oración sea ambigua.
2. Incorporar probabilidades en la gramática.
3. Calcular la probabilidad de cada árbol generado.
4. Seleccionar automáticamente el árbol más probable.
5. Mantener la posibilidad de inspeccionar todas las interpretaciones generadas.

---

## Fase 1: Comprensión obligatoria del proyecto

Antes de proponer cualquier cambio, analizar completamente el código fuente.

### Elementos que deben revisarse

#### Gramática

Analizar:

- Reglas de producción actuales.
- Representación interna de la gramática.
- Mecanismos utilizados para expansión.
- Posibles fuentes actuales de ambigüedad.

#### Léxico

Analizar:

- Estructura del léxico.
- Categorías léxicas existentes.
- Asociación entre tokens y categorías gramaticales.

#### Tokenización

Analizar:

- Flujo completo de tokenización.
- Normalización aplicada a la entrada.
- Tratamiento de palabras desconocidas.

#### Parser

Analizar:

- Algoritmo utilizado.
- Representación interna de árboles.
- Estrategia actual de búsqueda.
- Puntos donde actualmente se descartan árboles alternativos.

#### Estructuras de datos

Identificar:

- Clases principales.
- Dependencias entre módulos.
- Flujo completo desde la entrada hasta el árbol final.

---

## Fase 2: Diagnóstico

Elaborar un diagnóstico técnico que responda:

1. ¿Cómo maneja actualmente el parser la ambigüedad?
2. ¿En qué punto se pierde información sobre árboles alternativos?
3. ¿Qué componentes deben modificarse para soportar múltiples árboles?
4. ¿Qué limitaciones actuales podrían dificultar la implementación de PCFG?
5. ¿Qué riesgos técnicos existen?

---

## Fase 3: Diseño para soporte de múltiples árboles

Proponer una estrategia para que el parser pueda:

- Conservar todas las derivaciones válidas.
- Construir múltiples árboles sintácticos.
- Retornar una colección de árboles en lugar de uno solo.
- Mantener compatibilidad con el resto del sistema.

El análisis debe incluir:

### Cambios requeridos

- Archivos afectados.
- Clases afectadas.
- Funciones afectadas.
- Nuevas estructuras de datos necesarias.

### Complejidad

Explicar el impacto esperado en:

- Memoria.
- Tiempo de ejecución.
- Escalabilidad.

---

## Fase 4: Diseño para PCFG

Proponer una arquitectura para incorporar probabilidades a la gramática.

El análisis debe incluir:

### Representación de probabilidades

Definir cómo almacenar:

- Reglas de producción.
- Probabilidades asociadas.
- Restricciones de normalización.

### Cálculo de probabilidades

Explicar:

- Cómo calcular la probabilidad de una derivación.
- Cómo calcular la probabilidad de un árbol completo.
- Cómo comparar árboles alternativos.

### Selección del mejor árbol

Definir:

- Estrategia de ranking.
- Criterio de desempate.
- Formato de salida esperado.

---

## Fase 5: Plan de implementación

Generar un plan detallado dividido en etapas.

Para cada etapa indicar:

- Objetivo.
- Archivos afectados.
- Dependencias.
- Riesgos.
- Criterios de validación.

El plan debe minimizar cambios disruptivos y permitir pruebas incrementales.

---

## Entregables esperados

La respuesta debe contener:

### 1. Resumen de arquitectura actual

Descripción de cómo funciona actualmente el sistema.

### 2. Diagnóstico técnico

Identificación de limitaciones y puntos críticos.

### 3. Diseño para múltiples árboles

Propuesta detallada.

### 4. Diseño para PCFG

Propuesta detallada.

### 5. Plan de implementación

Plan paso a paso.

### 6. Riesgos y consideraciones

Lista de posibles problemas técnicos y estrategias de mitigación.

---

## Restricciones

- No modificar código durante esta tarea.
- No asumir comportamientos sin verificarlos en el código.
- Basar todas las conclusiones en la implementación existente.
- Identificar explícitamente cualquier información faltante.
- Justificar las decisiones técnicas propuestas.
