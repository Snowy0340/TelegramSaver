import os
import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from ytdlp import download_video

router = Router()

# @router.message()
# async def hello(message):
#     await message.answer("Hello!")


@router.message()
async def penis(message: Message):
    if "https://www.youtube.com" in message.text:
        url = message.text
        file = await asyncio.to_thread(download_video, url)
        if not file:
            await message.answer("К сожалению, я не умею скачивать горизонтальные видео или стримы :(")
            return
        video = FSInputFile(file)
        await message.answer_video(video)
        os.remove("video.mp4")
    else: return





# @router.message()
# async def penis(message: Message):
#     if "https://www.youtube.com" in message.text:
#         url = message.text
#         file = await asyncio.to_thread(download_video, url)
#         if not file:
#             await message.answer("К сожалению, я не умею скачивать горизонтальные видео или стримы :(")
#             return
#         video = FSInputFile(file)
#         await message.answer_video(video)
#         os.remove("video.mp4")
#     else: return