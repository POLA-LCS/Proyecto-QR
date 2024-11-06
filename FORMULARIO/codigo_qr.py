from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_L
from json import dumps

def crear_qr(datos_formulario: dict[str, str], id_unico: str):
    # Creamos el codigo QR con el formato mas legible que encontré
    QR = QRCode(
        version=10,
        error_correction=ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Convertimos datos_formulario a un json y lo añadimos al QR
    datos_json = dumps(
        {"ID": id_unico, **{
            key.upper(): '_'.join(value.lower().split(' ')) for key, value in datos_formulario.items()
        }, "QR_EXPO": "true"}
    )
    
    QR.add_data(datos_json)
    QR.make(fit=True)

    print(datos_json)
    
    # Imagen que va a usarse para mostrar en "templates/mostrar_qr.html"
    imagen_local = QR.make_image(fill='black', back_color='white')
    
    return imagen_local