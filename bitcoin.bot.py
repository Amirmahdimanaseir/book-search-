import requests
import json
import time

THRESHOLD_FILE = "threshold.json"
alert_percentage = 5

def get_bitcoin_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    price = float(data["bitcoin"]["usd"])
    return round(price, 2)

def save_threshold(price):
    with open(THRESHOLD_FILE, "w") as file:
        json.dump({"threshold": price}, file)

def load_threshold():
    try:
        with open(THRESHOLD_FILE, "r") as files:
            data = json.load(files)
            return data.get("threshold", None)
    except FileExistsError:
        return None

def check_price_change():
    current_price = get_bitcoin_price()
    stored_threshold = load_threshold()

    if stored_threshold is None:
        print("change the price marjae")
        return

    change_percentage = ((current_price - stored_threshold) / stored_threshold) * 100
    print(f"💰 price moment bitcoin: {current_price} dollar")
    print(f"📊 change bitcoin prices ({stored_threshold} dollar): {round(change_percentage, 2)}%")

    if abs(change_percentage) >= alert_percentage:
        print("🚨 price changed alert")
        save_threshold(current_price)

        # ارسال پیام فقط زمانی که تغییر قیمت بیش از 5% باشد
        message = f"🚀 قیمت بیت‌کوین تغییر کرد!\n🔹 قیمت جدید: {current_price} $\n📉 قیمت قبلی: {stored_threshold} $"
        send_telegram_message(message)

def send_telegram_message(message):
    bot_token = "8199237450:AAHR6iOIFQWITKTKxSQjtR66oL5Nabbrr1w"  # توکن خودت رو جایگزین کن
    chat_id = 840536018  # آیدی چت خودت رو جایگزین کن
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}

    response = requests.post(url, data=data)
    print(response.json())  # برای دیباگ

    return response.json()

def get_stored_price():
    try:
        with open("price_data.txt", "r") as file:
            return float(file.read().strip())
    except FileNotFoundError:
        return None

def save_price(price):
    with open("price_data.txt", "w") as file:
        file.write(str(price))

def check_price():
    current_price = get_bitcoin_price()
    stored_price = get_stored_price()

    if stored_price is None:
        save_price(current_price)
        return

    threshold = 3
    if abs(current_price - stored_price) >= threshold:
        message = f"🚀 قیمت بیت‌کوین تغییر کرد!\n🔹 قیمت جدید: {current_price} $\n📉 قیمت قبلی: {stored_price} $"
        send_telegram_message(message)
        save_price(current_price)

while True:
    check_price_change()
    time.sleep(80)
