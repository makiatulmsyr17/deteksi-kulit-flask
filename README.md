
# SkinTone AI: Aplikasi Web Deteksi Warna Kulit

**SkinTone AI** adalah aplikasi web berbasis Deep Learning yang mampu mendeteksi dan mengklasifikasikan warna kulit wajah manusia (misalnya: dark, light, mid-light) secara real-time. Aplikasi ini dapat digunakan dengan mengunggah gambar atau melalui kamera langsung pada perangkat.



## 🎯 Fitur Utama

- **Landing Page Profesional**: Halaman pembuka yang informatif dan menarik.
- **Dua Metode Input**:
  - **Unggah File**: Mendukung gambar berformat PNG, JPG, atau JPEG.
  - **Kamera Langsung**: Mengambil gambar secara langsung dari kamera perangkat.
- **Prediksi Real-time**: Hasil klasifikasi ditampilkan langsung setelah input gambar.
- **Antarmuka Responsif**: Optimal untuk desktop maupun mobile.
- **Tombol Reset**: Memungkinkan pengguna melakukan analisis ulang dengan mudah.



## 🛠️ Teknologi yang Digunakan

### Backend:
- **Python**
- **Flask**
- **TensorFlow / Keras**
- **Pillow (PIL)**
- **NumPy**

### Frontend:
- **HTML5**
- **Tailwind CSS**
- **CSS3 Kustom**
- **JavaScript**

### Model AI:
- **CNN (Convolutional Neural Network)**
- **Base Model**: MobileNetV2
- **Teknik**: Transfer Learning

---

## 🚀 Cara Instalasi & Menjalankan Aplikasi (Local)

### 1. Clone Repository
```bash
git clone https://github.com/username/nama-repository.git
cd nama-repository
````

### 2. Buat dan Aktifkan Virtual Environment

#### Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Jalankan Aplikasi

Pastikan file model (`model_kulit_baru.h5`) berada di folder proyek.

```bash
python app.py
```

Buka browser dan akses: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📁 Struktur Direktori

```
aplikasi_model_flask/
├── app.py                  # Logika utama aplikasi Flask
├── model
|    └── MobileNet_best.h5  # Model AI yang telah dilatih
├── requirements.txt        # Daftar dependencies Python
├── static/
│   ├── css/
│   │   └── style.css       # File CSS kustom
│   └── js/
│       └── main.js         # Interaktivitas kamera & preview
└── templates/
    ├── landing.html        # Halaman landing
    └── index.html          # Halaman prediksi
```

---

## 📌 Catatan

* Pastikan kamera perangkat telah diizinkan akses oleh browser.
* Model MobileNetV2 telah di-*fine-tuned* untuk klasifikasi warna kulit.
* Jika ada error saat membaca kamera, silakan cek browser permission.

---

## 👩‍💻 Kontributor

* **Nama**: Makiatul Musyaropah
* **Email**: [makiatulmusyaropah@gmail.com](mailto:makiatulmusyaropah@gmail.com)
* **LinkedIn**: [linkedin.com/in/makiatulmusyaropah](https://linkedin.com/in/makiatulmusyaropah)

---

## 📄 Lisensi

Proyek ini hanya untuk keperluan edukasi (skripsi). Silakan hubungi pengembang untuk penggunaan lebih lanjut.

```

Jika kamu ingin aku bantu menyesuaikan bagian tertentu (misalnya GitHub repo asli, nama domain jika online, atau ingin tambahkan badge seperti license, stars, dll.), tinggal beri tahu saja!
```
