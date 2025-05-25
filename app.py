from flask import Flask, render_template, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os # Importar 'os' para manejar variables de entorno de forma segura

# --- Configuración de la aplicación Flask ---
app = Flask(__name__)

# --- Configuración de MongoDB ---
# Es una buena práctica usar variables de entorno para las credenciales sensibles.
# Por ejemplo, puedes definir una variable de entorno llamada MONGODB_URI
# export MONGODB_URI="mongodb+srv://KimmyCesy:dLH5SqZntK53xu3z@clustercar.dd10bwo.mongodb.net/?retryWrites=true&w=majority&appName=ClusterCAR"
uri = os.getenv("MONGODB_URI", "mongodb+srv://KimmyCesy:dLH5SqZntK53xu3z@clustercar.dd10bwo.mongodb.net/?retryWrites=true&w=majority&appName=ClusterCAR")

# Conecta a MongoDB cuando la aplicación arranca, no en el main guard.
# Puedes usar la API de servidor para asegurar la compatibilidad futura.
client = MongoClient(uri, server_api=ServerApi('1'))

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

@app.route('/')
def camera():
    return render_template('index.html') 
# --- Ejecución de la aplicación ---
if __name__ == '__main__':
    # Antes de iniciar la aplicación Flask, asegúrate de que la conexión a MongoDB esté probada.
    test_mongodb_connection()
    app.run(debug=True)