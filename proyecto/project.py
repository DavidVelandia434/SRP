import pandas as pd
import ast
#Carga el dataset de metadatos de películas desde el archivo 'movies_metadata.csv'.
metadata = pd.read_csv("movies_metadata.csv", low_memory=False)

metadata = metadata.drop([19730, 29503, 35587], errors='ignore')


def load_and_merge_credits_keywords():
    global metadata
    #llamar a los archivos con los creditos y palabras claves
    credits = pd.read_csv("credits.csv")
    keywords = pd.read_csv("keywords.csv")

    #nos aseguramos que el parametro de id de cada archivo tenga el tipo int
    keywords['id'] = keywords['id'].astype('int')
    credits['id'] = credits['id'].astype('int')
    metadata['id'] = metadata['id'].astype('int')

    #juntamos los datos de los archivos.csv y keywords.csv con datos
    metadata = metadata.merge(credits, on='id')
    metadata = metadata.merge(keywords, on='id')


def estimate_votation():
    #Calcula dos valores estadísticos clave a partir de los siguientes datos:

    #El promedio global de claificaciones y el umbral minimo de votos necesario para considerar una pelicula para calificarla

    avg_rating = metadata['vote_average'].mean()
    minimum_votes = metadata['vote_count'].quantile(0.90)

    #retorna una tupla con el promedio y el minimo de votos para calificar
    return (avg_rating, minimum_votes)


def weighted_rating(x, m=estimate_votation()[1], c=estimate_votation()[0]):
    #calcular la puntuacion ponderada de una pelicula

    # v numero de votos
    # r promedio de votos
    # m numero minimo de votos
    #c promedio global de votos
    v = x['vote_count']
    r = x['vote_average']

    #retorna la puntuacion ponderada con la aplicación
    #la primera parte de la ecuacion mide un peso en base a los votos de 0 a 1 * r(promeio de votos)

    #la segunda parte de la ecuación suaviza la ecuacion al promedio global
    return (v/(v+m) * r + (m/(m+v) * c))

def get_qualified_movies_by_rating():
    # Filtrar las películas que cumplen el criterio de votos mínimos
    #loc filtra filas segun una condición booleana
    qualifited_movies = metadata.copy().loc[metadata["vote_count"] >= estimate_votation()[1]]

    # Calcular la puntuación ponderada para cada película
    #crear una nueva columna llamada score
    #apply() aplica la función weighted_rating fila por fila
    #axis=1 significa que recorremos las filas
    qualifited_movies["score"] = qualifited_movies.apply(weighted_rating, axis=1)

    # Ordenar las películas por la puntuación calculada de mayor a menor
    qualifited_movies = qualifited_movies.sort_values("score", ascending=False)

    return qualifited_movies

#obtener todos los generos disponibles
def get_all_genres():
    genres = []

    #se itera cada fila del dataframe de pandas
    for row in metadata.itertuples():
        #como el csv es un string con caracteres de python, podemos usar la libreria ast para convertir esos strings en estructuras que python puede leer, en este caso diccionarios
        g_dict = ast.literal_eval(row.genres)

        #recorremos el diccionario
        for d in g_dict:
            #si en el diccionaro, no se encuentra en generos, quiere decir que no esta duplicado, por lo cual se añade
            if d["name"] not in genres:
                genres.append(d["name"])
    
    #retorna generos
    return genres

    #filtrar por generos, toma un argumento de tipo lista genre, donde deben estar los generos a buscar por el usuario
def filter_by_genres(genre):
    filtered_movies = []
    for row in metadata.itertuples():
        g_dict = ast.literal_eval(row.genres)
        for d in g_dict:
            #el codigo es el mismo que al buscar la lista completa, pero en la condición buscamos si el genero del diccionario esta en el genero
            if d["name"] in genre:
                filtered_movies.append(row)

    return filtered_movies
        

load_and_merge_credits_keywords()

q_movies = get_qualified_movies_by_rating()

#print(metadata.columns.tolist())

print(filter_by_genres(get_all_genres()))