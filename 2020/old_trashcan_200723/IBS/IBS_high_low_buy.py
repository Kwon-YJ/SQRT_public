import ccxt
import time
import os
import operator


exchange_class = getattr(ccxt, "binance")
binance = exchange_class(
    {
        "urls": {
            "api": {
                "public": "https://fapi.binance.com/fapi/v1",
                "private": "https://fapi.binance.com/fapi/v1",
            },
        }
    }
)
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.apiKey = "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV"
binance.secret = "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87"
binance.load_markets()


# IBS = close - low / high - low

# ticker_list = ['ETH/USDT', 'NEO/USDT', 'LTC/USDT', 'QTUM/USDT', 'ADA/USDT', 'XRP/USDT', 'EOS/USDT', 'TUSD/USDT', 'IOTA/USDT', 'XLM/USDT', 'ONT/USDT', 'TRX/USDT', 'ETC/USDT', 'ICX/USDT', 'NULS/USDT', 'VET/USDT', 'PAX/USDT', 'BCH/USDT', 'USDC/USDT', 'LINK/USDT', 'WAVES/USDT', 'BTT/USDT', 'ONG/USDT', 'HOT/USDT', 'ZIL/USDT', 'ZRX/USDT', 'FET/USDT', 'BAT/USDT', 'XMR/USDT', 'ZEC/USDT', 'IOST/USDT', 'CELR/USDT', 'DASH/USDT', 'NANO/USDT', 'OMG/USDT', 'THETA/USDT', 'ENJ/USDT', 'MITH/USDT', 'MATIC/USDT', 'ATOM/USDT', 'TFUEL/USDT', 'ONE/USDT', 'FTM/USDT', 'ALGO/USDT', 'GTO/USDT', 'ERD/USDT', 'DOGE/USDT', 'DUSK/USDT', 'ANKR/USDT', 'WIN/USDT', 'COS/USDT', 'NPXS/USDT', 'COCOS/USDT', 'MTL/USDT', 'TOMO/USDT', 'PERL/USDT', 'DENT/USDT', 'MFT/USDT', 'KEY/USDT', 'DOCK/USDT', 'WAN/USDT', 'FUN/USDT', 'CVC/USDT', 'CHZ/USDT', 'BAND/USDT', 'BUSD/USDT', 'BEAM/USDT', 'XTZ/USDT', 'REN/USDT', 'RVN/USDT', 'HC/USDT', 'HBAR/USDT', 'NKN/USDT', 'STX/USDT', 'KAVA/USDT', 'ARPA/USDT', 'IOTX/USDT', 'RLC/USDT', 'MCO/USDT', 'CTXC/USDT', 'TROY/USDT', 'VITE/USDT', 'FTT/USDT', 'EUR/USDT', 'OGN/USDT', 'DREP/USDT', 'TCT/USDT', 'WRX/USDT', 'BTS/USDT', 'LSK/USDT', 'BNT/USDT', 'LTO/USDT', 'STRAT/USDT', 'AION/USDT', 'MBL/USDT', 'COTI/USDT', 'STPT/USDT', 'WTC/USDT', 'DATA/USDT', 'XZC/USDT', 'CTSI/USDT', 'HIVE/USDT', 'CHR/USDT', 'BTCUP/USDT', 'BTCDOWN/USDT', 'GXS/USDT', 'ARDR/USDT', 'LEND/USDT', 'MDT/USDT', 'STMX/USDT', 'KNC/USDT', 'REP/USDT', 'LRC/USDT', 'PNT/USDT']

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
]


def temp_func(day, times):
    result = {}
    for i in range(len(ticker_list)):
        try:
            ohlcv = binance.fetch_ohlcv(ticker_list[i], "1d")
            temp = (ohlcv[-day - 1][4] - ohlcv[-day - 1][3]) / (
                ohlcv[-day - 1][2] - ohlcv[-day - 1][3]
            )
            result[ticker_list[i]] = temp
        except:
            continue

    Sresult = sorted(result.items(), key=operator.itemgetter(1), reverse=True)
    # Sresult= sorted(result.items(), key=operator.itemgetter(1), reverse=False)
    temp = 0
    for i in range(times):
        time_frame = "1d"
        ticker_name = Sresult[i][0]
        ohlcv = binance.fetch_ohlcv(ticker_name, time_frame)
        buy_price = ohlcv[-day][1]
        sell_price = ohlcv[-day][4]

        # print('buy :',buy_price, " sell :", sell_price)
        earning = round(-100 + sell_price / buy_price * 99.9, 5)
        temp += earning

        ticker_name = Sresult[-i - 1][0]
        ohlcv = binance.fetch_ohlcv(ticker_name, time_frame)
        buy_price = ohlcv[-day][1]
        sell_price = ohlcv[-day][4]

        # print('buy :',buy_price, " sell :", sell_price)
        earning = round(-100 + sell_price / buy_price * 99.9, 5)
        temp += earning
        # print(earning)
    print("day:", day, "earning = ", temp)


for j in range(2, 60):
    print("day =", j)
    temp_func(j, 1)
