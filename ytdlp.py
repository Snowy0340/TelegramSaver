import yt_dlp
import os

ydl_opts = {
        'outtmpl': 'video.%(ext)s',  # перезаписывает файл каждый раз
        'noplaylist': True,  # не скачиваем плейлисты
        'quiet' : True,
        #'format' : 'best'
    }

def download_video(url):

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Получаем метаданные без скачивания
        info = ydl.extract_info(url, download=False)
        if info is None:
            return None

        # Исключаем стримы
        if info.get("is_live") or info.get("was_live"):
            return None
        
        if info.get("duration") > 1:
            return download_images(url)

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
    

def download_images(url):

    ydl_opts = {
        'skip_download': True,
        'writethumbnail': True,
        'quiet': True,
        'outtmpl': 'image_%(autonumber)s.%(ext)s'
    }
    files = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

        # если несколько картинок
        if 'entries' in info:
            for entry in info['entries']:
                if 'thumbnails' in entry:
                    for thumb in entry['thumbnails']:
                        filename = thumb.get('filepath')
                        if filename and os.path.exists(filename):
                            files.append(filename)

        # если одна картинка
        else:
            thumb = info.get('thumbnails')
            if thumb:
                filename = thumb[-1].get('filepath')
                if filename and os.path.exists(filename):
                    files.append(filename)

    return files