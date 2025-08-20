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


# 호가 갭 계산
def calc_spread(data):
    total = {}
    cdef float bids = 0.0
    cdef float asks = 0.0
    for ticker in data:
        try:
            temp = ticker.split('/')
            ticker = f'{temp[0]}{temp[1]}'
            url = f'https://api.binance.com/api/v3/depth?symbol={ticker}'
            text_data = urllib.request.urlopen(url).read().decode('utf-8')
            text_data = json.loads(text_data)
            b = float(text_data['bids'][0][0])
            c = float(text_data['asks'][0][0])
            total[f'{temp[0]}/{temp[1]}'] = c/b
        except:
            # print(ticker, text_data)
            time.sleep(0.5)
            continue
    return total

# get_ticker_list() 의 상폐 종목 제외를 위한 멀티프로세싱용 서브 루틴
def discard_delisting(ticker):
    if get_ohlcv(ticker, '1d', 2)[-1][0] == std_time_data:
        return ticker
    return None

# 신뢰 가능한 종목 얻기 : 평균 거래대금 하위 10퍼센트 제외, 호가 갭 상위 50퍼센트 제외 
def get_ticker_list(target = '/USDT'): # use only '/USDT', '/BTC', '/ETH', '/BNB'
    cdef float avg_bol = 0.0
    cdef float value_ = 0.0
    cdef float price = 0.0
    cdef int i = 0
    cdef int s = 0
    
    total = {}
    temp_list = list(binance.fetch_tickers().keys())
    time.sleep(60)
    temp_list = [ticker for ticker in temp_list if target in ticker]
    global std_time_data # 멀티프로세싱 참조 용 글로벌
    std_time_data = get_ohlcv('BTC/USDT', '1d', 2)[-1][0]
    # dropout_delisting = [ticker for ticker in temp_list if get_ohlcv(ticker, '1d', 2)[-1][0] == std_time_data] # 상폐 종목 제외 single
    dropout_delisting = parmap.map(discard_delisting, temp_list, pm_pbar=False, pm_processes = 4) # 상폐 종목 제외 multi
    dropout_delisting = list(set(dropout_delisting) - set([None])) # 싱글 케이스는 이 곳을 주석 처리
    for i in range(len(dropout_delisting)): # 전 종목 거래대금 구하기 루프
        temp__ = get_ohlcv(dropout_delisting[i], '1h', 500)
        vol_temp = [item[5] for idx, item in enumerate(temp__)]
        avg_vol = sum(vol_temp) / len(vol_temp)
        market_type = dropout_delisting[i].split('/')[1]
        if market_type == 'USDT':
            value_ = temp__[-1][4] * avg_vol
        else:
            price = get_ohlcv(market_type + '/USDT', '1h', 2)[-1][4]
            value_ = price * avg_vol
        total[dropout_delisting[i]] = value_
    sort_total = sorted(total.items(), key = lambda item: item[1])
    dropout_undervalue = sort_total[int(len(sort_total) * 0.1):] # 거래대금 하위 10프로 제외
    temp_result = [dropout_undervalue[s][0] for s in range(len(dropout_undervalue))]
    get_spread = calc_spread(temp_result)
    result = sorted(get_spread.items(), key = lambda item: item[1])
    result = result[:int(len(result) * 0.5)] # 호가 갭 상위 50프로 제외
    result = [result[s][0] for s in range(len(result))]
    return result

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
    temp = ticker.split('/')[1]
    if temp == 'USDT':
        total_money = 80
    elif temp == 'BTC':
        total_money = 0.000567
    elif temp == 'BNB':
        total_money = 0.0935
    elif temp == 'ETH':
        total_money = 0.00729
    price = binance.fetch_ohlcv(ticker)[-1][4]
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
    # "options": {"defaultType": "future"},
    "timeout": 30000,
    "apiKey":"f6LEy0POPdaukqwlrnC4KvJbGWkcXRfVmKbsPmFAaPlyL2Rytswf7ilTa3kAjnQh",
    "secret": "sLvrd7ZT6c49yZVlnFRhPvJcIg8z39S6dVwZcIfPhFueA5BAy5UpTT3ZbVZg9zA2",
    "enableRateLimit": False,
})
binance.load_markets()

is_entering = {}


