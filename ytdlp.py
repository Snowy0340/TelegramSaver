import yt_dlp
import os

ydl_opts = {
        'outtmpl': 'video.%(ext)s',  # расширение файла
        'noplaylist': True,  # не скачиваем плейлисты
        'quiet' : True,
        'format': 'bestvideo + bestaudio',
         'merge_output_format': 'mp4' # скачиваем в лучшем формате и склеиваем в mp4 с помощью ffmpeg
    }

def download_video(url):

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Получаем метаданные без скачивания
        try:
            info = ydl.extract_info(url, download=False)
            if info is None:
                return None
        except Exception:
            return "image"

        # Исключаем стримы
        if info.get("is_live") or info.get("was_live"):
            return None
        
        if not info.get("duration") > 1:
            return "image"

        # Проверка вертикальности (height > width)
        vertical = False
        for f in info.get("formats", []):
            h = f.get("height")
            w = f.get("width")
            if h and w and h >= w:
                vertical = True
                break

        if not vertical:
            return None  # видео не вертикальное

        # Скачиваем видео
        ydl.download([url])

        # Возвращаем путь к файлу
        filename = ydl.prepare_filename(info)
        return filename