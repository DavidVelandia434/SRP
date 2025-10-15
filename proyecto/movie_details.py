# DETALLES DE PELICULAS
import ast
import pandas as pd
#librerias de prueba
import sys
from urllib.parse import quote
# Importa la base de datosd ya fusionado por tu grupo
from DataBase import metadata  

#///////////////////////////////////////////////////////////////

#crear la url hacia google imagenes del poster de la pelicula
def get_google_poster_url(title: str) -> str:
    query = quote(f"{title} movie poster")
    return f"https://www.google.com/search?q={query}&tbm=isch"

#------------------------------------------------------------

#buscar el id de la pelicula seleccionada en metadata
def get_movie_details_by_id(movie_id: int) -> dict:

    # Buscar la película por ID
    row = metadata[metadata['id'] == movie_id]
    if row.empty:
        return {"error": "Película no encontrada"}
    return _extract_details(row.iloc[0])

#------------------------------------------------------------

#Titulo de la pelicula
def get_movie_details_by_title(title: str) -> dict:
   # Obtiene los detalles usando el título exacto (ignora mayúsculas/minúsculas y espacios mediante case y na de pandas).
    match = metadata[metadata['title'].str.fullmatch(title, case=False, na=False)]
    if match.empty:
        return {"error": f"No se encontró la película: {title}"}
    return _extract_details(match.iloc[0])

#------------------------------------------------------------

#extraer los datos y limpiar
def _extract_details(row):
    
    # Géneros
    #convierte en lista real, si presenta dato corrupto presenta como desconocida
    try:
        genres = [g['name'] for g in ast.literal_eval(row['genres'])]
    except:
        genres = ["Desconocido"]

    # Director (sacado de credits)
    director = "Desconocido"
    #se ubica en la casilla de crew en el dicciionario de job
    if 'crew' in row and pd.notna(row['crew']):
        try:
            crew_list = ast.literal_eval(row['crew'])
            directors = [p['name'] for p in crew_list if p.get('job') == 'Director']
            director = directors[0] if directors else "Desconocido"
        except:
            pass

    # Palabras clave (keywords)
    keywords = "Sin palabras clave"
    if 'keywords' in row and pd.notna(row['keywords']):
        try:
            kw_list = ast.literal_eval(row['keywords'])
            keywords = ", ".join([kw['name'] for kw in kw_list if isinstance(kw, dict)])
        except:
            pass

    #almacena la url generada para mostrarla
    poster_url = get_google_poster_url(row['title'])

    # Duración
    runtime = f"{int(row['runtime'])} minutos" if pd.notna(row['runtime']) and row['runtime'] > 0 else "Duración desconocida"

    # Sinopsis
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
        #"imdb_id": row['imdb_id'] if pd.notna(row['imdb_id']) else None
    }

#######################################################################################################
# Prueba 
#detalles = get_movie_details_by_id(862)

#if "error" in detalles:
 #   print(detalles["error"])
#else:
 #   print("\n === DETALLES DE LA PELÍCULA === ")
  #  print(f"Título: {detalles['title']}")
   # print(f"Director: {detalles['director']}")
   # print(f"Duración: {detalles['runtime']}")
   # print(f"Géneros: {detalles['genres']}")
   # print(f"Calificación: {detalles['vote_average']}/10")
   # print(f"Póster: {detalles['poster_url']}")
   # print(f"\n Sinopsis:\n{detalles['overview']}")