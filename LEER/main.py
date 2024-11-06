import cv2
from pyzbar.pyzbar import decode
from ast import literal_eval
import base_datos as db

MOSTRAR_CAMARA = True
LEER_IMAGEN = True
IMAGEN = cv2.imread('ejemplo-codigo.jpeg')

# Iniciar la camara
INDICE_CAMARA = 1
camara = cv2.VideoCapture(INDICE_CAMARA)

se_leyo = True
while camara.isOpened() and se_leyo:
    ret, frame = camara.read()
    
    if not ret:
        break

    if MOSTRAR_CAMARA:
        cv2.imshow('Frame', frame)

    # ENTRE LEER DESDE LA CAMARA O LEER DESDE IMAGEN
    if LEER_IMAGEN:
        h, w  = IMAGEN.shape[:2]
        qr_code = decode((IMAGEN[:, :, :1].tobytes(), w, h))[0]
    else:
        qr_code = decode(frame)[0]
    
    data: dict[str, str] = literal_eval(qr_code.data.decode('utf-8'))

    print(data)
    
    if (es_valido := data.get('QR_EXPO')) is not None and es_valido == "true":
        se_leyo = False
    
    if not se_leyo:
        break
    
    # Extraemos las coordenadas de la caja que encierra el QR
    (x, y, w, h) = qr_code.rect
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if cv2.waitKey(1) & 0xFF == 32:
        break

# Libera la cámara y cierra las ventanas
camara.release()
cv2.destroyAllWindows()
