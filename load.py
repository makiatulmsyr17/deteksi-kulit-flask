import tensorflow as tf

# Muat model lama
print("Mencoba memuat model .h5...")
model = tf.keras.models.load_model('./model/MobileNet_best.h5', compile=False)
print("Model .h5 berhasil dimuat.")

# Simpan dalam format baru
model.save('./model/MobileNet_best.keras')
print("Model berhasil disimpan dalam format .keras yang baru!")