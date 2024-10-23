from flask import Flask, render_template, request, redirect, url_for
from qrcode import QRCode
from qrcode.constants import ERROR_CORRECT_L
import uuid
from json import dumps

app = Flask(__name__)

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
        {**{
            key.upper(): '_'.join(value.lower().split(' ')) for key, value in datos_formulario.items()
        }, "QR_EXPO": "true", "ID": id_unico}
    )
    
    QR.add_data(datos_json)
    QR.make(fit=True)

    print(datos_json)
    
    # Imagen que va a usarse para mostrar en "templates/mostrar_qr.html"
    imagen_local = QR.make_image(fill='black', back_color='white')
    
    return imagen_local

# FLAAAAAASK!!!
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST': # Verificamos si se envió el formulario
        imagen_qr = crear_qr(    # Creamos el QR con:
            request.form,        # Los datos del formulario
            str(uuid.uuid4())    # Un ID
        )
        directorio_qr = 'static/codigo-qr.jpg'
        imagen_qr.save(directorio_qr)        
        return redirect(url_for('mostrar_qr', directorio_qr=directorio_qr))
    return render_template('index.html', mensaje='Completa el formulario para obtener el código QR.')

@app.route('/qr')
def mostrar_qr():
    directorio_qr = request.args.get('directorio_qr')
    return render_template('mostrar_qr.html', qr_src=directorio_qr)

if __name__ == '__main__':
    app.run(debug=True)