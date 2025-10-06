import tkinter as tk
from tkinter import ttk
import DataBase

#----------------------------
# Variables
#----------------------------

root = tk.Tk()  # Ventana principal
table_frame = tk.Frame(root)

# ---------------------------
# Funciones
# ---------------------------

def create_window():
    root.geometry("1280x720")
    root.title("SRP")

def show_selection(event = None):
    selection_indexes = list_genres_listbox.curselection()  # Índices de Listbox
    selected_genres = [list_genres_listbox.get(i) for i in selection_indexes]  # Obtener texto
    results_label.config(text="Géneros elegidos: " + ", ".join(selected_genres))

    if not selection_indexes:
        confirm_button.forget()
        results_label.forget()
    else:
        confirm_button.pack(before=table_frame)

def confirm_selection():
    # Limpiar tabla
    for row in tree.get_children():
        tree.delete(row)
    
    # Obtener selección de géneros
    selection_indexes = list_genres_listbox.curselection()
    selected_genres = [list_genres_listbox.get(i) for i in selection_indexes]
    
    movies = DataBase.get_qualified_movies_by_rate( DataBase.filter_by_genres(selected_genres))
    
    for movie in movies:
        tree.insert("", tk.END, values=(movie["title"], movie["overview"], movie["vote_average"]))

def show_overview(event = None):
    selected = tree.selection()
    if selected:
        overview_title_label.config(text=tree.item(selected[0])["values"][0])
        overview_label.config(text=tree.item(selected[0])["values"][1])

# ---------------------------
# Widgets
# ---------------------------
overview_title_label = tk.Label(root, text="", wraplength=800, justify="center")
overview_label = tk.Label(root, text="", wraplength=800, justify="left")
title_label = tk.Label(root, text="Movies recomendation system.")  
instruction_label = tk.Label(root, text="Choose the genres you´d like to filter.")  
results_label = tk.Label(root, text="")  
list_genres_listbox = tk.Listbox(root, height=10, selectmode="multiple")  
confirm_button = tk.Button(root, text="Confirm selection", command=confirm_selection)

# ---------------------------
# Llenar Listbox con géneros
# ---------------------------

genres = DataBase.get_all_genres()  # Lista de géneros
for genre in genres:
    list_genres_listbox.insert(tk.END, genre)

# ---------------------------
# Ubicación de widgets
# ---------------------------

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


create_window()
root.mainloop()
