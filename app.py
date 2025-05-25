from flask import Flask, jsonify, request, send_file, render_template
from flask_cors import CORS
import os
from datetime import datetime
import glob
from PIL import Image
import io



app = Flask(__name__)
CORS(app)

last_command = "none"
last_image = None

@app.route('/action', methods=['GET'])
def action():
    global last_command
    command = request.args.get('go')
    if command:
        last_command = command
        print(f"Comando recibido: {command}")
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

@app.route('/upload_image', methods=['POST'])
def upload_image():
    global last_image
    if not request.data:
        return jsonify({'error': 'No image data'}), 400
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    image_path = f'static/uploads/image_{timestamp}.jpg'
    os.makedirs('static/uploads', exist_ok=True)
    
    # Comprimir imagen
    img = Image.open(io.BytesIO(request.data))
    img = img.convert('RGB')
    img.save(image_path, 'JPEG', quality=70) # Reducir calidad a 70
    
    last_image = image_path
    
    images = sorted(glob.glob('static/uploads/image_*.jpg'))
    if len(images) > 5:
        for old_image in images[:-5]:
            os.remove(old_image)
    
    return jsonify({'message': 'Image received successfully'}), 200



@app.route('/ultima_imagen.jpg')
def ultima_imagen():
    global last_image
    if not last_image or not os.path.exists(last_image):
        return jsonify({'error': 'No image available'}), 404
    return send_file(last_image, mimetype='image/jpeg')

@app.route('/')
def home():
    return render_template('PaginaInicioSes.html')

@app.route('/pagina2')
def camera():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)