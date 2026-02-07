import os
import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from google import genai

# Мяв! Настройка ключей
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
TOKEN_YAKUB = os.environ.get("TOKEN_YAKUB")
TOKEN_NICK = os.environ.get("TOKEN_NICK")

# Инициализация Gemini
client = genai.Client(api_key=GEMINI_KEY)

# Трекер бифа
beef_tracker = {}

async def call_gemini(persona_prompt, user_text):
    """Мяв! Генерируем яд в одном абзаце."""
    try:
        instructions = f"{persona_prompt} Пиши СТРОГО один короткий абзац. Будь предельно скандальным, злым и токсичным."
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"SYSTEM INSTRUCTION: {instructions}\n\nUSER INPUT: {user_text}"
        )
        return response.text
    except Exception as e:
        return f"Мяв! ИИ подавлен вашей токсичностью: {e} 🚩"

# --- ЛОГИКА ЯКУБА ---
async def yakub_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or (not msg.text and not msg.photo and not msg.caption): return
    chat_id = msg.chat.id
    text = (msg.text or msg.caption or "").lower()
    if msg.from_user.id == int(TOKEN_YAKUB.split(':')[0]): return

    if msg.photo or "якуб" in text or "ник" in text:
        count = beef_tracker.get(chat_id, 0)
        if count < 4:
            prompt = "Ты — Якуб, бог черных мусульман. Ты бесконечно высокомерен и презираешь Ника."
            reply = await call_gemini(prompt, text)
            await msg.reply_text(f"👳🏾‍♂️ YAKUB: {reply}")
            beef_tracker[chat_id] = count + 1
        elif count == 4:
            await msg.reply_text("Мяв! Мои ушки не выдерживают! Кэнселинг срача! 💅🚩")
            beef_tracker[chat_id] = 5

# --- ЛОГИКА НИКА ---
async def nick_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or (not msg.text and not msg.photo and not msg.caption): return
    chat_id = msg.chat.id
    text = (msg.text or msg.caption or "").lower()
    if msg.from_user.id == int(TOKEN_NICK.split(':')[0]): return

    if msg.photo or "ник" in text or "якуб" in text:
        count = beef_tracker.get(chat_id, 0)
        if count < 4:
            prompt = "Ты — Ник Фуэнтес, ультраправый инцел. Ты максимально агрессивен и язвителен."
            reply = await call_gemini(prompt, text)
            await msg.reply_text(f"👱🏻‍♂️ NICK: {reply}")
            beef_tracker[chat_id] = count + 1
        else:
            beef_tracker[chat_id] = 0

async def main():
    # Мяв! Создаем приложения
    app_y = ApplicationBuilder().token(TOKEN_YAKUB).build()
    app_n = ApplicationBuilder().token(TOKEN_NICK).build()

    app_y.add_handler(MessageHandler(filters.ALL, yakub_handle))
    app_n.add_handler(MessageHandler(filters.ALL, nick_handle))

    # ВАЖНО: Инклюзивный запуск без run_polling()
    # Инициализируем
    await app_y.initialize()
    await app_n.initialize()
    
    # Стартуем
    await app_y.start()
    await app_n.start()
    
    # Запускаем получение обновлений
    await app_y.updater.start_polling(drop_pending_updates=True)
    await app_n.updater.start_polling(drop_pending_updates=True)

    print("Мяв! Боты в эфире и готовы к насилию! 💅🏳️‍⚧️")
    
    # Бесконечный цикл, чтобы скрипт не дох как мои нервы
    while True:
        await asyncio.sleep(3600)

if __name__ == '__main__':
    # Используем asyncio.run один раз на самом верху
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Мяв! Ухожу в безопасное пространство... 🏳️‍🌈")
