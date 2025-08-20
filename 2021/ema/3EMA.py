import ccxt
import time
import numpy as np
import pandas as pd
import datetime
import pandas_ta as ta
import json
import urllib

temp_temp = []
temp_temp_ = []


def TW(odd):
    return np.round(-np.log(0.99) / (np.log(1 + 0.01 * odd) - np.log(0.99)), 4)


def shortest_distance(odd, winrate, n=100000):
    lins = np.linspace(0, 10, n)
    y = TW(lins)
    least_distance = 1e100
    for i in range(n):
        dx = lins[i] - odd
        dy = y[i] - winrate
        distance = np.sqrt(dx**2 + dy**2)
        if distance < least_distance:
            least_distance = distance
    if winrate > TW(odd):
        return np.round(least_distance, 10)
    else:
        return -1 * np.round(least_distance, 10)


def timestamp_to_datetime(timestamp):
    datetimeobj = datetime.datetime.fromtimestamp(timestamp / 1000)
    original_time_data = str(datetimeobj)
    entry_time_data = str(datetimeobj)[11:-3]
    exit_time_data = str(datetimeobj)[5:-3]
    return entry_time_data, exit_time_data, original_time_data


def regular_array(price, ma1, ma2, ma3):
    if price > ma1 and ma1 > ma2 and ma1 > ma3 and ma2 > ma3:
        return True
    elif price < ma1 and ma1 < ma2 and ma1 < ma3 and ma2 < ma3:
        return False
    else:
        return None


def log_maker(name_, ohlcv_temp, ema_25, ema_50, ema_100):
    price = 0
    entry_time_buffer = []

    for i in range(2, len(ema_25) - 1):
        # if str(ema_100[i]) == 'nan' or ema_100[i] == None:
        #    continue
        if price == 0:
            # if regular_array(ema_25[i-1], ema_50[i-1], ema_100[i-1]) == True and ohlcv_temp[i][4] < ema_100[i]:
            # if regular_array(ohlcv_temp[i-1][4], ema_25[i-1], ema_50[i-1], ema_100[i-1]) == True and ohlcv_temp[i][4] < ema_100[i]:
            if (
                regular_array(
                    ohlcv_temp[i - 1][4], ema_25[i - 1], ema_50[i - 1], ema_100[i - 1]
                )
                == False
                and ohlcv_temp[i][4] > ema_100[i]
            ):
                price = ohlcv_temp[i + 1][1]
                entry_time_buffer.append(timestamp_to_datetime(ohlcv_temp[i + 1][0])[1])
        else:
            if ohlcv_temp[i][4] < ema_100[i]:  # reverse
                # if ohlcv_temp[i][4] > ema_100[i]:
                # if ohlcv_temp[i][4] > ema_25[i]:
                # if True:
                earning = 100 * (ohlcv_temp[i + 1][1] / price * Slippage - 1)
                buy_sell_log.append(earning)
                temp_temp.append(earning)
                exit_time = timestamp_to_datetime(ohlcv_temp[i + 1][0])[0]
                print(
                    name_
                    + "  "
                    + entry_time_buffer[0][:5]
                    + "  buy : "
                    + entry_time_buffer[0][6:]
                    + "  // sell : "
                    + exit_time
                    + "  "
                    + str(earning)
                )
                entry_time_buffer.clear()
                price = 0

    if price != 0:
        earning = 100 * (ohlcv_temp[-1][4] / price * Slippage - 1)
        buy_sell_log.append(earning)
        temp_temp.append(earning)
        exit_time = timestamp_to_datetime(ohlcv_temp[i + 1][0])[0]
        print(
            name_
            + "  "
            + entry_time_buffer[0][:5]
            + "  buy : "
            + entry_time_buffer[0][6:]
            + "  // sell : "
            + exit_time
            + "  "
            + str(earning)
        )
        entry_time_buffer.clear()
        price = 0
        return None


