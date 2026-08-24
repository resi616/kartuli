async function startScanner() {
  const video = document.getElementById('camera-feed');
  const canvas = document.getElementById('guide-overlay');
  const ctx = canvas.getContext('2d');
  const container = document.getElementById('scanner-container');

  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    showError(container, "Browser atau koneksi (HTTP) tidak mendukung akses kamera.<br><br>Gunakan HTTPS (seperti LocalTunnel/ngrok) atau aktifkan di settings browser.");
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
    showError(container, "Gagal mengakses kamera: " + err.message + "<br><br><small>Pastikan izin kamera diizinkan dan menggunakan URL HTTPS.</small>");
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
  const frameHeight = frameWidth * (3.5 / 2.5); // Rasio standar kartu TCG
  const x = (width - frameWidth) / 2;
  const y = (height - frameHeight) / 2;

  ctx.strokeStyle = '#00ff88';
  ctx.lineWidth = 4;
  ctx.strokeRect(x, y, frameWidth, frameHeight);
}

startScanner();