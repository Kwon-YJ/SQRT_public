import ccxt
import time
import urllib
import json


def get_round_up_price(num):
    if num < 1:
        if num < 0.0000001:
            return 0.0000001
        elif num < 0.000001:
            return 0.000001
        elif num < 0.00001:
            return 0.00001
        elif num < 0.0001:
            return 0.0001
        elif num < 0.001:
            return 0.001
        elif num < 0.01:
            return 0.01
        elif num < 0.1:
            return 0.1
        return 1
    else:
        return (num - float(str(num)[1:])) / float(str(num)[0]) * 10


def Validate(ticker):
    try:
        time.sleep(0.065)
        ohlcv = bithumb.fetch_ohlcv(ticker, "1d")
        ATH_price = max([ohlcv[s][2] for s in range(len(ohlcv))])
        round_up_price = get_round_up_price(ohlcv[-1][4])
        if ATH_price < round_up_price:
            ticker_result.append(ticker)
            price_result.append(round(round_up_price / ohlcv[-1][4], 3))
    except:
        time.sleep(0.1)
        return None


def get_ohlcv(ticker="BTC/KRW", interval="1m", limit=200):
    try:
        temp = ticker.split("/")
        ticker = f"{temp[1]}-{temp[0]}"
        url = "https://api.upbit.com/v1/candles/months?market=KRW-BTC&count=50"
        text_data = urllib.request.urlopen(url).read().decode("utf-8")
        output = json.loads(text_data)
    except Exception as e:
        print(f"{e}\n{ticker}")
        return None
    # output = [list(map(float,output[i])) for i in range(len(output))]
    return output


exchange_class = getattr(ccxt, "bithumb")
bithumb = exchange_class()
bithumb.enableRateLimit = False
bithumb.RateLimit = 10000
# bithumb.apiKey =
# bithumb.secret =
bithumb.load_markets()

ticker_result = []
price_result = []


def print_result():
    del_list = []
    for i in range(len(price_result)):
        if price_result[i] == min(price_result):
            print(f"ticker = {ticker_result[i]}, value = {price_result[i]}\n\n")
            del_list.append(ticker_result[i])
            del_list.append(price_result[i])
    ticker_result.remove(del_list[0])
    price_result.remove(del_list[1])


