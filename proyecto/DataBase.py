import json

#Filtro de peliculas por genero, recibe un parametro de tipo lista en el que se almacenaran strings con los distintos tipos de categorias
def movies_by_genre(favorite_genres):

    #Validación del parametro para verificar que se pase una lista como parametro
    if not isinstance(favorite_genres, list):
        raise TypeError("El objeto pasado")
    

    #Lista para guardar todas las peliculas que cumplan
    recommended_movies = []

    #Se abre el JSON con los datos de todas las peliculas disponibles que tiene, guarda los datos en bytes en un buffer de 10 mb
    with open("peliculas.jsonl", "rb", buffering=10*1024*1024) as file:
        
        #se hace un bucle para acceder a cada linea del jsonl
        for line in file:

            #se codifica el byte en utf-8 para que se convierta en un string, y luego se almacena en una variable f
            #convirtiendo el string a un diccionario JSON
            line = line.decode("utf-8")
            f = json.loads(line)

            #se hace una verificación para saber si el diccionario tiene la variable genres.
            if(f["genres"] != None):

                #Si la tiene, como la base de datos envia las cateogiras separadas por comas, se hace una lista temporal separando las palabras por comas
                f_genres = f["genres"].split(",")

                #luego se itera en la lista pasada como argumetno de la funcion, y se valida que con minimo una categoria que coincida con la propiedad del diccionario 
                #se guarda a en la lista recommended_movies
                for genre in favorite_genres:
                    if(not(genre in f_genres)):
                        continue
                    else: 
                        recommended_movies.append((f))
                        break

        #Se retorna la lista
        return recommended_movies


#Funcion para filtrar por formato, recibe dos argumentos, el primero es una lista con los objetos de la pelicula, y el segundo el formato como un string
def movies_by_format(movies, format):
    #Lista para guardar las peliculas filtradas por formato
    movies_by_format_lst = []

    #verificación que los argumentos pasados tengan el tipo de dato corresopndiente
    if not isinstance(movies, list) or not isinstance(format, str):
        raise TypeError("El objeto pasado")
    
    #se itera en la list ade peliculas hasta que una tenga el mismo formato, si sí, se guarda en la lista
    for movie in movies:
        if movie["titleType"] == format:
            movies_by_format_lst.append(movie)
    
    #se retorna la lista
    return movies_by_format_lst
        

values = movies_by_genre(["Animation", "Comedy", "Romance"])

final_movies = movies_by_format(values, "tvEpisode")

for i in range(100):
    print(final_movies[i]["primaryTitle"])
