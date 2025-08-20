import ccxt
import time
import operator


exchange_class = getattr(ccxt, "binance")
binance = exchange_class()
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.apiKey = "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV"
binance.secret = "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87"
binance.load_markets()


# IBS = close - low / high - low

ticker_list = [
    "ETH/USDT",
    "NEO/USDT",
    "LTC/USDT",
    "QTUM/USDT",
    "ADA/USDT",
    "XRP/USDT",
    "EOS/USDT",
    "TUSD/USDT",
    "IOTA/USDT",
    "XLM/USDT",
    "ONT/USDT",
    "TRX/USDT",
    "ETC/USDT",
    "ICX/USDT",
    "NULS/USDT",
    "VET/USDT",
    "PAX/USDT",
    "BCH/USDT",
    "USDC/USDT",
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
    "BUSD/USDT",
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
    "EUR/USDT",
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
    "BTCUP/USDT",
    "BTCDOWN/USDT",
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
        earning = round(-100 + buy_price / sell_price * 99.9, 5)
        temp += earning
        # print(earning)
    print("day:", day, "earning = ", temp)


for i in range(31, 60):
    temp_func(i, 3)
