import os
import time
import requests
import telebot
from flask import Flask, request
import schedule
import threading

BOT_TOKEN = os.getenv("BOT_TOKEN") or "8261351761:AAES_aRQ50v4SqUuAkkbqcRT9612Ngm_vLg"
CHANNEL_ID = os.getenv("CHANNEL_ID") or "-1002654232777"  # replace with your channel id

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# ---- Function to fetch TON price ----
def get_ton_price():
    try:
        url = "https://api.binance.com/api/v3/ticker/price?symbol=TONUSDT"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        price = float(data["price"])
        return f"💎 TON price: ${price:.2f}"
    except Exception as e:
        return f"⚠️ Error fetching price: {e}"


# ---- Send to channel ----
def send_price():
    price = get_ton_price()
    try:
        bot.send_message(CHANNEL_ID, price)
    except Exception as e:
        print("Send error:", e)

# ---- Schedule every minute ----
schedule.every(1).minutes.do(send_price)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_schedule, daemon=True).start()

# ---- Telegram webhook ----
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = request.stream.read().decode("utf-8")
    bot.process_new_updates([telebot.types.Update.de_json(update)])
    return "ok", 200

@app.route("/")
def index():
    return "🤖 TON Bot Running!", 200

# ---- Command ----
@bot.message_handler(commands=["price"])
def price_cmd(message):
    bot.reply_to(message, get_ton_price())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

