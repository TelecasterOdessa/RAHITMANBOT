import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Токен бота (замените на свой)
TOKEN = "7909575276:AAH8gq7lrpgBUlscwZ7Gn2Fd8-PTcYEysUA"

# ID чата с агентами (замените на актуальный)
AGENT_USER_ID = 271525995
  # Замените на Telegram ID нужного контакта

# Включение логирования
logging.basicConfig(level=logging.INFO)

# Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Клавиатура для выбора типа контейнера
container_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="20GP")], 
                                              [KeyboardButton(text="40GP")], 
                                              [KeyboardButton(text="40HQ")]], 
                                     resize_keyboard=True)

# Клавиатура для формы оплаты
payment_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Наличный расчёт")], 
                                            [KeyboardButton(text="Безналичный расчёт")]], 
                                     resize_keyboard=True)

# Словарь для хранения временных данных пользователей
user_data = {}

@dp.message(lambda message: message.text == "/start")
async def start(message: types.Message):
    await message.answer("Привет! Я бот для запроса ставок. Введи маршрут (например, Shanghai - Odessa)")

@dp.message(lambda message: " - " in message.text)
async def get_route(message: types.Message):
    user_data[message.from_user.id] = {"route": message.text}
    await message.answer("Выбери тип контейнера", reply_markup=container_kb)

@dp.message(lambda message: message.text in ["20GP", "40GP", "40HQ"])
async def get_container(message: types.Message):
    user_data[message.from_user.id]["container"] = message.text
    await message.answer("Выбери форму оплаты", reply_markup=payment_kb)

@dp.message(lambda message: message.text in ["Наличный расчёт", "Безналичный расчёт"])
async def get_payment(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in user_data:
        await message.answer("Ошибка: начни сначала, введи маршрут.")
        return
    
    user_data[user_id]["payment"] = message.text
    
    # Формируем запрос
    data = user_data[user_id]
    request_text = (f"📢 Запрос ставки:\n"
                    f"Маршрут: {data['route']}\n"
                    f"Тип контейнера: {data['container']}\n"
                    f"Форма оплаты: {data['payment']}")
    
    await message.answer(request_text + "\nОтправляем агентам...")
    
    # Отправляем запрос в чат агентов
    await bot.send_message(AGENT_USER_ID, request_text)
    
    del user_data[user_id]  # Очищаем данные

# Запуск бота
async def main():
    await dp.start_polling(bot, drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
