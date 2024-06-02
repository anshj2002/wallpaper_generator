from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from PIL import Image
from io import BytesIO
import requests
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict origins if needed
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Add OPTIONS method here
    allow_headers=["*"],
)

class WallpaperRequest(BaseModel):
    main_category: str
    sub_category: str
    style: str

def query_huggingface_api(prompt: str):
    API_TOKEN = os.getenv("backend")
    if not API_TOKEN:
        raise RuntimeError("HUGGING_FACE_API_TOKEN is not set in the environment variables.")
    
    API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {API_TOKEN}" }

    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.content

@app.post("/generate-wallpaper/")
async def generate_wallpaper(request_data: WallpaperRequest):
    prompt = f"wallpaper for {request_data.sub_category} in {request_data.main_category} in {request_data.style} way"
    image_bytes = query_huggingface_api(prompt)
    image = Image.open(BytesIO(image_bytes))
    buf = BytesIO()
    image.save(buf, format='PNG')
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
