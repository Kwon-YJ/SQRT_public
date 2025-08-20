import multiprocessing
import pandas_ta as ta
import pandas as pd
import numpy as np
import datetime
import urllib
import parmap
import ccxt
import time
import json


# ccxt ex.fetch_ohlcv() 보다 훨씬 빠르게 ohlcv 얻기
def get_ohlcv(ticker='BTC/USDT', interval='1m', limit=200):
    cdef int i = 0
    try:
        temp = ticker.split('/')
        ticker = f'{temp[0]}{temp[1]}'
        url = f'https://api.binance.com/api/v3/klines?symbol={ticker}&interval={interval}&limit={str(limit)}'
        text_data = urllib.request.urlopen(url).read().decode('utf-8')
        result = json.loads(text_data)
    # except Exception as e:
    except:
        # print(e, '\n', 'ccxt.base.errors.BadSymbol: binance does not have market symbol {0}'.format(ticker))
        return [[0]]
    result = [list(map(float,result[i])) for i in range(len(result))]
    return result

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
        MM = '0' + MM
    if len(DD) != 2:
        DD = '0' + DD
    if len(hh) != 2:
        hh = '0' + hh
    if len(mm) != 2:
        mm = '0' + mm

    return YYYY + MM + DD, hh + mm

# 매수 수량 얻기
def get_amount(ticker):
    price = binance.fetch_ohlcv(ticker)[-1][4]
    total_money = 80
    result = total_money / price
    return binance.amount_to_precision(ticker, amount = result)

# 매수 주문 실행
def buy_order(ticker):
    buy_amount = get_amount(ticker)
    order = binance.create_order(ticker , 'market', 'buy', buy_amount)
    is_entering[ticker] = float(order['amount'])


# 매수 종목 선정하기
def get_target(item):
    try:
        ohlcv_temp = get_ohlcv(item, '15m', 150)
        df = pd.DataFrame(data=np.array(ohlcv_temp), columns=['0','0', 'close', '0', '0', '0','0', '0', '0','0', '0', '0']) ## rsi(15, high)
        rsi_entry = df.ta.rsi(length=15).tolist()
        if rsi_entry[-2] < 19 and item not in list(is_entering.keys()):
            return item
    # except Exception as e:
    except:
        time.sleep(0.1)
    return None

binance = ccxt.binance({
    "options": {"defaultType": "future"},
    "timeout": 30000,
    "apiKey":"f6LEy0POPdaukqwlrnC4KvJbGWkcXRfVmKbsPmFAaPlyL2Rytswf7ilTa3kAjnQh",
    "secret": "sLvrd7ZT6c49yZVlnFRhPvJcIg8z39S6dVwZcIfPhFueA5BAy5UpTT3ZbVZg9zA2",
    "enableRateLimit": False,
})
binance.load_markets()

is_entering = {}

if __name__ == '__main__':
    
    ticker_list = ['BTC/USDT', 'ETH/USDT', 'BCH/USDT', 'XRP/USDT', 'EOS/USDT', 'LTC/USDT', 'TRX/USDT', 'ETC/USDT', 'LINK/USDT', 'XLM/USDT', 'ADA/USDT', 'XMR/USDT', 'DASH/USDT', 'ZEC/USDT', 'XTZ/USDT', 'BNB/USDT', 'ATOM/USDT', 'ONT/USDT', 'IOTA/USDT', 'BAT/USDT', 'VET/USDT', 'NEO/USDT', 'QTUM/USDT', 'IOST/USDT', 'THETA/USDT', 'ALGO/USDT', 'ZIL/USDT', 'KNC/USDT', 'ZRX/USDT', 'COMP/USDT', 'OMG/USDT', 'DOGE/USDT', 'SXP/USDT', 'KAVA/USDT', 'BAND/USDT', 'RLC/USDT', 'WAVES/USDT', 'MKR/USDT', 'SNX/USDT', 'DOT/USDT', 'DEFI/USDT', 'YFI/USDT', 'BAL/USDT', 'CRV/USDT', 'TRB/USDT', 'YFII/USDT', 'RUNE/USDT', 'SUSHI/USDT', 'SRM/USDT', 'BZRX/USDT', 'EGLD/USDT', 'SOL/USDT', 'ICX/USDT', 'STORJ/USDT', 'BLZ/USDT', 'UNI/USDT', 'AVAX/USDT', 'FTM/USDT', 'HNT/USDT', 'ENJ/USDT', 'FLM/USDT', 'TOMO/USDT', 'REN/USDT', 'KSM/USDT', 'NEAR/USDT', 'AAVE/USDT', 'FIL/USDT', 'RSR/USDT', 'LRC/USDT', 'MATIC/USDT', 'OCEAN/USDT', 'CVC/USDT', 'BEL/USDT', 'CTK/USDT', 'AXS/USDT', 'ALPHA/USDT', 'ZEN/USDT', 'SKL/USDT', 'GRT/USDT', '1INCH/USDT', 'AKRO/USDT', 'CHZ/USDT', 'SAND/USDT', 'ANKR/USDT', 'LUNA/USDT', 'BTS/USDT', 'LIT/USDT', 'UNFI/USDT', 'DODO/USDT', 'REEF/USDT', 'RVN/USDT', 'SFP/USDT', 'XEM/USDT', 'COTI/USDT', 'CHR/USDT', 'MANA/USDT', 'ALICE/USDT', 'HBAR/USDT', 'ONE/USDT', 'LINA/USDT', 'STMX/USDT', 'DENT/USDT', 'CELR/USDT', 'HOT/USDT', 'MTL/USDT', 'OGN/USDT', 'BTT/USDT', 'NKN/USDT', 'SC/USDT', 'DGB/USDT', '1000SHIB/USDT', 'ICP/USDT', 'BAKE/USDT', 'GTC/USDT', 'BTCDOM/USDT', 'KEEP/USDT']
    
    while True:
        time.sleep(2)
        now = int(get_time()[1][-2:])
        if now % 15 == 0:
            break

    while(1):
        temp = []

        target_list = parmap.map(get_target, ticker_list, pm_pbar=False, pm_processes = 4 )
        target_list = list(set(target_list) - set([None]))

        for target in target_list:
            try:
                buy_order(target)
            except:
                time.sleep(2)
                continue
        
        time.sleep(59.9)
        
        while True:
            time.sleep(1)
            now = int(get_time()[1][-2:])
            if now % 15 == 0:
                break

        for i in range(len(is_entering)):
            try:
                ticker = list(is_entering.keys())[i]
                ohlcv_temp = get_ohlcv(ticker, '15m', 150)
                df = pd.DataFrame(data=np.array(ohlcv_temp), columns=['0','0', '0', 'close', '0', '0','0', '0', '0','0', '0', '0']) ## rsi(8, low)
                rsi_exit = df.ta.rsi(length=8).tolist()
                if rsi_exit[-2] > 38:
                    sell_amount = is_entering[ticker]
                    binance.create_order(ticker , 'limit', 'sell', sell_amount, binance.fetch_order_book(ticker)['bids'][0][0])
                    temp.append(ticker)
            except:
                time.sleep(5)
                continue

        for i in range(len(temp)):
            del is_entering[temp[i]]


