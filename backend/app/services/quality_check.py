# pyrefly: ignore [missing-import]
import cv2
import numpy as np

BLUR_TRESHOLD = 100
BRIGHTNESS_MIN = 50
BRIGHTNESS_MAX = 210

def check_blur(gray_image: np.ndarray) -> float:
    laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
    return laplacian.var()

def check_brightness(gray_image: np.ndarray) -> float:
    return float(np.mean(gray_image))

def check_image_quality(image_bytes: bytes) -> dict:
    np_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    if image is None:
        return {"passed": False, "reason": "File bukan gambar yang valid"}
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blur_score = check_blur(gray)
    brightness_score = check_brightness(gray)

    reasons = []
    if blur_score < BLUR_TRESHOLD:
        reasons.append("Foto terlalu blur, coba tahan HP lebih stabil")
    if brightness_score < BRIGHTNESS_MIN:
        reasons.append("Foto terlalu gelap, nyalakan flash atau cari cahaya lebih terang")
    if brightness_score > BRIGHTNESS_MAX:
        reasons.append("Foto terlalu terang/overexposed")

    return {
        "passed": len(reasons) == 0,
        "blur_score": round(blur_score, 2),
        "brightness_score": round(brightness_score, 2),
        "reasons": reasons,
    }