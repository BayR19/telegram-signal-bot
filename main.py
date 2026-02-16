import os
import time
import requests
from telegram import Bot

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

COINS = ["ZEC-USDT", "SYRUP-USDT", "PENGU-USDT"]
INTERVAL = 60

def get_price(symbol: str):
    url = "https://open-api.bingx.com/openApi/swap/v2/quote/price"
    r = requests.get(url, params={"symbol": symbol}, timeout=10)
    data = r.json()
    if data.get("code") != 0:
        raise Exception(data)
    return float(data["data"]["price"])

def main():
    if not TOKEN or not CHAT_ID:
        raise RuntimeError("BOT_TOKEN ve CHAT_ID Railway Variables içinde olmalı.")

    bot = Bot(token=TOKEN)
    bot.send_message(chat_id=CHAT_ID, text="✅ Bot çalıştı.")

    while True:
        lines = []
        for c in COINS:
            try:
                p = get_price(c)
                lines.append(f"{c}: {p}")
            except Exception as e:
                lines.append(f"{c}: hata")
        bot.send_message(chat_id=CHAT_ID, text="📈\n" + "\n".join(lines))
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
