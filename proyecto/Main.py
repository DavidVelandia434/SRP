print("SPR")
generos=[
        "acción",
        "Aventura",
        "Animacion",
        "Biografia",
        "Comedia",
        "Crimen",
        "Documenta",
        "Drama",
        "Familiar",
        "Fantasia",
        "Cine-negro",
        "Concurso",
        "Historia",
        "Terror",
        "Musica",
        "Musical",
        "Misterio",
        "Noticias",
        "Reality",
        "Romance",
        "Ciencia-ficcion",
        "Corto",
        "Deporte",
        "Tertulia",
        "Suspense",
        "Belico",
        "Del-oeste"]


print("----MENU GENERO-----")
for i in range(len(generos)):
    print(f"{i+1}.{generos[i]}")
          
opcion=int(input("seleccione genero"))         
        
if 1<=opcion<=len(generos):
    print("elegiste",generos[opcion-1])
else:
    print("inavido.intente de nuevo")    

  







