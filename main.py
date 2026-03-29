import os
import anthropic
from openai import AsyncOpenAI
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

async def ask_claude(text):
    client = anthropic.Anthropic(api_key=os.environ["claud-api"])
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": text}]
    )
    return message.content[0].text

async def ask_gpt(text):
    client = AsyncOpenAI(api_key=os.environ["gpt-api"])
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": text}]
    )
    return response.choices[0].message.content

async def ask_gemini(text):
    genai.configure(api_key=os.environ["gemini-api"])
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(text)
    return response.text

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text("🤖 Claude 답변 중...")
    try:
        reply = await ask_claude(user_text)
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"오류: {str(e)}")

async def claude_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = " ".join(context.args)
    if not user_text:
        await update.message.reply_text("사용법: /claude 질문내용")
        return
    await update.message.reply_text("🤖 Claude 답변 중...")
    try:
        reply = await ask_claude(user_text)
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"오류: {str(e)}")

async def gpt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = " ".join(context.args)
    if not user_text:
        await update.message.reply_text("사용법: /gpt 질문내용")
        return
    await update.message.reply_text("💬 GPT 답변 중...")
    try:
        reply = await ask_gpt(user_text)
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"오류: {str(e)}")

async def gemini_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = " ".join(context.args)
    if not user_text:
        await update.message.reply_text("사용법: /gemini 질문내용")
        return
    await update.message.reply_text("✨ Gemini 답변 중...")
    try:
        reply = await ask_gemini(user_text)
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"오류: {str(e)}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "안녕하세요! AI 봇입니다 🤖\n\n"
        "• 그냥 말하면 → Claude 답변\n"
        "• /claude 질문 → Claude\n"
        "• /gpt 질문 → ChatGPT\n"
        "• /gemini 질문 → Gemini"
    )

if __name__ == "__main__":
    token = os.environ["telegram_token"]
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("claude", claude_command))
    app.add_handler(CommandHandler("gpt", gpt_command))
    app.add_handler(CommandHandler("gemini", gemini_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("봇 시작!")
    app.run_polling()
