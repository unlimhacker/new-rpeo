import os
import logging
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# === CONFIG ===
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "8261351761:AAES_aRQ50v4SqUuAkkbqcRT9612Ngm_vLg")  
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://new-rpeo.onrender.com")  # set this on Render

if not BOT_TOKEN or ":" not in BOT_TOKEN:
    raise SystemExit("❌ TELEGRAM_BOT_TOKEN is missing or invalid.")

# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# fastapi app
app = FastAPI()
tg_app = Application.builder().token(BOT_TOKEN).build()

# === Handlers ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello! I’m alive via webhook on Render ✅")

tg_app.add_handler(CommandHandler("start", start))

# === Webhook endpoint ===
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, tg_app.bot)
    await tg_app.process_update(update)
    return {"ok": True}

# === Startup: set webhook ===
@app.on_event("startup")
async def startup():
    await tg_app.bot.delete_webhook()
    if not WEBHOOK_URL:
        logger.error("⚠️ WEBHOOK_URL not set. Please set it on Render.")
        return
    await tg_app.bot.set_webhook(WEBHOOK_URL + "/webhook")
    logger.info(f"✅ Webhook set to {WEBHOOK_URL}/webhook")


