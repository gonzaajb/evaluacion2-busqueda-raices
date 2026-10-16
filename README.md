# Evaluación 2 - La raíz que se esconde

Comparación de seis métodos para encontrar raíces (bisección, falsa posición, punto fijo, secante, Newton y Newton mejorado) en seis funciones distintas.

Universidad Católica del Maule - Laboratorio evaluado 2
Integrante: Gonzalo Jaque Barros

## Cómo correrlo

Primero crear el entorno e instalar lo necesario:

```bash
python3 -m venv venv
source venv/bin/activate        # en Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Después, desde la carpeta de los scripts:

```bash
cd src/scripts
python generar_datos.py     # crea los CSV en src/data
python graficos.py          # crea los PNG en src/assets
```

Se usa tolerancia 1e-6 y máximo 100 iteraciones. El programa para cuando |f(x)| < tol o cuando |x - x anterior| < tol.

## Qué hace cada script

- `metodos.py`: los seis métodos. Cada uno devuelve el historial de iteraciones y un estado (convergió, no aplica, falla o llegó al máximo).
- `funciones.py`: las seis funciones con sus derivadas, la g(x) para punto fijo y los intervalos / valores iniciales.
- `utils.py`: funciones de apoyo que usan los otros dos scripts (correr un método, calcular la raíz de referencia).
- `generar_datos.py`: revisa el cambio de signo (Bolzano), corre todos los métodos y guarda los CSV.
- `graficos.py`: hace los gráficos de cada función, de convergencia y el resumen de iteraciones.

## Carpetas

```
README.md
requirements.txt
informe.md
src/
  assets/     gráficos PNG
  data/       CSV
  scripts/    código en Python
```

## Archivos generados

En `src/data/`:
- `<funcion>.csv`: columnas x, f(x).
- `ambiente_controlado.csv`: intervalos, valores iniciales y chequeo de Bolzano.
- `resumen_convergencia.csv`: iteraciones, raíz, error y orden estimado de cada método en cada función.
- `historial_convergencia.csv`: x, f(x) y error en cada iteración.
- `sensibilidad.csv`: qué pasa al cambiar el intervalo o el valor inicial.

En `src/assets/`:
- `funcion_<nombre>.png`: la función con su raíz marcada.
- `convergencia_<nombre>.png`: error vs iteración en escala log.
- `resumen_iteraciones.png`: iteraciones por método y función.
