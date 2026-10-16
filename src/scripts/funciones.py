import numpy as np

# a, b = intervalo | xn = x0 para newton y punto fijo | s0, s1 = x0 y x1 de la secante
FUNCIONES = [
    dict(id="polinomica_simple", titulo="f(x) = x³ − x − 2", categoria="Polinómica (raíz simple)",
         f=lambda x: x**3 - x - 2, df=lambda x: 3 * x**2 - 1, d2f=lambda x: 6 * x,
         g=lambda x: np.cbrt(x + 2),
         a=1.0, b=2.0, xn=1.5, s0=1.0, s1=2.0, rango=(0.5, 2.5)),

    dict(id="polinomica_doble", titulo="f(x) = (x − 2)²", categoria="Polinómica (raíz doble)",
         f=lambda x: (x - 2)**2, df=lambda x: 2 * (x - 2), d2f=lambda x: 2.0 + 0 * x,
         g=lambda x: x + 0.5 * (x - 2)**2,
         a=1.0, b=3.0, xn=1.2, s0=1.2, s1=1.3, rango=(1.0, 3.0), raiz_exacta=2.0),

    dict(id="logaritmica", titulo="f(x) = ln(x) + x − 4", categoria="Logarítmica",
         f=lambda x: np.log(x) + x - 4, df=lambda x: 1 / x + 1, d2f=lambda x: -1 / x**2,
         g=lambda x: 4 - np.log(x),
         a=2.0, b=3.0, xn=2.5, s0=2.0, s1=3.0, rango=(1.0, 4.0)),

    dict(id="exponencial", titulo="f(x) = e^(−x) − x", categoria="Exponencial",
         f=lambda x: np.exp(-x) - x, df=lambda x: -np.exp(-x) - 1, d2f=lambda x: np.exp(-x),
         g=lambda x: np.exp(-x),
         a=0.0, b=1.0, xn=0.5, s0=0.0, s1=1.0, rango=(-0.5, 1.5)),

    dict(id="trigonometrica", titulo="f(x) = cos(x) − x", categoria="Trigonométrica",
         f=lambda x: np.cos(x) - x, df=lambda x: -np.sin(x) - 1, d2f=lambda x: -np.cos(x),
         g=lambda x: np.cos(x),
         a=0.0, b=1.0, xn=0.5, s0=0.0, s1=1.0, rango=(-0.5, 1.5)),

    dict(id="mixta", titulo="f(x) = √x − cos(x)", categoria="Mixta",
         f=lambda x: np.sqrt(x) - np.cos(x), df=lambda x: 0.5 / np.sqrt(x) + np.sin(x),
         d2f=lambda x: -0.25 / x**1.5 + np.cos(x),
         g=lambda x: np.cos(x)**2,
         a=0.1, b=1.0, xn=0.5, s0=0.1, s1=1.0, rango=(0.05, 1.5)),
]
