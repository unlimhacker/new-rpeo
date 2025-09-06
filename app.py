import os
import requests
import telebot
from flask import Flask, request

TOKEN = os.getenv("BOT_TOKEN", "8261351761:AAES_aRQ50v4SqUuAkkbqcRT9612Ngm_vLg")
CHANNEL_ID = os.getenv("CHANNEL_ID", "-1002654232777")  # replace with your channel id

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

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

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = request.get_data().decode("utf-8")
    bot.process_new_updates([telebot.types.Update.de_json(update)])
    return "!", 200

@app.route("/")
def index():
    return "🤖 TON Price Bot running!", 200

# send price every minute
import schedule, time, threading

def send_price():
    msg = get_ton_price()
    try:
        bot.send_message(CHANNEL_ID, msg)
    except Exception as e:
        print(f"Send error: {e}")

def scheduler():
    schedule.every(1).minutes.do(send_price)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=scheduler, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))


