from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo
from aiogram.utils import executor

TOKEN = "ТОКЕН_БОТА"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Открыть карту", web_app=WebAppInfo(url="https://YOUR-WEB-APP-URL"))
    keyboard.add(button)

    await message.answer("Привет! Нажми кнопку, чтобы открыть карту.", reply_markup=keyboard)

@dp.message_handler(content_types=types.ContentType.WEB_APP_DATA)
async def web_app_data_handler(message: types.Message):
    data = message.web_app_data.data
    await message.answer(f"Получены данные: {data}")

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
