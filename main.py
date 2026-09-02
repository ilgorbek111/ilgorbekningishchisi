import os
import asyncio
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
DIFY_API_KEY = os.getenv("DIFY_API_KEY")
DIFY_URL = os.getenv("DIFY_URL", "https://api.dify.ai/v1/chat-messages")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum! AI Agentga xabaringizni yuboring.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = str(update.message.chat_id)

    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": {},
        "query": user_text,
        "response_mode": "blocking",
        "user": user_id
    }

    try:
        response = requests.post(DIFY_URL, json=payload, headers=headers)
        if response.status_code == 200:
            answer = response.json().get("answer", "Javob olishda xatolik bo'ldi.")
        else:
            answer = "Xatolik yuz berdi, qaytadan urinib ko'ring."
    except Exception:
        answer = "Server bilan bog'lanishda xatolik yuz berdi."

    await update.message.reply_text(answer)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
