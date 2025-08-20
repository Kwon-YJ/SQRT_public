import websocket
import json
import rel
import datetime
import time

import threading

global_list = []


class WsHandler:
    def __init__(self):
        pass

    def on_message(self, ws, message):
        obj = json.loads(message)
        # print(obj["u"], obj["U"])
        # print(obj["a"][0])
        global_list.append(obj["a"][0])

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")

    def on_open(self, ws):
        print("Opened connection")

    def wsDiffDepthStream(self, ticker):
        # websocket.enableTrace(True)
        ws = websocket.WebSocketApp(
            f"wss://stream.binance.com:9443/ws/{ticker}@depth@1000ms",
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )

        ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
        rel.signal(2, rel.abort)  # Keyboard Interrupt
        rel.dispatch()


def check_orderbook():
    while 1:
        try:
            time.sleep(1)
            print(global_list[-1])
        except:
            print("err")
            time.sleep(1)


if __name__ == "__main__":
    ws_thread = threading.Thread(target=check_orderbook)
    ws_thread.start()
    inst = WsHandler()
    inst.wsDiffDepthStream("btcusdt")
