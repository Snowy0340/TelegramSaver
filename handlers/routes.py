import os
import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, InputMediaVideo
from ytdlp import download_video

router = Router()

debug_flag = False

@router.message(Command("debug"))
async def debug(message: Message):
    global debug_flag
    if not debug_flag:
        debug_flag = True
        await message.reply("debug mode enabled")
    else:
        debug_flag = False
        await message.reply("debug mode disabled")


@router.message()
async def mesage_interaction(message: Message):
    if not message.text: return
     
    if (
    "youtube.com" in message.text
    or "youtu.be" in message.text
    or "tiktok.com" in message.text
    or "instagram.com" in message.text
):
        url = message.text
        file = await asyncio.to_thread(download_video, url)

        if file[0] == "image": # Если картинка, выводим "Пошел нахуй"
            if debug_flag:
                await message.reply("format error: image")
            return
        
        if file[0] == "vertical": # Если картинка, выводим "Пошел нахуй"
            if debug_flag:
                await message.reply("format error: vertical")
            return
        
        if file[0] == "stream": # Если картинка, выводим "Пошел нахуй"
                if debug_flag:
                    await message.reply("error: stream")
                return

        if file[0] == "duration": # Если картинка, выводим "Пошел нахуй"
            if debug_flag:
                await message.reply(f"duration error\nduration: {file[1]} sec")
            return
        
        # else: 
        #     if debug_flag: await message.reply(file)

        video = FSInputFile(file[0])
        await message.reply_video(
            video=FSInputFile("video.mp4")
        )
        os.remove("video.mp4")
    else: return