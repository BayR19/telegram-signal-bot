import os
import asyncio
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

async def main():
    if not TOKEN or not CHAT_ID:
        raise RuntimeError("BOT_TOKEN ve CHAT_ID Railway Variables içinde olmalı.")

    bot = Bot(token=TOKEN)
    chat_id = int(CHAT_ID)  # string geliyorsa garanti olsun

    await bot.send_message(chat_id=chat_id, text="✅ Bot çalıştı.")

    while True:
        lines = []
        for c in COINS:
            try:
                p = get_price(c)
                lines.append(f"{c}: {p}")
            except Exception:
                lines.append(f"{c}: hata")
        await bot.send_message(chat_id=chat_id, text="📈\n" + "\n".join(lines))
        await asyncio.sleep(INTERVAL)

if __name__ == "__main__":
    asyncio.run(main())
