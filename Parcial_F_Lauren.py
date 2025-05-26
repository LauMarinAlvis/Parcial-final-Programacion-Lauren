#Sistema de Gestión de Rendimiento en Pruebas Deportivas

import tkinter as tk 
from tkinter import simpledialog, messagebox, ttk
import random
import math
import pandas as pd 
import matplotlib.pyplot as plt
import os
from PIL import Image, ImageTk

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
            "clasifica": clasifica}

        #creando diciionario desde los datos q ingresan como participantes, y su posicion en la fila q se añade al csv histo. participantes
        registro_csv = {"nombre": nombre,
        "puntaje_resistencia": puntajes[0],
        "dificultad_resistencia": dificultades[0],
        "puntaje_fuerza": puntajes[1],
        "dificultad_fuerza": dificultades[1],
        "puntaje_velocidad": puntajes[2],
        "dificultad_velocidad": dificultades[2],
        "puntaje_final": puntaje_final,
        "clasifica": clasifica }    

        df_fila = pd.DataFrame([registro_csv])

        archivo_csv = "historial_participantes.csv"
        escribir_encabezado = not os.path.exists(archivo_csv)  

        df_fila.to_csv(archivo_csv, mode='a', index=False, header=escribir_encabezado)
        messagebox.showinfo("regis participante", f"participante {nombre} ingreso OK.\nPuntaje final: {puntaje_final}\nClasifica: {clasifica}")
        
    except ValueError as e:
        messagebox.showerror("atencion", f"invalido: {str(e)}. Solo numeros entre 0 y 100.") 

     #cambiar colores de graficos con lista https://www.youtube.com/watch?v=XEG4eh5l_qU    y https://www.youtube.com/watch?v=Vtn8w2sqMtA
def grafico_torta(datos, titulo): 
    plt.figure(figsize=(4, 3), facecolor="#FCE4EC")  
    ax = plt.gca()
    ax.set_facecolor("#FCE4EC")
    colores = ["#F8BBD0", "#F48FB1" ]
    plt.pie(datos.values(), labels=datos.keys(), autopct="%1.1f%%",colors=colores,textprops={"color": "#AD1457"}) 
    plt.title(titulo, color="#AD1457", fontsize=12)  
    temp_file = "temp_pie.png"
    plt.savefig(temp_file)      
    plt.close()    
    return temp_file   

    
def grafico_barras(datos, titulo):
    plt.figure(figsize=(4, 3),facecolor="#FCE4EC") 
    ax = plt.gca()
    ax.set_facecolor("#FCE4EC")
    colores = ["#F8BBD0", "#F48FB1", "#F06292"]
    plt.bar(datos.keys(), datos.values(),color ="#F48FB1", edgecolor= "#AD1457")
    plt.title(titulo, color="#AD1457", fontsize=12) 
    plt.ylabel("cantidad", color="#AD1457")
    plt.xticks(rotation=10 ,color="#AD1457")
    plt.yticks(color= "#AD1457")
    
    temp_file = "temp_plot.png" 
    plt.savefig(temp_file)
    plt.close()     
    return temp_file     