if __name__ == '__main__':
    # ticker_list = get_ticker_list('/USDT') + get_ticker_list('/BTC') + get_ticker_list('/ETH') + get_ticker_list('/BNB')

    ticker_list = ['BTC/USDT', 'AUD/USDT', 'BCH/USDT', 'DOGE/USDT', 'ETH/USDT', 'GBP/USDT', 'EUR/USDT', 'EOS/USDT', 'BUSD/USDT', 'PAX/USDT', 'TUSD/USDT', 'USDC/USDT', 'XRP/USDT', 'LTC/USDT', 'TRX/USDT', 'BNB/USDT', 'DOT/USDT', 'CAKE/USDT', 'ADA/USDT', 'LINK/USDT', 'FIL/USDT', 'XMR/USDT', 'MDX/USDT', 'ETC/USDT', 'XLM/USDT', 'THETA/USDT', 'UNI/USDT', 'SXP/USDT', 'AAVE/USDT', 'MATIC/USDT', 'CHZ/USDT', 'ZEN/USDT', 'PUNDIX/USDT', 'SOL/USDT', 'GRT/USDT', 'NEO/USDT', 'NEAR/USDT', 'ONT/USDT', 'BAT/USDT', 'ZEC/USDT', 'VET/USDT', 'REEF/USDT', 'LUNA/USDT', 'WAVES/USDT', 'HARD/USDT', 'HOT/USDT', 'ALGO/USDT', 'DASH/USDT', '1INCH/USDT', 'SNX/USDT', 'CELR/USDT', 'ATOM/USDT', 'BTT/USDT', 'IOTX/USDT', 'TRB/USDT', 'QTUM/USDT', 'ZIL/USDT', 'MIR/USDT', 'RSR/USDT', 'IOST/USDT', 'FLM/USDT', 'ENJ/USDT', 'RUNE/USDT', 'XTZ/USDT', 'SUSHI/USDT', 'MANA/USDT', 'ANKR/USDT', 'OMG/USDT', 'BNT/USDT', 'FTM/USDT', 'CRV/USDT', 'SHIB/USDT', 'ICP/USDT', 'BAND/USDT', 'PAXG/USDT', 'MKR/USDT', 'ALPHA/USDT', 'ALICE/USDT', 'BAR/USDT', 'KSM/USDT', 'HBAR/USDT', 'JST/USDT', 'COMP/USDT', 'YFI/USDT', 'EGLD/USDT', 'OCEAN/USDT', 'AVAX/USDT', 'SC/USDT', 'XVS/USDT', 'DODO/USDT', 'BAL/USDT', 'WIN/USDT', 'ANT/USDT', 'VTHO/USDT', 'SRM/USDT', 'XEM/USDT', 'AXS/USDT', 'KAVA/USDT', 'YFII/USDT', 'ICX/USDT', 'AUDIO/USDT', 'RVN/USDT', 'ONE/USDT', 'SAND/USDT', 'IOTA/USDT', 'BAKE/USDT', 'TRU/USDT', 'OGN/USDT', 'DGB/USDT', 'FTT/USDT', 'RLC/USDT', 'CTSI/USDT', 'CELO/USDT', 'MTL/USDT', 'COTI/USDT', 'FET/USDT', 'CVC/USDT', 'RAMP/USDT', 'REN/USDT', 'LRC/USDT', 'ETH/BTC', 'LINK/BTC', 'MATIC/BTC', 'XRP/BTC', 'ALGO/BTC', 'SOL/BTC', 'XVS/BTC', 'BNB/BTC', 'NXS/BTC', 'CELO/BTC', 'EOS/BTC', 'LTC/BTC', 'KNC/BTC', 'ADA/BTC', 'SKL/BTC', 'GAS/BTC', 'DOT/BTC', 'FIL/BTC', 'MANA/BTC', 'ETC/BTC', 'ONT/BTC', 'XLM/BTC', 'BQX/BTC', 'CTSI/BTC', 'XTZ/BTC', 'UNI/BTC', 'ZRX/BTC', 'AVAX/BTC', 'AAVE/BTC', 'THETA/BTC', 'ATOM/BTC', 'BNT/BTC', 'GLM/BTC', 'DOGE/BTC', 'GXS/BTC', 'NAV/BTC', 'MDA/BTC', 'CHZ/BTC', 'WTC/BTC', 'LUNA/BTC', 'ICX/BTC', 'FET/BTC', 'TOMO/BTC', 'ENJ/BTC', 'VIDT/BTC', 'AGI/BTC', 'BAT/BTC', 'POWR/BTC', 'QTUM/BTC', 'GVT/BTC', 'EPS/BTC', 'NEBL/BTC', 'ZEC/BTC', 'ARDR/BTC', 'AUDIO/BTC', 'SUSHI/BTC', 'ANT/BTC', 'IOTA/BTC', 'OMG/BTC', 'LTO/BTC', 'BLZ/BTC', 'CAKE/BTC', 'OXT/BTC', 'OCEAN/BTC', 'KAVA/BTC', 'LSK/BTC', 'SRM/BTC', 'MTL/BTC', 'XEM/BTC', 'NULS/BTC', 'RUNE/BTC', 'NEO/BTC', 'EVX/BTC', 'NANO/BTC', 'WAVES/BTC', 'ARK/BTC', 'GRT/BTC', 'BAND/BTC', 'XMR/BTC', 'CTK/BTC', 'FLM/BTC', 'SNX/BTC', 'SXP/BTC', 'RLC/BTC', 'UTK/BTC', 'FTT/BTC', 'ICP/BTC', '1INCH/BTC', 'STX/BTC', 'BZRX/BTC', 'CVC/BTC', 'CRV/BTC', 'STRAX/BTC', 'SKY/BTC', 'NEAR/BTC', 'BCD/BTC', 'DODO/BTC', 'OGN/BTC', 'AVA/BTC', 'BEL/BTC', 'LRC/BTC', 'PERP/BTC', 'POLY/BTC', 'REN/BTC', 'SCRT/BTC', 'SUSD/BTC', 'INJ/BTC', 'POLS/BTC', 'ELF/BTC', 'NKN/BTC', 'STORJ/BTC', 'VIA/BTC', 'SYS/BTC', 'HBAR/BTC', 'MIR/BTC', 'KMD/BTC', 'VET/BTC', 'COTI/BTC', 'SAND/BTC', 'ZIL/BTC', 'HIVE/BTC', 'BNB/ETH', 'VET/ETH', 'XRP/ETH', 'TRX/ETH', 'LINK/ETH', 'ADA/ETH', 'DEXE/ETH', 'EOS/ETH', 'RLC/ETH', 'PROS/ETH', 'LTC/ETH', 'XLM/ETH', 'SNT/ETH', 'STMX/ETH', 'GRT/ETH', 'NEO/ETH', 'ZIL/ETH', 'QTUM/ETH', 'SLP/ETH', 'ZRX/ETH', 'THETA/ETH', 'ETC/ETH', 'LRC/ETH', 'OMG/ETH', 'HOT/ETH', 'FRONT/ETH', 'KEY/ETH', 'NANO/ETH', 'QSP/ETH', 'IOTX/ETH', 'PIVX/ETH', 'BAT/ETH', 'NAS/ETH', 'XVG/ETH', 'IOST/ETH', 'ONT/ETH', 'BQX/ETH', 'BNT/ETH', 'SCRT/ETH', 'VIB/ETH', 'WAVES/ETH', 'FUN/ETH', 'BAKE/BNB', 'CAKE/BNB', 'DOT/BNB', 'XRP/BNB', 'ADA/BNB', 'TRX/BNB', 'LTC/BNB', 'BURGER/BNB', 'LUNA/BNB', 'BTT/BNB', 'ZEN/BNB', 'SUSHI/BNB', 'HOT/BNB', 'UNI/BNB', 'CHR/BNB', 'PROM/BNB', 'ICP/BNB', 'CHZ/BNB', 'RUNE/BNB', 'VET/BNB', 'EOS/BNB', 'BAT/BNB', 'SOL/BNB', 'ATOM/BNB', 'ETC/BNB', 'FIL/BNB', 'OGN/BNB', 'MATIC/BNB', 'ENJ/BNB', 'AAVE/BNB', 'WABI/BNB', 'CELR/BNB', 'INJ/BNB', 'DIA/BNB', 'XLM/BNB', 'CTK/BNB', 'EGLD/BNB', 'NEO/BNB', 'COS/BNB', 'WRX/BNB', 'ANT/BNB', 'BAND/BNB', 'AXS/BNB', 'XVS/BNB', 'AVAX/BNB', 'FTT/BNB', 'FTM/BNB', 'RVN/BNB', 'OCEAN/BNB', 'ZEC/BNB', 'SRM/BNB', 'THETA/BNB', 'ZIL/BNB']
    ticker_list = list(set(ticker_list) - set(['AUD/USDT', 'BRL/USDT', 'EUR/USDT', 'GBP/USDT', 'RUB/USDT', 'TRY/USDT', 'TUSD/USDT', 'USDC/USDT', 'PAX/USDT', 'BIDR/USDT', 'DAI/USDT', 'IDRT/USDT', 'UAH/USDT', 'NGN/USDT', 'VAI/USDT', 'BNVD/USDT']))


    while True:
        time.sleep(2)
        now = int(get_time()[1][-2:])
        if now % 15 == 0:
            break

    while(1):
        temp = []

        # now = get_time()[1]
        # if now == '0900':
        #     ticker_list = get_ticker_list('/USDT') + get_ticker_list('/BTC') + get_ticker_list('/ETH') + get_ticker_list('/BNB')

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


