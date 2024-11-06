from flask import Flask, render_template, request, redirect, url_for
import uuid
from codigo_qr import *

app = Flask(__name__)

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