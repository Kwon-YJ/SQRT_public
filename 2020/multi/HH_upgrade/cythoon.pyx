###%%cython -annotation

# -*- coding: utf-8 -*- 
from pykrx import stock
import time
from datetime import datetime
import multiprocessing
import numpy as np
import parmap
import telegram


def get_perfomance(trade_log):
    win = []
    lose = []
    risk_free = 0.038 / 365
    avg = np.mean(trade_log)
    std = np.std(trade_log)
    size = (avg - risk_free) / (std * std)
    
    
    
    cdef int i = 0
    for i, item in enumerate(trade_log):
        if item >= 0:
            win.append(item)
        else:
            lose.append(item)
    '''
    print('총거래 : ', len(trade_log))
    print('수익거래수 :', len(win))
    print('손실거래수 :', len(lose))
    print('평균거래 :',avg)
    print('평균수익거래 :', np.mean(win))
    print('평균손실거래 :', np.mean(lose))
    print('평균손익비 :', -1 * np.mean(win) / np.mean(lose))
    print('승률 :', int(round(len(win) / len(trade_log),2) * 100), '%')
    print('포지션 사이징 :', size)
    print('')
    '''
    result = []
    result.append(['총거래 : ', len(trade_log)])
    result.append(['수익거래수 :', len(win)])
    result.append(['손실거래수 :', len(lose)])
    result.append(['평균거래 :',avg])
    result.append(['평균수익거래 :', np.mean(win)])
    result.append(['평균손실거래 :', np.mean(lose)])
    result.append(['평균손익비 :', -1 * np.mean(win) / np.mean(lose)])
    # result.append(['승률 :', float(round(len(win) / len(trade_log),2) * 100), '%'])
    result.append(['포지션 사이징 :', size])
    telegram_send(result)


def telegram_send(data):
    bot = telegram.Bot(token = my_token)
    if type(data) != 'str':
        data = str(data)
    while(1):
        try:
            bot.send_message(chat_id = 801167350, text = data)
            time.sleep(3)
            return None
        except:
            continue


def get_time(temp):
    now = temp
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

    return YYYY+MM+DD, hh+mm

def get_ATR(int day,ticker):
    cdef int i = 0
    cdef float case_1
    cdef float case_2
    cdef float case_3
    cdef float TR = 0
    cdef float value = 0
    for i in range(day):
        today_ = ticker.iloc[-day-1+i]
        yesterday_ = ticker.iloc[-day-2+i]
        case_1 = today_['고가'] - today_['저가']
        case_2 = abs(today_['고가'] - yesterday_['종가'])
        case_3 = abs(today_['저가'] - yesterday_['종가'])
        TR = max(case_1, case_2, case_3)
        value = value + TR
    return value/day

def get_ma(int day,ticker):
    # ticker = df.iloc[i-17:i]
    temp = ticker['종가']
    cdef int i = 0
    cdef float reuslt = 0
    cdef float price
    for i in range(day):
        price = temp.iloc[i]
        reuslt = reuslt + price
    return reuslt/day

def log_maker(ticker): # 오리지날
    if '스팩' in stock.get_market_ticker_name(ticker):
        return []

    buy_sell_log = []
    price = []
    df = stock.get_market_ohlcv_by_date("20000101", Today, ticker)
    
    cdef double HH_price = 0
    cdef int i = 0
    cdef double now_close
    cdef double tomorrow_open
    
    for i in range(17, len(df)-2):
        now_close = df.iloc[i-1]['종가']

        if now_close == 0:
            continue

        if HH_price < now_close:
            HH_price = now_close
            if len(price) == 0:
                tomorrow_open = df.iloc[i]['시가']
                if tomorrow_open == 0:
                    continue
                price.append(tomorrow_open)

        if len(price) != 0:
            now_ohlcv = df.iloc[i-17:i]
            ATR_ = get_ATR(15, now_ohlcv)
            if now_close < HH_price - (3.1 * ATR_) or i == len(df)-2:
                tomorrow_open = df.iloc[i]['시가']
                if tomorrow_open == 0:
                    continue
                earning = 100 * ((tomorrow_open / price[0]) * 0.99925 * 0.99925 - 1)
                buy_sell_log.append(earning)
                price.clear()

    return buy_sell_log


