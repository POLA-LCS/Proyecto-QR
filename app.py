from flask import Flask, render_template, request, redirect, url_for
import qrcode
import uuid

app = Flask(__name__)

"""
Para crear un codigo QR con los datos que le pases en forma de diccionario
Tiene el formato:
['clave:va_lor', 'otraclave:otro_valor', ...]

Ej:
[nombre:Baltazar_Zara, apellido:Pilling, curso:6, división:5]
"""
def crear_qr(formulario: dict, id_unico: str):
    qr_data = {**formulario, "QR_EXPO": "true", "id": id_unico}
    informacion = [f'{key}:{'_'.join(value.split(' '))}' for key, value in qr_data.items()]
    
    qr = qrcode.QRCode(
        version=10,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    for info in informacion:
        qr.add_data(info)

    print(informacion)
    
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white')
    img.save(f"static/codigo-qr.jpg")
    
    return f"static/codigo-qr.jpg"

# FLAAAAAASK!!!
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        id_unico = str(uuid.uuid4())  # Genera un ID único
        url_qr = crear_qr(request.form, id_unico)
        return redirect(url_for('mostrar_qr', qr_url=url_qr))
    return render_template('index.html', mensaje='Completa el formulario para obtener el código QR.')

@app.route('/qr')
def mostrar_qr():
    qr_url = request.args.get('qr_url')
    return render_template('mostrar_qr.html', url_qr=qr_url)

if __name__ == '__main__':
    app.run(debug=True)