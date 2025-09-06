import os
import requests
from flask import Flask, request

# =========================
# CONFIG
# =========================
TOKEN = "8034673353:AAGPFeh1cXlWllpQGDKJpBUUv1baBaAekxw"
APP_URL = "https://instabot-2-gu4t.onrender.com"
TELEGRAM_API = f"https://api.telegram.org/bot{TOKEN}"

app = Flask(__name__)

# =========================
# ROUTES
# =========================
@app.route("/", methods=["GET"])
def home():
    return "🤖 InstaBot is running on Render!"

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json()
    print("📩 Incoming update:", update)

    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        if text.startswith("http"):
            requests.post(
                f"{TELEGRAM_API}/sendMessage",
                json={"chat_id": chat_id, "text": f"✅ Got your link: {text}"}
            )
        else:
            requests.post(
                f"{TELEGRAM_API}/sendMessage",
                json={"chat_id": chat_id, "text": "❌ Please send me a valid link."}
            )

    return {"ok": True}

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    print("🚀 Starting bot in WEBHOOK mode...")

    # Auto-set the webhook
    webhook_url = f"{APP_URL}/webhook/{TOKEN}"
    r = requests.get(f"{TELEGRAM_API}/setWebhook", params={"url": webhook_url})
    print("🔗 Webhook setup:", r.json())

    app.run(host="0.0.0.0", port=5000)
