# DETALLES DE PELICULAS
import ast
import pandas as pd
#libreria para funciones relacionadas con el interpete de python como salir del programa
import sys
#manipular y construir convirtiendo caracteres especiales de texto para Urls
from urllib.parse import quote
# Importa la base de datosd ya fusionado por tu grupo
from DataBase import metadata  

#///////////////////////////////////////////////////////////////

#Crear la url hacia google imagenes del poster de la pelicula
def get_google_poster_url(title: str) -> str:
    query = quote(f"{title} movie poster")
    return f"https://www.google.com/search?q={query}&tbm=isch"

#------------------------------------------------------------

#Buscar el id de la pelicula seleccionada en metadata
def get_movie_details_by_id(movie_id: int) -> dict:

    # Buscar la película por ID en DataBase
    row = metadata[metadata['id'] == movie_id]
    #Empty por si se tiene ausencia de dato
    if row.empty:
        return {"error": "Película no encontrada"}
    return _extract_details(row.iloc[0])

#------------------------------------------------------------

#Titulo de la pelicula
def get_movie_details_by_title(title: str) -> dict:
   #Obtiene los detalles usando el título exacto (ignora mayúsculas/minúsculas y espacios mediante case y na de pandas).
    match = metadata[metadata['title'].str.fullmatch(title, case=False, na=False)]
    #Empty por si se tiene ausencia de dato
    if match.empty:
        return {"error": f"No se encontró la película: {title}"}
    return _extract_details(match.iloc[0])

#------------------------------------------------------------

#Extraer los datos y limpiar
def _extract_details(row):
    
    # Géneros
    #convierte en lista real, si presenta dato corrupto presenta como desconocida
    try:
        genres = [g['name'] for g in ast.literal_eval(row['genres'])]
    except:
        genres = ["Desconocido"]

    # Director (sacado de credits)
    director = "Desconocido"
    #Se ubica en la casilla de crew en el dicciionario de job
    #Identifica la columna crew no este vacia (notna)
    if 'crew' in row and pd.notna(row['crew']):
        try:
            crew_list = ast.literal_eval(row['crew'])
            directors = [p['name'] for p in crew_list if p.get('job') == 'Director']
        #si la pelicula tiene más de un director, seleccionara el primero que se muestra
            director = directors[0] if directors else "Desconocido"
        except:
            pass

    # Palabras clave (keywords)
    keywords = "Sin palabras clave"
    #Identifica la columna keywords no este vacia (notna)
    if 'keywords' in row and pd.notna(row['keywords']):
        try:
            kw_list = ast.literal_eval(row['keywords'])
            #isinstance verifica si el dato en la posicion kw es diccionario o dato corrupto
            keywords = ", ".join([kw['name'] for kw in kw_list if isinstance(kw, dict)])
        except:
            pass

    #Almacena la url generada para mostrarla
    poster_url = get_google_poster_url(row['title'])

    # Duración
    #Identifica la columna runtime no este vacia (notna)
    runtime = f"{int(row['runtime'])} minutos" if pd.notna(row['runtime']) and row['runtime'] > 0 else "Duración desconocida"

    # Sinopsis
    #Identifica la columna overview no este vacia (notna)
    #Strip evita caracteres no deseados como espacios
    overview = row['overview'] if pd.notna(row['overview']) and str(row['overview']).strip() else "Sinopsis no disponible."

    # Devolver diccionario limpio
    return {
        "id": row['id'],
        "title": row['title'],
        "overview": overview,
        "runtime": runtime,
        "director": director,
        "genres": ", ".join(genres),
        "keywords": keywords,
        "poster_url": poster_url,  # Ahora es una URL de búsqueda en Google
        "vote_average": round(row['vote_average'], 1) if pd.notna(row['vote_average']) else "N/A",
        "vote_count": int(row['vote_count']) if pd.notna(row['vote_count']) else 0,
        "release_date": row['release_date'] if pd.notna(row['release_date']) else "Fecha desconocida",
    }

#######################################################################################################
# Prueba 

if "error" in detalles:
  print("\n === DETALLES DE LA PELÍCULA === ")
  print(f"Título: {detalles['title']}")
   # print(f"Director: {de


















