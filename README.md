# Telegram AI Bot (Qwen + aiogram)

## Описание
Бот для Telegram на Python с использованием aiogram и Qwen (через OpenAI-совместимый API).

## Установка
1. Клонируйте репозиторий или скачайте файлы.
2. Установите зависимости:
   ```bash
pip install -r requirements.txt
```

## Настройка переменных окружения
Создайте файл `.env` или экспортируйте переменные:
- `TELEGRAM_BOT_TOKEN` — токен Telegram-бота (получить у [BotFather](https://t.me/BotFather))
- `QWEN_API_KEY` — ваш API-ключ Qwen
- `QWEN_API_BASE` — базовый URL Qwen API (например, `https://YOUR_QWEN_API_URL/v1`)

Пример для Windows PowerShell:
```powershell
$env:TELEGRAM_BOT_TOKEN="ваш_тг_токен"
$env:QWEN_API_KEY="ваш_qwen_api_key"
$env:QWEN_API_BASE="https://your_qwen_api_url/v1"
```

## Запуск
```bash
python main.py
```

## Использование
Просто напишите сообщение боту — он ответит с помощью Qwen.
