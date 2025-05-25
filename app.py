from flask import Flask, request, send_file
import os
from PIL import Image
import io
from threading import Lock

app = Flask(__name__)
UPLOAD_FOLDER = 'temp_images'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

latest_image_path = os.path.join(UPLOAD_FOLDER, 'latest.jpg') # Seguimos guardando como JPG
image_lock = Lock()

# Función para convertir RGB565 a JPEG
def convert_rgb565_to_jpeg(rgb565_data, width, height, quality=80):
    # Crear una imagen Pillow desde los bytes RGB565
    # PIL (Pillow) espera el formato 'RGB' (8 bits por canal)
    # Por lo que necesitamos desempaquetar el RGB565
    # Esto es un poco más complejo y puede requerir una librería C para eficiencia
    # O un bucle lento en Python para cada píxel si no es crítico el rendimiento.
    # Para simplicidad y prueba, asumimos una librería como 'pysdcam' o conversión manual
    # Para una implementación real, buscarías librerías que manejen raw RGB565.

    # Simulación de conversión:
    # En un escenario real, harías algo como:
    # from your_custom_lib import rgb565_to_rgb888
    # rgb888_data = rgb565_to_rgb888(rgb565_data)
    # img = Image.frombytes('RGB', (width, height), rgb888_data)

    # **Simplificación IMPORTANTE para el ejemplo:**
    # Asumimos que la data viene de ESP32 en un formato que Pillow puede entender,
    # o que la conversión se hará fuera de Flask.
    # Si la ESP32 envía *raw* RGB565, necesitarías un conversor.
    # Para este ejemplo, simularé que recibimos datos válidos para un Image.frombytes.
    # ¡CUIDADO! Esto es un placeholder.
    # El tamaño de `rgb565_data` debería ser `width * height * 2`.
    # Pillow no tiene un modo directo para 'RGB565'.
    # La mejor forma sería desempaquetar cada pixel de 16 bits en 3 bytes (RGB888)
    # Ejemplo con un conversor manual (puede ser lento para alta frecuencia):
    rgb888_bytes = bytearray(width * height * 3)
    for i in range(0, len(rgb565_data), 2):
        pixel_565 = int.from_bytes(rgb565_data[i:i+2], 'little') # O 'big' según el endianness de ESP32
        r = (pixel_565 >> 11) & 0x1F
        g = (pixel_565 >> 5) & 0x3F
        b = pixel_565 & 0x1F

        # Escalar de 5/6 bits a 8 bits
        r_8bit = (r * 255) // 31
        g_8bit = (g * 255) // 63
        b_8bit = (b * 255) // 31

        idx_888 = (i // 2) * 3
        rgb888_bytes[idx_888] = r_8bit
        rgb888_bytes[idx_888 + 1] = g_8bit
        rgb888_bytes[idx_888 + 2] = b_8bit
    
    img = Image.frombytes('RGB', (width, height), bytes(rgb888_bytes))


    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG', quality=quality)
    img_byte_arr.seek(0)
    return img_byte_arr

@app.route('/upload_image', methods=['POST'])
def upload_image():
    # Asumimos que el ESP32 envía el ancho y alto en los headers o como parte de los datos
    # Para este ejemplo, los hardcodeamos o los pasamos en headers si la ESP32 los envía.
    # ESP32-CAM con OV2640 en QVGA es 320x240
    img_width = 320
    img_height = 240

    if request.data:
        rgb565_bytes = request.data
        if len(rgb565_bytes) != img_width * img_height * 2: # 2 bytes por píxel para RGB565
            return 'Invalid image data size for RGB565', 400

        try:
            # Convertir RGB565 a JPEG
            jpeg_buffer = convert_rgb565_to_jpeg(rgb565_bytes, img_width, img_height)

            with image_lock:
                with open(latest_image_path, 'wb') as f:
                    f.write(jpeg_buffer.read())
            return 'Image uploaded and converted to JPEG', 200
        except Exception as e:
            return f'Error converting image: {e}', 500
    else:
        return 'No image data received', 400

@app.route('/latest_image')
def get_latest_image():
    with image_lock:
        if os.path.exists(latest_image_path):
            return send_file(latest_image_path, mimetype='image/jpeg')
        else:
            return 'No image available', 404

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=os.environ.get('PORT', 5000))