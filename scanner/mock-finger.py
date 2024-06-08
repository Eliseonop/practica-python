import json
import os
from pyzkfp import ZKFP2
from base64 import b64encode, b64decode
import requests
import time


# Inicialización del dispositivo
zkfp2 = ZKFP2()
zkfp2.Init()
device_count = zkfp2.GetDeviceCount()
listemp: list = []

if device_count > 0:
    zkfp2.OpenDevice(0)
else:
    print("No se encontraron dispositivos")
    exit()

# Archivo JSON para almacenar las huellas
DB_FILE = "fingerprints.json"


def cargar_huellas():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return []


# Función para guardar huellas en el archivo JSON
def guardar_huellas():
    with open(DB_FILE, 'w') as f:
        json.dump(listemp, f)


# Cargar las huellas al iniciar
listemp = cargar_huellas()


# Q
def registrar_huella():
    print("Coloca tu dedo en el escáner para registrar...")
    templates = []
    # base64_templates = ""
    for i in range(1):
        while True:
            capture = zkfp2.AcquireFingerprint()
            if capture:
                print('Huella dactilar capturada')
                # with open('fingerprint', 'w') as f:
                #     f.write(b64encode(bytes(capture[0])).decode())
                tmp, img = capture
                # zkfp2.show_image(img)

                templates.append(tmp)
                break

    base64_templates = b64encode(bytes(templates[0])).decode()
    print(templates)
    # regTemp, regTempLen = zkfp2.DBMerge(*templates)
    # print(regTemp)
    # print(type(regTemp))
    finger_id = int(input("Ingrese el ID de usuario para registrar: "))

    # Guardar en la lista con la estructura {id: <id dado>, temp: <temp dado>}
    # mytemp = zkfp2.ByteArray2Int(regTemp)

    listemp.append({"id": finger_id, "temp": base64_templates})

    if finger_id != 1:
        for _ in range(1000):
            # temp = zkfp2.ByteArray2Int(regTemp)
            # print(temp)
            listemp.append({"id": finger_id, "temp": base64_templates})

    # zkfp2.DBAdd(finger_id, mytemp)
    guardar_huellas()

    print(f"Huella dactilar registrada con ID = {finger_id}")


def autenticar_usuario():
    print(f"Cantidad de elementos para iterar: {len(listemp)}")

    print("Coloca tu dedo en el escáner para autenticación...")
    # for member in listemp:
    #     print(member["temp"])
    #     convert = b64decode(member["temp"])
    #     id = member["id"]
    #     zkfp2.DBAdd(id, convert)

    while True:
        capture = zkfp2.AcquireFingerprint()
        if capture:
            tmp, img = capture
            print("Huella dactilar capturada para autenticación")
            start_time = time.time()

            # for member in listemp:    duracion mas larga 3.7 el indice 5000 y cuando no hay  5.6
            # for index, entry in enumerate(listemp):
            #     temp = b64decode(entry["temp"])
            #
            #     match = zkfp2.DBMatch(tmp, temp)
            #     if match:
            #         print(f"Usuario identificado: ID = {entry['id']} con indice = {index}  , Score = {match}")
            #         break

            decoded_temps = [b64decode(entry["temp"]) for entry in listemp]

            # Realizar la comparación con zkfp2.DBMatch
            for temp, entry in zip(decoded_temps, listemp):
                match = zkfp2.DBMatch(tmp, temp)
                if match:
                    print(f"Usuario identificado: ID = {entry['id']}")
                    break


            end_time = time.time()

            elapsed_time = end_time - start_time
            print(f"Tiempo transcurrido: {elapsed_time} segundos")
            # zkfp2.show_image(img)
            # fid, score = zkfp2.DBIdentify(tmp)
            # if score > 0:
            #
            #     print(f"Usuario identificado: ID = {fid}, Score = {score}")
            #     break  # Usuario identificado, salir del bucle
            # else:
            #     print("Usuario no identificado. Huella no coincide con ningún registro.")

            # retry = input("¿Deseas intentar de nuevo? (s/n): ")
            # if retry.lower() != 's':
            #     print("Autenticación cancelada.")
            #     break  # Salir del bucle si el usuario no quiere intentar de nuevo


def mostrar_menu():
    print("\nMenu:")
    print("1. Registrar usuario")
    print("2. Autenticar usuario")
    print("3. Salir")
    opcion = input("Seleccione una opción: ")
    return opcion


while True:
    opcion = mostrar_menu()
    if opcion == '1':
        registrar_huella()
    elif opcion == '2':
        autenticar_usuario()
    elif opcion == '3':
        print("Saliendo...")
        break
    else:
        print("Opción no válida. Por favor, intente de nuevo.")

zkfp2.Terminate()
