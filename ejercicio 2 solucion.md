# Ejercicio 2 — Solución detallada
## David Castellanos

### Gramática (tal como aparece)
S → B uno
S → dos C
S → ε
A → S tres B C
A → cuatro
A → ε
B → A cinco C seis
B → ε
C → siete B
C → ε

---
## a) FIRST (paso a paso)
En este caso empezamos calculando FIRST de los no terminales básicos:
- FIRST(C) = { siete, ε }
- FIRST(A) incluye { cuatro } por la producción A → cuatro, y también puede empezar como FIRST(S) por A → S tres ... por lo que es necesario iterar.
- Tras iterar por punto fijo obtenemos:
  - FIRST(S) = { dos, cuatro, tres, ε }
  - FIRST(A) = { cuatro, dos, tres, ε }
  - FIRST(B) = { cuatro, dos, tres, ε }
  - FIRST(C) = { siete, ε }

Aca lo que pasa es que las producciones recursivas y la presencia de ε requieren varias pasadas hasta la estabilidad.

---
## b) FOLLOW (resumen iterativo)
Inicializamos FOLLOW(S) = { $ } y propagamos según las reglas. El resultado (resumen):
- FOLLOW(S) = { $, tres }
- FOLLOW(A) = { cinco }
- FOLLOW(B) = { uno, siete, $, seis, cinco, tres }
- FOLLOW(C) = { $, seis, cinco, tres }

Aca podemos ver que los símbolos que vienen después en distintas producciones terminan en los conjuntos de FOLLOW correspondientes.

---
## c) PREDICCIÓN (resumen)
- PRED(S → B uno) = FIRST(B uno) \ {ε} = { cuatro, dos, tres, uno }
- PRED(S → dos C) = { dos }
- PRED(S → ε) = FOLLOW(S) = { $, tres }
- PRED(A → S tres B C) = { dos, cuatro, tres }
- PRED(A → cuatro) = { cuatro }
- PRED(A → ε) = FOLLOW(A) = { cinco }
- PRED(B → A cinco C seis) = { dos, cuatro, tres }
- PRED(B → ε) = FOLLOW(B) = { uno, siete, $, seis, cinco, tres }
- PRED(C → siete B) = { siete }
- PRED(C → ε) = FOLLOW(C) = { $, seis, cinco, tres }

---
## d) ¿Es LL(1)?
No. Aca lo que pasa es que existen intersecciones entre conjuntos de predicción (por ejemplo entre `S → B uno` y `S → dos C`), por lo que no es LL(1).