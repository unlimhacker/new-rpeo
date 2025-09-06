from flask import Flask
import threading, time, requests
import telebot, schedule

BOT_TOKEN = "8261351761:AAES_aRQ50v4SqUuAkkbqcRT9612Ngm_vLg"
CHANNEL_ID = "@tonovoi"
bot = telebot.TeleBot(BOT_TOKEN)

app = Flask(__name__)

def get_ton_price():
    try:
        data = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=usd").json()
        return f"TON Price: ${data['the-open-network']['usd']}"
    except:
        return "Error getting TON price"

def send_price():
    bot.send_message(CHANNEL_ID, get_ton_price())

# Schedule job
schedule.every(1).minutes.do(send_price)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start scheduler in background
threading.Thread(target=run_scheduler, daemon=True).start()

@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
