import os
import requests
import telebot
from flask import Flask, request
import threading
import schedule
import time

TOKEN = os.getenv("BOT_TOKEN", "8261351761:AAES_aRQ50v4SqUuAkkbqcRT9612Ngm_vLg")
CHANNEL_ID = os.getenv("CHANNEL_ID", "-1002654232777")  # replace with your channel id

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Get TON price
def get_ton_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=usd"
        r = requests.get(url).json()
        return f"💎 TON price: ${r['the-open-network']['usd']}"
    except Exception as e:
        return f"Error getting price: {e}"

# Send price to channel
def send_price():
    price = get_ton_price()
    try:
        bot.send_message(CHANNEL_ID, price)
    except Exception as e:
        print(f"Failed to send price: {e}")

# Handle /price command
@bot.message_handler(commands=['price'])
def price_command(message):
    bot.reply_to(message, get_ton_price())

# Flask route for webhook
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
    if update:
        bot.process_new_updates([telebot.types.Update.de_json(update)])
    return "OK", 200

@app.route("/", methods=["GET"])
def index():
    return "🤖 TON Price Bot is running!", 200

# Scheduler loop (runs in background thread)
def run_scheduler():
    schedule.every(1).minutes.do(send_price)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Start background scheduler
    threading.Thread(target=run_scheduler, daemon=True).start()

    # Start Flask
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