if __name__ == "__main__":
    # all_ticker = list(bithumb.fetch_tickers().keys())
    # all_ticker = [all_ticker[s] for s in range(len(all_ticker)) if '/KRW' in all_ticker[s]]

    all_ticker = [
        "BTC/KRW",
        "ETH/KRW",
        "LTC/KRW",
        "ETC/KRW",
        "XRP/KRW",
        "BCH/KRW",
        "QTUM/KRW",
        "BTG/KRW",
        "EOS/KRW",
        "ICX/KRW",
        "TRX/KRW",
        "ELF/KRW",
        "OMG/KRW",
        "KNC/KRW",
        "GLM/KRW",
        "ZIL/KRW",
        "WAXP/KRW",
        "POWR/KRW",
        "LRC/KRW",
        "STEEM/KRW",
        "STRAX/KRW",
        "ZRX/KRW",
        "REP/KRW",
        "XEM/KRW",
        "SNT/KRW",
        "ADA/KRW",
        "CTXC/KRW",
        "BAT/KRW",
        "WTC/KRW",
        "THETA/KRW",
        "LOOM/KRW",
        "WAVES/KRW",
        "TRUE/KRW",
        "LINK/KRW",
        "ENJ/KRW",
        "VET/KRW",
        "MTL/KRW",
        "IOST/KRW",
        "TMTG/KRW",
        "QKC/KRW",
        "HDAC/KRW",
        "AMO/KRW",
        "BSV/KRW",
        "ORBS/KRW",
        "TFUEL/KRW",
        "VALOR/KRW",
        "CON/KRW",
        "ANKR/KRW",
        "MIX/KRW",
        "CRO/KRW",
        "FX/KRW",
        "CHR/KRW",
        "MBL/KRW",
        "MXC/KRW",
        "FCT/KRW",
        "TRV/KRW",
        "DAD/KRW",
        "WOM/KRW",
        "SOC/KRW",
        "EM/KRW",
        "BOA/KRW",
        "FLETA/KRW",
        "SXP/KRW",
        "COS/KRW",
        "APIX/KRW",
        "EL/KRW",
        "BASIC/KRW",
        "HIVE/KRW",
        "XPR/KRW",
        "VRA/KRW",
        "FIT/KRW",
        "EGG/KRW",
        "BORA/KRW",
        "ARPA/KRW",
        "APM/KRW",
        "CKB/KRW",
        "AERGO/KRW",
        "ANW/KRW",
        "CENNZ/KRW",
        "EVZ/KRW",
        "CYCLUB/KRW",
        "SRM/KRW",
        "QTCON/KRW",
        "UNI/KRW",
        "YFI/KRW",
        "UMA/KRW",
        "AAVE/KRW",
        "COMP/KRW",
        "REN/KRW",
        "BAL/KRW",
        "RSR/KRW",
        "NMR/KRW",
        "RLC/KRW",
        "UOS/KRW",
        "SAND/KRW",
        "GOM2/KRW",
        "RINGX/KRW",
        "BEL/KRW",
        "OBSR/KRW",
        "ORC/KRW",
        "POLA/KRW",
        "AWO/KRW",
        "ADP/KRW",
        "DVI/KRW",
        "GHX/KRW",
        "MIR/KRW",
        "MVC/KRW",
        "BLY/KRW",
        "WOZX/KRW",
        "ANV/KRW",
        "GRT/KRW",
        "MM/KRW",
        "BIOT/KRW",
        "XNO/KRW",
        "SNX/KRW",
        "RAI/KRW",
        "COLA/KRW",
        "NU/KRW",
        "OXT/KRW",
        "LINA/KRW",
        "MAP/KRW",
        "AQT/KRW",
        "WIKEN/KRW",
        "CTSI/KRW",
        "MANA/KRW",
        "LPT/KRW",
        "MKR/KRW",
        "SUSHI/KRW",
        "ASM/KRW",
        "PUNDIX/KRW",
        "CELR/KRW",
        "LF/KRW",
        "ARW/KRW",
        "MSB/KRW",
        "RLY/KRW",
        "OCEAN/KRW",
        "BFC/KRW",
        "ALICE/KRW",
        "CAKE/KRW",
        "BNT/KRW",
        "XVS/KRW",
        "CHZ/KRW",
        "AXS/KRW",
        "DAI/KRW",
        "MATIC/KRW",
        "BAKE/KRW",
        "VELO/KRW",
        "BCD/KRW",
        "XLM/KRW",
        "GXC/KRW",
        "BTT/KRW",
        "VSYS/KRW",
        "IPX/KRW",
        "WICC/KRW",
        "ONT/KRW",
        "LUNA/KRW",
        "AION/KRW",
        "META/KRW",
        "KLAY/KRW",
        "ONG/KRW",
        "ALGO/KRW",
        "JST/KRW",
        "XTZ/KRW",
        "MLK/KRW",
        "WEMIX/KRW",
        "DOT/KRW",
        "ATOM/KRW",
        "SSX/KRW",
        "TEMCO/KRW",
        "HIBS/KRW",
        "BURGER/KRW",
        "DOGE/KRW",
        "KSM/KRW",
        "CTK/KRW",
        "XYM/KRW",
        "BNB/KRW",
        "SUN/KRW",
        "XEC/KRW",
        "PCI/KRW",
        "SOL/KRW",
    ]

    for ticker in all_ticker:
        Validate(ticker)

    print_result()
    print_result()
    print_result()
    print_result()
    print_result()

    print(get_ohlcv()[0])