def log_maker_2(ticker): # 특정 기간 후 매도
    if '스팩' in stock.get_market_ticker_name(ticker):
        return []

    buy_sell_log = []
    df = stock.get_market_ohlcv_by_date("20000101", Today, ticker)
    
    cdef double HH_price = 0
    cdef int i = 0
    cdef double now_close
    cdef double tomorrow_open
    cdef double sell_price
    
    for i in range(5, len(df)-17):
        now_close = df.iloc[i-1]['종가']

        if now_close == 0:
            continue

        if HH_price < now_close:
            HH_price = now_close
            tomorrow_open = df.iloc[i]['시가']
            sell_price = df.iloc[i+15]['종가']
            if tomorrow_open == 0 or sell_price == 0:
                continue
            earning = 100 * ((sell_price / tomorrow_open) * 0.99925 * 0.99925 - 1)
            buy_sell_log.append(earning)
            i = i + 15

    return buy_sell_log






def log_maker_3(ticker): # 모멘텀 필터
    if '스팩' in stock.get_market_ticker_name(ticker):
        return []

    buy_sell_log = []
    price = []
    df = stock.get_market_ohlcv_by_date("20000101", Today, ticker)
    
    cdef double HH_price = 0
    cdef int i = 0
    cdef double now_close
    cdef double tomorrow_open
    cdef double temp_price
    
    for i in range(35, len(df)-2):
        now_close = df.iloc[i-1]['종가']

        if now_close == 0:
            continue

        if HH_price < now_close:
            HH_price = now_close
            temp_price = float(min(df.iloc[i-30]['종가']))
            temp_price = now_close / temp_price
            if len(price) == 0 and temp_price < 1.5:
                tomorrow_open = df.iloc[i]['시가']
                if tomorrow_open == 0:
                    continue
                price.append(tomorrow_open)

        if len(price) != 0:
            now_ohlcv = df.iloc[i-17:i]
            ATR_ = get_ATR(15, now_ohlcv)
            if now_close < HH_price - (2.7 * ATR_) or i == len(df)-2:
                tomorrow_open = df.iloc[i]['시가']
                if tomorrow_open == 0:
                    continue
                earning = 100 * ((tomorrow_open / price[0]) * 0.99925 * 0.99925 - 1)
                buy_sell_log.append(earning)
                price.clear()

    return buy_sell_log


def log_maker_4(ticker): # 오리지날( 익일시가 대신 당일 종가 )
    if '스팩' in stock.get_market_ticker_name(ticker):
        return []

    buy_sell_log = []
    price = []
    df = stock.get_market_ohlcv_by_date("20000101", Today, ticker)
    
    cdef double HH_price = 0
    cdef int i = 0
    cdef double now_close
    
    for i in range(17, len(df)-2):
        now_close = df.iloc[i-1]['종가']

        if now_close == 0:
            continue

        if HH_price < now_close:
            HH_price = now_close
            if len(price) == 0:
                price.append(now_close)

        if len(price) != 0:
            now_ohlcv = df.iloc[i-17:i]
            ATR_ = get_ATR(15, now_ohlcv)
            if now_close < HH_price - (3.1 * ATR_) or i == len(df)-2:
                earning = 100 * ((now_close / price[0]) * 0.99925 * 0.99925 - 1)
                buy_sell_log.append(earning)
                price.clear()

    return buy_sell_log


