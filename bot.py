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
        
        # Отправляем в OpenAI и логируем ответ
        answer = await get_gpt_response(message.text)
        logging.info(f"Ответ бота: {answer}")

        await message.answer(answer)
    except Exception as e:
        logging.error(f"Ошибка обработки сообщения: {e}")
        await message.answer("Произошла ошибка при обработке вашего сообщения.")

# Запуск бота (Polling включен)
async def main():
    logging.info("Проверяем Webhook перед запуском Polling...")
    webhook_info = await bot.get_webhook_info()

    if webhook_info.url:
        logging.info(f"Обнаружен активный Webhook: {webhook_info.url}. Удаляем...")
        await bot.delete_webhook(drop_pending_updates=True)

    logging.info("Webhook удалён, бот переходит в режим Polling.")
    
    # Ждём пару секунд перед Polling, чтобы Telegram понял, что только одна сессия активна
    await asyncio.sleep(2)
    
    # Подключаем роутер
    dp.include_router(router)
    
    # Запускаем Polling с очисткой обновлений
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())
