import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.methods import DeleteWebhook
from aiogram.types import Message
from mistralai import Mistral
from dotenv import load_dotenv
load_dotenv()

mistral_api_key = os.getenv("MISTRAL_API_KEY", "")  # API-ключ теперь берется из переменной окружения
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")  # Токен бота теперь берется из переменной окружения

if not mistral_api_key or not TOKEN:
    raise ValueError("Не заданы переменные окружения MISTRAL_API_KEY и/или TELEGRAM_BOT_TOKEN!")

model = "mistral-large-latest"
client = Mistral(api_key=mistral_api_key)

# Словарь для хранения истории сообщений для каждого чата
chat_history = {}

logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN)
dp = Dispatcher()

# ОБРАБОТЧИК КОМАНДЫ СТАРТ
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer('Привет! Я - бот с подключенной нейросетью Mistral, отправь свой запрос')

# ОБРАБОТЧИК ЛЮБОГО ТЕКСТОВОГО СООБЩЕНИЯ
@dp.message(F.text)
async def filter_messages(message: Message):
    chat_id = message.chat.id

    # Если чат новый, инициализируем историю
    if chat_id not in chat_history:
        chat_history[chat_id] = [
            {
                "role": "system",
                "content": "Ты полезный ассистент, отвечай кратко и по делу."
            }
        ]

    # Добавляем сообщение пользователя в историю
    chat_history[chat_id].append({
        "role": "user",
        "content": message.text
    })

    # Отправляем запрос в Mistral с полной историей чата
    try:
        chat_response = client.chat.complete(
            model=model,
            messages=chat_history[chat_id]
        )
        response_text = chat_response.choices[0].message.content
    except Exception as e:
        response_text = f"Ошибка при обращении к Mistral: {e}"

    # Добавляем ответ в историю
    chat_history[chat_id].append({
        "role": "assistant",
        "content": response_text
    })

    # Ограничиваем историю, чтобы не превышать лимиты (например, 10 сообщений)
    if len(chat_history[chat_id]) > 10:
        chat_history[chat_id] = [chat_history[chat_id][0]] + chat_history[chat_id][-9:]

    # Отправляем ответ пользователю
    await message.answer(response_text)

async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 