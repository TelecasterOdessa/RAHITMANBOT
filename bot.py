import logging
import asyncio
from openai import OpenAI
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

# Указываем токены напрямую
TOKEN = "7909575276:AAH8gq7lrpgBUlscwZ7Gn2Fd8-PTcYEysUA"  # Вставь свой Telegram Bot Token
OPENAI_API_KEY = "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"  # Вставь свой OpenAI API Key

# Включение логирования
logging.basicConfig(level=logging.INFO)

# Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Создаём OpenAI клиент
client = OpenAI(api_key=OPENAI_API_KEY)

# Функция для запроса к OpenAI GPT
async def get_gpt_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Ошибка OpenAI: {e}")
        return "Произошла ошибка. Попробуйте позже."

# Обработчик команды /start
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Я бот с поддержкой GPT. Задай мне любой вопрос, и я помогу!")

# Обработчик всех текстовых сообщений
@dp.message()
async def handle_message(message: Message):
    answer = await get_gpt_response(message.text)
    await message.answer(answer)

# Запуск бота
async def main():
    logging.info("Бот запущен!")
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
