# Ejercicio 1 — Solución detallada
## David Castellanos

### Gramática (tal como aparece)
S → A B C
S → D E
A → dos B tres
A → ε
B → B cuatro C cinco
B → ε
C → seis A B
C → ε
D → uno A E
D → B
E → tres

---
## a) Eliminación de recursividad por la izquierda en B
En este caso, la producción `B → B cuatro C cinco | ε` tiene recursividad directa. Aca lo que pasa es que aplicamos la transformación estándar:
- Introducimos un nuevo no terminal `B'`.
- Reescribimos:
  - `B → B'`
  - `B' → cuatro C cinco B' | ε`

Ahora la gramática equivalente (sin recursividad directa en B) se usa para calcular los conjuntos.

---
## b) Cálculo de FIRST (paso a paso)
Aca podemos ver que procedemos por punto fijo; inicializamos FIRST de cada no terminal vacío y vamos llenando según las producciones.

1. Inicialmente:
- FIRST(A) = { dos, ε } (porque A → dos B tres | ε)
- FIRST(B') = { cuatro, ε } (por B' → cuatro ... | ε) ⇒ FIRST(B) = FIRST(B') = { cuatro, ε }
- FIRST(C) = { seis, ε }
- FIRST(D) contiene 'uno' (por D → uno A E) y también lo que produce B (por D → B). Aca lo que pasa es que D puede iniciar con 'uno' o con FIRST(B).
- FIRST(E) = { tres }
- FIRST(S) = union de FIRST(A B C) y FIRST(D E)

Iteramos hasta estabilidad y obtenemos (resumen):
- FIRST(A) = { dos, ε }
- FIRST(B) = { cuatro, ε }
- FIRST(C) = { seis, ε }
- FIRST(D) = { uno, cuatro, ε }
- FIRST(E) = { tres }
- FIRST(S) = { dos, cuatro, seis, uno, tres, ε }

---
## c) Cálculo de FOLLOW (punto fijo, iteraciones)
En este caso inicializamos FOLLOW(S) = { $ } y propagamos:
- Desde `S → A B C`, FOLLOW(A) incluye FIRST(B C) \ {ε}, etc.
- Si una porción a la derecha puede derivar ε, propagamos FOLLOW(LHS).

Iteraciones (resumen):
- FOLLOW(S) = { $ }
- FOLLOW(A) = { cuatro, seis, tres, $ }
- FOLLOW(B) = { seis, tres, cuatro, $ }
- FOLLOW(C) = { uno, tres, $ }
- FOLLOW(D) = { tres, cuatro }
- FOLLOW(E) = { $, tres, cuatro }

Aca lo que pasa es que los símbolos que siguen a cada no terminal se agregan por estas reglas; y aqui podemos ver que al final se estabilizan.

---
## d) Conjuntos de PREDICCIÓN (resumen)
Recordar: PRED(A → α) = FIRST(α) \ {ε} ∪ (si ε ∈ FIRST(α) entonces FOLLOW(A))

Algunos ejemplos:
- PRED(S → A B C) = { dos, cuatro, seis } (y si α puede ser ε, agregar FOLLOW(S))
- PRED(S → D E) = { uno, cuatro, tres }
- PRED(A → dos B tres) = { dos }
- PRED(A → ε) = FOLLOW(A) = { cuatro, seis, tres, $ }
- PRED(B' → cuatro C cinco B') = { cuatro }
- PRED(B' → ε) = FOLLOW(B) = { seis, tres, cuatro, $ }

---
## e) ¿Es LL(1)?
No. Aca podemos ver que hay solapamientos en conjuntos de predicción (por ejemplo `S → A B C` y `S → D E` comparten terminales como `cuatro`), por lo que la gramática no cumple la propiedad LL(1).