def report_general():
    if not participantes: 
        messagebox.showinfo("reporte", "sin participants registrados") 
        return

    reporte_ventana = tk.Toplevel(ventana)
    reporte_ventana.title("reporte general")
    reporte_ventana.geometry("900x700")
    reporte_ventana.configure(bg="#FCE4EC")

    #https://www.youtube.com/watch?v=kqbkUKIc1Gk 
    notebook = ttk.Notebook(reporte_ventana) 
    tab1 = ttk.Frame(notebook) 
    notebook.add(tab1, text="Datos de participantes") 

    
    #https://www.youtube.com/watch?v=lqHcKT7ZwOo
    tree = ttk.Treeview(tab1, columns=("nombre", "Puntaje final", "clasifica"), show="headings")
    tree.heading("nombre", text="nombre")
    tree.heading("Puntaje final", text="Puntaje final")
    tree.heading("clasifica", text="clasifica")  

    for nombre, datos in participantes.items():
        tree.insert("", "end", values=(nombre, datos["puntaje_final"], datos["clasifica"]))    
    tree.pack(expand=True, fill="both", padx=10, pady=10)
    
    tab2 = ttk.Frame(notebook)
    notebook.add(tab2, text="estadistica")
    
    # Creando estadsticas promedio,clasificar los participants califican si o no
    df = pd.DataFrame.from_dict (participantes, orient="index")
    
    stats_text = tk.Text(tab2, wrap="word")
    scroll = ttk.Scrollbar(tab2, orient="vertical", command=stats_text.yview)
    stats_text.configure(yscrollcommand=scroll.set)
    
    scroll.pack(side="right", fill="y")
    stats_text.pack(expand=True, fill="both", padx=10, pady=10) 

    stats_text.insert("end", "estadisticas import:\n\n")
    stats_text.insert("end", df["puntaje_final"].describe().to_string()) 
    
    promedio = df["puntaje_final"].mean()
    stats_text.insert("end", f"\n\nPuntaje promedio del grupo: {promedio:.2f}")
    
    clasificados = df["clasifica"].value_counts()
    stats_text.insert("end", f"\n\nConteo de clasificacion:\n{clasificados.to_string()}")
    #- Matriz de correlación de los puntajes (si se usó pandas)
    # Bendita m de correlacion :C
    if len(participantes) > 1:
        puntajes_df = pd.DataFrame([p["puntajes"] for p in participantes.values()], columns=["resistencia", "fuerza", "velocidad"])
        stats_text.insert("end", "\n\nmatriz correlacion:\n")
        stats_text.insert("end", puntajes_df.corr().to_string())

    # - Gráfico de torta con el total de clasificados y no clasificados
    tab3 = ttk.Frame(notebook)
    notebook.add(tab3, text="graficos")

    frame_graficos = ttk.Frame(tab3)
    frame_graficos.pack(expand=True, fill="both", padx=10, pady=10)

    clasificados_dict = clasificados.to_dict()#clasificacion
    temp_file_pie = grafico_torta(clasificados_dict, "clasificacion")

    img_pie = Image.open(temp_file_pie)
    photo_pie = ImageTk.PhotoImage(img_pie)
    label_pie = tk.Label(frame_graficos, image=photo_pie)
    label_pie.image = photo_pie
    label_pie.grid(row=0, column=0, padx=10, pady=10)

    #- Gráfico de torta con el total de clasificados y no clasificados
    # Gráfico de barras de puntajes promedio
    if len(participantes) > 1:
        puntajes_promedio = {
            "Resistencia": sum(p["puntajes"][0] for p in participantes.values()) / len(participantes),
            "Fuerza": sum(p["puntajes"][1] for p in participantes.values()) / len(participantes),
            "Velocidad": sum(p["puntajes"][2] for p in participantes.values()) / len(participantes)
        }

        temp_file_bar = grafico_barras(puntajes_promedio, "promedio prueba")

        img_bar = Image.open(temp_file_bar)
        photo_bar = ImageTk.PhotoImage(img_bar)
        label_bar = tk.Label(frame_graficos, image=photo_bar)
        label_bar.image = photo_bar
        label_bar.grid(row=0, column=1, padx=10, pady=10)

        os.remove(temp_file_bar)
         
        # grafico de m de correlacion :C
        puntajes_df = pd.DataFrame([p["puntajes"] for p in participantes.values()] , columns=["resistencia", "fuerza", "velocidad"])
        matriz_corr = puntajes_df.corr() 
        #dandole forma m de correl 
        plt.figure(figsize=(4, 4))
        plt.title("Matriz de Correlación")
        plt.imshow(matriz_corr, cmap="Purples", interpolation="nearest")
        plt.colorbar(label="coeficiente")

        etiquetas = matriz_corr.columns
        plt.xticks(range(len(etiquetas)), etiquetas, rotation=59)
        plt.yticks(range(len(etiquetas)), etiquetas) 
        for i in range(len(etiquetas)):
            for j in range(len(etiquetas)):
                valor = matriz_corr.iloc[i, j]
                plt.text(j, i, f"{valor:.2f}", ha="center", va="center", color="black")

        plt.tight_layout()
        temp_file_corr = "temp_correlacion.png"
        plt.savefig(temp_file_corr)
        plt.close()

        img_corr = Image.open(temp_file_corr)
        photo_corr = ImageTk.PhotoImage(img_corr)
        label_corr = tk.Label(frame_graficos, image=photo_corr)
        label_corr.image = photo_corr
        label_corr.grid(row=1, column=1, padx=10, pady=10)

        os.remove(temp_file_corr)

    os.remove(temp_file_pie)
    notebook.pack(expand=True, fill="both", padx=10, pady=10)






