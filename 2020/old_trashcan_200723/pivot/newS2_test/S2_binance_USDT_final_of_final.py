import ccxt
import time
import datetime


def get_amount(ticker):
    price = binance.fetch_ohlcv(ticker)[-1][4]
    return (today_money_USDT * 0.09) / price


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


def exit_ALL():
    for i in range(len(is_entering)):
        ticker = list(is_entering.keys())[i]
        sell_amount = is_entering[ticker]
        binance.create_order(ticker, "market", "sell", sell_amount)
    reset = {}
    return reset


def buy_order(ticker):
    buy_amount = get_amount(ticker)
    order = binance.create_order(ticker, "market", "buy", buy_amount)
    is_entering[ticker] = float(order["amount"]) * 0.999
    banList.append(ticker)


def get_ticekr_list():
    temp_list = [
        "ETH/USDT",
        "NEO/USDT",
        "LTC/USDT",
        "QTUM/USDT",
        "ADA/USDT",
        "XRP/USDT",
        "EOS/USDT",
        "IOTA/USDT",
        "XLM/USDT",
        "ONT/USDT",
        "TRX/USDT",
        "ETC/USDT",
        "ICX/USDT",
        "NULS/USDT",
        "VET/USDT",
        "LINK/USDT",
        "WAVES/USDT",
        "BTT/USDT",
        "ONG/USDT",
        "HOT/USDT",
        "ZIL/USDT",
        "ZRX/USDT",
        "FET/USDT",
        "BAT/USDT",
        "XMR/USDT",
        "ZEC/USDT",
        "IOST/USDT",
        "CELR/USDT",
        "DASH/USDT",
        "NANO/USDT",
        "OMG/USDT",
        "THETA/USDT",
        "ENJ/USDT",
        "MITH/USDT",
        "MATIC/USDT",
        "ATOM/USDT",
        "TFUEL/USDT",
        "ONE/USDT",
        "FTM/USDT",
        "ALGO/USDT",
        "GTO/USDT",
        "ERD/USDT",
        "DOGE/USDT",
        "DUSK/USDT",
        "ANKR/USDT",
        "WIN/USDT",
        "COS/USDT",
        "NPXS/USDT",
        "COCOS/USDT",
        "MTL/USDT",
        "TOMO/USDT",
        "PERL/USDT",
        "DENT/USDT",
        "MFT/USDT",
        "KEY/USDT",
        "DOCK/USDT",
        "WAN/USDT",
        "FUN/USDT",
        "CVC/USDT",
        "CHZ/USDT",
        "BAND/USDT",
        "BEAM/USDT",
        "XTZ/USDT",
        "REN/USDT",
        "RVN/USDT",
        "HC/USDT",
        "HBAR/USDT",
        "NKN/USDT",
        "STX/USDT",
        "KAVA/USDT",
        "ARPA/USDT",
        "IOTX/USDT",
        "RLC/USDT",
        "MCO/USDT",
        "CTXC/USDT",
        "TROY/USDT",
        "VITE/USDT",
        "FTT/USDT",
        "OGN/USDT",
        "DREP/USDT",
        "TCT/USDT",
        "WRX/USDT",
        "BTS/USDT",
        "LSK/USDT",
        "BNT/USDT",
        "LTO/USDT",
        "STRAT/USDT",
        "AION/USDT",
        "MBL/USDT",
        "COTI/USDT",
        "STPT/USDT",
        "WTC/USDT",
        "DATA/USDT",
        "XZC/USDT",
        "CTSI/USDT",
        "HIVE/USDT",
        "CHR/USDT",
        "GXS/USDT",
        "ARDR/USDT",
        "LEND/USDT",
        "MDT/USDT",
        "STMX/USDT",
        "KNC/USDT",
        "REP/USDT",
        "LRC/USDT",
        "PNT/USDT",
    ]
    result = []
    for i, item in enumerate(temp_list):
        try:
            ohlcv = binance.fetch_ohlcv(item, "1d")
            ohlcv_2ago = ohlcv[-2]
            PP = (ohlcv_2ago[2] + ohlcv_2ago[3] + (ohlcv_2ago[4] * 2)) / 4

            if ohlcv[-1][4] < PP:
                result.append(item)
        except:
            time.sleep(2)
            continue
    time.sleep(70)
    return result


exchange_class = getattr(ccxt, "binance")
binance = exchange_class()
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.apiKey = "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV"
binance.secret = "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87"
binance.load_markets()

banList = []
is_entering = {}
today_money_USDT = binance.fetch_balance()["USDT"]["total"]
ticker_list = get_ticekr_list()


while True:
    time_ = get_time()[1][2:]
    if time_ == "04" or time_ == "05":
        ticker_list = get_ticekr_list()

    for i, item in enumerate(ticker_list):
        try:
            time_ = get_time()[1]
            if time_ == "2359":
                is_entering = exit_ALL()
                banList = []
                today_money_USDT = binance.fetch_balance()["USDT"]["total"]
                time.sleep(180)

            if len(is_entering) == 3:
                time.sleep(25)
                continue


            if ohlcv[-1][4] < S2 and item not in banList:
                buy_order(item)
        except:
            time.sleep(2)
            continue
