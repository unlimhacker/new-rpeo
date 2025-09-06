# app.py
from flask import Flask, request
import telebot
import requests
import os

API_TOKEN = "8261351761:AAES_aRQ50v4SqUuAkkbqcRT9612Ngm_vLg"
bot = telebot.TeleBot(API_TOKEN)
WEBHOOK_URL = "https://new-rpeo.onrender.com/"  # your Render URL

app = Flask(__name__)

def get_ton_price():
    try:
        url = "https://api.bybit.com/v5/market/tickers?category=spot&symbol=TONUSDT"
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        price = float(data["result"]["list"][0]["lastPrice"])
        return f"💎 TON price: ${price:.2f}"
    except Exception as e:
        return f"⚠️ Error fetching price: {e}"

# Telegram webhook route
@app.route(f"/{API_TOKEN}", methods=['POST'])
def telegram_webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# Command handler
@bot.message_handler(commands=['price'])
def send_price(message):
    bot.reply_to(message, get_ton_price())

# Set webhook
@app.route("/")
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL + API_TOKEN)
    return "Webhook set!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
