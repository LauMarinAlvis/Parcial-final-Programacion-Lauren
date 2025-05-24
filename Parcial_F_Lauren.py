#Sistema de Gestión de Rendimiento en Pruebas Deportivas

import tkinter as tk 
from tkinter import simpledialog, messagebox
import random
import math
import pandas as pd 
import matplotlib

#1. Registrar participante
#Los datos pueden almacenarse en listas o en un diccionario.
#- El usuario ingresa el nombre del participante.
#- Ingresa los resultados (puntajes entre 0 y 100) en tres pruebas físicas: resistencia, fuerza y velocidad.
#- Para cada prueba, el programa genera automáticamente un nivel de dificultad decimal aleatorio entre 1.0 y 1.3 usando random.
#- Se calcula el puntaje final ponderado con la fórmula:
#  Puntaje Final = (∑ (puntaje × dificultad)) / (∑ dificultades)



def regis_participante():
    nombre = simpledialog.askstring("Registre", "nombre del participante:")
    if not nombre:
        return


def report_general():
def reporte_individual():



ventana = tk.Tk()
ventana.title("Sistema de Rendimiento Pruebas Deportivas")