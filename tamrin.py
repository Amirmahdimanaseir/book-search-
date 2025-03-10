import requests

bot_token = "8199237450:AAHR6iOIFQWITKTKxSQjtR66oL5Nabbrr1w"  # 🔹 جایگزین کن با توکن خودت
url = f"https://api.telegram.org/bot{bot_token}/getUpdates"

response = requests.get(url)
print(response.json())  # خروجی رو ببین
