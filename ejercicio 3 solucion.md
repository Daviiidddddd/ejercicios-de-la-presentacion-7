# Ejercicio 3 — Solución detallada
## David Castellanos

### Gramática (tal como aparece)
S → A B C
S → S uno
A → dos B C
A → ε
B → C tres
B → ε
C → cuatro B
C → ε

---
## a) Eliminación de recursividad por la izquierda en S
En este caso la recursión `S → S uno` es directa. Aca lo que pasa es que aplicamos la transformación estándar:
- Introducimos `S'` y reescribimos:
  - `S → A B C S'`
  - `S' → uno S' | ε`

Así evitamos la recursividad a la izquierda y obtenemos una forma adecuada para LL(1).

---
## b) FIRST (paso a paso)
Iteramos por punto fijo:
- FIRST(A) = { dos, ε }
- FIRST(C) = { cuatro, ε }
- FIRST(B) = { cuatro, tres, ε }  (porque B → C tres y C puede ser ε)
- FIRST(S') = { uno, ε }
- FIRST(S) = { dos, cuatro, tres, uno, ε }

Aca podemos ver que la presencia de ε en A, B, C hace que FIRST de S incluya múltiples terminales.

---
## c) FOLLOW (resumen)
Tras propagar reglas:
- FOLLOW(S) = { $ }
- FOLLOW(A) = { cuatro, tres, uno, $ }
- FOLLOW(B) = { cuatro, uno, tres, $ }
- FOLLOW(C) = { uno, cuatro, tres, $ }
- FOLLOW(S') = { $ }

Aquí podemos ver que los conjuntos se forman por lo que sigue a cada no terminal en las producciones.

---
## d) PREDICCIÓN y LL(1)
- PRED(S → A B C S') = { dos, cuatro, tres, uno }
- PRED(S' → uno S') = { uno }
- PRED(S' → ε) = { $ }
- PRED(A → dos B C) = { dos }
- PRED(A → ε) = { cuatro, tres, uno, $ }
- PRED(B → C tres) = { cuatro, tres }
- PRED(B → ε) = { cuatro, uno, tres, $ }
- PRED(C → cuatro B) = { cuatro }
- PRED(C → ε) = { uno, cuatro, tres, $ }

Aca lo que pasa es que se detectan solapamientos en PRED (por ejemplo en B), por lo que la gramática **no es LL(1)**.
