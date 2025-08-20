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


# ticker_list = ['ETH/BTC', 'LTC/BTC', 'NEO/BTC', 'GAS/BTC', 'MCO/BTC', 'WTC/BTC', 'LRC/BTC', 'QTUM/BTC', 'YOYOW/BTC', 'OMG/BTC', 'ZRX/BTC', 'STRAT/BTC', 'SNGLS/BTC', 'BQX/BTC', 'KNC/BTC', 'FUN/BTC', 'SNM/BTC', 'IOTA/BTC', 'LINK/BTC', 'XVG/BTC', 'MDA/BTC', 'MTL/BTC', 'EOS/BTC', 'SNT/BTC', 'ETC/BTC', 'MTH/BTC', 'ENG/BTC', 'DNT/BTC', 'ZEC/BTC', 'BNT/BTC', 'AST/BTC', 'DASH/BTC', 'OAX/BTC', 'BTG/BTC', 'EVX/BTC', 'REQ/BTC', 'VIB/BTC', 'TRX/BTC', 'POWR/BTC', 'ARK/BTC', 'XRP/BTC', 'ENJ/BTC', 'STORJ/BTC', 'KMD/BTC', 'RCN/BTC', 'NULS/BTC', 'RDN/BTC', 'XMR/BTC', 'DLT/BTC', 'AMB/BTC', 'BAT/BTC', 'BCPT/BTC', 'ARN/BTC', 'GVT/BTC', 'CDT/BTC', 'GXS/BTC', 'POE/BTC', 'QSP/BTC', 'BTS/BTC', 'XZC/BTC', 'LSK/BTC', 'TNT/BTC', 'FUEL/BTC', 'MANA/BTC', 'BCD/BTC', 'ADX/BTC', 'ADA/BTC', 'PPT/BTC', 'CMT/BTC', 'XLM/BTC', 'CND/BTC', 'LEND/BTC', 'WABI/BTC', 'TNB/BTC', 'WAVES/BTC', 'GTO/BTC', 'ICX/BTC', 'OST/BTC', 'ELF/BTC', 'AION/BTC', 'NEBL/BTC', 'BRD/BTC', 'NAV/BTC', 'LUN/BTC', 'APPC/BTC', 'VIBE/BTC', 'RLC/BTC', 'INS/BTC', 'PIVX/BTC', 'IOST/BTC', 'STEEM/BTC', 'NANO/BTC', 'VIA/BTC', 'BLZ/BTC', 'AE/BTC', 'POA/BTC', 'ZIL/BTC', 'ONT/BTC', 'XEM/BTC', 'WAN/BTC', 'WPR/BTC', 'QLC/BTC', 'SYS/BTC', 'GRS/BTC', 'GNT/BTC', 'LOOM/BTC', 'REP/BTC', 'ZEN/BTC', 'SKY/BTC', 'CVC/BTC', 'THETA/BTC', 'IOTX/BTC', 'QKC/BTC', 'AGI/BTC', 'NXS/BTC', 'DATA/BTC', 'SC/BTC', 'NAS/BTC', 'ARDR/BTC', 'HOT/BTC', 'VET/BTC', 'DOCK/BTC', 'POLY/BTC', 'HC/BTC', 'GO/BTC', 'RVN/BTC', 'DCR/BTC', 'MITH/BTC', 'BCH/BTC', 'REN/BTC', 'ONG/BTC', 'FET/BTC', 'CELR/BTC', 'MATIC/BTC', 'ATOM/BTC', 'PHB/BTC', 'TFUEL/BTC', 'ONE/BTC', 'FTM/BTC', 'ALGO/BTC', 'ERD/BTC', 'DOGE/BTC', 'DUSK/BTC', 'ANKR/BTC', 'COS/BTC', 'TOMO/BTC', 'PERL/BTC', 'CHZ/BTC', 'BAND/BTC', 'BEAM/BTC', 'XTZ/BTC', 'HBAR/BTC', 'NKN/BTC', 'STX/BTC', 'KAVA/BTC', 'ARPA/BTC', 'CTXC/BTC', 'TROY/BTC', 'VITE/BTC', 'FTT/BTC', 'OGN/BTC', 'DREP/BTC', 'TCT/BTC', 'WRX/BTC', 'LTO/BTC', 'MBL/BTC', 'COTI/BTC', 'STPT/BTC', 'SOL/BTC', 'CTSI/BTC', 'HIVE/BTC', 'CHR/BTC', 'MDT/BTC', 'STMX/BTC', 'PNT/BTC', 'DGB/BTC']
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
        # print(earning)
    print("day:", day, "earning = ", temp)


for i in range(31, 60):
    temp_func(i, 3)