def get_perfomance(trade_log):
    # print(trade_log)
    if len(trade_log) == 0:
        return None
    win = []
    lose = []
    risk_free = 0.038 / 365
    avg = np.mean(trade_log)
    std = np.std(trade_log)
    size = (avg - risk_free) / (std * std)

    for i in range(len(trade_log)):
        if trade_log[i] > 0:
            win.append(trade_log[i])
        elif trade_log[i] < 0:
            lose.append(trade_log[i])

    avg_W_L_ratio = -1 * np.mean(win) / np.mean(lose)
    total_perform = shortest_distance(avg_W_L_ratio, len(win) / len(trade_log))

    print("총거래 : ", len(trade_log))
    print("수익거래수 :", len(win))
    print("손실거래수 :", len(lose))
    print("평균손익 :", avg)
    print("평균수익거래 :", np.mean(win))
    print("평균손실거래 :", np.mean(lose))
    print("평균손익비 :", avg_W_L_ratio)
    win_rate = int(round(len(win) / len(trade_log), 2) * 100)
    print("승률 :", win_rate, "%")
    if len(lose) > 0:
        # print(lose)
        print("MDD :", min(lose))
    print("시그마 포지션 사이징 :", size)
    win_rate = win_rate * 0.01
    temp = (1 - win_rate) / avg_W_L_ratio
    kelly = win_rate - temp
    print("켈리 레이쇼 :", kelly)

    print("성능 지수 :", total_perform)

    if len(trade_log) == 0:
        return None

    if len(lose) == 0:
        temp_temp_.append(0.25)
    elif len(win) == 0:
        temp_temp_.append(-0.25)
    else:
        temp_temp_.append(total_perform)

    print("")


# ccxt ex.fetch_ohlcv() 보다 훨씬 빠르게 ohlcv 얻기
def get_ohlcv(ticker="BTC/USDT", interval="1m", limit=200):
    try:
        temp = ticker.split("/")
        ticker = f"{temp[0]}{temp[1]}"
        # url = f'https://fapi.binance.com/fapi/v1/klines?symbol={ticker}&interval={interval}&limit={str(limit)}' # monitoring
        url = f"https://fapi.binance.com/fapi/v1/klines?symbol={ticker}&interval={interval}&endTime={endTime}&limit={str(limit)}"  # backtesting
        text_data = urllib.request.urlopen(url).read().decode("utf-8")
        buy_sell_log = json.loads(text_data)
    # except Exception as e:
    except Exception as e:
        # print(e, '\n', 'ccxt.base.errors.BadSymbol: binance does not have market symbol {0}'.format(ticker))
        # return [[0]]
        return None
    buy_sell_log = [list(map(float, buy_sell_log[i])) for i in range(len(buy_sell_log))]
    return buy_sell_log


exchange_class = getattr(ccxt, "binance")
binance = exchange_class()
binance.enableRateLimit = False
binance.RateLimit = 10000
# binance.apiKey = 'key'
# binance.secret = 'key'
binance.load_markets()


All_ohlcv = []
price = []
buy_sell_log = []
all_tickers_final = []
time_frame = "15m"
# time_frame = '5m'
# time_frame = '3m'
# time_frame = '1h'

Slippage = 0.9992 * 0.9992


ticker_list = [
    "BTC/USDT",
    "ETH/USDT",
    "BCH/USDT",
    "XRP/USDT",
    "EOS/USDT",
    "LTC/USDT",
    "TRX/USDT",
    "ETC/USDT",
    "LINK/USDT",
    "XLM/USDT",
    "ADA/USDT",
    "XMR/USDT",
    "DASH/USDT",
    "ZEC/USDT",
    "XTZ/USDT",
    "BNB/USDT",
    "ATOM/USDT",
    "ONT/USDT",
    "IOTA/USDT",
    "BAT/USDT",
    "VET/USDT",
    "NEO/USDT",
    "QTUM/USDT",
    "IOST/USDT",
    "THETA/USDT",
    "ALGO/USDT",
    "ZIL/USDT",
    "KNC/USDT",
    "ZRX/USDT",
    "COMP/USDT",
    "OMG/USDT",
    "DOGE/USDT",
    "SXP/USDT",
    "KAVA/USDT",
    "BAND/USDT",
    "RLC/USDT",
    "WAVES/USDT",
    "MKR/USDT",
    "SNX/USDT",
    "DOT/USDT",
    "DEFI/USDT",
    "YFI/USDT",
    "BAL/USDT",
    "CRV/USDT",
    "TRB/USDT",
    "YFII/USDT",
    "RUNE/USDT",
    "SUSHI/USDT",
    "SRM/USDT",
    "BZRX/USDT",
    "EGLD/USDT",
    "SOL/USDT",
    "ICX/USDT",
    "STORJ/USDT",
    "BLZ/USDT",
    "UNI/USDT",
    "AVAX/USDT",
    "FTM/USDT",
    "HNT/USDT",
    "ENJ/USDT",
    "FLM/USDT",
    "TOMO/USDT",
    "REN/USDT",
    "KSM/USDT",
    "NEAR/USDT",
    "AAVE/USDT",
    "FIL/USDT",
    "RSR/USDT",
    "LRC/USDT",
    "MATIC/USDT",
    "OCEAN/USDT",
    "CVC/USDT",
    "BEL/USDT",
    "CTK/USDT",
    "AXS/USDT",
    "ALPHA/USDT",
    "ZEN/USDT",
    "SKL/USDT",
    "GRT/USDT",
    "1INCH/USDT",
    "AKRO/USDT",
    "CHZ/USDT",
    "SAND/USDT",
    "ANKR/USDT",
    "LUNA/USDT",
    "BTS/USDT",
    "LIT/USDT",
    "UNFI/USDT",
    "DODO/USDT",
    "REEF/USDT",
    "RVN/USDT",
    "SFP/USDT",
    "XEM/USDT",
    "COTI/USDT",
    "CHR/USDT",
    "MANA/USDT",
    "ALICE/USDT",
    "HBAR/USDT",
    "ONE/USDT",
    "LINA/USDT",
    "STMX/USDT",
    "DENT/USDT",
    "CELR/USDT",
    "HOT/USDT",
    "MTL/USDT",
    "OGN/USDT",
    "BTT/USDT",
    "NKN/USDT",
    "SC/USDT",
    "DGB/USDT",
    "1000SHIB/USDT",
    "ICP/USDT",
    "BAKE/USDT",
    "GTC/USDT",
    "BTCDOM/USDT",
    "KEEP/USDT",
]


