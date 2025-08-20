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
    time.sleep(0.065)
    ohlcv = upbit.fetch_ohlcv(ticker, "1M")
    ATH_price = max([ohlcv[s][2] for s in range(len(ohlcv))])
    round_up_price = get_round_up_price(ohlcv[-1][4])
    if ATH_price < round_up_price:
        ticker_result.append(ticker)
        price_result.append(round(round_up_price / ohlcv[-1][4], 3))


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


exchange_class = getattr(ccxt, "upbit")
upbit = exchange_class()
upbit.enableRateLimit = False
upbit.RateLimit = 10000
# upbit.apiKey =
# upbit.secret =
upbit.load_markets()

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
    # all_ticker = list(upbit.fetch_tickers().keys())
    # all_ticker = [all_ticker[s] for s in range(len(all_ticker)) if '/BTC' in all_ticker[s]]

    all_ticker = [
        "BTC/KRW",
        "1INCH/KRW",
        "AAVE/KRW",
        "ADA/KRW",
        "AERGO/KRW",
        "AHT/KRW",
        "ANKR/KRW",
        "AQT/KRW",
        "ARDR/KRW",
        "ARK/KRW",
        "ATOM/KRW",
        "AXS/KRW",
        "BAT/KRW",
        "BCH/KRW",
        "BORA/KRW",
        "BSV/KRW",
        "BTG/KRW",
        "BTT/KRW",
        "CBK/KRW",
        "CHZ/KRW",
        "CRE/KRW",
        "CRO/KRW",
        "CVC/KRW",
        "DAWN/KRW",
        "DKA/KRW",
        "DOGE/KRW",
        "DOT/KRW",
        "ELF/KRW",
        "ENJ/KRW",
        "EOS/KRW",
        "ETC/KRW",
        "ETH/KRW",
        "FCT2/KRW",
        "FLOW/KRW",
        "GAS/KRW",
        "GLM/KRW",
        "GRS/KRW",
        "HBAR/KRW",
        "HIVE/KRW",
        "HUM/KRW",
        "HUNT/KRW",
        "ICX/KRW",
        "IOST/KRW",
        "IOTA/KRW",
        "IQ/KRW",
        "JST/KRW",
        "KAVA/KRW",
        "KNC/KRW",
        "LINK/KRW",
        "LOOM/KRW",
        "LSK/KRW",
        "LTC/KRW",
        "MANA/KRW",
        "MATIC/KRW",
        "MBL/KRW",
        "MED/KRW",
        "META/KRW",
        "MFT/KRW",
        "MLK/KRW",
        "MOC/KRW",
        "MTL/KRW",
        "MVL/KRW",
        "NEO/KRW",
        "NU/KRW",
        "OMG/KRW",
        "ONG/KRW",
        "ONT/KRW",
        "ORBS/KRW",
        "PLA/KRW",
        "POLY/KRW",
        "POWR/KRW",
        "PUNDIX/KRW",
        "QKC/KRW",
        "QTUM/KRW",
        "REP/KRW",
        "RFR/KRW",
        "SAND/KRW",
        "SBD/KRW",
        "SC/KRW",
        "SNT/KRW",
        "SOL/KRW",
        "SRM/KRW",
        "SSX/KRW",
        "STEEM/KRW",
        "STMX/KRW",
        "STORJ/KRW",
        "STPT/KRW",
        "STRAX/KRW",
        "STRK/KRW",
        "STX/KRW",
        "SXP/KRW",
        "TFUEL/KRW",
        "THETA/KRW",
        "Tokamak Network/KRW",
        "TRX/KRW",
        "TT/KRW",
        "UPP/KRW",
        "VET/KRW",
        "WAVES/KRW",
        "WAXP/KRW",
        "XEC/KRW",
        "XEM/KRW",
        "XLM/KRW",
        "XRP/KRW",
        "XTZ/KRW",
        "ZIL/KRW",
        "ZRX/KRW",
    ]
    # all_ticker = ['1INCH/BTC', 'AAVE/BTC', 'ADA/BTC', 'AERGO/BTC', 'AHT/BTC', 'ALGO/BTC', 'ANKR/BTC', 'AQT/BTC', 'ARDR/BTC', 'ARK/BTC', 'ATOM/BTC', 'AUCTION/BTC', 'AUDIO/BTC', 'AXS/BTC', 'BASIC/BTC', 'BAT/BTC', 'BCH/BTC', 'BFC/BTC', 'BNT/BTC', 'BORA/BTC', 'BSV/BTC', 'BTT/BTC', 'CBK/BTC', 'CELO/BTC', 'CHR/BTC', 'CHZ/BTC', 'COMP/BTC', 'CRO/BTC', 'CRV/BTC', 'CTSI/BTC', 'CVC/BTC', 'DAD/BTC', 'DAI/BTC', 'DAWN/BTC', 'DENT/BTC', 'DGB/BTC', 'DKA/BTC', 'DNT/BTC', 'DOGE/BTC', 'DOT/BTC', 'ELF/BTC', 'ENJ/BTC', 'EOS/BTC', 'ETC/BTC', 'ETH/BTC', 'FCT2/BTC', 'FIL/BTC', 'FLOW/BTC', 'FOR/BTC', 'FX/BTC', 'GLM/BTC', 'GO/BTC', 'GRS/BTC', 'GRT/BTC', 'GXC/BTC', 'HBD/BTC', 'HIVE/BTC', 'HUM/BTC', 'HUNT/BTC', 'INJ/BTC', 'IOST/BTC', 'IOTX/BTC', 'IQ/BTC', 'JST/BTC', 'JUV/BTC', 'KAVA/BTC', 'LINA/BTC', 'LINK/BTC', 'LOOM/BTC', 'LRC/BTC', 'LSK/BTC', 'LTC/BTC', 'LUNA/BTC', 'MANA/BTC', 'MARO/BTC', 'MASK/BTC', 'MATIC/BTC', 'MED/BTC', 'META/BTC', 'MFT/BTC', 'MKR/BTC', 'MLK/BTC', 'MOC/BTC', 'MTL/BTC', 'MVL/BTC', 'NEAR/BTC', 'NKN/BTC', 'NMR/BTC', 'NU/BTC', 'OBSR/BTC', 'OGN/BTC', 'OMG/BTC', 'ONIT/BTC', 'ORBS/BTC', 'OXT/BTC', 'PCI/BTC', 'PLA/BTC', 'POLY/BTC', 'POWR/BTC', 'PROM/BTC', 'PSG/BTC', 'PUNDIX/BTC', 'QTCON/BTC', 'QTUM/BTC', 'REP/BTC', 'RFR/BTC', 'RLC/BTC', 'RSR/BTC', 'RVN/BTC', 'SAND/BTC', 'SBD/BTC', 'SC/BTC', 'SNT/BTC', 'SNX/BTC', 'SOL/BTC', 'SOLVE/BTC', 'SRM/BTC', 'SSX/BTC', 'STEEM/BTC', 'STMX/BTC', 'STORJ/BTC', 'STPT/BTC', 'STRAX/BTC', 'STRK/BTC', 'STX/BTC', 'SUN/BTC', 'SXP/BTC', 'Tokamak Network/BTC', 'TRX/BTC', 'TUSD/BTC', 'UNI/BTC', 'UPP/BTC', 'USDP/BTC', 'VAL/BTC', 'VET/BTC', 'WAVES/BTC', 'WAXP/BTC', 'XEM/BTC', 'XLM/BTC', 'XRP/BTC', 'XTZ/BTC', 'ZIL/BTC', 'ZRX/BTC']

    for ticker in all_ticker:
        Validate(ticker)

    print_result()
    print_result()
    print_result()
    print_result()
    print_result()

    # for i in range(len(price_result)):
    #    print(ticker_result[i], price_result[i])

    # print(get_ohlcv()[0])
