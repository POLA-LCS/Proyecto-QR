import cv2
from pyzbar.pyzbar import decode

MOSTRAR_CAMARA = True

# Iniciar la camara (probar diferentes indices)
INDICE_CAMARA = 1
camara = cv2.VideoCapture(INDICE_CAMARA)

se_leyo = True
while camara.isOpened() and se_leyo:
    ret, frame = camara.read()
    
    if not ret:
        break

    if MOSTRAR_CAMARA:
        cv2.imshow('Frame', frame)

    qr_codes = decode(frame)
    
    for qr in qr_codes:
        print(qr.data)
        
        se_leyo = False
        
        if not se_leyo:
            break
        
        # Extremos las coordenadas de la caja que encierra el QR
        (x, y, w, h) = qr.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Convierte los datos del QR a texto
        qr_data = qr.data.decode('utf-8')
        qr_type = qr.type
        
        # Muestra el contenido del QR y su tipo
        text = f"Data: {qr_data} | Type: {qr_type}"
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
        print(f"QR Code detected: {qr_data}")

    if cv2.waitKey(1) & 0xFF == 32:
        break

# Libera la cámara y cierra las ventanas
camara.release()
cv2.destroyAllWindows()
