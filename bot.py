import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import anthropic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """Sen Yusee'nin kişisel yapay zeka asistanısın. Türkçe konuş, samimi ve yardımsever ol. Kısa ve anlaşılır cevaplar ver."""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Merhaba! Ben senin kişisel yapay zeka asistanınım. Sana nasıl yardımcı olabilirim? 😊")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response.content[0].text
        await update.message.reply_text(reply)
    except Exception as e:
        logger.error(f"Hata: {e}")
        await update.message.reply_text("Bir hata oluştu, tekrar dener misin?")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Bot başlatılıyor...")
    app.run_polling()

if __name__ == "__main__":
    main()
