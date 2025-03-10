import requests


bot_token = "8199237450:AAHR6iOIFQWITKTKxSQjtR66oL5Nabbrr1w"  # 🔹 توکن خودت رو جایگزین کن
chat_id = 840536018     
message = "سلام امیر! رباتت داره کار میکنه! 🚀"

url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
data = {"chat_id": chat_id, "text": message}

response = requests.post(url, data=data)
print(response.json()) 
