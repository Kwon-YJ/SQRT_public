import ccxt
import pandas as pd
from urllib.request import Request, urlopen
import urllib.request
import json
import time

from bs4 import BeautifulSoup

import requests

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

"""
while(1):
	time.sleep(1)
	# url = 'https://fapi.binance.com/fapi/v1/premiumIndex'
	url = 'https://www.binance.com/kr/futures/legacy/FILUSDT'

	text_data = urllib.request.urlopen(url).read().decode('utf-8')
	# tickers = json.loads(text_data)


	target = '이 가격이 PNL과 마진 계산을 위해 사용됩니다'

	index = text_data.find(target)

	print(text_data[index+len(target):index+len(target)+120])
"""
"""
import os
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



display = Display(visible=0, size=(1920, 1080))
display.start()
path="/usr/lib/chromium-browser/chromedriver"
driver = webdriver.Chrome(path)
driver.maximize_window()
driver.implicitly_wait(10)
# URL = 'https://upbit.com/service_center/notice'
URL = 'https://upbit.com/service_center/notice?id=1617'



driver.get(URL)
# wait = WebDriverWait(driver, 10)
# element = wait.until(EC.element_to_be_clickable((By.ID, 'bgWhite')))

WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.bgWhite'))
    )

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
print(soup.text)
"""


req = Request(
    "https://api-manager.upbit.com/api/v1/notices?page=1&per_page=20&thread_name=general",
    headers={"User-Agent": "Chrome/66.0.3359.181"},
)
webpage = urlopen(req).read().decode("utf-8")

json.loads(webpage)
len_ = len(webpage)


while 1:
    time.sleep(1)
    req = Request(
        "https://api-manager.upbit.com/api/v1/notices?page=1&per_page=20&thread_name=general",
        headers={"User-Agent": "Chrome/66.0.3359.181"},
    )
    webpage = urlopen(req).read().decode("utf-8")

    json.loads(webpage)
    if len(webpage) != len_:
        print("diff")


# 웹사이트의 글자수를 비교하여 다르게 될 경우 https://upbit.com/service_center/notice + {공지 페이지 넘버} 를 텔레그램으로 전송하는 프로그램 (미완성)
