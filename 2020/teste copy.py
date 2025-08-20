import ccxt
import pandas as pd
import urllib.request
import json
import time

# 123

"""
def ATR(data, length):
	TR = []
	ATR_ = []
	for i in range(length):
	# for i in range(len(data)):
		TR.append(max((data[i - length][2] - data[i - length][3]), abs(data[i - length][2] - data[i - length - 1][4]), abs(data[i - length][3] - data[i - length -1][4])))
	i = 0
	while(i < len(TR)):
		if i == 0:
			ATR_.append(TR[i])
		else:
			ATR_.append((TR[i] * 1/length) + (ATR_[i-1] * (1 - 1/length)))
		i += 1
	return ATR_
"""


exchange_class = getattr(ccxt, "binance")
binance = exchange_class(
    {
        "urls": {
            "api": {
                "public": "https://fapi.binance.com/fapi/v1",
                "private": "https://fapi.binance.com/fapi/v1",
            },
        }
    }
)

binance.enableRateLimit = True
binance.RateLimit = 10000
binance.load_markets()


ticker_list = list(binance.fetch_tickers().keys())


def ATR(data, length):
    TR = []
    for i in range(int(length)):
        TR.append(
            max(
                (data[i - length][2] - data[i - length][3]),
                abs(data[i - length][2] - data[i - length - 1][4]),
                abs(data[i - length][3] - data[i - length - 1][4]),
            )
        )
    ATR = pd.Series(TR).rolling(length).mean()
    return ATR.tolist()


def ma(data, length):
    result = []
    for i in range(len(data)):
        result.append(data[i][4])
    return pd.Series(result).rolling(length).mean().tolist()


"""
for i in range(len(ticker_list)):
	try:
		a = binance.fetch_ohlcv(ticker_list[i], '1h')
		b = ma(a, 20)[-1]
		c = ATR(a, 9)[-1] * 1.9
		
		if (a[-1][4] + a[-1][1]) / 2 > b+c and (a[-2][4] + a[-2][1]) / 2 < b+c:
			print(ticker_list[i])
	except:
		print('err', ticker_list[i])
		continue
"""


while 1:
    time.sleep(1)
    # url = 'https://fapi.binance.com/fapi/v1/premiumIndex'
    url = "https://www.binance.com/kr/futures/legacy/FILUSDT"

    text_data = urllib.request.urlopen(url).read().decode("utf-8")
    # tickers = json.loads(text_data)

    target = "이 가격이 PNL과 마진 계산을 위해 사용됩니다"

    index = text_data.find(target)

    print(text_data[index + len(target) : index + len(target) + 120])
