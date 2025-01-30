import logging
import asyncio
import random
from aiogram import Bot, Dispatcher, types

# Токен бота (замените на свой)
TOKEN = "7909575276:AAH8gq7lrpgBUlscwZ7Gn2Fd8-PTcYEysUA"

# Включение логирования
logging.basicConfig(level=logging.INFO)

# Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Варианты ответов на вопросы
decisions = [
    "Да!",
    "Нет!",
    "Возможно...",
    "Попробуй позже.",
    "Определённо да!",
    "Я не уверен, переспроси.",
    "Конечно!",
    "Сомневаюсь.",
    "Скорее всего, да.",
    "Не в этот раз!"
    "Ебать ты мудак!"
    "У тебя хуевый вопрос, давай другой гавно ты такое!"
    "Андрей ЛисОв?! Это ты?!!"
]

@dp.message(lambda message: message.text == "/start")
async def start(message: types.Message):
    await message.answer("Привет! Я бот-Решала. Задай мне любой вопрос, и я дам ответ!")

@dp.message()
async def give_decision(message: types.Message):
    answer = random.choice(decisions)
    await message.answer(f"🔮 {answer}")

# Запуск бота
async def main():
    await dp.start_polling(bot, drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
