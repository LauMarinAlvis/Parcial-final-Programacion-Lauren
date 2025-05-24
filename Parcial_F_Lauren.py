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
    nombre = simpledialog.askstring("Registro", "nombre del participante:")
    if not nombre:
        return 

    try:
        puntajes = []
        dificultades = []
        pruebas = ["resistencia", "fuerza", "velocidad"]
        for prueba in pruebas:
            puntaje = float(simpledialog.askstring("Registro", f"ingrese puntaje {prueba} (0-100):"))
            if puntaje < 0 or puntaje > 100:
                raise ValueError("fuera de rango")
            dificultad = round(random.uniform(1.0, 1.3), 2) 
            puntajes.append(puntaje)
            dificultades.append(dificultad)



        
        suma_ponderada = sum([p * d for p, d in zip(puntajes, dificultades)])
        suma_dificultades = sum(dificultades)
        puntaje_final = round(suma_ponderada / suma_dificultades)

        clasifica = "si" if puntaje_final >= 70 else "no"

        participantes[nombre] = {
            "puntajes": puntajes,
            "dificultades": dificultades,
            "puntaje_final": puntaje_final,
            "clasifica": clasifica
        }

        messagebox.showinfo("regis participante", f"participante {nombre} ingreso OK.\nPuntaje final: {puntaje_final}\nClasifica: {clasifica}")

    except ValueError as e:
        messagebox.showerror("atencion", f"invalido: {str(e)}. Solo numeros entre 0 y 100.")

def report_general():
    if not participantes: 
        messagebox.showinfo("Reporte", "No hay participantes registrados.") 
        return


def reporte_individual():
    nombre = simpledialog.askstring("Buscar participante", "nombre del participante:")
    if not nombre: 
        return

df = pd.DataFrame.from_dict (participantes, orient="index")   




ventana = tk.Tk()
ventana.title("Sistema de Rendimiento Pruebas Deportivas")

tk.Label(ventana, text="Menu Principal", font=("Arial", 18)).pack(pady=10) 
tk.Button(ventana, text="1. Registrar Participante", width=45, command=regis_participante).pack(pady=10)
tk.Button(ventana, text="2. Reporte General", width=45, command=report_general).pack(pady=10) 
tk.Button(ventana, text="3. Reporte Individual",  width=45, command=reporte_individual).pack(pady=10)
tk.Button(ventana, text="4. salir", width=45, command=ventana.quit).pack(pady=15) 


ventana.mainloop()