# app.py
from flask import Flask, request
import telebot
import os

API_TOKEN = "8261351761:AAES_aRQ50v4SqUuAkkbqcRT9612Ngm_vLg"
WEBHOOK_URL = f"https://new-rpeo.onrender.com/{API_TOKEN}"

bot = telebot.TeleBot(API_TOKEN, parse_mode="HTML")
app = Flask(__name__)

# Catch all messages including /start
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    if text == "/start":
        bot.send_message(message.chat.id, "Hello! Welcome to the Support Bot.")
    else:
        bot.send_message(message.chat.id, "Thank you for your message! Our support will contact you soon.")
    print(f"Handled message from {message.chat.id}: {text}")

@app.route(f"/{API_TOKEN}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    return f"Webhook set to {WEBHOOK_URL}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
