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


participantes = {} #dicicionario 

def regis_participante():
    nombre = simpledialog.askstring("Registre", "nombre del participante:")
    if not nombre:
        return

clasifica = "Sí" if puntaje_final >= 70 else "No"        

puntajes 
dificultad

participantes[nombre] = {
            "puntajes": puntajes,
            "dificultades": dificultades,
            "puntaje_final": puntaje_final,
            "clasifica": clasifica
        }

def report_general():
    if not participantes: 
        messagebox.showinfo("Reporte", "No hay participantes registrados.") 
        return

def reporte_individual():



ventana = tk.Tk()
ventana.title("Sistema de Rendimiento Pruebas Deportivas")

tk.Label(ventana, text="Menu Principal")
tk.Button(ventana, text="1. Registrar Participante")
tk.Button(ventana, text="2. Reporte General")
tk.Button(ventana, text="3. Reporte Individual")
tk.Button(ventana, text="4. salir")

ventana.mainloop()