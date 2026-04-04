from os import getenv
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers.routes import router

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()  
dp.include_router(router)


async def main():
    print("running")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())