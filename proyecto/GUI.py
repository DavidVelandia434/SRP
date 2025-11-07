import tkinter as tk
from tkinter import ttk
import DataBase
from movie_details import get_movie_details_by_id
import webbrowser

# ---------------------------- PALETA "CINE PREMIUM" ----------------------------
BG_MAIN = "#1c1c1c"
BG_PANEL = "#2a2a2a"
ACCENT = "#d4af37"
TEXT_MAIN = "#f5f5f5"
TEXT_SECONDARY = "#bdbdbd"
ROW_ALT = "#242424"
SELECT_BG = "#3c3c3c"

# ---------------------------- CONFIGURACIÓN VENTANA ----------------------------
root = tk.Tk()
root.geometry("1000x700")
root.title("🎬 Sistema de Recomendación de Películas")
root.configure(bg=BG_MAIN)
root.state("zoomed")

# ---------------------------- VARIABLES GLOBALES ----------------------------
table_frame = tk.Frame(root, bg=BG_MAIN)
details_frame = tk.Frame(root, bg=BG_PANEL, relief="flat")

# ---------------------------- WIDGETS DE DETALLES ----------------------------
# Subframes para separar la información
left_info_frame = tk.Frame(details_frame, bg=BG_PANEL)
right_info_frame = tk.Frame(details_frame, bg=BG_PANEL)

# Izquierda
title_label_widget = tk.Label(left_info_frame, text="", font=("Segoe UI", 16, "bold"), bg=BG_PANEL, fg=ACCENT)
director_label = tk.Label(left_info_frame, text="", bg=BG_PANEL, fg=TEXT_SECONDARY, font=("Segoe UI", 11))
runtime_label = tk.Label(left_info_frame, text="", bg=BG_PANEL, fg=TEXT_SECONDARY, font=("Segoe UI", 11))
genres_label = tk.Label(left_info_frame, text="", bg=BG_PANEL, fg=TEXT_SECONDARY, font=("Segoe UI", 11))
rating_label = tk.Label(left_info_frame, text="", bg=BG_PANEL, fg=TEXT_SECONDARY, font=("Segoe UI", 11))
poster_link = tk.Label(left_info_frame, text="", fg=ACCENT, cursor="hand2", bg=BG_PANEL, font=("Segoe UI", 10, "underline"))

# Derecha
overview_label = tk.Label(right_info_frame, text="", wraplength=700, justify="left", bg=BG_PANEL, fg=TEXT_MAIN, font=("Segoe UI", 10))

# Empaquetar detalles
title_label_widget.pack(anchor="w", pady=3)
director_label.pack(anchor="w", pady=2)
runtime_label.pack(anchor="w", pady=2)
genres_label.pack(anchor="w", pady=2)
rating_label.pack(anchor="w", pady=2)
poster_link.pack(anchor="w", pady=5)

overview_label.pack(anchor="w", pady=3, padx=10)

left_info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
right_info_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# ---------------------------- FUNCIONES ----------------------------
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
    
    for i, m in enumerate(movies):
        if not m["title"] in selected_movies:
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            tree.insert("", "end", values=(m["id"], m["title"], m["vote_average"]), tags=(tag,))
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
        title_label_widget.config(text="Error loading details")
        for lbl in [director_label, runtime_label, genres_label, rating_label, overview_label, poster_link]:
            lbl.config(text="")
        return
    
    title_label_widget.config(text=details["title"])
    director_label.config(text=f"🎥 Director: {details['director']}")
    runtime_label.config(text=f"⏱️ Runtime: {details['runtime']}")
    genres_label.config(text=f"🎭 Genres: {details['genres']}")
    rating_label.config(text=f"⭐ Rating: {details['vote_average']}/10")
    overview_label.config(text=f"📝 Overview:\n{details['overview']}")
    
    poster_link.config(text="🎞️ See poster in Google Images", fg=ACCENT, cursor="hand2")
    poster_link.bind("<Button-1>", lambda e: open_poster(details["poster_url"]))

# ---------------------------- CABECERA ----------------------------
tk.Label(root, text="🎬 Movie Recomendation System",
         font=("Segoe UI", 20, "bold"), bg=BG_MAIN, fg=ACCENT).pack(pady=15)

tk.Label(root, text="Select one or more genres:",
         font=("Segoe UI", 13, "bold"), bg=BG_MAIN, fg=TEXT_MAIN).pack()

# ---------------------------- LISTBOX ----------------------------
list_genres_listbox = tk.Listbox(
    root,
    height=8,
    selectmode="multiple",
    font=("Segoe UI", 11),
    bg=BG_PANEL,
    fg=TEXT_MAIN,
    selectbackground=SELECT_BG,
    selectforeground=ACCENT,
    highlightthickness=1,
    highlightcolor=ACCENT,
    relief="flat",
    bd=0,
    activestyle="none"
)
for g in DataBase.get_all_genres():
    list_genres_listbox.insert(tk.END, "             " + g)
list_genres_listbox.pack(pady=5, ipadx=5, ipady=3)

# ---------------------------- BOTÓN ----------------------------
def on_enter(e): filter_button.config(bg=ACCENT, fg=BG_MAIN)
def on_leave(e): filter_button.config(bg=BG_PANEL, fg=ACCENT)

filter_button = tk.Button(root, text="🎞️ Filter movies.", command=confirm_selection,
                          font=("Segoe UI", 12, "bold"), bg=BG_PANEL, fg=ACCENT,
                          activebackground=ACCENT, activeforeground=BG_MAIN,
                          cursor="hand2", bd=0, padx=15, pady=5)
filter_button.bind("<Enter>", on_enter)
filter_button.bind("<Leave>", on_leave)
filter_button.pack(pady=10)

# ---------------------------- TABLA ----------------------------
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=BG_PANEL,
    foreground=TEXT_MAIN,
    rowheight=28,
    fieldbackground=BG_PANEL,
    font=("Segoe UI", 10),
    borderwidth=0
)
style.configure(
    "Treeview.Heading",
    background=ACCENT,
    foreground=BG_MAIN,
    font=("Segoe UI", 11, "bold"),
    borderwidth=0
)
style.map(
    "Treeview",
    background=[("selected", SELECT_BG)],
    foreground=[("selected", ACCENT)]
)

columns = ("ID", "Title", "Rating")
tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
for col, width in zip(columns, [80, 400, 100]):
    tree.heading(col, text=col)
    tree.column(col, width=width)
tree.tag_configure("evenrow", background=BG_PANEL)
tree.tag_configure("oddrow", background=ROW_ALT)
tree.pack(fill="both", expand=True, padx=10, pady=5)
tree.bind("<<TreeviewSelect>>", show_movie_details)

table_frame.pack(pady=10, fill="both", expand=True)

# ---------------------------- DETALLES ----------------------------
details_frame.pack(pady=15, fill="x", padx=10)

# ---------------------------- STARTUP ----------------------------
def startup():
    root.mainloop()
