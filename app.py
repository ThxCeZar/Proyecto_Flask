from flask import Flask, jsonify, render_template, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os # Importar 'os' para manejar variables de entorno de forma segura
from flask_cors import CORS


# --- Configuración de la aplicación Flask ---
app = Flask(__name__)
CORS(app)
# --- Configuración de MongoDB ---
# Es una buena práctica usar variables de entorno para las credenciales sensibles.
# Por ejemplo, puedes definir una variable de entorno llamada MONGODB_URI
# export MONGODB_URI="mongodb+srv://KimmyCesy:dLH5SqZntK53xu3z@clustercar.dd10bwo.mongodb.net/?retryWrites=true&w=majority&appName=ClusterCAR"
uri = os.getenv("MONGODB_URI", "mongodb+srv://KimmyCesy:dLH5SqZntK53xu3z@clustercar.dd10bwo.mongodb.net/?retryWrites=true&w=majority&appName=ClusterCAR")

# Conecta a MongoDB cuando la aplicación arranca, no en el main guard.
# Puedes usar la API de servidor para asegurar la compatibilidad futura.
client = MongoClient(uri, server_api=ServerApi('1'))

last_command = "none"
esp32_ip = "None"


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
    return render_template('index.html') 





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
    esp32_ip = data.get("ip")
    print(f"ESP32-CAM IP actualizada: {esp32_ip}")
    return "OK"





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