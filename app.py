from flask import Flask, request
import telebot

TOKEN = "8261351761:AAES_aRQ50v4SqUuAkkbqcRT9612Ngm_vLg"
bot = telebot.TeleBot(TOKEN, threaded=False)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "🤖 Simple Bot is running!"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json(force=True)
    if update:
        bot.process_new_updates([telebot.types.Update.de_json(update)])
    return "OK", 200

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "👋 Hello! I am alive!")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.reply_to(message, f"✅ You said: {message.text}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
