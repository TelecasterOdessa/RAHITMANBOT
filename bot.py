import logging
import asyncio
import random
import requests
from aiogram import Bot, Dispatcher, types

# Токен бота (замените на свой)
TOKEN = "7909575276:AAH8gq7lrpgBUlscwZ7Gn2Fd8-PTcYEysUA"

# Включение логирования
logging.basicConfig(level=logging.INFO)

# Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для получения анекдота с моего источника
async def get_joke():
    url = "https://official-joke-api.appspot.com/random_joke"  # Публичный API с анекдотами
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return f"{data['setup']} \n{data['punchline']}"
    return "Не удалось получить анекдот, попробуй ещё раз!"

@dp.message(lambda message: message.text == "/start")
async def start(message: types.Message):
    await message.answer("Привет! Я бот-анекдотчик. Напиши 'анекдот', и я расскажу тебе что-нибудь смешное!")

@dp.message(lambda message: message.text.lower() == "анекдот")
async def send_joke(message: types.Message):
    joke = await get_joke()
    await message.answer(f"😂 Вот тебе анекдот: {joke}")

# Запуск бота
async def main():
    await dp.start_polling(bot, drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
