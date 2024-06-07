from pyzkfp import ZKFP2
from PIL import Image

zkfp2 = ZKFP2()
zkfp2.Init()
device_count = zkfp2.GetDeviceCount()
print(f"{device_count} dispositivos encontrados")
if device_count > 0:
    zkfp2.OpenDevice(0)


    print("Coloca tu dedo en el escáner para autenticación...")
    while True:
        capture = zkfp2.AcquireFingerprint()
        if capture:
            tmp, img = capture
            print("Huella dactilar capturada para autenticación")


            fingerprint_id, score = zkfp2.DBIdentify(tmp)
            if fingerprint_id != -1:
                print(f"Usuario identificado: ID = {fingerprint_id}, Score = {score}")
            else:
                print("Usuario no identificado. Huella no coincide con ningún registro.")
            break

    # Terminar el dispositivo y liberar recursos
    zkfp2.Terminate()
else:
    print("No se encontraron dispositivos")
