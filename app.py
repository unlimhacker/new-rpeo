import os
import telebot
from flask import Flask, request
import requests
import yt_dlp

# === CONFIG ===
TOKEN = "8261351761:AAES_aRQ50v4SqUuAkkbqcRT9612Ngm_vLg"
APP_URL = "https://new-rpeo.onrender.com" + TOKEN

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# === ROUTES ===
@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@app.route('/')
def webhook():
    return "🤖 InstaBot is live on Render!", 200

# === HANDLERS ===
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Hello! Send me any Instagram or TikTok link and I’ll download it for you.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text.strip()

    if not (url.startswith("http://") or url.startswith("https://")):
        bot.reply_to(message, "⚠️ Please send a valid Instagram or TikTok link.")
        return

    msg = bot.reply_to(message, "⏳ Downloading... Please wait.")

    try:
        # yt-dlp options
        ydl_opts = {
            "format": "mp4",
            "outtmpl": "video.%(ext)s",
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        # send video
        with open(file_path, "rb") as f:
            bot.send_video(message.chat.id, f, caption="✅ Here’s your video!")

        os.remove(file_path)

        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ Error: {str(e)}", message.chat.id, msg.message_id)


# === AUTO WEBHOOK SETUP ===
if __name__ == "__main__":
    # Remove old webhook (if exists)
    requests.get(f"https://api.telegram.org/bot{TOKEN}/deleteWebhook")

    # Set new webhook
    set_hook = requests.get(
        f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={APP_URL}"
    )

    if set_hook.status_code == 200:
        print("✅ Webhook set successfully!")
    else:
        print("❌ Webhook setup failed:", set_hook.text)

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