for day in range(2, 13):
    multiple = 1
    print(f"{day*multiple}일 전")

    endTime = str(binance.fetch_ohlcv("BTC/USDT", "1d")[(-day + 1) * multiple][0])

    for i in range(len(ticker_list)):
        try:
            temp = get_ohlcv(ticker_list[i], time_frame, 1400)
            if i == 0:
                print(len(temp))
            all_tickers_final.append(ticker_list[i])
            All_ohlcv.append(temp)
            # time.sleep(0.001)
        except Exception as e:
            print(e)
            # time.sleep(0.5)
            print(ticker_list[i])

    for i in range(len(All_ohlcv)):
        ohlcv_temp = All_ohlcv[i]
        if ohlcv_temp == None or len(ohlcv_temp) == 0:
            continue

        df = pd.DataFrame(
            data=np.array(ohlcv_temp),
            columns=["0", "0", "0", "0", "close", "0", "0", "0", "0", "0", "0", "0"],
        )

        # ema_25 = (df['close'].ewm(50).mean()).tolist()     #25

        ema_25 = (df["close"].ewm(25).mean()).tolist()  # 25
        ema_50 = (df["close"].ewm(50).mean()).tolist()  # 50
        ema_100 = (df["close"].ewm(100).mean()).tolist()  # 100

        # ema_25 = (df['close'].ewm(27).mean()).tolist()     #25
        # ema_50 = (df['close'].ewm(55).mean()).tolist()    #50
        # ema_100 = (df['close'].ewm(120).mean()).tolist()   #100

        # ema_25 = (df['close'].ewm(30).mean()).tolist()     #25
        # ema_50 = (df['close'].ewm(60).mean()).tolist()    #50
        # ema_100 = (df['close'].ewm(140).mean()).tolist()   #100

        # ema_25 = (df['close'].rolling(25).mean()).tolist()     #25
        # ema_50 = (df['close'].rolling(50).mean()).tolist()    #50
        # ema_100 = (df['close'].rolling(99).mean()).tolist()   #100

        # log_maker(all_tickers_final[i], ohlcv_temp[-25:],ema_25[-25:], ema_50[-25:], ema_100[-25:])
        # log_maker(all_tickers_final[i], ohlcv_temp[-49:],ema_25[-49:], ema_50[-49:], ema_100[-49:])
        log_maker(
            all_tickers_final[i],
            ohlcv_temp[-97:],
            ema_25[-97:],
            ema_50[-97:],
            ema_100[-97:],
        )
        # log_maker(all_tickers_final[i], ohlcv_temp[-289:],ema_25[-289:], ema_50[-289:], ema_100[-289:])
        # log_maker(all_tickers_final[i], ohlcv_temp[-769:],ema_25[-769:], ema_50[-769:], ema_100[-769:])
        # log_maker(all_tickers_final[i], ohlcv_temp[-865:],ema_25[-865:], ema_50[-865:], ema_100[-865:])
        # log_maker(all_tickers_final[i], ohlcv_temp[-961:],ema_25[-961:], ema_50[-961:], ema_100[-961:])

    get_perfomance(buy_sell_log)
    get_perfomance(temp_temp)
    All_ohlcv.clear()
    buy_sell_log.clear()
    all_tickers_final.clear()

print(temp_temp_)

print(sum(temp_temp_) / len(temp_temp_))
