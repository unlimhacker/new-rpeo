# app.py
import os
from flask import Flask, request
import telebot

API_TOKEN = "8261351761:AAES_aRQ50v4SqUuAkkbqcRT9612Ngm_vLg"
WEBHOOK_URL = f"https://new-rpeo.onrender.com/{API_TOKEN}"

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# Reply to /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Hello! This is your support bot.")

# Catch all other messages
@bot.message_handler(func=lambda m: True)
def all_messages(message):
    bot.send_message(message.chat.id, "Thanks for your message. We'll get back to you soon!")

# Webhook route
@app.route(f"/{API_TOKEN}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# Root route to set webhook
@app.route("/")
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    return f"Webhook set to {WEBHOOK_URL}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

