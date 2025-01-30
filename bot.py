import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

# Токен бота (замените на свой)
TOKEN = "7909575276:AAH8gq7lrpgBUlscwZ7Gn2Fd8-PTcYEysUA"

# Включение логирования
logging.basicConfig(level=logging.INFO)

# Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Клавиатура для выбора типа контейнера
container_kb = ReplyKeyboardMarkup(resize_keyboard=True)
container_kb.add("20GP", "40GP", "40HQ")

# Клавиатура для формы оплаты
payment_kb = ReplyKeyboardMarkup(resize_keyboard=True)
payment_kb.add("Наличный расчёт", "Безналичный расчёт")

# Словарь для хранения временных данных пользователей
user_data = {}

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("Привет! Я бот для запроса ставок. Введи маршрут (например, Shanghai - Odessa)")

@dp.message_handler(lambda message: message.text and " - " in message.text)
async def get_route(message: types.Message):
    user_data[message.from_user.id] = {"route": message.text}
    await message.reply("Выбери тип контейнера", reply_markup=container_kb)

@dp.message_handler(lambda message: message.text in ["20GP", "40GP", "40HQ"])
async def get_container(message: types.Message):
    user_data[message.from_user.id]["container"] = message.text
    await message.reply("Выбери форму оплаты", reply_markup=payment_kb)

@dp.message_handler(lambda message: message.text in ["Наличный расчёт", "Безналичный расчёт"])
async def get_payment(message: types.Message):
    user_data[message.from_user.id]["payment"] = message.text
    
    # Формируем запрос
    data = user_data[message.from_user.id]
    request_text = (f"Запрос ставки:\n"
                    f"Маршрут: {data['route']}\n"
                    f"Тип контейнера: {data['container']}\n"
                    f"Форма оплаты: {data['payment']}")
    
    await message.reply(request_text + "\nОтправляем агентам...")
    
    # Здесь можно добавить логику отправки в Skype или email
    
    del user_data[message.from_user.id]  # Очищаем данные

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
