import ccxt
import time
import numpy as np
import pandas as pd
import datetime
import pandas_ta as ta
import json
import parmap
import urllib
import multiprocessing
import telegram


# ccxt ex.fetch_ohlcv() 보다 훨씬 빠르게 ohlcv 얻기
def get_ohlcv(ticker="BTC/USDT", interval="1m", limit=200):
    try:
        temp = ticker.split("/")
        ticker = f"{temp[0]}{temp[1]}"
        url = f"https://fapi.binance.com/fapi/v1/klines?symbol={ticker}&interval={interval}&limit={str(limit)}"  # monitoring
        # url = f'https://api.binance.com/api/v3/klines?symbol={ticker}&interval={interval}&limit={str(limit)}' # monitoring
        text_data = urllib.request.urlopen(url).read().decode("utf-8")
        output = json.loads(text_data)
    except Exception as e:
        print(
            e,
            "\n",
            "ccxt.base.errors.BadSymbol: binance does not have market symbol {0}".format(
                ticker
            ),
        )
        return None
    output = [list(map(float, output[i])) for i in range(len(output))]
    return output


# get_time()[0] = 오늘 날짜 str
# get_time()[1] = 현재 시각 str
def get_time():
    now = datetime.datetime.now()
    YYYY = str(now.year)
    MM = str(now.month)
    DD = str(now.day)
    hh = str(now.hour)
    mm = str(now.minute)

    if len(MM) != 2:
        MM = "0" + MM
    if len(DD) != 2:
        DD = "0" + DD
    if len(hh) != 2:
        hh = "0" + hh
    if len(mm) != 2:
        mm = "0" + mm

    return YYYY + MM + DD, hh + mm


