import os
import logging
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, ContextTypes

# Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Token do bot
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Flask app
app = Flask(__name__)

# Bot
application = Application.builder().token(TOKEN).build()

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Oi, desgraçadinho 🤖! Tô rodando no Render!")

application.add_handler(CommandHandler("start", start))

# Webhook route
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

@app.route("/")
def index():
    return "Bot tá online 🎉"

if __name__ == "__main__":
    bot = Bot(TOKEN)
    url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
    bot.delete_webhook()
    bot.set_webhook(url=url)

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
