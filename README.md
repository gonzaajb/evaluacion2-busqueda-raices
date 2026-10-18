# Evaluación 2: Búsqueda de Raíces

**Nombre:** Gonzalo Jaque Barros  
**Carrera:** Ingeniería Civil Informática  
**Ramo:** Métodos Numéricos  

Comparación y análisis de seis métodos numéricos para encontrar raíces (bisección, falsa posición, punto fijo, secante, Newton-Raphson y Newton mejorado) aplicados sobre seis funciones distintas.

## Cómo ejecutar

1. Crear el entorno virtual e instalar librerías:
```bash
python -m venv venv

# En Windows:
.\venv\Scripts\activate

# En Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

2. Generar los datos y gráficos (desde `src/scripts`):
```bash
cd src/scripts
python generar_datos.py
python graficos.py
```

Los resultados quedan guardados en:
- `src/data/`: tablas CSV con los historiales de iteración, errores y pruebas de sensibilidad.
- `src/assets/`: gráficos de las funciones y curvas de convergencia.

## Parámetros usados
- **Tolerancia:** 1e-6
- **Iteraciones máximas:** 100
- **Criterio de parada:** el algoritmo termina cuando $|f(x)| < 10^{-6}$ o cuando la diferencia entre pasos $|x_k - x_{k-1}| < 10^{-6}$.

El análisis detallado de los resultados está en [`informe.md`](informe.md).
