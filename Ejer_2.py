if __name__ == "__main__":

    texto = input("Ingrese una texto: ")

    lista = []
    longitud = 0

    for c in texto:
        longitud += 1

    i = longitud - 1
    while i >= 0:
        lista.append(texto[i])
        i -= 1

    print("{")
    print("items :", lista)
    print("length:", longitud)
    print("}")