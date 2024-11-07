import cv2
from pyzbar.pyzbar import decode
from ast import literal_eval
import base_datos as db

LEER_IMAGEN = False
IMAGEN = cv2.imread('ejemplo-codigo.jpeg')
print(IMAGEN)

# Iniciar la cámara
INDICE_CAMARA = 1
camara = cv2.VideoCapture(INDICE_CAMARA)

while camara.isOpened():
    sucess, frame = camara.read()
    
    if not sucess:
        continue

    # ENTRE LEER DESDE LA CÁMARA O LEER DESDE IMAGEN
    decoded_frame = decode(frame if not LEER_IMAGEN else (IMAGEN[:, :, :1].tobytes(), *IMAGEN.shape[:2]))

    if len(decoded_frame) > 0:
        qr_code = decoded_frame[0]

        data: dict[str, str] = literal_eval(qr_code.data.decode('utf-8'))

        print(data)
        
        if (es_valido := data.get('QR_EXPO')) is not None and es_valido == "true":
            (x, y, w, h) = qr_code.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if cv2.waitKey(1) & 0xFF == 32:
        break

    cv2.imshow('Frame', frame)
    
camara.release()
cv2.destroyAllWindows()
