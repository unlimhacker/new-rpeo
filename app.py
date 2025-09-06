import os
import telebot
from flask import Flask, request
import yt_dlp

# Telegram bot token
TOKEN = "8261351761:AAES_aRQ50v4SqUuAkkbqcRT9612Ngm_vLg"
APP_URL = f"https://new-rpeo.onrender.com/{TOKEN}"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- Handlers ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Hello! Send me any Instagram or TikTok link and I’ll download it for you.")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    url = message.text.strip()

    if not (url.startswith("http://") or url.startswith("https://")):
        bot.reply_to(message, "❌ Please send a valid Instagram or TikTok link.")
        return

    bot.reply_to(message, "⏳ Downloading... Please wait.")

    try:
        # Download settings
        ydl_opts = {
            'format': 'mp4',
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'quiet': True,
        }

        os.makedirs("downloads", exist_ok=True)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        # Send video back to Telegram
        with open(file_path, 'rb') as video:
            bot.send_video(message.chat.id, video, caption="✅ Here is your video!")

        # Cleanup
        os.remove(file_path)

    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {e}")

# --- Webhook ---
@app.route(f'/{TOKEN}', methods=['POST'])
def get_message():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/", methods=['GET'])
def index():
    return "🤖 InstaBot is running!"

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    app.run(host="0.0.0.0", port=10000)

