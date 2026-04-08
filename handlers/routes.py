import os
import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, InputMediaVideo
from ytdlp import download_video

router = Router()

@router.message()
async def penis(message: Message):
    if not message.text: return
     
    if (
    "youtube.com" in message.text
    or "youtu.be" in message.text
    or "tiktok.com" in message.text
    or "instagram.com" in message.text
):
        url = message.text
        file = await asyncio.to_thread(download_video, url)

        if file == "image": # Если картинка, выводим "Пошел нахуй"
            await message.reply("К сожалению, я не умею скачивать картинки.")
            return
        
        if file == "duration": # Если картинка, выводим "Пошел нахуй"
            await message.reply("К сожалению, я не умею скачивать видео длиннее 10 минут.")
            return

        video = FSInputFile(file)
        await message.reply_video(
            video=FSInputFile("video.mp4")
        )
        os.remove("video.mp4")
    else: return