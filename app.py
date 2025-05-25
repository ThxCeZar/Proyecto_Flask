from io import BytesIO
from flask import Flask, jsonify, request, send_file, abort, render_template
from flask_cors import CORS
import os
import logging

app = Flask(__name__)
CORS(app)


last_command = "none"
# Si no vas a usar IP ni proxy, eliminas esp32_ip




@app.route('/action', methods=['GET'])
def action():
    global last_command
    command = request.args.get('go')  # Obtiene el comando de la consulta
    if command:
        last_command = command  # Actualiza el último comando
        print(f"Comando recibido: {command}")
        
        # Reiniciar last_command a "none" si el comando es "stop"
        if command == "stop":
            last_command = "none"
        
        return jsonify({"status": "success", "command": command})
    return jsonify({"status": "error", "message": "No command provided"}), 400


@app.route('/send_command', methods=['POST', 'GET'])
def send_command():
    global last_command
    data = request.get_json()
    command = data.get('command') if data else None

    if command:
        last_command = command
        print(f"Comando '{command}' recibido de la web.")
        return jsonify({"status": "success", "command": command})
    return jsonify({"status": "error", "message": "No command provided"}), 400

@app.route('/get_command', methods=['GET'])
def get_command():
    global last_command
    return jsonify({"action": last_command})







@app.route('/upload', methods=['POST'])
def recibir_imagen():
    # Guardamos la imagen en disco para persistencia simple
    with open('/tmp/ultima_imagen.jpg', 'wb') as f:
        f.write(request.data)
    return jsonify({"status": "ok", "message": "Imagen recibida"}), 200

@app.route('/ultima_imagen.jpg')
def servir_imagen():
    imagen_path = '/tmp/ultima_imagen.jpg'
    if os.path.exists(imagen_path):
        return send_file(imagen_path, mimetype='image/jpeg')
    else:
        return abort(404, description="Imagen no encontrada")














@app.route('/')
def home():
    return render_template('PaginaInicioSes.html')

@app.route('/pagina2')
def camera():
    # No se necesita pasar IP si no haces proxy
    return render_template("index.html")









def test_mongodb_connection():
    # Si no usas MongoDB aún, puedes comentar o dejar solo para pruebas
    pass








if __name__ == '__main__':
    test_mongodb_connection()
    app.run(debug=True)