import yt_dlp

def download_video(url):
    # Настройки yt-dlp
    ydl_opts = {
        'outtmpl': 'video.%(ext)s',  # перезаписывает файл каждый раз
        'noplaylist': True,  # не скачиваем плейлисты
        'quiet' : True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Получаем метаданные без скачивания
        info = ydl.extract_info(url, download=False)
        if info is None:
            return None

        # Исключаем стримы
        if info.get("is_live") or info.get("was_live"):
            return None

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