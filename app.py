from flask import Flask, render_template, request, redirect, url_for
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import io
import base64

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# --- MEMUAT MODEL .h5 DAN MENANGKAP ERROR DETAIL ---
MODEL_LOADING_ERROR = None
model = None

try:
    model = load_model('./model/MobileNet_best.h5')
    print("Model berhasil dimuat dari 'model_kulit.h5'")
    MODEL_INPUT_SHAPE = (128, 128)
except Exception as e:
    MODEL_LOADING_ERROR = f"Gagal memuat file 'model_kulit.h5'. Detail Error: {e}"
    print(f"PERINGATAN: {MODEL_LOADING_ERROR}")

# Definisikan label kelas sesuai urutan training model Anda
CLASS_NAMES = ['dark', 'light', 'mid-light']

def preprocess_image(image_file):
    img = Image.open(image_file.stream).convert('RGB')
    img = img.resize(MODEL_INPUT_SHAPE)
    img_array = np.array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def image_to_base64(image_file):
    image_file.seek(0)
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:image/jpeg;base64,{encoded_string}"

# Rute untuk halaman awal (landing page)
@app.route('/')
def landing():
    """Menampilkan halaman pembuka."""
    return render_template('landing.html')

# Rute untuk halaman prediksi
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Menangani logika upload gambar dan prediksi."""
    prediction_label = None
    error_message = None
    uploaded_image_b64 = None

    # Jika model gagal dimuat, langsung tampilkan error
    if MODEL_LOADING_ERROR:
        error_message = MODEL_LOADING_ERROR
        return render_template('index.html', error=error_message)

    if request.method == 'POST':
        if 'image_file' not in request.files or request.files['image_file'].filename == '':
            error_message = "Mohon pilih file gambar untuk diupload."
        else:
            image_file = request.files['image_file']
            try:
                uploaded_image_b64 = image_to_base64(image_file)
                processed_image = preprocess_image(image_file)
                prediction = model.predict(processed_image)
                predicted_class_index = np.argmax(prediction[0])
                prediction_label = CLASS_NAMES[predicted_class_index]
            except Exception as e:
                error_message = f"Terjadi error saat prediksi: {e}"

    return render_template('index.html', 
                           prediction=prediction_label, 
                           error=error_message,
                           uploaded_image=uploaded_image_b64)

# Jalankan aplikasi
if __name__ == '__main__':
    app.run(debug=True)