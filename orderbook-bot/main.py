import os
import json
import requests
import websockets
import asyncio
from telegram import Bot

# Load environment variables
WEEX_API_KEY = os.getenv("WEEX_API_KEY")
WEEX_API_SECRET = os.getenv("WEEX_API_SECRET")
SYMBOL = os.getenv("SYMBOL", "SPDGUSDT")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

async def send_telegram_message(message):
    try:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as e:
        print(f"Telegram Error: {e}")

async def track_orderbook():
    url = f"wss://stream.weex.com/market/{SYMBOL.lower()}@depth"

    async with websockets.connect(url) as ws:
        print(f"Connected to WEEX order book for {SYMBOL}")
        await send_telegram_message(f"✅ Bot started: Tracking {SYMBOL} order book...")

        while True:
            data = await ws.recv()
            order_data = json.loads(data)
            best_bid = order_data['bids'][0] if order_data['bids'] else None
            best_ask = order_data['asks'][0] if order_data['asks'] else None

            if best_bid and best_ask:
                price_info = f"Best Bid: {best_bid[0]} | Best Ask: {best_ask[0]}"
                print(price_info)
                await send_telegram_message(price_info)

if __name__ == "__main__":
    asyncio.run(track_orderbook())
