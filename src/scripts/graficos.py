# genera los graficos en src/assets
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from funciones import FUNCIONES
from metodos import TOL
from utils import ASSETS, METODOS, NOMBRES, correr_todo

resultados = correr_todo()
marcadores = ["o", "s", "^", "D", "v", "*"]

# 1) cada funcion con su raiz
for fd in FUNCIONES:
    xs = np.linspace(fd["rango"][0], fd["rango"][1], 400)
    with np.errstate(all="ignore"):
        ys = fd["f"](xs)
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(xs, ys, color="tab:blue", label=fd["titulo"])
    ax.axhline(0, color="k", lw=0.8)
    ax.axvspan(fd["a"], fd["b"], color="orange", alpha=0.12,
               label="intervalo [%s, %s]" % (fd["a"], fd["b"]))
    ax.plot(fd["raiz"], 0, "ro", ms=8, label="raíz ≈ %.6f" % fd["raiz"])
    if fd["id"] == "polinomica_doble":
        ax.annotate("tangencia al eje x\n(raíz doble, sin cambio de signo)",
                    (fd["raiz"], 0), (2.2, 0.5), arrowprops=dict(arrowstyle="->"))
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.set_title(fd["categoria"] + ": " + fd["titulo"])
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(ASSETS / ("funcion_" + fd["id"] + ".png"), dpi=130)
    plt.close(fig)

# 2) |error| vs iteracion (escala log)
for fd in FUNCIONES:
    fig, ax = plt.subplots(figsize=(7, 4.4))
    for i, m in enumerate(METODOS):
        hist, estado = resultados[fd["id"]][m]
        if len(hist) == 0:
            continue
        iteraciones = [k for (k, x, fx) in hist]
        errores = np.maximum([abs(x - fd["raiz"]) for (k, x, fx) in hist], 1e-17)
        ax.semilogy(iteraciones, errores, marker=marcadores[i], ms=5, label=NOMBRES[m])
    ax.axhline(TOL, color="gray", ls="--", lw=0.9, label="tol = 1e-6")
    ax.set_xlabel("iteración")
    ax.set_ylabel("|error| = |x − raíz| (escala log)")
    ax.set_title("Convergencia: " + fd["titulo"])
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, which="both")
    fig.tight_layout()
    fig.savefig(ASSETS / ("convergencia_" + fd["id"] + ".png"), dpi=130)
    plt.close(fig)

# 3) resumen de iteraciones
fig, ax = plt.subplots(figsize=(11, 5))
ancho = 0.13
for j, m in enumerate(METODOS):
    alturas = []
    textos = []
    for fd in FUNCIONES:
        hist, estado = resultados[fd["id"]][m]
        if estado in ("convergio", "max_iter"):
            alturas.append(len(hist))
            textos.append(str(len(hist)))
        else:
            alturas.append(0)
            textos.append("N/A" if estado == "no aplica" else "X")
    pos = np.arange(len(FUNCIONES)) + (j - 2.5) * ancho
    ax.bar(pos, alturas, ancho, label=NOMBRES[m])
    for p, h, t in zip(pos, alturas, textos):
        ax.text(p, h + 0.3, t, ha="center", fontsize=7)
ax.set_xticks(np.arange(len(FUNCIONES)))
ax.set_xticklabels([fd["id"].replace("_", "\n") for fd in FUNCIONES])
ax.set_ylabel("iteraciones hasta tol = 1e-6")
ax.set_title("Iteraciones por método y función (N/A = no aplica, X = falla)")
ax.legend(ncol=3, fontsize=8)
ax.grid(alpha=0.3, axis="y")
fig.tight_layout()
fig.savefig(ASSETS / "resumen_iteraciones.png", dpi=130)
plt.close(fig)

print("graficos listos en src/assets")
