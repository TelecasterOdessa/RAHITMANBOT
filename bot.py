import logging
import asyncio
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command

# Включение логирования
logging.basicConfig(level=logging.INFO)

# Указываем токены (замени на свои)
TOKEN = "7909575276:AAG_C-blvdI71VyLo6yGnkvzU6xk-2XCIg4"

# Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

# Функция для расчета стоимости пропорционально весу
async def calculate_shipping_cost(total_cost, weights):
    total_weight = sum(weights.values())
    if total_weight == 0:
        return {client: 0 for client in weights}
    return {client: round((weight / total_weight) * total_cost, 2) for client, weight in weights.items()}

# Инструкция для пользователей
INSTRUCTION = "Привет, грамотей! Училка по математике в шоке от тебя! Отправь мне данные для просчета стоимости транспортировки в следующем формате: \nОбщая стоимость грн/usd: сумма\nКлиент1: вес\nКлиент2: вес"

# Обработчик команды /start
@router.message(Command("start"))
async def start(message: Message):
    logging.info(f"Команда /start от {message.from_user.id}")
    await message.answer(INSTRUCTION)

# Обработчик расчета стоимости
@router.message()
async def handle_calculation(message: Message):
    try:
        lines = message.text.split("\n")
        total_cost = float(lines[0].split(":")[1].strip())
        weights = {line.split(":")[0].strip(): float(line.split(":")[1].strip()) for line in lines[1:]}
        costs = await calculate_shipping_cost(total_cost, weights)
        response = "Распределение стоимости (грн/usd):\n" + "\n".join([f"{client}: {cost} грн/usd" for client, cost in costs.items()])
        await message.answer(response)
    except Exception as e:
        logging.error(f"Ошибка обработки данных: {e}")
        await message.answer(f"Ошибка! Проверь формат ввода.\n{INSTRUCTION}")

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
