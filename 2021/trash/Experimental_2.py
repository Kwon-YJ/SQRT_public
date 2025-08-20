from random import randint
import datetime
import ccxt
import time
import telegram


def send_MSG(message):
    while True:
        try:
            bot.send_message(chat_id=801167350, text=str(message))
            time.sleep(3)
            return None
        except:
            time.sleep(3)
            continue


def get_time_gap():
    date_time_str = get_time()[0] + " 00:00:00.000000"
    date_time_obj = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S.%f")
    time_gap = date_time_obj + datetime.timedelta(days=1) - datetime.datetime.now()
    H, M, S = str(time_gap)[:-7].split(":")
    result = int(H) * 3600 + int(M) * 60 + int(S)
    return result


def get_decimal(ticker):
    ticker = ticker[:-5]
    Group_14 = [
        "XRP",
        "ONT",
        "IOTA",
        "BAT",
        "LEND",
        "SXP",
        "OMG",
        "ZRX",
        "ALGO",
        "THETA",
        "KAVA",
        "BAND",
        "RLC",
        "WAVES",
    ]
    Group_13 = [
        "EOS",
        "XTZ",
        "QTUM",
        "SNX",
        "DOT",
        "BAL",
        "CRV",
        "TRB",
        "NEO",
        "LIT",
        "ALICE",
        "KSM",
        "DODO",
        "UNFI",
        "EGLD",
        "FIL",
        "AAVE",
    ]
    Group_05 = ["TRX", "XLM", "ADA", "KNC", "ZIL", "RUNE", "SUSHI", "SRM", "BZRX"]
    Group_06 = ["VET", "IOST", "DOGE"]
    Group_23 = ["LINK", "COMP", "ETC", "BNB", "ATOM", "ZEN"]
    Group_31 = ["DEFI", "YFI", "YFII", "XMR"]
    Group_32 = ["MKR", "BTC", "ETH", "BCH", "LTC", "DASH", "ZEC"]
    Group_0X = [
        "SOL",
        "ICX",
        "STORJ",
        "BLZ",
        "UNI",
        "AVAX",
        "FTM",
        "HNT",
        "ENJ",
        "FLM",
        "TOMO",
        "REN",
        "NEAR",
        "RSR",
        "LRC",
        "MATIC",
        "OCEAN",
        "CVC",
        "BEL",
        "CTK",
        "AXS",
        "ALPHA",
        "SKL",
        "GRT",
        "1INCH",
        "AKRO",
        "CHZ",
        "SAND",
        "ANKR",
        "LUNA",
        "BTS",
        "REEF",
        "RVN",
        "SFP",
        "XEM",
        "COTI",
        "CHR",
        "MANA",
        "HBAR",
        "ONE",
        "LINA",
        "STMX",
        "DENT",
        "CELR",
        "HOT",
        "MTL",
        "OGN",
        "BTT",
        "NKN",
        "SC",
    ]

    if any(ticker in i for i in Group_14):
        return 1, 4
    elif any(ticker in i for i in Group_13):
        return 1, 3
    elif any(ticker in i for i in Group_05):
        return 0, 5
    elif any(ticker in i for i in Group_06):
        return 0, 6
    elif any(ticker in i for i in Group_23):
        return 2, 3
    elif any(ticker in i for i in Group_31):
        return 3, 1
    elif any(ticker in i for i in Group_32):
        return 3, 2
    elif any(ticker in i for i in Group_0X):
        return 0, 3
    # else:
    #    return ticker


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

    # return YYYY + MM + DD, hh + mm
    return YYYY + "-" + MM + "-" + DD, hh + mm


def entry_order(ticker, side):
    entry_amount = get_amount(ticker)
    order = binance.create_order(ticker, "market", side, entry_amount)
    is_entering[ticker] = float(order["amount"])


def get_amount(ticker):
    price = binance.fetch_ohlcv(ticker)[-1][4]
    today_money_USDT = float(binance.fetch_balance()["info"]["totalWalletBalance"])
    decimal_amount = get_decimal(ticker)[0]
    result = round(today_money_USDT / price * 0.33, decimal_amount)
    return result


def get_random_ticker():
    tickers = list(binance.fetch_tickers().keys())
    tickers = [
        ticker for ticker in tickers if "/USDT" in ticker and get_amount(ticker) != 0
    ]  # /USDT 고정, 매수 불가 제외

    while True:  # 중복 피하기
        rand_ticker_list = [tickers[randint(0, len(tickers) - 1)] for s in range(6)]
        if len(rand_ticker_list) == len(list(set(rand_ticker_list))):
            break
        else:
            rand_ticker_list.clear()
            continue

    return rand_ticker_list


binance = ccxt.binance({"enableRateLimit": True, "options": {"defaultType": "future"}})
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.apiKey = "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV"
binance.secret = "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87"
binance.load_markets()

is_entering = {}


def is_valid_exit():
    while True:
        try:
            today_money_USDT = float(
                binance.fetch_balance()["info"]["totalWalletBalance"]
            )
            if today_money_USDT * 1.003 < float(
                binance.fetch_balance()["total"]["USDT"]
            ):
                return True
            else:
                return False
        except:
            time.sleep(5)
            continue


bot = telegram.Bot(token=my_token)


while True:
    time_ = get_time()[1]  # str, HHmm
    # if time_ != '0135':
    #    time.sleep(25)
    #    continue
    # else:
    #    today_money_USDT = float(binance.fetch_balance()['info']['assets'][0]['walletBalance'])

    while True:
        time.sleep(5)
        try:
            if len(is_entering) == 0:
                ticker_list = get_random_ticker()

                for i in range(len(ticker_list)):
                    while True:
                        try:
                            if i % 2 == 0:
                                entry_order(ticker_list[i], "buy")
                                break
                            else:
                                entry_order(ticker_list[i], "sell")
                                break
                        except:
                            time.sleep(5)
                            continue

            if is_valid_exit() == True:
                for i in range(len(is_entering)):
                    if i % 2 == 0:
                        side = "sell"
                    else:
                        side = "buy"
                    ticker = list(is_entering.keys())[i]
                    sell_amount = is_entering[ticker]
                    while True:
                        try:
                            binance.create_order(ticker, "market", side, sell_amount)
                            break
                        except:
                            time.sleep(5)
                            continue
                is_entering.clear()
                # time.sleep(get_time_gap())
                send_MSG(
                    "이익 실현, 총 자산 :",
                    float(binance.fetch_balance()["total"]["USDT"]),
                )
        except:
            time.sleep(1)
            continue