# 매수 종목 선정하기
def get_target(item):
    try:
        ohlcv_temp = get_ohlcv(item, "15m", 800)
        df = pd.DataFrame(
            data=np.array(ohlcv_temp),
            columns=["0", "0", "close", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
        )  ## rsi(15, high)
        rsi_entry = df.ta.rsi(length=15).tolist()
        # if rsi_entry[-2] < 23 and ohlcv_temp[-1][1] > ohlcv_temp[-1][4] and ohlcv_temp[-1][5] > ohlcv_temp[-2][5] and ohlcv_temp[-1][5] > ohlcv_temp[-3][5]:
        if (
            rsi_entry[-3] < 21
            and ohlcv_temp[-2][1] > ohlcv_temp[-2][4]
            and ohlcv_temp[-2][5] > ohlcv_temp[-3][5]
            and ohlcv_temp[-2][5] > ohlcv_temp[-4][5]
        ):
            # if rsi_entry[-2] < 23:
            return item
    except Exception as e:
        print(e)
        time.sleep(0.1)
        return None


def get_tickers():
    base_ticker = list(binance.fetch_tickers().keys())
    base_ticker = [
        base_ticker[i] for i in range(len(base_ticker)) if "/USDT" in base_ticker[i]
    ]
    base_ticker.remove("BTCDOM/USDT")
    time.sleep(60)
    return base_ticker


def telegram_send(data):
    bot = telegram.Bot(token=my_token)
    if type(data) != "str":
        data = str(data)
    while 1:
        try:
            bot.send_message(chat_id=801167350, text=data)
            time.sleep(3)
            return None
        except:
            continue


"""
exchange_class = getattr(ccxt, 'binance')
binance = exchange_class()
binance.enableRateLimit = False
binance.RateLimit = 10000
binance.apiKey = 'bOHcvOmxqFVGN6FPsJwcnh4QOxw0D6oaFGHjEhpU2pby1bt7EJDb6t9TExauOccU'
binance.secret = 'Yece0g5APcAZR4sXJl1M007tLL9w9bB7Qp2o3fGFYJjN3f6tfx6lOCq1LdmRk4Ob'
binance.load_markets()
"""

binance = ccxt.binance(
    {
        "options": {"defaultType": "future"},
        "timeout": 30000,
        "apiKey": "bOHcvOmxqFVGN6FPsJwcnh4QOxw0D6oaFGHjEhpU2pby1bt7EJDb6t9TExauOccU",
        "secret": "Yece0g5APcAZR4sXJl1M007tLL9w9bB7Qp2o3fGFYJjN3f6tfx6lOCq1LdmRk4Ob",
        "enableRateLimit": False,
    }
)
binance.load_markets()


ticker_list = list(binance.fetch_tickers().keys())

# ticker_list = ['BAKE/USDT', 'NKN/USDT', 'XEM/USDT', 'LRC/USDT', 'ZEC/USDT', 'LINA/USDT', 'YFI/USDT', 'RVN/USDT', 'QTUM/USDT', 'SXP/USDT', 'CVC/USDT', 'CHZ/USDT', 'REEF/USDT', 'FIL/USDT', 'MTL/USDT', 'XRP/USDT', 'MATIC/USDT', 'COTI/USDT', 'NEO/USDT', 'ALGO/USDT', 'HBAR/USDT', 'BAT/USDT', 'REN/USDT', 'ADA/USDT', 'AVAX/USDT', 'HOT/USDT', 'TRX/USDT', 'AXS/USDT', 'AKRO/USDT', 'SC/USDT', 'ALPHA/USDT', 'KNC/USDT', 'CHR/USDT', 'AUDIO/USDT', 'NU/USDT', 'XTZ/USDT', 'KSM/USDT', 'BTS/USDT', 'HNT/USDT', 'DASH/USDT', 'ICP/USDT', 'DGB/USDT', 'DOGE/USDT', 'MASK/USDT', 'ARPA/USDT', 'VET/USDT', 'AAVE/USDT', 'IOTX/USDT', 'SRM/USDT', 'ONE/USDT', 'RLC/USDT', 'NEAR/USDT', 'GTC/USDT', 'STORJ/USDT', 'EGLD/USDT', 'WAVES/USDT', 'AR/USDT', 'ETH/USDT', '1INCH/USDT', 'EOS/USDT', 'LUNA/USDT', 'UNFI/USDT', 'SUSHI/USDT', 'RSR/USDT', 'OMG/USDT', 'IOTA/USDT', 'DODO/USDT', 'CRV/USDT', 'ICX/USDT', 'ALICE/USDT', 'OGN/USDT', 'RAY/USDT', 'BCH/USDT', 'FTM/USDT', 'BLZ/USDT', 'BNB/USDT', 'KAVA/USDT', 'SKL/USDT', 'SOL/USDT', 'OCEAN/USDT', 'BTC/USDT', 'LINK/USDT', 'SAND/USDT', 'ZRX/USDT', 'C98/USDT', 'XLM/USDT', 'GALA/USDT', 'ANKR/USDT', 'MANA/USDT', 'TRB/USDT', 'BTT/USDT', 'THETA/USDT', 'UNI/USDT', 'STMX/USDT', 'KEEP/USDT', 'IOST/USDT', 'BAND/USDT', 'KLAY/USDT', 'ETC/USDT', 'ZIL/USDT', 'CTSI/USDT', 'ENJ/USDT', 'LTC/USDT', 'BZRX/USDT', 'RUNE/USDT', 'DYDX/USDT', 'CTK/USDT', 'LIT/USDT', 'SFP/USDT', 'ATOM/USDT', 'ZEN/USDT', 'TOMO/USDT', 'YFII/USDT', 'FLM/USDT', '1000XEC/USDT', 'CELO/USDT', 'ATA/USDT', 'BEL/USDT', 'COMP/USDT', 'ONT/USDT', 'TLM/USDT', 'DOT/USDT', 'GRT/USDT', 'XMR/USDT', 'MKR/USDT', 'CELR/USDT', 'BAL/USDT', 'DENT/USDT', 'SNX/USDT']

if __name__ == "__main__":
    while 1:
        while True:
            time.sleep(2)
            now = int(get_time()[1][-2:])
            if now % 15 == 0:
                break

        target_list = parmap.map(get_target, ticker_list, pm_pbar=False, pm_processes=8)
        target_list = list(set(target_list) - set([None]))
        telegram_send(target_list)
        print(target_list)

        time.sleep(59.5)
