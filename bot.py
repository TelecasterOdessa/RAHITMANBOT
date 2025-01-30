import logging
import asyncio
import openai
from aiogram import Bot, Dispatcher, types

# Токен бота (замените на свой)
TOKEN = "7909575276:AAH8gq7lrpgBUlscwZ7Gn2Fd8-PTcYEysUA"
OPENAI_API_KEY = "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"

# Включение логирования
logging.basicConfig(level=logging.INFO)

# Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для запроса к OpenAI GPT
async def get_gpt_response(prompt):
    async def get_gpt_response(prompt):
    try:
        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"].strip()
    except openai.error.OpenAIError as e:
        logging.error(f"Ошибка OpenAI: {e}")
        return f"Ошибка OpenAI: {e}"
    except Exception as e:
        logging.error(f"Другая ошибка: {e}")
        return f"Ошибка: {e}"


@dp.message(lambda message: message.text == "/start")
async def start(message: types.Message):
    await message.answer("Привет! Я бот с поддержкой GPT. Задай мне любой вопрос, и я помогу!")

@dp.message()
async def handle_message(message: types.Message):
    answer = await get_gpt_response(message.text)
    await message.answer(answer)

# Запуск бота
async def main():
    await dp.start_polling(bot, drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
