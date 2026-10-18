# Informe: Comparación de Métodos de Búsqueda de Raíces

**Alumno:** Gonzalo Jaque Barros  
**Carrera:** Ingeniería Civil Informática  
**Tolerancia:** 1e-6 | **Máximo de iteraciones:** 100  

---

## 1. Planteamiento y funciones evaluadas

Se implementaron seis métodos para encontrar raíces y se probaron en seis funciones con distintas características (raíces simples, raíz doble con tangencia, funciones exponenciales, logarítmicas y trigonométricas).

Para los métodos cerrados (bisección y falsa posición) se revisó el teorema de Bolzano ($f(a) \cdot f(b) < 0$). Para los métodos abiertos se asignaron puntos de partida razonables cercanos a la raíz.

**Tabla 1.** Funciones y condiciones iniciales.

| Función | Tipo | Intervalo [a, b] | f(a) | f(b) | f(a)·f(b) | x₀ (Newton / PF) | x₀ ; x₁ (Secante) |
|---|---|---|---|---|---|---|---|
| x³ − x − 2 | Polinómica simple | [1, 2] | −2 | 4 | −8 (cumple Bolzano) | 1,5 | 1,0 ; 2,0 |
| (x − 2)² | Polinómica doble | [1, 3] | 1 | 1 | 1 (no cumple Bolzano) | 1,2 | 1,2 ; 1,3 |
| ln(x) + x − 4 | Logarítmica | [2, 3] | −1,307 | 0,099 | −0,129 (cumple Bolzano) | 2,5 | 2,0 ; 3,0 |
| e^(−x) − x | Exponencial | [0, 1] | 1 | −0,632 | −0,632 (cumple Bolzano) | 0,5 | 0,0 ; 1,0 |
| cos(x) − x | Trigonométrica | [0, 1] | 1 | −0,460 | −0,460 (cumple Bolzano) | 0,5 | 0,0 ; 1,0 |
| √x − cos(x) | Mixta | [0,1 ; 1] | −0,679 | 0,460 | −0,312 (cumple Bolzano) | 0,5 | 0,1 ; 1,0 |

En la función $(x - 2)^2$, la curva toca el eje en $x = 2$ pero nunca se hace negativa, por lo que $f(1) \cdot f(3) > 0$ y no hay cambio de signo.

Para punto fijo ($x = g(x)$) se despejó:
- Polinómica simple: $g(x) = \sqrt[3]{x + 2}$
- Polinómica doble: $g(x) = x + 0,5(x - 2)^2$
- Logarítmica: $g(x) = 4 - \ln(x)$
- Exponencial: $g(x) = e^{-x}$
- Trigonométrica: $g(x) = \cos(x)$
- Mixta: $g(x) = \cos^2(x)$

---

## 2. Resultados obtenidos

Corriendo cada método con tolerancia 1e-6 se obtuvo la siguiente cantidad de iteraciones:

**Tabla 2.** Iteraciones necesarias hasta converger.

| Función | Bisección | Falsa posición | Punto fijo | Secante | Newton | Newton mejorado |
|---|---|---|---|---|---|---|
| Polinómica simple | 20 | 12 | 7 | 6 | **2** | **2** |
| Polinómica doble | No aplica | No aplica | 100 (falla) | 14* | 10* | **1** |
| Logarítmica | 19 | 4 | 13 | **3** | **3** | **3** |
| Exponencial | 20 | 7 | 21 | 4 | **2** | **2** |
| Trigonométrica | 20 | 5 | 33 | 4 | **3** | **3** |
| Mixta | 20 | 4 | 100 (falla) | 3 | **2** | **2** |

*\*Nota:* En la raíz doble, secante y Newton se detienen porque $|f(x)| < 10^{-6}$, pero el error real sigue en torno a $7,8 \cdot 10^{-4}$.

![Resumen de iteraciones](src/assets/resumen_iteraciones.png)

Las curvas de convergencia completas están en la carpeta `src/assets/`. Como muestra:

![Convergencia Trigonométrica](src/assets/convergencia_trigonometrica.png)
![Convergencia Raíz Doble](src/assets/convergencia_polinomica_doble.png)

---

## 3. Análisis

### Rapidez y orden de convergencia
- **Newton y Newton mejorado:** Fueron los más rápidos en casi todos los casos (2 a 3 iteraciones). Al usar la derivada, el método tiene convergencia cuadrática ($p \approx 2$), lo que hace que los decimales correctos prácticamente se dupliquen en cada paso.
- **Secante:** Logra una velocidad muy similar a Newton (3 a 6 iteraciones) sin necesidad de calcular la derivada analítica. Tiene orden superlineal ($p \approx 1,6$).
- **Bisección:** Es constante y predecible. En todas las funciones con cambio de signo tomó 19-20 iteraciones, lo que calza con dividir el intervalo a la mitad en cada paso ($\log_2(1 / 10^{-6}) \approx 19,9$).
- **Falsa posición y Punto fijo:** Su velocidad depende mucho de la curva. Falsa posición anduvo bien en la logarítmica y mixta (4 iteraciones), pero en punto fijo la convergencia depende de qué tan chico sea $|g'(r)|$. Por ejemplo, en la mixta $|g'(r)| \approx 0,96$ es muy cercano a 1, por lo que avanzó tan lento que no alcanzó la tolerancia en 100 pasos.

### El caso de la raíz doble: (x − 2)²
Este caso mostró tres cosas importantes:
1. **Bisección y falsa posición no sirven:** Al ser una raíz con tangencia, la función no cruza el eje y no hay cambio de signo.
2. **Parada prematura en Newton y secante:** Como $f(x) = (x - 2)^2$, cuando $|x - 2| \approx 10^{-3}$, la función ya vale $10^{-6}$ y el programa se corta creyendo que llegó a la solución, aunque el error real sigue siendo grande ($7,8 \cdot 10^{-4}$).
3. **Newton mejorado:** Usando la segunda derivada, corrigió el problema de la multiplicidad y llegó a $x = 2$ exacto en 1 sola iteración.

### Sensibilidad al punto inicial
Revisando los resultados de `sensibilidad.csv`:
- **Bisección:** Si se agranda el intervalo de $[1, 2]$ a $[-1000, 1000]$, solo sube de 20 a 31 iteraciones. Es casi inmune al tamaño del intervalo.
- **Falsa posición:** Al agrandar el intervalo a $[-10, 10]$ no logró converger en 100 pasos, porque un extremo queda fijo y el otro avanza muy lento.
- **Newton:** Si se elige un punto donde la derivada está cerca de cero (por ejemplo en $\cos(x) - x$ con $x_0 = 4,7$), el método se dispara y falla por división por cero o números gigantes.

---

## 4. Conclusiones

1. **Seguridad vs velocidad:** Newton y secante son los métodos a elegir si se busca rapidez (resuelven en 2 a 4 pasos), pero dependen de un buen punto de partida para no dispararse. Bisección es más lenta (20 pasos), pero es el único método que asegura llegar siempre que haya cambio de signo.
2. **Cuidado con las raíces múltiples:** Cuando una función toca el eje sin cruzarlo, los métodos cerrados quedan descartados. Además, los criterios de parada basados solo en $|f(x)|$ son engañosos porque la función se achica mucho más rápido que la distancia a la raíz. En estos casos, Newton mejorado es la mejor alternativa.
3. **Punto fijo:** Solo conviene si es fácil despejar una $g(x)$ con pendiente suave ($|g'| \ll 1$); de lo contrario, el avance se vuelve eterno o derechamente diverge.
