# MotorInferencia
Resuelve los ejercicios de sistemas de producciones de IASI.
## Como usar
- Introduce las reglas
  - Introduce el nombre
  - Introduce la lista de consecuentes
  - Introduce la lista de tuplas que añadir
  - Introduce la lista de tuplas que eliminar

  - Para no introducir un campo simplemente pulsar enter sin introducir nada
  - Para terminar de escribir las reglas inserta una regla con nombre vacio
- Introduce la lista con las tuplas de la base de hechos
- Introduce la tupla a buscar
  - Si no introduces ninguna puedes introducir el número máximo de ciclos a realizar   
-
- Los elementos de las tuplas van separados con comas 
  ```A,B,C```
- Las variables van precedidas de dollar ```$x```
- Las tuplas van separadas por coma y espacio o caret (^) ```(A,B,C), (C,$x,A)``` ```(A,B,C) ^ (C,$x,A)```
- Para añadir terminos que no tienen que aparecer en el consecuente preceder con negación (¬) ```(A,B,C), ¬(C,$x,A)```

## Ejemplo
_Se corresponde con el ejercicio  5 del examen de junio de 2019_
```
R1		# Regla 1
(A,$x,D), ($y,$y,$y) 	# Consecuente
(A,$y,D) 		# Eliminar
(B,$x,D)		# Añadir
R2		# Regla 2
(A,C,$x) 		# Consecuente
			# Eliminar
(B,$x,D), ($x,C,D)	# Añadir
R3		# Regla 3
(A,$x,$x), ¬(B,$x,D)  	# Consecuente
($x,A,$x)		# Eliminar
($x,$x,D), ($x,B,D)	# Añadir
R4		# Regla 4
(B,$x,B)		# Consecuente
			# Eliminar
(A,C,$x), (A,$x,D)	# Añadir

(A,A,A), (B,B,B)# Base de hechos
		# Hecho a demostrar
5		# Número máximo de ciclos

```
