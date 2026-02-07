import os
import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from openai import OpenAI

# Секреты для Грока и Теlegi (Environment Variables на Render)
GROK_KEY = os.environ.get("GROK_API_KEY")
TOKEN_YAKUB = os.environ.get("TOKEN_YAKUB")
TOKEN_NICK = os.environ.get("TOKEN_NICK")

client = OpenAI(api_key=GROK_KEY, base_url="https://api.x.ai/v1")

# Глобальный счетчик срача: {chat_id: count}
beef_tracker = {}

async def call_grok(persona_name, system_prompt, input_text):
    """Мяв! Грок генерирует один агрессивный абзац."""
    try:
        response = client.chat.completions.create(
            model="grok-beta",
            messages=[
                {"role": "system", "content": f"{system_prompt} Пиши строго ОДИН абзац. Будь максимально скандальным и злым."},
                {"role": "user", "content": input_text},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Мяв! Ошибка: {e}"

# --- ЛОГИКА ЯКУБА ---
async def yakub_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    msg = update.message
    text = (msg.text or msg.caption or "").lower()
    
    # Триггер: фото или упоминание (но не от самого себя!)
    if (msg.photo or "якуб" in text) and msg.from_user.id != int(TOKEN_YAKUB.split(':')[0]):
        count = beef_tracker.get(chat_id, 0)
        if count < 4:
            prompt = "Ты — Якуб, злой ученый, бог-создатель 'белых дьяволов' по версии Nation of Islam. Ты высокомерен, агрессивен и ненавидишь всех."
            reply = await call_grok("YAKUB", prompt, text)
            await msg.reply_text(f"👳🏾‍♂️ YAKUB: {reply}")
            beef_tracker[chat_id] = count + 1
        else:
            beef_tracker[chat_id] = 0 # Сброс

# --- ЛОГИКА НИКА ---
async def nick_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    msg = update.message
    text = (msg.text or msg.caption or "").lower()

    # Ник отвечает на сообщения Якуба (или на фото/ключи)
    if (msg.photo or "ник" in text or "yakub" in text) and msg.from_user.id != int(TOKEN_NICK.split(':')[0]):
        count = beef_tracker.get(chat_id, 0)
        if count < 4:
            prompt = "Ты — Ник Фуэнтес, инцел, ультраправый провокатор. Ты ненавидишь леваков, черных и евреев. Ты максимально скандальный."
            reply = await call_grok("NICK", prompt, text)
            await msg.reply_text(f"👱🏻‍♂️ NICK: {reply}")
            beef_tracker[chat_id] = count + 1
            # Не сбрасываем тут, ждем пока круг замкнется

async def main():
    # Запускаем Якуба
    app_y = ApplicationBuilder().token(TOKEN_YAKUB).build()
    app_y.add_handler(MessageHandler(filters.ALL, yakub_logic))

    # Запускаем Ника
    app_n = ApplicationBuilder().token(TOKEN_NICK).build()
    app_n.add_handler(MessageHandler(filters.ALL, nick_logic))

    # Мяв! Запуск обеих сущностей одновременно
    await asyncio.gather(app_y.run_polling(), app_n.run_polling())

if __name__ == '__main__':
    print("Мяв! Бот-срач активирован. Трясусь от ярости! 💅🚩")
    asyncio.run(main())
