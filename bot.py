import logging
import asyncio
from openai import OpenAI
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command

# Включение логирования
logging.basicConfig(level=logging.INFO)

# Указываем токены (замени на свои)
TOKEN = "7909575276:AAG_C-blvdI71VyLo6yGnkvzU6xk-2XCIg4"
OPENAI_API_KEY = "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"

# Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

# Создаём OpenAI клиент
client = OpenAI(api_key=OPENAI_API_KEY)

# Функция для запроса к OpenAI GPT
async def get_gpt_response(prompt):
    try:
        logging.info(f"Отправляем запрос в OpenAI: {prompt}")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        gpt_answer = response.choices[0].message.content.strip()
        logging.info(f"Ответ OpenAI: {gpt_answer}")
        return gpt_answer
    except Exception as e:
        logging.error(f"Ошибка OpenAI: {e}")
        return "Произошла ошибка. Попробуйте позже."

# Обработчик команды /start
@router.message(Command("start"))
async def start(message: Message):
    logging.info(f"Команда /start от {message.from_user.id}")
    await message.answer("Привет! Я бот с поддержкой GPT. Задай мне любой вопрос, и я помогу!")

# Обработчик всех текстовых сообщений
@router.message()
async def handle_message(message: Message):
    try:
        logging.info(f"Получено сообщение от {message.from_user.id}: {message.text}")
        answer = await get_gpt_response(message.text)
        await message.answer(answer)
    except Exception as e:
        logging.error(f"Ошибка обработки сообщения: {e}")
        await message.answer("Произошла ошибка при обработке вашего сообщения.")

# Запуск бота
async def main():
    logging.info("Бот запущен!")
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
