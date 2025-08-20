# -*- coding: utf-8 -*-
import ccxt
import time
import datetime
import urllib.request
import json
import pandas as pd
import numpy as np

# from pandas.core.indexing import convert_missing_indexer
import pandas_ta
import parmap


# ccxt ex.fetch_ohlcv() 보다 훨씬 빠르게 ohlcv 얻기
def get_ohlcv(ticker="BTC/USDT", interval="1m", limit=200):
    try:
        temp = ticker.split("/")
        ticker = f"{temp[0]}{temp[1]}"
        # url = f'https://fapi.binance.com/fapi/v1/klines?symbol={ticker}&interval={interval}&limit={str(limit)}' # monitoring
        url = f"https://api.binance.com/api/v3/klines?symbol={ticker}&interval={interval}&limit={str(limit)}"  # backtesting
        text_data = urllib.request.urlopen(url).read().decode("utf-8")
        output = json.loads(text_data)
    except Exception as e:
        # print(e, '\n', 'ccxt.base.errors.BadSymbol: binance does not have market symbol {0}'.format(ticker))
        return None
    output = [list(map(float, output[i])) for i in range(len(output))]
    return output


binance = ccxt.binance(
    {
        # "options": {"defaultType": "future"},
        "timeout": 30000,
        "apiKey": "f6LEy0POPdaukqwlrnC4KvJbGWkcXRfVmKbsPmFAaPlyL2Rytswf7ilTa3kAjnQh",
        "secret": "sLvrd7ZT6c49yZVlnFRhPvJcIg8z39S6dVwZcIfPhFueA5BAy5UpTT3ZbVZg9zA2",
        "enableRateLimit": False,
    }
)
binance.load_markets()


# ticker_list = ['BAKE/USDT', 'NKN/USDT', 'XEM/USDT', 'LRC/USDT', 'ZEC/USDT', 'LINA/USDT', 'YFI/USDT', 'RVN/USDT', 'QTUM/USDT', 'SXP/USDT', 'CVC/USDT', 'CHZ/USDT', 'REEF/USDT', 'FIL/USDT', 'MTL/USDT', 'XRP/USDT', 'MATIC/USDT', 'COTI/USDT', 'NEO/USDT', 'ALGO/USDT', 'HBAR/USDT', 'BAT/USDT', 'REN/USDT', 'ADA/USDT', 'AVAX/USDT', 'HOT/USDT', 'TRX/USDT', 'AXS/USDT', 'AKRO/USDT', 'SC/USDT', 'ALPHA/USDT', 'KNC/USDT', 'CHR/USDT', 'AUDIO/USDT', 'XTZ/USDT', 'KSM/USDT', 'BTS/USDT', 'HNT/USDT', 'DASH/USDT', 'ICP/USDT', 'DGB/USDT', 'DOGE/USDT', 'VET/USDT', 'AAVE/USDT', 'IOTX/USDT', 'SRM/USDT', 'ONE/USDT', 'RLC/USDT', 'NEAR/USDT', 'GTC/USDT', 'STORJ/USDT', 'EGLD/USDT', 'WAVES/USDT', 'ETH/USDT', '1INCH/USDT', 'EOS/USDT', 'LUNA/USDT', 'UNFI/USDT', 'SUSHI/USDT', 'RSR/USDT', 'OMG/USDT', 'IOTA/USDT', 'DODO/USDT', 'CRV/USDT', 'ICX/USDT', 'ALICE/USDT', 'OGN/USDT', 'RAY/USDT', 'BCH/USDT', 'FTM/USDT', 'BLZ/USDT', 'BNB/USDT', 'KAVA/USDT', 'SKL/USDT', 'SOL/USDT', 'OCEAN/USDT', 'BTC/USDT', 'BTCDOM/USDT', 'LINK/USDT', 'SAND/USDT', 'ZRX/USDT', 'C98/USDT', 'XLM/USDT', 'ANKR/USDT', 'MANA/USDT', 'TRB/USDT', 'BTT/USDT', 'THETA/USDT', 'UNI/USDT', 'STMX/USDT', 'KEEP/USDT', 'IOST/USDT', 'BAND/USDT', 'ETC/USDT', 'ZIL/USDT', 'ENJ/USDT', 'LTC/USDT', 'BZRX/USDT', 'RUNE/USDT', 'CTK/USDT', 'LIT/USDT', 'SFP/USDT', 'ATOM/USDT', 'ZEN/USDT', 'TOMO/USDT', 'YFII/USDT', 'DEFI/USDT', 'FLM/USDT', 'BEL/USDT', 'COMP/USDT', 'ONT/USDT', '1000SHIB/USDT', 'TLM/USDT', 'DOT/USDT', 'GRT/USDT', 'XMR/USDT', 'MKR/USDT', 'CELR/USDT', 'BAL/USDT', 'DENT/USDT', 'SNX/USDT']

