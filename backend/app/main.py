from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.services.quality_check import check_image_quality

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/check-quality")
async def check_quality(file: UploadFile = File(...)):
    image_bytes = await file.read()
    result = check_image_quality(image_bytes)
    return result

app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")