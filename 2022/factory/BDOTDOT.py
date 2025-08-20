import Utils
import time

if __name__ == "__main__":

    binance = Utils.use_binance()
    ticker = "BDOT/DOT"
    timeframe = "1h"
    is_orderd = False

    while 1:
        # time.sleep(30)

        bdotdot = binance.fetch_ohlcv(ticker, timeframe, None, 12)
        max_high = max([ohlcv[2] for ohlcv in bdotdot])
        min_low = min([ohlcv[3] for ohlcv in bdotdot])
        buy_price = round(0.27 * (max_high - min_low) + min_low, 4)
        sell_price = round(0.73 * (max_high - min_low) + min_low, 4)

        print(buy_price, sell_price)

        exit()

        wallet_data = binance.fetch_balance()
        free_useable_dot = wallet_data["DOT"]["free"]
        amount = free_useable_dot / bdotdot[-1][4] * 0.99
        if is_orderd == False:
            request = binance.create_limit_buy_order(ticker, amount, buy_price)
            id = request["info"]["orderId"]
            is_orderd = True
        state = binance.fetch_order_status(id, "BDOT/DOT")
        time.sleep(30)
        if state != "open":
            is_orderd = False
            break

    while 1:
        bdotdot = binance.fetch_ohlcv(ticker, timeframe, None, 12)
        max_high = max([ohlcv[2] for ohlcv in bdotdot])
        min_low = min([ohlcv[3] for ohlcv in bdotdot])
        sell_price = round(0.73 * (max_high - min_low) + min_low, 4)
        wallet_data = binance.fetch_balance()
        free_useable_bdot = wallet_data["BDOT"]["free"]
        amount = free_useable_bdot * 0.99
        if is_orderd == False:
            request = binance.create_limit_sell_order(ticker, amount, sell_price)
            id = request["info"]["orderId"]
            is_orderd = True
        state = binance.fetch_order_status(id, "BDOT/DOT")
        time.sleep(30)
        if state != "open":
            is_orderd = False
            break

        time.sleep(30)
