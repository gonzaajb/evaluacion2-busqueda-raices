from pathlib import Path
import numpy as np
from metodos import (biseccion, falsa_posicion, punto_fijo,
                     secante, newton, newton_mejorado)

SRC = Path(__file__).resolve().parents[1]
DATA = SRC / "data"
ASSETS = SRC / "assets"
DATA.mkdir(exist_ok=True)
ASSETS.mkdir(exist_ok=True)

METODOS = ["biseccion", "falsa_posicion", "punto_fijo", "secante", "newton", "newton_mejorado"]
NOMBRES = {
    "biseccion": "Bisección",
    "falsa_posicion": "Falsa posición",
    "punto_fijo": "Punto fijo",
    "secante": "Secante",
    "newton": "Newton-Raphson",
    "newton_mejorado": "Newton mejorado"
}

def ejecutar(fd, metodo, a=None, b=None, x0=None, s0=None, s1=None):
    f= fd["f"]
    if a is None: a=fd["a"]
    if b is None: b=fd["b"]
    if x0 is None: x0=fd["xn"]
    if s0 is None: s0=fd["s0"]
    if s1 is None: s1=fd["s1"]
    
    with np.errstate(all="ignore"):
        if metodo == "biseccion":
            return biseccion(f, a, b)
        if metodo == "falsa_posicion":
            return falsa_posicion(f, a, b)
        if metodo == "punto_fijo":
            return punto_fijo(f, fd["g"], x0)
        if metodo == "secante":
            return secante(f, s0, s1)
        if metodo == "newton":
            return newton(f, fd["df"], x0)
        return newton_mejorado(f, fd["df"], fd["d2f"], x0)

def raiz_ref(fd):
    if "raiz_exacta" in fd:
        return fd["raiz_exacta"]
    a, b, f = fd["a"], fd["b"], fd["f"]
    for _ in range(200):
        c = (a+b)/2.0
        if f(a)*f(c) <= 0:
            b = c
        else:
            a = c
    return (a+b)/2.0

def correr_todo():
    resultados = {}
    for fd in FUNCIONES_LISTA:
        fd["raiz"] = raiz_ref(fd)
        resultados[fd["id"]] = {}
        for m in METODOS:
            resultados[fd["id"]][m] = ejecutar(fd, m)
    return resultados

from funciones import FUNCIONES as FUNCIONES_LISTA