def reporte_individual():
    nombre = simpledialog.askstring("Buscar participante", "nombre del participante:")
    if not nombre: 
        return

    datos = participantes.get(nombre)
    if datos:
        
        reporte_ventana = tk.Toplevel(ventana)
        reporte_ventana.title(f"repote individual - {nombre}")
        reporte_ventana.geometry("900x700")
        reporte_ventana.configure(bg="#FCE4EC") 
    
        notebook = ttk.Notebook(reporte_ventana)
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="info general")
        
        info_text = tk.Text(tab1, wrap="word", font=("Arial", 12))
        scroll = ttk.Scrollbar(tab1, orient="vertical", command=info_text.yview) 
        info_text.configure(yscrollcommand=scroll.set) 
        
        scroll.pack(side="right", fill="y") 
        info_text.pack(expand=True, fill="both", padx=10, pady=10)           
        info_text.insert("end", f"REPORTE INDIVIDUAL\n{'='*30}\n\n")
        info_text.insert("end", f"Nombre: {nombre}\n")
        info_text.insert("end", f"Puntaje final: {datos['puntaje_final']}\n")
        info_text.insert("end", f"Clasificación: {'CLASIFICA' if datos['clasifica'] == 'Si' else 'NO CLASIFICA'}\n\n") 

        pruebas = ["resistencia", "ruerza", "velocidad"]
        info_text.insert("end", f"DETALLE POR PRUEBA\n{'='*30}\n")
        
        for i, prueba in enumerate(pruebas):
            info_text.insert("end", f"\n{prueba.upper()}:\n")
            info_text.insert("end", f"  Puntaje Bruto: {datos['puntajes'][i]}/100\n")
            info_text.insert("end", f"  Dificultad: {datos['dificultades'][i]}\n")
            info_text.insert("end", f"  Puntaje Ponderado: {round(datos['puntajes'][i] * datos['dificultades'][i], 2)}\n") 


  #faltan puntajes - Puntaje promedio del grupoEstado graficar
  #- Resultados por prueba en un histograma con matplotlib
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Graficos derendimiento")
        
    
        frame_graficos = ttk.Frame(tab2)
        frame_graficos.pack(expand=True, fill="both", padx=10, pady=10)
        
        # puntajes totales prueba
        plt.figure(figsize=(6, 3))
        plt.bar(pruebas, datos['puntajes'], color='blue', alpha=0.7)
        plt.title(f"puntajes totales x prueba - {nombre}")
        plt.ylabel("puntaje (0-100)")
        plt.ylim(0, 100)
        
        temp_file1 = "temp_puntajes.png"
        plt.savefig(temp_file1)
        plt.close()
        
        img1 = Image.open(temp_file1)
        photo1 = ImageTk.PhotoImage(img1)
        label1 = tk.Label(frame_graficos, image=photo1)
        label1.image = photo1
        label1.grid(row=0, column=0, padx=5, pady=5)
  #- Nivel de dificultad aplicado en cada prueba en un histograma con matplotlib
    #dificultad por pruebas
        plt.figure(figsize=(6, 3))
        plt.bar(pruebas, datos['dificultades'], color='orange', alpha=0.7)
        plt.title(f"niveles de dificultad x prueba - {nombre}")
        plt.ylabel("factor de dificltad")
        plt.ylim(1.0, 1.3)
        
        temp_file2 = "temp_dificultad.png"
        plt.savefig(temp_file2)
        plt.close()
        
        img2 = Image.open(temp_file2)
        photo2 = ImageTk.PhotoImage(img2)
        label2 = tk.Label(frame_graficos,  image=photo2) 
        label2.image =  photo2
        label2.grid(row=1, column=0, padx=5, pady=5) 

        
  #- Puntaje ponderado por prueba en un histograma con matplotlib
        calculos_poderados = [round(p * d, 2) for p, d in zip(datos['puntajes'], datos['dificultades'])]
        plt.figure(figsize=(6, 3))
        plt.bar(pruebas, calculos_poderados,  color='green', alpha=0.7)
        plt.title(f"puntajes ponderados x prueba - {nombre}") 
        plt.ylabel("puntaje ponderado") 
        plt.ylim(0, 130)  # 100 * 1.3 = 130 
        
        temp_file3 = "temp_ponderados.png"
        plt.savefig(temp_file3)
        plt.close()
        
        img3 = Image.open(temp_file3)
        photo3 = ImageTk.PhotoImage(img3)
        label3 = tk.Label(frame_graficos, image=photo3) 
        label3.image = photo3
        label3.grid(row=0,  column=1 , padx=5, pady=5,) 

        for temp_file in [temp_file1, temp_file2, temp_file3 ]:  
            try: 
                os.remove(temp_file)
            except:
                pass
        
        notebook.pack(expand=True, fill="both", padx=10, pady=10)
    else:
        messagebox.showinfo("NO SE ENCUENTRA", "participant sin registro ") 
        #crracion de funcion para me de el reporte acumulado con todo el historial de datos del csv
