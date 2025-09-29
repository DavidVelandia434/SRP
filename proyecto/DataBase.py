import json

def load_movies(file_path="peliculas.jsonl"):
    movies = []

    #Se abre el JSONl con los datos de todas las peliculas disponibles que tiene, guarda los datos en bytes en un buffer de 10 mb
    with open(file_path, "rb", buffering=10*1024*1024) as file:
        #se hace un bucle para acceder a cada linea del JSONl
        for line in file:
            #se codifica el byte en utf-8 para que se convierta en un string, y luego se almacena en una variable line
            #convirtiendo el string a un diccionario JSONl
            
            #luego se usa el retorno yield para enviar una pelicula a la vez
            line = line.decode("utf-8")
            yield json.loads(line)
            

#Filtro de peliculas por genero, recibe un parametro de tipo lista en el que se almacenaran strings con los distintos tipos de categorias
def movies_by_genre(favorite_genres):
    #convertimos la lista en un set para manejar de forma mas eficiente las comparaciones
    favorite_genres_set = set(favorite_genres)

    #guardamos la funcion generadora en una variable para su uso posterior
    load_movies_gen = load_movies()

    #Lista para guardar todas las peliculas que cumplan
    recommended_movies = []

    #Validación del parametro para verificar que se pase una lista como parametro
    if not isinstance(favorite_genres, list):
        raise TypeError("Both movies and favorite_genres must be lists")
    
    #Se itera en la funcion generadora para obtener cada pelicula
    for movie in load_movies_gen:
        #Se obtiene el valor del diccionario en la clave genres
        genres = movie.get("genres")
        #Si no la encuentra, pasa por alto esa categoria
        if not genres:
            continue

        #Si encuentra el valor, por ejemplo ("Animation,Comedy,Romance") separa cada palabra por comas
        movie_genres = set(genres.split(","))

        #si este set tiene intersecciones con categorias de favorite_genres_set, es añadido a la lista de pelciulas recomendadas
        if movie_genres & favorite_genres_set:  
            recommended_movies.append(movie)


    #Se retorna peliculas recomendadas
    return recommended_movies

#Funcion para filtrar por formato, recibe un argumento, el formato como un string
def movies_by_format(format):


    #Lista para guardar las peliculas filtradas por formato
    movies_by_format_lst = []

    load_movies_gen = load_movies()

    #verificación que el argumento pasado tengan el tipo de dato corresopndiente
    if not isinstance(format, str):
        raise TypeError("El objeto pasado")
    
    #se itera en la lista de peliculas hasta que una tenga el mismo formato, si sí, se guarda en la lista
    for movie in load_movies_gen:
        if movie["titleType"] == format:
            movies_by_format_lst.append(movie)
    
    #se retorna la lista
    return movies_by_format_lst

def movies_by_age(is_adult, movies):
    movies_by_age_lst = []

    for movie in movies:
        if is_adult == int(movie.get("isAdult")):
            movies_by_age_lst.append(movie)
    
    return movies_by_age_lst

values = movies_by_genre(["Animation", "Comedy", "Romance"])
first_movies = []
for i in range(100):
    first_movies.append(values[i])

by_age = movies_by_age(0, first_movies)
print("Peliculas para menores de edad")

for i in by_age:
    print(i)
