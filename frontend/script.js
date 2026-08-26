async function startScanner() {
  const video = document.getElementById('camera-feed');
  const canvas = document.getElementById('guide-overlay');
  const ctx = canvas.getContext('2d');
  const container = document.getElementById('scanner-container');

  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    showError(
      container,
      "Browser atau koneksi (HTTP) tidak mendukung akses kamera.<br><br>" +
      "Gunakan HTTPS (seperti ngrok) atau aktifkan di settings browser."
    );
    return;
  }

  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: { ideal: 'environment' } }
    });

    video.srcObject = stream;
    video.addEventListener('loadedmetadata', () => {
      canvas.width = container.clientWidth || video.videoWidth || 300;
      canvas.height = container.clientHeight || video.videoHeight || 400;
      drawGuideFrame(ctx, canvas.width, canvas.height);
    });

    window.addEventListener('resize', () => {
      canvas.width = container.clientWidth;
      canvas.height = container.clientHeight;
      drawGuideFrame(ctx, canvas.width, canvas.height);
    });

  } catch (err) {
    console.error("Gagal membuka kamera:", err);
    showError(
      container,
      "Gagal mengakses kamera: " + err.message +
      "<br><br><small>Pastikan izin kamera diizinkan dan menggunakan URL HTTPS.</small>"
    );
  }
}

function showError(container, msg) {
  const errDiv = document.createElement('div');
  errDiv.className = 'error-message';
  errDiv.innerHTML = msg;
  container.appendChild(errDiv);
}

function drawGuideFrame(ctx, width, height) {
  ctx.clearRect(0, 0, width, height);

  const frameWidth = width * 0.7;
  const frameHeight = frameWidth * (3.5 / 2.5);
  const x = (width - frameWidth) / 2;
  const y = (height - frameHeight) / 2;

  ctx.strokeStyle = '#00ff88';
  ctx.lineWidth = 4;
  ctx.strokeRect(x, y, frameWidth, frameHeight);
}

async function captureAndCheckQuality() {
  const video = document.getElementById('camera-feed');

  const captureCanvas = document.createElement('canvas');
  captureCanvas.width = video.videoWidth;
  captureCanvas.height = video.videoHeight;
  captureCanvas.getContext('2d').drawImage(video, 0, 0);

  const blob = await new Promise(resolve =>
    captureCanvas.toBlob(resolve, 'image/jpeg', 0.9)
  );

  const formData = new FormData();
  formData.append('file', blob, 'capture.jpg');

  try {
    const response = await fetch('/check-quality', {
      method: 'POST',
      body: formData,
    });

    const result = await response.json();

    if (result.passed) {
      console.log('Foto oke, lanjut proses berikutnya', result);
    } else {
      alert(result.reasons.join('\n'));
    }
  } catch (err) {
    console.error('Gagal hubungi backend:', err);
    alert('Gagal cek kualitas foto: ' + err.message);
  }
}

document.getElementById('capture-btn').addEventListener('click', captureAndCheckQuality);
startScanner();