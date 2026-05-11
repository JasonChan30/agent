import yt_dlp


url = 'https://www.bilibili.com/video/BV1y4411c72u/?spm_id_from=333.337.search-card.all.click&vd_source=e9cbbdc4a6cb7b076ccb6518fdf5de26'
start_seconds = 19*60+28
end_seconds = 20*60+28
ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'download_sections': [{
        'start_time': start_seconds,
        'end_time': end_seconds,
    }],
    'external_downloader': 'ffmpeg',
    'outtmpl': './video/%(title)s_clip.%(ext)s',
    'external_downloader_args': {
        'ffmpeg_i': ['-ss', str(start_seconds), '-to', str(end_seconds)]
    },
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
