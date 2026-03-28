import os
import anthropic
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

async def ask_claude(text):
    client = anthropic.Anthropic(api_key=os.environ["CLAUDE_API_KEY"])
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": text}]
    )
    return message.content[0].text

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text("⏳ 생각 중...")
    try:
        reply = await ask_claude(user_text)
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"오류 발생: {str(e)}")

if __name__ == "__main__":
    token = os.environ["TELEGRAM_TOKEN"]
    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("봇 시작!")
    app.run_polling()
