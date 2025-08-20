import ccxt
import time
import datetime


def get_amount(ticker):
    price = binance.fetch_ohlcv(ticker)[-1][4]
    return (today_money_BTC * 0.155) / price


def get_time(temp):
    now = temp
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
    is_entering[ticker] = float(order["amount"]) * 0.998
    banList.append(ticker)


def get_tickers(base):
    # base = '/USDT' or '/BNB' or '/BTC' or ...
    All_ticker = binance.fetch_tickers().keys()
    tickers = [s for s in All_ticker if base in s]
    result = []
    for i, item in enumerate(tickers):
        ohlcv = binance.fetch_order_book(item)
        if len(ohlcv["bids"]) != 0:
            result.append(item)
    return result


exchange_class = getattr(ccxt, "binance")
binance = exchange_class()
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.apiKey = "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV"
binance.secret = "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87"
binance.load_markets()

# ticker_list = get_tickers('/BTC')
ticker_list = [
    "ETH/BTC",
    "LTC/BTC",
    "NEO/BTC",
    "GAS/BTC",
    "MCO/BTC",
    "WTC/BTC",
    "LRC/BTC",
    "QTUM/BTC",
    "YOYOW/BTC",
    "OMG/BTC",
    "ZRX/BTC",
    "STRAT/BTC",
    "SNGLS/BTC",
    "BQX/BTC",
    "KNC/BTC",
    "FUN/BTC",
    "SNM/BTC",
    "IOTA/BTC",
    "LINK/BTC",
    "XVG/BTC",
    "MDA/BTC",
    "MTL/BTC",
    "EOS/BTC",
    "SNT/BTC",
    "ETC/BTC",
    "MTH/BTC",
    "ENG/BTC",
    "DNT/BTC",
    "ZEC/BTC",
    "BNT/BTC",
    "AST/BTC",
    "DASH/BTC",
    "OAX/BTC",
    "BTG/BTC",
    "EVX/BTC",
    "REQ/BTC",
    "VIB/BTC",
    "TRX/BTC",
    "POWR/BTC",
    "ARK/BTC",
    "XRP/BTC",
    "ENJ/BTC",
    "STORJ/BTC",
    "KMD/BTC",
    "RCN/BTC",
    "NULS/BTC",
    "RDN/BTC",
    "XMR/BTC",
    "DLT/BTC",
    "AMB/BTC",
    "BAT/BTC",
    "BCPT/BTC",
    "ARN/BTC",
    "GVT/BTC",
    "CDT/BTC",
    "GXS/BTC",
    "POE/BTC",
    "QSP/BTC",
    "BTS/BTC",
    "XZC/BTC",
    "LSK/BTC",
    "TNT/BTC",
    "FUEL/BTC",
    "MANA/BTC",
    "BCD/BTC",
    "ADX/BTC",
    "ADA/BTC",
    "PPT/BTC",
    "CMT/BTC",
    "XLM/BTC",
    "CND/BTC",
    "LEND/BTC",
    "WABI/BTC",
    "TNB/BTC",
    "WAVES/BTC",
    "GTO/BTC",
    "ICX/BTC",
    "OST/BTC",
    "ELF/BTC",
    "AION/BTC",
    "NEBL/BTC",
    "BRD/BTC",
    "NAV/BTC",
    "LUN/BTC",
    "APPC/BTC",
    "VIBE/BTC",
    "RLC/BTC",
    "INS/BTC",
    "PIVX/BTC",
    "IOST/BTC",
    "STEEM/BTC",
    "NANO/BTC",
    "VIA/BTC",
    "BLZ/BTC",
    "AE/BTC",
    "POA/BTC",
    "ZIL/BTC",
    "ONT/BTC",
    "XEM/BTC",
    "WAN/BTC",
    "WPR/BTC",
    "QLC/BTC",
    "SYS/BTC",
    "GRS/BTC",
    "GNT/BTC",
    "LOOM/BTC",
    "REP/BTC",
    "ZEN/BTC",
    "SKY/BTC",
    "CVC/BTC",
    "THETA/BTC",
    "IOTX/BTC",
    "QKC/BTC",
    "AGI/BTC",
    "NXS/BTC",
    "DATA/BTC",
    "SC/BTC",
    "NAS/BTC",
    "ARDR/BTC",
    "HOT/BTC",
    "VET/BTC",
    "DOCK/BTC",
    "POLY/BTC",
    "HC/BTC",
    "GO/BTC",
    "RVN/BTC",
    "DCR/BTC",
    "MITH/BTC",
    "BCH/BTC",
    "REN/BTC",
    "ONG/BTC",
    "FET/BTC",
    "CELR/BTC",
    "MATIC/BTC",
    "ATOM/BTC",
    "PHB/BTC",
    "TFUEL/BTC",
    "ONE/BTC",
    "FTM/BTC",
    "ALGO/BTC",
    "ERD/BTC",
    "DOGE/BTC",
    "DUSK/BTC",
    "ANKR/BTC",
    "COS/BTC",
    "TOMO/BTC",
    "PERL/BTC",
    "CHZ/BTC",
    "BAND/BTC",
    "BEAM/BTC",
    "XTZ/BTC",
    "HBAR/BTC",
    "NKN/BTC",
    "STX/BTC",
    "KAVA/BTC",
    "ARPA/BTC",
    "CTXC/BTC",
    "TROY/BTC",
    "VITE/BTC",
    "FTT/BTC",
    "OGN/BTC",
    "DREP/BTC",
    "TCT/BTC",
    "WRX/BTC",
    "LTO/BTC",
    "MBL/BTC",
    "COTI/BTC",
    "STPT/BTC",
    "SOL/BTC",
    "CTSI/BTC",
    "HIVE/BTC",
    "CHR/BTC",
    "MDT/BTC",
    "STMX/BTC",
    "PNT/BTC",
    "DGB/BTC",
]

banList = []
is_entering = {}
today_money_BTC = binance.fetch_balance()["BTC"]["total"]


while True:
    for i, item in enumerate(ticker_list):
        try:
            time.sleep(0.1)

            time_ = get_time(datetime.datetime.now())[1]

            if time_ == "2359":
                is_entering = exit_ALL()
                banList = []
                today_money_BTC = binance.fetch_balance()["BTC"]["total"]
                time.sleep(180)

            if len(is_entering) == 6:
                time.sleep(25)
                continue

            ohlcv = binance.fetch_ohlcv(item, "1d")
            ohlcv_2ago = ohlcv[-2]
            PP = (ohlcv_2ago[2] + ohlcv_2ago[3] + (ohlcv_2ago[4] * 2)) / 4
            S1_5 = 1.97 * PP - ohlcv_2ago[2]

            if ohlcv[-1][4] < S1_5 and item not in banList:
                buy_order(item)

        except Exception as ex:
            time.sleep(3)
            continue
