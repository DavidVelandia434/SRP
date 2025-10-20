import tkinter as tk
from tkinter import ttk
import DataBase
from movie_details import get_movie_details_by_id
import webbrowser

# ---------------------------- Configuración ventana ----------------------------
root = tk.Tk()
root.geometry("1000x700")
root.title("Sistema de Recomendación de Películas")

# ---------------------------- Variables globales ----------------------------
table_frame = tk.Frame(root)
details_frame = tk.Frame(root, bg="#f0f0f0", padx=10, pady=10)

# Widgets detalles
title_label_widget = tk.Label(details_frame, text="", font=("Arial", 16, "bold"), bg="#6dbdff")
director_label = tk.Label(details_frame, text="", bg="#f0f0f0")
runtime_label = tk.Label(details_frame, text="", bg="#f0f0f0")
genres_label = tk.Label(details_frame, text="", bg="#f0f0f0")
rating_label = tk.Label(details_frame, text="", bg="#f0f0f0")
overview_label = tk.Label(details_frame, text="", wraplength=500, justify="left", bg="#f0f0f0")
poster_link = tk.Label(details_frame, text="", fg="blue", cursor="hand2", bg="#f0f0f0", font=("Arial", 10))

# ---------------------------- Funciones ----------------------------
def open_poster(url):
    webbrowser.open(url)

def confirm_selection():
    selected_movies = []
    for row in tree.get_children():
        tree.delete(row)
    
    selection = list_genres_listbox.curselection()
    if not selection:
        return
    
    selected_genres = [list_genres_listbox.get(i) for i in selection]
    
    movies = DataBase.get_qualified_movies_by_rate(DataBase.filter_by_genres(selected_genres))
    
    for m in movies:
        if not m["title"] in selected_movies:
            tree.insert("", "end", values=(m["id"], m["title"], m["vote_average"]))
            selected_movies.append(m["title"])

    tree.yview_moveto(0)

def show_movie_details(event=None):
    selected = tree.selection()
    if not selected:
        return
    
    item = tree.item(selected[0])
    movie_id = item["values"][0]
    
    details = get_movie_details_by_id(movie_id)
    
    if "error" in details:
        title_label_widget.config(text="Error al cargar detalles")
        director_label.config(text="")
        runtime_label.config(text="")
        genres_label.config(text="")
        rating_label.config(text="")
        overview_label.config(text="")
        poster_link.config(text="", cursor="")
        return
    
    title_label_widget.config(text=details["title"])
    director_label.config(text=f"🎥 Director: {details['director']}")
    runtime_label.config(text=f"⏱️ Duración: {details['runtime']}")
    genres_label.config(text=f"🎭 Géneros: {details['genres']}")
    rating_label.config(text=f"⭐ Calificación: {details['vote_average']}/10")
    overview_label.config(text=f"📝 Sinopsis:\n{details['overview']}")
    
    poster_link.config(text="🎞️ Ver pósters en Google Images", fg="blue", cursor="hand2")
    poster_link.bind("<Button-1>", lambda e: open_poster(details["poster_url"]))

# ---------------------------- Widgets principales ----------------------------
tk.Label(root, text="Sistema de Recomendación de Películas", font=("Arial", 18)).pack(pady=10)

tk.Label(root, text="Selecciona uno o más géneros:").pack()
list_genres_listbox = tk.Listbox(root, height=8, selectmode="multiple")
for g in DataBase.get_all_genres():
    list_genres_listbox.insert(tk.END, g)
list_genres_listbox.pack(pady=5)

tk.Button(root, text="Filtrar Películas", command=confirm_selection).pack(pady=5)

columns = ("ID", "Título", "Calificación")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
for col, width in zip(columns, [80, 300, 100]):
    tree.heading(col, text=col)
    tree.column(col, width=width)
tree.pack(fill="both", expand=True)
tree.bind("<<TreeviewSelect>>", show_movie_details)

table_frame.pack(pady=10, fill="both", expand=True)

details_frame.pack(pady=10, fill="x")
for widget in [title_label_widget, director_label, runtime_label, genres_label, rating_label, overview_label, poster_link]:
    widget.pack(anchor="w", pady=2)

# ---------------------------- Función startup ----------------------------
def startup():
    root.mainloop()
