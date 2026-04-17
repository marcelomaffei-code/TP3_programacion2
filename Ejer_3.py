def encode(texto):
    resultado = []
    i = 0
    while i < len(texto):
        resultado.append(ord(texto[i]))
        i += 1
    return resultado

def decode(lista):
    resultado = ""
    i = 0
    while i < len(lista):
        resultado = resultado + chr(lista[i])
        i += 1
    return resultado


if __name__ == "__main__":
    texto = input("Ingrese un texto a codificar: ")

    codificado = encode(texto)
    print("Codificado: ", codificado)

    decodificado = decode(codificado)
    print("Decodificado: ", decodificado)
