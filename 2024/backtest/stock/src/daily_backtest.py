from pykrx import stock
import time
import csv
import datetime
import pandas as pd
import pandas_ta as ta
import csv
import os


def load_csv2list(dir, name):
    encodings = ["utf-8", "euc-kr", "cp949"]
    for encoding in encodings:
        try:
            with open(os.path.join(dir, name), "r", encoding=encoding) as f:
                return [x for x in csv.reader(f)][1:]
        except UnicodeDecodeError:
            continue
    raise Exception(f"Failed to read file with encodings: {encodings}")


def load_csv2pd(dir, name):
    encodings = ["utf-8", "euc-kr", "cp949"]
    for encoding in encodings:
        try:
            return pd.read_csv(os.path.join(dir, name), encoding=encoding)
        except UnicodeDecodeError:
            continue
    raise Exception(f"Failed to read file with encodings: {encodings}")


def get_ema(df, length):
    df = df.rename(columns={"종가": "close"})
    return df.ta.ema(length)


def load_params(dir, name):
    return load_csv2list(dir, name)[-1]


def csv_writer(data, file_name):
    with open(
        f"../daily_result/{file_name}.csv", mode="a", encoding="utf-8", newline=""
    ) as file:
        writer = csv.writer(file)
        writer.writerow(data)


def back_test(
    open_data,
    high_data,
    low_data,
    close_data,
    time_data,
    ema_8,
    ema_16,
    tail_d,
    body_d,
    param_1,
    param_2,
    ticker_name,
):
    is_long = False
    # slippage = 1
    slippage = 0.995

    long_entry_price = []
    trade_log = []
    long_sl = []
    long_tp = []

    long_entry_time = ""

    for i in range(len(close_data) - 1):
        low_ = low_data[i]
        close_ = close_data[i]
        short_ema = ema_8[i]
        long_ema = ema_16[i]
        open_ = open_data[i]

        if open_data[i] == 0 or open_data[i + 1] == 0:
            continue

        if is_long == False:
            if (
                low_ < short_ema
                and min(close_, open_) > short_ema
                and short_ema > long_ema
            ):
                if body_d[i] * param_1 < tail_d[i]:
                    is_long = True
                    long_entry_price.append(open_data[i + 1])
                    long_sl.append(low_)
                    long_tp.append(
                        open_data[i + 1] + param_2 * abs((low_ - max(close_, open_)))
                    )
                    long_entry_time = time_data[i]
        else:
            if low_ < long_sl[-1]:
                is_long = False
                earning = 100 * (long_sl[-1] / long_entry_price[-1] * slippage - 1)
                exit_time = time_data[i]
                data = [ticker_name, exit_time, earning]
                csv_writer(data, long_entry_time)

            elif high_data[i] > long_tp[-1]:
                is_long = False
                earning = 100 * (long_tp[-1] / long_entry_price[-1] * slippage - 1)
                exit_time = time_data[i]
                data = [ticker_name, exit_time, earning]
                csv_writer(data, long_entry_time)


if __name__ == "__main__":
    os.makedirs("../daily_result", exist_ok=True)

    target_dir = "../csv_raw_file"
    params_dir = "../post_result"
    file_names = sorted(os.listdir(params_dir))

    for file_name in file_names:

        if "스팩" in file_name:
            continue

        print(f"start : {file_name}")

        ohlc_list = load_csv2list(target_dir, file_name)
        ohlc_df = load_csv2pd(target_dir, file_name)

        ema_8 = get_ema(ohlc_df, length=8)
        ema_16 = get_ema(ohlc_df, length=16)

        tail_d = []
        body_d = []

        time_data = []
        open_data = []
        high_data = []
        low_data = []
        close_data = []

        for ohlc in ohlc_list:
            o, h, l, c, v = list(map(float, ohlc[1:-1]))
            tail_d.append(min(c, o) - l)
            body_d.append(abs(c - o))
            time_data.append(ohlc[0])
            open_data.append(o)
            high_data.append(h)
            low_data.append(l)
            close_data.append(c)

        params = load_csv2list(params_dir, file_name)[-1]
        param_1 = float(params[0])
        param_2 = float(params[1])

        back_test(
            open_data,
            high_data,
            low_data,
            close_data,
            time_data,
            ema_8,
            ema_16,
            tail_d,
            body_d,
            param_1,
            param_2,
            file_name.split(".")[0],
        )
