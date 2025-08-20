import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta
import time
import csv
import os

time_frame_table = {
    "1m": mt5.TIMEFRAME_M1,
    "5m": mt5.TIMEFRAME_M5,
    "15m": mt5.TIMEFRAME_M15,
    "30m": mt5.TIMEFRAME_M30,
    "1h": mt5.TIMEFRAME_H1,
    "2h": mt5.TIMEFRAME_H2,
    "4h": mt5.TIMEFRAME_H4,
    "6h": mt5.TIMEFRAME_H6,
    "8h": mt5.TIMEFRAME_H8,
    "12h": mt5.TIMEFRAME_H12,
    "1d": mt5.TIMEFRAME_D1,
}

time_shift_table = {
    "1m": [1440, 86400],
    "5m": [288, 86400],
    "15m": [96, 86400],
    "30m": [48, 86400],
    "1h": [24, 86400],
    "2h": [12, 86400],
    "4h": [6, 86400],
    "6h": [4, 86400],
    "8h": [3, 86400],
    "12h": [2, 86400],
    "1d": [1, 86400],
}


def fetch_all_data(symbol, time_frame, start_time):
    result = []
    dt_obj = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
    start_pos = int(time.mktime(dt_obj.timetuple()))
    end_pos = int(time.time())  # 현재 시간까지의 데이터를 가져옵니다.

    while start_pos < end_pos:
        rates = mt5.copy_rates_range(
            symbol,
            time_frame_table[time_frame],
            start_pos,
            min(start_pos + 86400, end_pos),
        )
        if rates is None or len(rates) == 0:
            print(
                f"데이터 없음: {symbol}, 시작 시간: {datetime.fromtimestamp(start_pos)}"
            )
            start_pos += 86400  # 다음 날로 이동
            continue
        result.extend(rates)
        start_pos = int(rates[-1]["time"]) + 60  # 마지막 데이터의 다음 분부터 시작
        time.sleep(0.1)  # API 호출 사이에 짧은 대기 시간 추가

    result.sort(key=lambda x: x["time"])  # 시간순으로 정렬
    return result


def write_csv(data, time_frame, symbol):
    filename = f"{symbol}_{time_frame}.csv"
    mode = "a" if os.path.exists(filename) else "w"
    with open(filename, mode, newline="") as f:
        writer = csv.writer(f)
        if mode == "w":
            writer.writerow(
                [
                    "time",
                    "open",
                    "high",
                    "low",
                    "close",
                    "volume",
                    "spread",
                    "real_volume",
                ]
            )

        for row in data:
            writer.writerow(
                [
                    datetime.fromtimestamp(row["time"]),
                    row["open"],
                    row["high"],
                    row["low"],
                    row["close"],
                    row["tick_volume"],
                    row["spread"],
                    row["real_volume"],
                ]
            )


def find_last_data_time(symbol, time_frame):
    filename = f"{symbol}_{time_frame}.csv"
    if not os.path.exists(filename):
        return "2000-01-01 00:00"

    with open(filename, "r") as f:
        lines = f.readlines()
        if len(lines) > 1:
            last_line = lines[-1].strip().split(",")
            last_time = datetime.strptime(last_line[0], "%Y-%m-%d %H:%M:%S")
            return (last_time + timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M")

    return "2000-01-01 00:00"


if __name__ == "__main__":
    if not mt5.initialize():
        print("초기화 실패, 에러 코드 =", mt5.last_error())
        quit()

    symbols = mt5.symbols_get()
    for symbol in symbols:
        symbol = symbol.name
        print(f"심볼: {symbol}")
        for time_frame in time_frame_table.keys():
            print(f"시간프레임: {time_frame}")
            start_time = find_last_data_time(symbol, time_frame)
            data = fetch_all_data(symbol, time_frame, start_time)
            if data:
                write_csv(data, time_frame, symbol)
                print(
                    f"{symbol}의 {time_frame} 데이터 저장 완료. 마지막 데이터 시간: {datetime.fromtimestamp(data[-1]['time'])}"
                )
            else:
                print(f"{symbol}의 {time_frame} 데이터를 가져오지 못했습니다.")

    mt5.shutdown()
