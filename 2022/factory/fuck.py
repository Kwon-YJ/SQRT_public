# -*- coding:utf-8 -*-
import Utils
import time
import datetime


def main():
    binance = Utils.use_binance("future")
    ticker = "XRP/BUSD"
    target_price_log = [1]
    id = []
    while 1:
        if len(id) != 0:
            time.sleep(0.6)
            if binance.fetch_order_status(id[-1], ticker) != "open":
                Utils.telegram_send(f"buy {ticker}")
                wallet_data = binance.fetch_balance()
                LUNA_amount = wallet_data[ticker]["free"]
                # sell_order = binance.create_limit_sell_order(ticker, LUNA_amount, float(request['price'])*1.0049)
                sell_order = binance.create_limit_sell_order(
                    ticker, LUNA_amount, float(request["price"]) * 1.0033
                )
                while 1:
                    time.sleep(5)
                    wallet_data = binance.fetch_balance()
                    BUSD_margin = wallet_data["BUSD"]["free"]
                    if float(BUSD_margin) > 5000:
                        return None
        ohlcv_temp = binance.fetch_ohlcv(ticker, "1m", None, 2)
        high = ohlcv_temp[0][2]  # D-2 high
        low = ohlcv_temp[0][3]  # D-2 low
        close = ohlcv_temp[0][4]  # D-2 close
        # PP = (high + low + (close*4) ) / 6
        PP = (high + low + (close * 1)) / 3
        # target_price = 1.9777 * PP - high
        # target_price = 1.9775 * PP - high
        target_price = 1.984 * PP - high
        if target_price_log[-1] != target_price:
            # print(target_price, target_price*1.009)
            target_price_log.append(target_price)
            # wallet_data = binance.fetch_balance()
            # free_useable_dot = wallet_data['BUSD']['free']
            free_useable_dot = 5100
            if len(id) != 0:
                binance.cancel_order(id[-1], ticker)
                print("cancle finish", datetime.datetime.now())
            time.sleep(3.5)
            amount = free_useable_dot / ohlcv_temp[-1][4] * 0.9999
            request = binance.create_limit_buy_order(ticker, amount, target_price)
            print("buy finish", datetime.datetime.now())
            # print(request)
            # exit()
            id.append(request["info"]["orderId"])


if __name__ == "__main__":
    while 1:
        time.sleep(10)
        main()