def cargar_datos_csv ():
    archivo_csv = "historial_participantes.csv"
    if os.path.exists(archivo_csv):
        df = pd.read_csv(archivo_csv)
        for _, fila in df.iterrows():
            participantes[fila["nombre"]] = {"puntajes":[fila["puntaje_resistencia"],fila["puntaje_fuerza"], fila["puntaje_velocidad"]
                ],"dificultades":[fila["dificultad_resistencia"], fila["dificultad_fuerza"],fila["dificultad_velocidad"]],"puntaje_final": 
                fila["puntaje_final"],"clasifica": fila["clasifica"]}
cargar_datos_csv()                 

ventana = tk.Tk()
ventana.geometry("600x750")  
ventana.configure(bg="#FCE4EC")
ventana.title("Sistema de Rendimiento Pruebas Deportivas")

tk.Label(ventana, text="Sistema de Rendimiento Pruebas Deportivas", font=("Arial", 20, "bold"), bg="#FCE4EC", fg="#AD1457").pack(pady=10)
tk.Button(ventana, text="1. Registrar Participante", width=45,bg="#F8BBD0", fg="#333333",relief="raised",  bd=3,activebackground="#F48FB1",activeforeground="#ffffff", command=regis_participante).pack(pady=10)
tk.Button(ventana, text="2. Reporte General", width=45,bg="#F8BBD0", fg="#333333", relief="raised",  bd=3,activebackground="#F48FB1",activeforeground="#ffffff",command=report_general).pack(pady=10) 
tk.Button(ventana, text="3. Reporte Individual",  width=45,bg="#F8BBD0", fg="#333333", relief="raised",  bd=3,activebackground="#F48FB1",activeforeground="#ffffff",command=reporte_individual).pack(pady=10)
tk.Button(ventana, text="4. salir", width=45,bg="#F8BBD0", fg="#333333", relief="raised",  bd=3,activebackground="#F48FB1",activeforeground="#ffffff",command=ventana.quit).pack(pady=15) 


ventana.mainloop()

#https://www.youtube.com/watch?v=MpkTYMzhV0A
#https://www.youtube.com/watch?v=y69rqjEfwYI