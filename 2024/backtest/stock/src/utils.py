from pykrx import stock
import time
import csv
import os


def data_saver():
    ticker_list = stock.get_market_ticker_list("20250112", market="ALL")
    for ticker in ticker_list:
        ticker_name = stock.get_market_ticker_name(ticker)
        df = stock.get_market_ohlcv("20001210", "20251112", ticker)
        # save_dir = os.path.join(os.path.abspath(__file__), "csv_raw_file", f"{ticker_name}.csv")
        df.to_csv(f"./csv_raw_file/{ticker_name}.csv")
        time.sleep(1)


os.makedirs("./csv_raw_file", exist_ok=True)
data_saver()
