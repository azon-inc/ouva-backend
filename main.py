# Codigo Python Atualizado

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yt_dlp
import os
import imageio_ffmpeg as ffmpeg

# Configura o ffmpeg no PATH
ffmpeg_path = ffmpeg.get_ffmpeg_exe()
os.environ["PATH"] = os.path.dirname(ffmpeg_path) + os.pathsep + os.environ.get("PATH", "")

app = FastAPI()

# Permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restringir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LinkInput(BaseModel):
    url: str

@app.post("/extrair-audio")
async def extrair_audio(data: LinkInput):
    url = data.url

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'skip_download': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            audio_url = info.get('url')
            title = info.get('title')
            thumbnail = info.get('thumbnail')

        return {
            "success": True,
            "stream_url": audio_url,
            "title": title,
            "thumbnail": thumbnail
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
