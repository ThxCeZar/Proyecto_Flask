from io import BytesIO
from flask import Flask, abort, jsonify, render_template, request, send_file
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os # Importar 'os' para manejar variables de entorno de forma segura
from flask_cors import CORS


# --- Configuración de la aplicación Flask ---
app = Flask(__name__)
CORS(app)


#######

#######

#######

#######

uri = os.getenv("MONGODB_URI", "mongodb+srv://KimmyCesy:dLH5SqZntK53xu3z@clustercar.dd10bwo.mongodb.net/?retryWrites=true&w=majority&appName=ClusterCAR")
client = MongoClient(uri, server_api=ServerApi('1'))

#######

#######

#######

#######


last_command = "none"
esp32_ip = "none"



#######

#######

#######

#######


# --- Prueba de conexión a MongoDB ---
def test_mongodb_connection():
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(f"Error al conectar con MongoDB: {e}")
        # En una aplicación real, podrías querer manejar esto de forma más robusta,
        # como salir de la aplicación o reintentar.

# --- Rutas de la aplicación Flask ---
@app.route('/')
def home():
    # El método HEAD es manejado automáticamente por Flask para rutas GET.
    # Si una solicitud HEAD llega aquí, Flask simplemente enviará los encabezados
    # de la respuesta que normalmente se enviarían para una solicitud GET,
    # sin enviar el cuerpo de la plantilla. Esto es lo esperado.
    return render_template('PaginaInicioSes.html')

@app.route('/pagina2')
def camera():
    global esp32_ip
    return render_template("index.html", ip_camara=esp32_ip)





#####
#####
#####
#####
#####
#####






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


@app.route('/get_command', methods=['GET'])
def get_command():
    global last_command
    command_to_send = last_command # Envía el último comando establecido
    return jsonify({"action": command_to_send})


# Ruta para que el frontend (HTML con botones) envíe comandos a Flask
# Asume que tu HTML en Render.com enviará el comando a esta ruta
@app.route('/send_command', methods=['POST', 'GET']) # Puedes usar GET si es simple, pero POST es mejor
def send_command():
    global last_command
    command = request.args.get('command') # Si usas GET para enviar
    # O: command = request.json.get('command') # Si usas POST con JSON

    if command:
        last_command = command
        print(f"Comando '{command}' recibido de la web. Siguiente comando para ESP32: {last_command}")
        return jsonify({"status": "success", "command": command})
    return jsonify({"status": "error", "message": "No command provided"}), 400


@app.route('/actualizar_ip', methods=['POST'])
def actualizar_ip():
    global esp32_ip
    data = request.get_json()
    if not data or 'ip' not in data:
        return jsonify({"error": "Falta el campo 'ip'"}), 400

    esp32_ip = data['ip']
    print(f"[+] IP de cámara actualizada: {esp32_ip}")
    return jsonify({"status": "ok", "ip": esp32_ip}), 200

@app.route('/upload', methods=['POST'])
def recibir_imagen():
    global ultima_imagen
    ultima_imagen = BytesIO(request.data)
    return "Imagen recibida", 200

@app.route('/guardar_imagen', methods=['POST'])
def guardar_imagen():
    with open('ultima_imagen.jpg', 'wb') as f:
        f.write(request.data)
    return 'Imagen recibida', 200

@app.route('/ultima_imagen.jpg')
def servir_imagen():
    return send_file('ultima_imagen.jpg', mimetype='image/jpeg')







#####
#####
#####
#####
#####
#####
#####
#####
#####
#####











# --- Ejecución de la aplicación ---
if __name__ == '__main__':
    # Antes de iniciar la aplicación Flask, asegúrate de que la conexión a MongoDB esté probada.
    test_mongodb_connection()
    app.run(debug=True)