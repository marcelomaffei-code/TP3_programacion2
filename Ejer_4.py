import csv
import os

def normalizar_texto(valor):
    if valor is None:
        return ""
    return str(valor).strip()

def normalizar_reserve(valor):
    texto = normalizar_texto(valor).replace(",", ".")
    try:
        return float(texto)
    except ValueError:
        return 0.0

def obtener_archivos_csv(directorio):
    archivos = []

    for nombre in os.listdir(directorio):
        es_csv = nombre.lower().endswith(".csv")
        no_es_salida = nombre.upper() != "BANK_DATA_ORD.CSV"
        if es_csv and no_es_salida:
            ruta = os.path.join(directorio, nombre)
            archivos.append(ruta)
    return archivos

def leer_y_procesar_archivos(lista_archivos):
    registros_vistos = set()
    acumulados = {}
    for archivo_nombre in lista_archivos:
        try:
            with open(archivo_nombre, mode="r", encoding="utf-8-sig", newline="") as archivo:
                lector = csv.DictReader(archivo)

                for fila in lector:
                    city_bank = normalizar_texto(fila.get("city_bank"))
                    name = normalizar_texto(fila.get("name"))
                    routing_bank = normalizar_texto(fila.get("routing_bank"))
                    reserve = normalizar_reserve(fila.get("reserve"))
                    code_country = normalizar_texto(fila.get("code_country"))

                    clave_unica = (city_bank, name, routing_bank, reserve, code_country)

                    if clave_unica not in registros_vistos:
                        registros_vistos.add(clave_unica)

                        clave = (name, code_country)

                        if clave not in acumulados:
                            acumulados[clave] = {
                                "name": name,
                                "total_reserve": 0.0,
                                "total_cant": 0,
                                "code_country": code_country
                            }

                        acumulados[clave]["total_reserve"] += reserve
                        acumulados[clave]["total_cant"] += 1
        except Exception as e:
            print(f"Error leyendo {archivo_nombre}: {e}")
    return acumulados


def generar_archivo_ordenado(acumulados, archivo_salida):
    registros_ordenados = sorted(
        acumulados.values(),
        key=lambda x: x["name"].lower()
    )
    with open(archivo_salida, mode="w", encoding="utf-8", newline="") as archivo:
        campos = ["name", "total_reserve", "total_cant", "code_country"]
        writer = csv.DictWriter(archivo, fieldnames=campos)
        writer.writeheader()
        for registro in registros_ordenados:
            writer.writerow({
                "name": registro["name"],
                "total_reserve": f"{registro['total_reserve']:.2f}",
                "total_cant": registro["total_cant"],
                "code_country": registro["code_country"]
            })
    print("Archivo generado:", archivo_salida)

def cargar_archivo_final(archivo):
    datos = []
    try:
        with open(archivo, mode="r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for fila in reader:
                datos.append(fila)
    except Exception as e:
        print("No se pudo leer el archivo final:", e)
    return datos

def buscar_registros(registros, campo, valor):
    resultados = []
    for registro in registros:
        dato = registro.get(campo, "")
        if dato.strip().lower() == valor.strip().lower():
            resultados.append(registro)
    return resultados

def mostrar_resultados(resultados):
    if len(resultados) == 0:
        print("No se encontraron registros.")
    else:
        print("\nResultados encontrados:")
        for registro in resultados:
            print(
                "name:", registro["name"],
                "| total_reserve:", registro["total_reserve"],
                "| total_cant:", registro["total_cant"],
                "| code_country:", registro["code_country"]
            )

def menu_busqueda(archivo_salida):
    registros = cargar_archivo_final(archivo_salida)

    if len(registros) > 0:
        salir = False
        while salir == False:
            print("\n--- BUSQUEDA ---")
            print("1. Buscar por name")
            print("2. Buscar por code_country")
            print("3. Salir")
            opcion = input("Opcion: ").strip()

            if opcion == "1":
                valor = input("Ingrese name: ")
                resultados = buscar_registros(registros, "name", valor)
                mostrar_resultados(resultados)
            elif opcion == "2":
                valor = input("Ingrese code_country: ")
                resultados = buscar_registros(registros, "code_country", valor)
                mostrar_resultados(resultados)
            elif opcion == "3":
                print("Fin.")
                salir = True
            else:
                print("Opcion invalida.")

def main():
    directorio = os.path.dirname(os.path.abspath(__file__))
    archivo_salida = os.path.join(directorio, "BANK_DATA_ORD.csv")
    print("Buscando archivos en:", directorio)
    archivos = obtener_archivos_csv(directorio)

    if len(archivos) == 0:
        print("No hay archivos CSV en el directorio.")
    else:
        print("\nArchivos encontrados:")
        for archivo in archivos:
            print("-", archivo)

        acumulados = leer_y_procesar_archivos(archivos)
        generar_archivo_ordenado(acumulados, archivo_salida)
        menu_busqueda(archivo_salida)

if __name__ == "__main__":
    main()