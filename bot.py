import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.filters import Command

TOKEN = "8058130669:AAFnKlYEBjyo3tGzIdNh8qeBRMaRsTryZ9I"
WEB_APP_URL = "https://tour-turum-webapp.vercel.app"  # Проверь, что URL правильный

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Открыть карту", web_app=WebAppInfo(url=WEB_APP_URL))]
        ],
        resize_keyboard=True
    )

    await message.answer("Привет! Нажми кнопку, чтобы открыть карту.", reply_markup=keyboard)

@dp.message()
async def web_app_data_handler(message: types.Message):
    if message.web_app_data:
        data = message.web_app_data.data
        await message.answer(f"Получены данные: {data}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
