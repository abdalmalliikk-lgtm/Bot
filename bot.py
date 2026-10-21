import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# استخراج التوكن ومعرف الشات من متغيّرات البيئة
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("خطأ: لم يتم ضبط توكن البوت أو معرف الشات!")
        return False
        
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=payload)
        return response.ok
    except Exception as e:
        print(f"حدث خطأ أثناء إرسال الرسالة: {e}")
        return False

@app.route('/', methods=['GET'])
def home():
    return "Bot Server is Running Successfully!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_data(as_text=True)
    if data:
        send_telegram_message(data)
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "no data received"}), 400

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
