# app.py
from flask import Flask, request
import telebot
import os

API_TOKEN = "8261351761:AAES_aRQ50v4SqUuAkkbqcRT9612Ngm_vLg"
WEBHOOK_URL = f"https://new-rpeo.onrender.com/{API_TOKEN}"

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Handle /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Welcome to Support Bot. How can we help you today?")

# Handle all other messages
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    user_id = message.from_user.id
    text = message.text
    print(f"Message from {user_id}: {text}")  # log in server console
    bot.reply_to(message, "Thank you for your message! Our support will contact you soon.")

# Telegram webhook route
@app.route(f"/{API_TOKEN}", methods=['POST'])
def telegram_webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# Route to set webhook
@app.route("/")
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    return f"Webhook set to {WEBHOOK_URL}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