def log_maker_5(ticker): # 기간 저점 매도
    if '스팩' in stock.get_market_ticker_name(ticker):
        return []

    buy_sell_log = []
    price = []
    df = stock.get_market_ohlcv_by_date("20000101", Today, ticker)
    
    cdef double HH_price = 0
    cdef int i = 0
    cdef double now_close
    cdef double tomorrow_open
    
    for i in range(17, len(df)-2):
        now_close = df.iloc[i-1]['종가']

        if now_close == 0:
            continue

        if HH_price < now_close:
            HH_price = now_close
            if len(price) == 0:
                tomorrow_open = df.iloc[i]['시가']
                if tomorrow_open == 0:
                    continue
                price.append(tomorrow_open)

        if len(price) != 0:
            now_ohlcv = df.iloc[i-5:i]['종가']
            if float(min(now_ohlcv)) == now_close or i == len(df)-2:
                tomorrow_open = df.iloc[i]['시가']
                if tomorrow_open == 0:
                    continue
                earning = 100 * ((tomorrow_open / price[0]) * 0.99925 * 0.99925 - 1)
                buy_sell_log.append(earning)
                price.clear()

    return buy_sell_log



def log_maker_6(ticker): # ma + ATR
    if '스팩' in stock.get_market_ticker_name(ticker):
        return []

    buy_sell_log = []
    price = []
    df = stock.get_market_ohlcv_by_date("20000101", Today, ticker)
    
    cdef int i = 0
    cdef double now_close
    cdef double tomorrow_open
    cdef double target_price

    
    for i in range(11, len(df)-2):
        now_close = df.iloc[i-1]['종가']

        if now_close == 0:
            continue

        temp = df.iloc[i-10:]        
        if len(price) == 0:
            target_price = get_ma(10, temp) + (1.5 * get_ATR(10, temp))
            if now_close > target_price:
                tomorrow_open = df.iloc[i]['시가']
                if tomorrow_open == 0:
                    continue
                price.append(tomorrow_open)
        else:
            target_price = get_ma(10, temp) - (1.5 * get_ATR(10, temp))
            if now_close < target_price or i == len(df) -2:
                tomorrow_open = df.iloc[i]['시가']
                if tomorrow_open == 0:
                    continue
                earning = 100 * ((tomorrow_open / price[0]) * 0.99925 * 0.99925 - 1)
                buy_sell_log.append(earning)
                price.clear()

    return buy_sell_log




Today = get_time(datetime.now())[0]

if __name__ == '__main__':
    num_cores = multiprocessing.cpu_count()
    konex = ['341310','179530','336040','331660','337840','093510','327970','329050','309900','317860','323350','311840','314130','308700','311060','303360','271780','279060','302920','276240','299480','299670','163430','288490','285770','281310','236030','284420','277880','278990','270020','267060','270660','270210','271850','224880','266170','267810','266870','225860','284610','278380','242350','258250','258540','232830','243870','251280','251960','239890','191600','246250','245450','208850','224020','244880','112190','241510','238500','217910','212310','222160','250030','240340','327610','236340','232530','215570','233990','232680','211050','227420','229500','228180','229000','224760','223220','233250','238170','252370','149300','221800','217880','258050','222670','220110','225220','215050','217950','205290','208890','214610','140610','200580','203400','206950','200350','217320','178600','189330','189540','189350','183350','150440','179720','086080','260870','158300','180060','140290','120780','210120','084440','121060','140660','216280','058970','207490','234070','260970','224810','149010','185190','126340','199290','225850','162120','176750','183410','199150','135160','076340','107640','136660','220250','103660','114920','216400','116100','101360','202960','199800','066830','148780','092590','064850','044990','086460','067370','086220']
    All_tickers = list(set(stock.get_market_ticker_list()) - set(konex))
    # All_tickers = ['005930']
    a = time.time()
    result_ =sum( parmap.map(log_maker_6, All_tickers, pm_pbar=True, pm_processes=num_cores), [])
    b = time.time()
    print(b-a)
    get_perfomance(result_)

# %%
