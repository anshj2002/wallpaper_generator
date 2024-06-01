# 
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import io
from PIL import Image
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv("Api_Token")
if not API_TOKEN:
    raise RuntimeError("HUGGING_FACE_API_TOKEN is not set in the environment variables.")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {API_TOKEN}" }

app = FastAPI()

class WallpaperRequest(BaseModel):
    category: str
    custom_prompt: str = None

def query_huggingface_api(prompt: str):
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.content

@app.post("/generate-wallpaper/")
async def generate_wallpaper(request: WallpaperRequest):
    prompt = request.custom_prompt if request.category == "custom" else f"{request.category} wallpaper"
    image_bytes = query_huggingface_api(prompt)
    image = Image.open(io.BytesIO(image_bytes))
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@app.get("/categories/")
async def get_categories():
    categories = ["movies", "games", "sports", "custom"]
    return {"categories": categories}
