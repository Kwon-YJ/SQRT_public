from pybit.unified_trading import WebSocket
import time
from datetime import datetime

ws = WebSocket(
    testnet=False,
    channel_type="linear",
)


def handle_message(message):
    a = time.time()
    try:
        ticker = message["data"]["s"]
        # price = message["data"]["a"][1]
        time_ = datetime.fromtimestamp(message["cts"] / 1000)
        print(f"{ticker}\n{time_}\n{datetime.now()}")
    except Exception as e:
        print(e)
    print(time.time() - a)


ws.orderbook_stream(1, ["BTCUSDT", "XRPUSDT"], handle_message)


while True:
    time.sleep(10)