# ticker_list = ['ETH/BTC', 'LTC/BTC', 'BNB/BTC', 'NEO/BTC', 'BCC/BTC', 'GAS/BTC', 'HSR/BTC', 'MCO/BTC', 'WTC/BTC', 'LRC/BTC', 'QTUM/BTC', 'YOYOW/BTC', 'OMG/BTC', 'ZRX/BTC', 'STRAT/BTC', 'SNGLS/BTC', 'BQX/BTC', 'KNC/BTC', 'FUN/BTC', 'SNM/BTC', 'IOTA/BTC', 'LINK/BTC', 'XVG/BTC', 'SALT/BTC', 'MDA/BTC', 'MTL/BTC', 'SUB/BTC', 'EOS/BTC', 'SNT/BTC', 'ETC/BTC', 'MTH/BTC', 'ENG/BTC', 'DNT/BTC', 'ZEC/BTC', 'BNT/BTC', 'AST/BTC', 'DASH/BTC', 'OAX/BTC', 'ICN/BTC', 'BTG/BTC', 'EVX/BTC', 'REQ/BTC', 'VIB/BTC', 'TRX/BTC', 'POWR/BTC', 'ARK/BTC', 'XRP/BTC', 'MOD/BTC', 'ENJ/BTC', 'STORJ/BTC', 'VEN/BTC', 'KMD/BTC', 'RCN/BTC', 'NULS/BTC', 'RDN/BTC', 'XMR/BTC', 'DLT/BTC', 'AMB/BTC', 'BAT/BTC', 'BCPT/BTC', 'ARN/BTC', 'GVT/BTC', 'CDT/BTC', 'GXS/BTC', 'POE/BTC', 'QSP/BTC', 'BTS/BTC', 'XZC/BTC', 'LSK/BTC', 'TNT/BTC', 'FUEL/BTC', 'MANA/BTC', 'BCD/BTC', 'DGD/BTC', 'ADX/BTC', 'ADA/BTC', 'PPT/BTC', 'CMT/BTC', 'XLM/BTC', 'CND/BTC', 'LEND/BTC', 'WABI/BTC', 'TNB/BTC', 'WAVES/BTC', 'GTO/BTC', 'ICX/BTC', 'OST/BTC', 'ELF/BTC', 'AION/BTC', 'NEBL/BTC', 'BRD/BTC', 'EDO/BTC', 'WINGS/BTC', 'NAV/BTC', 'LUN/BTC', 'TRIG/BTC', 'APPC/BTC', 'VIBE/BTC', 'RLC/BTC', 'INS/BTC', 'PIVX/BTC', 'IOST/BTC', 'CHAT/BTC', 'STEEM/BTC', 'NANO/BTC', 'VIA/BTC', 'BLZ/BTC', 'AE/BTC', 'RPX/BTC', 'NCASH/BTC', 'POA/BTC', 'ZIL/BTC', 'ONT/BTC', 'STORM/BTC', 'XEM/BTC', 'WAN/BTC', 'WPR/BTC', 'QLC/BTC', 'SYS/BTC', 'GRS/BTC', 'CLOAK/BTC', 'GNT/BTC', 'LOOM/BTC', 'BCN/BTC', 'REP/BTC', 'TUSD/BTC', 'ZEN/BTC', 'SKY/BTC', 'CVC/BTC', 'THETA/BTC', 'IOTX/BTC', 'QKC/BTC', 'AGI/BTC', 'NXS/BTC', 'DATA/BTC', 'SC/BTC', 'NPXS/BTC', 'KEY/BTC', 'NAS/BTC', 'MFT/BTC', 'DENT/BTC', 'ARDR/BTC', 'HOT/BTC', 'VET/BTC', 'DOCK/BTC', 'POLY/BTC', 'PHX/BTC', 'HC/BTC', 'GO/BTC', 'PAX/BTC', 'RVN/BTC', 'DCR/BTC', 'MITH/BTC', 'BCH/BTC', 'BSV/BTC', 'REN/BTC', 'BTT/BTC', 'ONG/BTC', 'FET/BTC', 'CELR/BTC', 'MATIC/BTC', 'ATOM/BTC', 'PHB/BTC', 'TFUEL/BTC', 'ONE/BTC', 'FTM/BTC', 'BTCB/BTC', 'ALGO/BTC', 'ERD/BTC', 'DOGE/BTC', 'DUSK/BTC', 'ANKR/BTC', 'WIN/BTC', 'COS/BTC', 'COCOS/BTC', 'TOMO/BTC', 'PERL/BTC', 'CHZ/BTC', 'BAND/BTC', 'BEAM/BTC', 'XTZ/BTC', 'HBAR/BTC', 'NKN/BTC', 'STX/BTC', 'KAVA/BTC', 'ARPA/BTC', 'CTXC/BTC', 'TROY/BTC', 'VITE/BTC', 'FTT/BTC', 'OGN/BTC', 'DREP/BTC', 'TCT/BTC', 'WRX/BTC', 'LTO/BTC', 'MBL/BTC', 'COTI/BTC', 'STPT/BTC', 'SOL/BTC', 'CTSI/BTC', 'HIVE/BTC', 'CHR/BTC', 'MDT/BTC', 'STMX/BTC', 'PNT/BTC', 'DGB/BTC', 'COMP/BTC', 'SXP/BTC', 'SNX/BTC', 'IRIS/BTC', 'MKR/BTC', 'DAI/BTC', 'RUNE/BTC', 'FIO/BTC', 'AVA/BTC', 'BAL/BTC', 'YFI/BTC', 'JST/BTC', 'SRM/BTC', 'ANT/BTC', 'CRV/BTC', 'SAND/BTC', 'OCEAN/BTC', 'NMR/BTC', 'DOT/BTC', 'LUNA/BTC', 'IDEX/BTC', 'RSR/BTC', 'PAXG/BTC', 'WNXM/BTC', 'TRB/BTC', 'BZRX/BTC', 'WBTC/BTC', 'SUSHI/BTC', 'YFII/BTC', 'KSM/BTC', 'EGLD/BTC', 'DIA/BTC', 'UMA/BTC', 'BEL/BTC', 'WING/BTC', 'UNI/BTC', 'NBS/BTC', 'OXT/BTC', 'SUN/BTC', 'AVAX/BTC', 'HNT/BTC', 'FLM/BTC', 'SCRT/BTC', 'ORN/BTC', 'UTK/BTC', 'XVS/BTC', 'ALPHA/BTC', 'VIDT/BTC', 'AAVE/BTC', 'NEAR/BTC', 'FIL/BTC', 'INJ/BTC', 'AERGO/BTC', 'AUDIO/BTC', 'CTK/BTC', 'BOT/BTC', 'AKRO/BTC', 'AXS/BTC', 'HARD/BTC', 'RENBTC/BTC', 'STRAX/BTC', 'FOR/BTC', 'UNFI/BTC', 'ROSE/BTC', 'SKL/BTC', 'SUSD/BTC', 'GLM/BTC', 'GRT/BTC', 'JUV/BTC', 'PSG/BTC', '1INCH/BTC', 'REEF/BTC', 'OG/BTC', 'ATM/BTC', 'ASR/BTC', 'CELO/BTC', 'RIF/BTC', 'BTCST/BTC', 'TRU/BTC', 'CKB/BTC', 'TWT/BTC', 'FIRO/BTC', 'LIT/BTC', 'SFP/BTC', 'FXS/BTC', 'DODO/BTC', 'FRONT/BTC', 'EASY/BTC', 'CAKE/BTC', 'ACM/BTC', 'AUCTION/BTC', 'PHA/BTC', 'TVK/BTC', 'BADGER/BTC', 'FIS/BTC', 'OM/BTC', 'POND/BTC', 'DEGO/BTC', 'ALICE/BTC', 'LINA/BTC', 'PERP/BTC', 'RAMP/BTC', 'SUPER/BTC', 'CFX/BTC', 'EPS/BTC', 'AUTO/BTC', 'TKO/BTC', 'TLM/BTC', 'MIR/BTC', 'BAR/BTC', 'FORTH/BTC', 'EZ/BTC', 'ICP/BTC', 'AR/BTC', 'POLS/BTC', 'MDX/BTC', 'LPT/BTC', 'AGIX/BTC', 'NU/BTC', 'ATA/BTC', 'GTC/BTC', 'TORN/BTC', 'BAKE/BTC', 'KEEP/BTC', 'KLAY/BTC', 'BOND/BTC', 'MLN/BTC', 'QUICK/BTC', 'C98/BTC', 'CLV/BTC', 'QNT/BTC', 'FLOW/BTC', 'MINA/BTC', 'FARM/BTC', 'ALPACA/BTC', 'MBOX/BTC', 'VGX/BTC', 'WAXP/BTC', 'TRIBE/BTC']
ticker_list = [
    "ETH/BTC",
    "BNB/BTC",
    "LINK/BTC",
    "ENJ/BTC",
    "LTC/BTC",
    "ADA/BTC",
    "MATIC/BTC",
    "ARK/BTC",
    "UNI/BTC",
    "SXP/BTC",
    "EZ/BTC",
    "FTT/BTC",
    "XRP/BTC",
    "ONT/BTC",
    "ALICE/BTC",
    "SOL/BTC",
    "GRT/BTC",
    "WAVES/BTC",
    "FIL/BTC",
    "MTL/BTC",
    "AVAX/BTC",
    "QTUM/BTC",
    "CAKE/BTC",
    "PPT/BTC",
    "SNX/BTC",
    "LUNA/BTC",
    "SUSHI/BTC",
    "BAKE/BTC",
    "NEO/BTC",
    "ADX/BTC",
    "ZRX/BTC",
    "ATOM/BTC",
    "OGN/BTC",
    "KMD/BTC",
    "DOT/BTC",
    "FTM/BTC",
    "ALGO/BTC",
    "EOS/BTC",
    "NEBL/BTC",
    "IOTA/BTC",
    "MANA/BTC",
    "RUNE/BTC",
    "SAND/BTC",
    "GLM/BTC",
    "XMR/BTC",
    "MBOX/BTC",
    "MDA/BTC",
    "CRV/BTC",
    "NMR/BTC",
    "CTSI/BTC",
    "KLAY/BTC",
    "BAT/BTC",
    "KNC/BTC",
    "BAL/BTC",
    "AXS/BTC",
    "CHZ/BTC",
    "ANT/BTC",
    "STX/BTC",
    "BEL/BTC",
    "C98/BTC",
    "MDX/BTC",
    "MIR/BTC",
    "POLY/BTC",
    "THETA/BTC",
    "ICP/BTC",
    "ICX/BTC",
    "NANO/BTC",
    "GAS/BTC",
    "REN/BTC",
    "FLM/BTC",
    "XTZ/BTC",
    "OMG/BTC",
    "TFUEL/BTC",
    "1INCH/BTC",
    "ETC/BTC",
    "BAND/BTC",
    "RAMP/BTC",
    "NU/BTC",
    "PERP/BTC",
    "RLC/BTC",
    "SUPER/BTC",
    "HARD/BTC",
    "TRU/BTC",
    "VIDT/BTC",
    "STEEM/BTC",
    "OCEAN/BTC",
    "XVS/BTC",
    "DOGE/BTC",
    "ORN/BTC",
    "KAVA/BTC",
    "WAN/BTC",
    "GTC/BTC",
    "BNT/BTC",
    "PIVX/BTC",
    "BCD/BTC",
    "HBAR/BTC",
    "HNT/BTC",
    "LPT/BTC",
    "LIT/BTC",
    "NEAR/BTC",
    "WABI/BTC",
    "CHR/BTC",
    "BLZ/BTC",
    "RIF/BTC",
    "TKO/BTC",
    "SYS/BTC",
    "REQ/BTC",
    "AUDIO/BTC",
    "BEAM/BTC",
    "LSK/BTC",
    "FIO/BTC",
    "NKN/BTC",
    "AERGO/BTC",
    "SKY/BTC",
    "INJ/BTC",
    "LRC/BTC",
    "ALPHA/BTC",
    "BRD/BTC",
    "NULS/BTC",
    "KEEP/BTC",
    "FET/BTC",
    "EPS/BTC",
    "DEGO/BTC",
    "SUSD/BTC",
    "SKL/BTC",
    "SRM/BTC",
]

