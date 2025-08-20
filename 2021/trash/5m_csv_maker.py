import datetime
import time
import ccxt
import csv


def calculate(ticker, time_):
    # if len(basis) > 10000:
    #    return None
    ohlcv = binance.fetch_ohlcv(ticker, "5m", binance.parse8601(time_))

    for i in range(1, len(ohlcv) + 1):
        basis.append(ohlcv[-i])

    timestamp = ohlcv[0][0] - 182500000
    datetimeobj = str(datetime.datetime.fromtimestamp(timestamp / 1000))
    nexttime = datetimeobj[0:10] + "T" + datetimeobj[11:19]

    try:
        calculate(ticker, nexttime)
    except:
        print(" ")


binance = ccxt.binance()
basis = []
start = "2021-02-19T00:00:00"  # today-1
calculate("BTC/USDT", start)

f = open("result.csv", "w", encoding="euc-kr", newline="")
wr = csv.writer(f)

try:
    i = 1
    while len(basis):
        if i == 0:
            wr.writerow(["time", "Open", "High", "low", "Close"])
        # wr.writerow([basis[i], basis[i+1], basis[i+2], basis[i+3], basis[i+4]])
        wr.writerow(
            [
                datetime.datetime.fromtimestamp(basis[-i][0] / 1000),
                basis[-i][1],
                basis[-i][2],
                basis[-i][3],
                basis[-i][4],
            ]
        )
        i = i + 5
except:
    print("프로그램 실행 완료")
f.close()
