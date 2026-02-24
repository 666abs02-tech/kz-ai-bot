import os
from openai import OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """Ты ИИ-юрист. Отвечай ясно и структурировано.
Если не хватает данных — задай уточняющие вопросы.
Ответы носят информационный характер и не заменяют консультацию юриста.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет. Опиши юридическую ситуацию.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ],
        temperature=0.2
    )

    answer = response.choices[0].message.content
    await update.message.reply_text(answer)

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
