from flask import Flask, render_template, request, send_from_directory, jsonify
from PIL import Image, ImageDraw
import os

app = Flask(__name__)

# Ruta para servir los archivos estáticos (imágenes) desde la carpeta 'uploads'
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Configurar la carpeta de carga (uploads)
app.config['UPLOAD_FOLDER'] = 'uploads'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def generate_collage():
    # Obtener datos del formulario
    images = []
    for i in range(1, 7):
        image = request.files.get(f'image{i}')
        width = int(request.form[f'width{i}'])
        height = int(request.form[f'height{i}'])
        emotion = request.form[f'emotion{i}']
        if image:
            images.append((image, width, height, emotion))

    # Procesar las imágenes y generar el collage
    collage_images = []
    for image, width, height, emotion in images:
        # Procesar la imagen y redimensionarla según el ancho y alto especificados
        img = Image.open(image)
        img = img.resize((width, height))

        # Dibujar la emoción en la imagen (esto es solo un ejemplo, puedes personalizarlo según tus necesidades)
        draw = ImageDraw.Draw(img)
        draw.text((100, 100), emotion, fill='red')  # Dibuja la emoción en la esquina superior izquierda

        collage_images.append(img)

    # Crear el collage combinando todas las imágenes
    collage_width = max(img.width for img in collage_images)
    collage_height = sum(img.height for img in collage_images)
    collage = Image.new('RGB', (collage_width, collage_height), (255, 255, 255))
    y_offset = 0
    for img in collage_images:
        collage.paste(img, (0, y_offset))
        y_offset += img.height

    # Guardar el collage en la carpeta de carga
    collage_path = os.path.join(app.config['UPLOAD_FOLDER'], 'collage.jpg')
    collage.save(collage_path)

    # Devolver el nombre del archivo del collage como respuesta al cliente
    return jsonify({'collage_filename': 'collage.jpg'})

if __name__ == '__main__':
    app.run(debug=True)
