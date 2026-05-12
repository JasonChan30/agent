import yt_dlp
from pydantic import BaseModel, Field
from langchain_core.tools import tool

class DownloadVideoInput(BaseModel):
    """Input for download video queries."""
    url: str = Field(description="download url")
    start_seconds : float = Field(description="start form", default=0),
    end_seconds : float = Field(description="end from"),
    path : str = Field(description="save path", default="../video")

@tool(args_schema=DownloadVideoInput)
def download_video(url: str, start_seconds: float, end_seconds: float, path: str) -> str:
    """Download video from the URL."""
    path = f"{path}/%(title)s.%(ext)s"
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'download_sections': [{
            'start_time': start_seconds,
            'end_time': end_seconds,
        }],
        'external_downloader': 'ffmpeg',
        'outtmpl': path,
        'external_downloader_args': {
            'ffmpeg_i': ['-ss', str(start_seconds), '-to', str(end_seconds)]
        },
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return path

