import tkinter as tk # Importar tkinter para el GUI
from tkinter import ttk # Importar el treeview y widgets avanzados
import DataBase # Importar el módulo database.py
import ast # Importar la libreria ast para convertir strings a estructuras

#----------------------------
# Variables
#----------------------------

root = tk.Tk()  # Ventana principal
table_frame = tk.Frame(root) # Contenedor para la tabla de resultados
movies = [] # Lista global para almacenar las peliculas filtradas

# ---------------------------
# Funciones
# ---------------------------

def create_window():
    root.geometry("1280x720") # Tamaño de la ventana
    root.title("SRP") # Titulo de la ventana


def show_selection(event = None):
    selection_indexes = list_genres_listbox.curselection() # Obtener indices seleccionados en Listbox

    selected_genres = [list_genres_listbox.get(i) for i in selection_indexes] # Mostrar los géneros elegidos en la etiqueta

    results_label.config(text="Chosen genres: " + ", ".join(selected_genres))
    # Mostrar los generos elegidos en la etiqueta

    if not selection_indexes:
        # Ocultar botón y etiqueta si no hay selección
        confirm_button.forget()
        results_label.forget()
    else:
        # Mostrar boton de confirmación
        confirm_button.pack(before=table_frame)

def confirm_selection():
    selected_movies = [] # Lista creada para evitar duplicados

    global movies

    # Limpiar tabla de resultados cada vez que se refresque
    for row in tree.get_children():
        tree.delete(row)
    
    # Obtener selección de géneros
    selection_indexes = list_genres_listbox.curselection()
    selected_genres = [list_genres_listbox.get(i) for i in selection_indexes]
    
    # Se llama a la función get_qualified_movies_by_rate del modulo DataBase para almacenar una lista de las peliculas filtradas en la variable global
    movies = DataBase.get_qualified_movies_by_rate(DataBase.filter_by_genres(selected_genres))
    
    # Insertar peliculas en la tabla sin duplicar titulos
    for movie in movies:
        # Si la pelicula no se encuentra en la lista creada, entonces la agrega y es insertada en el arbol de la tabla
        if not movie["title"] in selected_movies:
            tree.insert("", tk.END, values=(movie["title"], movie["overview"], movie["vote_average"]))
            selected_movies.append(movie["title"])
    
    # Si el usuario ya ha hecho scroll con anterioridad, al refrescar la tabla vuelve al inicio automaticamente
    tree.yview_moveto(0)


def show_overview(event = None):
    # Obtener la fila seleccionada en la tabla
    selected = tree.selection()
    if selected:
        # Mostrar titulo y descripción en etiquetas
        overview_title_label.config(text=tree.item(selected[0])["values"][0])
        overview_label.config(text=tree.item(selected[0])["values"][1])

        # Obtener la lista de productoras de la película
        production_company = DataBase.metadata.loc[DataBase.metadata["title"] == tree.item(selected[0])["values"][0], "production_companies"].values[0]
        
        # Convertir el string a lista de diccionarios
        names_dict = ""
        p_dict = ast.literal_eval(production_company)

        # Concatenar nombres de productoras si en el archivo hay varias compañias productoras
        for p_company in p_dict:
            names_dict += p_company["name"] + ", "
        names_dict = names_dict[0:-2]
        
        # Mostrar productoras en etiqueta
        productor_label.config(text="Production companies: " + names_dict)
        productor_label.pack(before=confirm_button)

# ---------------------------
# Widgets
# ---------------------------

# Se crean todos los widgets de la aplicación
overview_title_label = tk.Label(root, text="", wraplength=800, justify="center") # Etiqueta para título
overview_label = tk.Label(root, text="", wraplength=800, justify="left") # Etiqueta para descripción
title_label = tk.Label(root, text="Movies recomendation system.") # Título principal
instruction_label = tk.Label(root, text="Choose the genres you would like to filter.") # Instrucciones
productor_label = tk.Label(root) # Etiqueta para productoras
results_label = tk.Label(root, text="") # Etiqueta para mostrar géneros elegidos
list_genres_listbox = tk.Listbox(root, height=10, selectmode="multiple") # Listbox para géneros 
confirm_button = tk.Button(root, text="Confirm selection", command=confirm_selection) # Botón de confirmación

# ---------------------------
# Llenar Listbox con géneros
# ---------------------------

genres = DataBase.get_all_genres()  # Lista de géneros
for genre in genres:
    list_genres_listbox.insert(tk.END, genre)

# ---------------------------
# Ubicación de widgets
# ---------------------------

#Se despliegan los widgets
title_label.pack()
instruction_label.pack()
list_genres_listbox.pack()
results_label.pack()
overview_title_label.pack()
overview_label.pack()
tree = ttk.Treeview(table_frame, columns=("Title", "Overview", "Rating"), show="headings")
tree.heading("Title", text="Title")
tree.heading("Rating", text="Rating")
tree.heading("Overview", text="Overview")


tree.pack(fill="both", expand=True)
table_frame.pack(pady=10, fill="both", expand=True)

#----------------------------
# Eventos
#----------------------------

list_genres_listbox.bind("<<ListboxSelect>>", show_selection)
tree.bind("<<TreeviewSelect>>", show_overview)
# ---------------------------
# Configuración de la ventana
# ---------------------------

def startup():
    create_window()
    root.mainloop()
