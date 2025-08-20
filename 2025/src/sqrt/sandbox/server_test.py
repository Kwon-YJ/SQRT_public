import requests
import datetime


def main(params):
    url = "http://127.0.0.1:8000/"
    response = requests.get(url, params=params)
    print(f"Status code: {response.status_code}")
    result = eval(response.text)
    print(result)
    print(len(result))
    print(result[0][0])


if __name__ == "__main__":
    # print(int(datetime.datetime(2023, 1, 1, 0, 0).timestamp() * 1000))
    params = {
        # "exchange": "binance_future",
        "exchange": "gateio_future",
        "method": "fetch_ohlcv",
        # "args": f"'BTC/USDT','1w', 1672617600000, 400",
        "args": f"'BTC/USDT','1w'",
        "kwargs": "{'limit':960}"
    }

    params = {
        "exchange": "gateio_spot",
        "method": "fetch_tickers",
    }
    main(params)


# import ccxt

# binance = ccxt.binance()
# start_time = int(datetime.datetime(2023, 1, 1, 0, 0).timestamp() * 1000)
# # start_time = # 2023-01-01
# # end_time =  # 2023-12-25
# result = binance.fetch_ohlcv("BTC/USDT", "1d", start_time, 499)
# print(len(result))
