import DataBase

print("SPR")
generos=DataBase.get_all_genres()
generos_seleccionados = []
peliculas_filtradas_por_genero = []

print("----MENU GENERO----")
for i in range(len(generos)):
    print(f"{i+1}.{generos[i]}")
           
while(True):
   
    opcion=int(input("seleccione genero: "))        
   
    if 1<=opcion<=len(generos) and not(generos[opcion-1] in generos_seleccionados):
        print("elegiste el genero de ",generos[opcion-1])

        continuar= input("Deseas agregar mas generos? (s/n)")
        if(continuar.lower() == "n"):
            generos_seleccionados.append(generos[opcion-1])
            break
        elif(continuar.lower() == "s"):
            generos_seleccionados.append(generos[opcion-1])
        else:
            print("Escribe solo s o n para confirmar")
    elif  generos[opcion-1] in generos_seleccionados:
        print("El genero ya fue seleccionado")
    else:
        print("invalido, intente de nuevo")    

peliculas_filtradas_por_genero = DataBase.filter_by_genres(generos_seleccionados)
if len(peliculas_filtradas_por_genero) > 0:
    print("\nPelículas filtradas por género(s):")
    for pelicula in peliculas_filtradas_por_genero:
        print(pelicula.title)
else:
    print("No se encontraron películas para los géneros seleccionados.")