# ticker_list = list(set(ticker_list))

today = []


for item in ticker_list:

    print(item)

    BTC_ohlcv = get_ohlcv("BTC/USDT", "1d", 1400)
    # print(len(BTC_ohlcv))

    ohlcvs = get_ohlcv(item, "1d", 1400)
    # print(len(ohlcvs))

    _USDT_ohlcvs = get_ohlcv(item[:-4] + "/USDT", "1d", 1400)
    # print(len(_USDT_ohlcvs))

    if ohlcvs == None or _USDT_ohlcvs == None:
        continue

    max_len = max(len(BTC_ohlcv), len(ohlcvs), len(_USDT_ohlcvs))

    min_len = min(len(BTC_ohlcv), len(ohlcvs), len(_USDT_ohlcvs))

    BTC_ohlcv = BTC_ohlcv[-min_len:]

    ohlcvs = ohlcvs[-min_len:]

    _USDT_ohlcvs = _USDT_ohlcvs[-min_len:]

    # print(len(BTC_ohlcv) , len(ohlcvs), len(_USDT_ohlcvs))

    win = 0
    lose = 0

    for ohlcv in ohlcvs:
        if ohlcv[1] < ohlcv[4]:
            win += 1
        elif ohlcv[1] > ohlcv[4]:
            lose += 1

    new_win = 0
    new_lose = 0

    for i in range(len(ohlcvs) - 1):
        try:
            # if BTC_ohlcv[i][1] > BTC_ohlcv[i][4] and _USDT_ohlcvs[i][1] < _USDT_ohlcvs[i][4]:
            if (
                ohlcvs[i][1] > ohlcvs[i][4]
                and _USDT_ohlcvs[i][1] > _USDT_ohlcvs[i][4]
                and BTC_ohlcv[i][1] > BTC_ohlcv[i][4]
            ):
                if ohlcvs[i + 1][1] < ohlcvs[i + 1][4]:
                    new_win += 1
                elif ohlcvs[i + 1][1] > ohlcvs[i + 1][4]:
                    new_lose += 1
        except:
            break

    if new_win + new_lose == 0:
        continue

    print(f"total : {win + lose}")
    print(f"winrate : {round(win / (win + lose) * 100, 2)}%")
    print(f"win : {win}")
    print(f"lose : {lose}")

    print("")

    print(f"total : {new_win + new_lose}")
    print(f"winrate : {round(new_win / (new_win + new_lose) * 100, 2)}%")
    print(f"new_win : {new_win}")
    print(f"new_lose : {new_lose}")
    print("")


"""

for item in ticker_list:
    ohlcvs = get_ohlcv(item, '1d', 1400)

    if ohlcvs[-2][1] < ohlcvs[-2][4]:
            today.append(item)

print(len(today))
print(today)
"""
