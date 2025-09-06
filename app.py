# app.py
from flask import Flask, request
import telebot
import os

API_TOKEN = "8261351761:AAES_aRQ50v4SqUuAkkbqcRT9612Ngm_vLg"
WEBHOOK_URL = "https://new-rpeo.onrender.com/"  # your Render URL

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Handle /start command
@bot.message_handler(commands=['start'])
def send_id(message):
    user_id = message.from_user.id
    bot.reply_to(message, f"Welcome! Your Telegram ID is: {user_id}")

# Telegram webhook route
@app.route(f"/{API_TOKEN}", methods=['POST'])
def telegram_webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# Set webhook
@app.route("/")
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + API_TOKEN)
    return "Webhook set!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
