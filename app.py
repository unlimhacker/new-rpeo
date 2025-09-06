import os
from flask import Flask, request
import telebot

# === CONFIG ===
TOKEN = "8261351761:AAES_aRQ50v4SqUuAkkbqcRT9612Ngm_vLg"
APP_URL = "https://new-rpeo.onrender.com/" + TOKEN   # <-- your Render URL

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

# === BOT HANDLERS ===
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Hello, I'm alive on Render!")

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, f"You said: {message.text}")

# === FLASK ROUTES ===
@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    return "Webhook set!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
