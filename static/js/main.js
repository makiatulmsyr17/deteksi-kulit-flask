document.addEventListener('DOMContentLoaded', () => {
    // Elemen-elemen UI
    const form = document.getElementById('upload-form');
    const imageInput = document.getElementById('image_file');
    const cameraDataInput = document.getElementById('camera-data');
    const submitButton = document.getElementById('submit-button');
    const buttonText = document.getElementById('button-text');
    const loader = document.getElementById('loader');
    const resultContainer = document.getElementById('result-content');
    
    // Elemen-elemen Tab
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabPanels = document.querySelectorAll('.tab-panel');

    // Elemen-elemen Kamera
    const startCameraButton = document.getElementById('start-camera-btn');
    const captureButton = document.getElementById('capture-btn');
    const videoFeed = document.getElementById('camera-feed');
    const canvas = document.getElementById('capture-canvas');
    const cameraPlaceholder = document.getElementById('camera-placeholder');
    let stream = null;

    // Fungsi untuk mengaktifkan tombol submit
    const enableSubmit = () => {
        submitButton.disabled = false;
    };

    // Logika Tab
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            tabButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            tabPanels.forEach(panel => {
                panel.classList.toggle('active', panel.id === `tab-${button.dataset.tab}`);
            });
            // Hentikan kamera jika pindah dari tab kamera
            if (button.dataset.tab !== 'camera' && stream) {
                stream.getTracks().forEach(track => track.stop());
                videoFeed.classList.add('hidden');
                cameraPlaceholder.classList.remove('hidden');
                startCameraButton.classList.remove('hidden');
                captureButton.classList.add('hidden');
                stream = null;
            }
        });
    });

    // Logika Upload File
    imageInput.addEventListener('change', function() {
        if (this.files[0]) {
            const reader = new FileReader();
            reader.onload = (e) => {
                resultContainer.innerHTML = `<img src="${e.target.result}" alt="Pratinjau" class="h-40 w-40 object-cover rounded-lg mx-auto shadow-md">`;
            };
            reader.readAsDataURL(this.files[0]);
            cameraDataInput.value = null; // Kosongkan data kamera jika ada
            enableSubmit();
        }
    });

    // Logika Kamera
    startCameraButton.addEventListener('click', async () => {
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            try {
                stream = await navigator.mediaDevices.getUserMedia({ video: { width: 1280, height: 720 } });
                videoFeed.srcObject = stream;
                videoFeed.classList.remove('hidden');
                cameraPlaceholder.classList.add('hidden');
                startCameraButton.classList.add('hidden');
                captureButton.classList.remove('hidden');
            } catch (err) {
                cameraPlaceholder.textContent = "Gagal mengakses kamera. Mohon izinkan akses.";
                console.error("Error accessing camera: ", err);
            }
        }
    });

    captureButton.addEventListener('click', () => {
        if (stream) {
            canvas.width = videoFeed.videoWidth;
            canvas.height = videoFeed.videoHeight;
            const context = canvas.getContext('2d');
            // Balikkan gambar secara horizontal saat menggambar ke canvas
            context.translate(canvas.width, 0);
            context.scale(-1, 1);
            context.drawImage(videoFeed, 0, 0, canvas.width, canvas.height);
            const dataUrl = canvas.toDataURL('image/jpeg');
            cameraDataInput.value = dataUrl;
            resultContainer.innerHTML = `<img src="${dataUrl}" alt="Gambar Jepretan" class="h-40 w-40 object-cover rounded-lg mx-auto shadow-md" style="transform: scaleX(-1);">`;
            imageInput.value = null; // Kosongkan input file jika ada
            enableSubmit();
            // Ubah teks tombol untuk menandakan gambar sudah diambil
            captureButton.textContent = "Ambil Ulang";
            captureButton.classList.replace('bg-indigo-600', 'bg-green-600');
        }
    });

    // Logika Form Submission
    form.addEventListener('submit', function() {
        buttonText.textContent = 'Memproses...';
        loader.classList.remove('hidden');
        submitButton.disabled = true;
    });
});
