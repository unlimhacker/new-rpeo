import os
import time
import requests
import telebot
import schedule

# ===============================
# CONFIG
# ===============================
TOKEN = os.getenv("BOT_TOKEN", "8261351761:AAES_aRQ50v4SqUuAkkbqcRT9612Ngm_vLg")
CHANNEL_ID = os.getenv("-1002654232777", "@tonovoi")  # example: "@mychannel"

bot = telebot.TeleBot(TOKEN)

# Function to fetch TON price
def get_ton_price():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=usd"
        res = requests.get(url).json()
        price = res["the-open-network"]["usd"]
        return f"💎 TON Price: ${price:.2f}"
    except Exception as e:
        return f"⚠️ Error fetching price: {e}"

# Function to send TON price to channel
def send_price():
    price = get_ton_price()
    bot.send_message(CHANNEL_ID, price)

# Schedule task every minute
schedule.every(1).minutes.do(send_price)

print("🤖 TON Price Bot is running...")

# ===============================
# MAIN LOOP
# ===============================
while True:
    schedule.run_pending()
    time.sleep(1)
