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
listemp = []
from envi import  Config

# baseUrl = baseUrl

if device_count > 0:
    zkfp2.OpenDevice(0)
else:
    print("No se encontraron dispositivos")
    exit()

# Archivo JSON para almacenar las huellas
# DB_FILE = "fingerprints.json"


# def cargar_huellas():
#     if os.path.exists(DB_FILE):
#         with open(DB_FILE, 'r') as f:
#             return json.load(f)
#     return []
#
#
# # Función para guardar huellas en el archivo JSON
# def guardar_huellas():
#     with open(DB_FILE, 'w') as f:
#         json.dump(listemp, f)


# Cargar las huellas al iniciar



# Q
def registrar_huella():
    print("Coloca tu dedo en el escáner para registrar...")
    templates = []
    # base64_templates = ""
    # for i in range(1):
    #     while True:
    zkfp2.Light('green')

    time.sleep(0.09)
    for i in range(3):
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

    finger_id = int(input("Ingrese el ID de usuario para registrar: "))



    listemp.append({"id": finger_id, "temp": base64_templates})

    try:
        data = {
            "empleado": finger_id,
            "template": base64_templates
        }
        response = requests.post(Config.baseUrl, json=data)

        if response.status_code == 200:
            print(f"Huella dactilar registrada y enviada al servidor con ID = {finger_id}")
        else:
            print(f"Error al enviar la huella dactilar al servidor: {response.status_code}")

        print(f"Huella dactilar registrada con ID = {finger_id}")
    except Exception as e:
        print(f"Error al registrar la huella: {e}")


def cargar_huellas():
    # Enviar la solicitud HTTP GET para obtener las huellas dactilares del servidor
    # url = "http://tu-servidor.com/api/obtener_huellas"  # Reemplaza con tu URL
    response = requests.get(Config.baseUrl)

    if response.status_code == 200:
        listemp = response.json()
        return listemp
    else:
        print(f"Error al cargar las huellas dactilares del servidor: {response.status_code}")
        return []



def autenticar_usuario():

    cargar_huellas()


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

            for entry in listemp:
                temp = b64decode(entry["temp"])

                match = zkfp2.DBMatch(tmp, temp)
                if match:
                    print(f"Usuario identificado: ID = {entry['id']}")
                    zkfp2.show_image(img)

                    break

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
