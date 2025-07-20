# Impor library yang diperlukan
from flask import Flask, render_template, request
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import io
import base64
import re # Diperlukan untuk memproses data dari kamera
import os

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# --- KONFIGURASI APLIKASI ---
MODEL_PATH = os.path.join('model', 'MobileNet_best.h5')
MODEL_INPUT_SHAPE = (128, 128)
CLASS_NAMES = ['dark', 'light', 'mid-light']

# --- MEMUAT MODEL ---
model = None
MODEL_LOADING_ERROR = None

try:
    # Menggunakan metode pemuatan yang Anda berikan, yang sepertinya bekerja untuk Anda
    model = load_model(
        MODEL_PATH,
        custom_objects={'InputLayer': tf.keras.layers.InputLayer},
        compile=False
    )
    print(f"Model berhasil dimuat dari '{MODEL_PATH}'")
except Exception as e:
    MODEL_LOADING_ERROR = f"Gagal memuat file model '{MODEL_PATH}'. Pastikan file ada di lokasi yang benar. Detail Error: {e}"
    print(f"PERINGATAN: {MODEL_LOADING_ERROR}")

# --- FUNGSI BANTU ---

def preprocess_image(image_data):
    """
    Mengubah data gambar (dalam bentuk bytes) menjadi format yang sesuai untuk input model.
    Fungsi ini sekarang bisa menangani data dari file upload maupun kamera.
    """
    # Menggunakan io.BytesIO untuk membaca data gambar dari memori
    img = Image.open(io.BytesIO(image_data)).convert('RGB')
    img = img.resize(MODEL_INPUT_SHAPE)
    img_array = np.array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# --- RUTE FLASK ---

@app.route('/')
def landing():
    """Menampilkan halaman pembuka (landing page)."""
    return render_template('landing.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """
    Menangani logika untuk upload gambar, jepretan kamera, dan prediksi.
    """
    prediction_label = None
    error_message = None
    uploaded_image_b64 = None

    if MODEL_LOADING_ERROR:
        return render_template('index.html', error=MODEL_LOADING_ERROR)

    if request.method == 'POST':
        image_data = None
        
        # Opsi 1: Cek apakah data berasal dari jepretan kamera
        camera_data_url = request.form.get('camera_data')
        if camera_data_url and camera_data_url != 'null':
            # Hapus header 'data:image/jpeg;base64,' dari string
            img_str = re.search(r'base64,(.*)', camera_data_url).group(1)
            image_data = base64.b64decode(img_str)
            uploaded_image_b64 = camera_data_url

        # Opsi 2: Jika tidak ada data kamera, cek dari upload file
        elif 'image_file' in request.files and request.files['image_file'].filename != '':
            image_file = request.files['image_file']
            image_data = image_file.read() # Baca data gambar sebagai bytes
            # Buat base64 untuk ditampilkan di frontend
            b64_str = base64.b64encode(image_data).decode('utf-8')
            uploaded_image_b64 = f"data:image/jpeg;base64,{b64_str}"
        
        # Jika ada data gambar (dari salah satu sumber), lakukan prediksi
        if image_data:
            try:
                processed_image = preprocess_image(image_data)
                prediction = model.predict(processed_image)
                predicted_class_index = np.argmax(prediction[0])
                prediction_label = CLASS_NAMES[predicted_class_index]
            except Exception as e:
                error_message = f"Terjadi kesalahan saat melakukan prediksi: {e}"
        else:
            # Jika tidak ada data gambar sama sekali, baru tampilkan error
            error_message = "Mohon pilih file gambar atau ambil gambar dari kamera."

    return render_template('index.html',
                           prediction=prediction_label,
                           error=error_message,
                           uploaded_image=uploaded_image_b64)

# --- JALANKAN APLIKASI ---
if __name__ == '__main__':
    app.run(debug=True)
