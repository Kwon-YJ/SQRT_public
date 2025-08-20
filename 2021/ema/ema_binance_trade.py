from collections import UserDict
import multiprocessing
import pandas_ta as ta
import pandas as pd
import numpy as np
import datetime
import urllib
import parmap
import ccxt
import time
import json


# ccxt ex.fetch_ohlcv() 보다 훨씬 빠르게 ohlcv 얻기
def get_ohlcv(ticker="BTC/USDT", interval="1m", limit=500):
    try:
        temp = ticker.split("/")
        ticker = f"{temp[0]}{temp[1]}"
        # url = f'https://fapi.binance.com/fapi/v1/klines?symbol={ticker}&interval={interval}&limit={str(limit)}' # futures
        url = f"https://api.binance.com/api/v3/klines?symbol={ticker}&interval={interval}&limit={str(limit)}"  # spot
        text_data = urllib.request.urlopen(url).read().decode("utf-8")
        result = json.loads(text_data)
    except:
        return [[0]]
    result = [list(map(float, result[i])) for i in range(len(result))]
    return result


# get_time()[0] = 오늘 날짜 str
# get_time()[1] = 현재 시각 str
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


# 매수 수량 얻기
def get_amount(ticker):
    price = binance.fetch_ohlcv(ticker)[-1][4]
    result = (USDT_size / price) / total_buy_count
    return binance.amount_to_precision(ticker, amount=result)


# 매수 주문 실행
def buy_order(ticker):
    try:
        buy_amount = get_amount(ticker)
        order = binance.create_order(ticker, "market", "buy", buy_amount)
        is_entering[ticker] = float(order["amount"])
    except:
        return None


# 이평 정배열 검증
def regular_array(ma1, ma2, ma3):
    if ma1 > ma2 and ma1 > ma3 and ma2 > ma3:
        return True
    else:
        return False


# 매수 종목 선정하기
def get_target(item):
    try:
        ohlcv_temp = get_ohlcv(item, "15m", 600)

        # df = pd.DataFrame(data=np.array(ohlcv_temp), columns=['0','0', 'close', '0', '0', '0','0', '0', '0','0', '0', '0']) ## rsi(14, high)

        df = pd.DataFrame(
            data=np.array(ohlcv_temp),
            columns=["0", "0", "0", "0", "close", "0", "0", "0", "0", "0", "0", "0"],
        )

        ema_25 = (df["close"].ewm(50).mean()).tolist()  # 50
        ema_50 = (df["close"].ewm(100).mean()).tolist()  # 100
        ema_100 = (df["close"].ewm(200).mean()).tolist()  # 200

        if (
            regular_array(ema_25[-3], ema_50[-3], ema_100[-3]) == True
            and ohlcv_temp[-2][4] < ema_25[-2]
            and ohlcv_temp[-3][4] > ema_25[-3]
        ):
            return item
    except Exception as e:
        # except:
        print(item)
        print(e)
        time.sleep(0.1)
    return None


binance = ccxt.binance(
    {
        # "options": {"defaultType": "future"},
        "timeout": 30000,
        "apiKey": "f6LEy0POPdaukqwlrnC4KvJbGWkcXRfVmKbsPmFAaPlyL2Rytswf7ilTa3kAjnQh",
        "secret": "sLvrd7ZT6c49yZVlnFRhPvJcIg8z39S6dVwZcIfPhFueA5BAy5UpTT3ZbVZg9zA2",
        # "apiKey":"Wofk7BIStGtvLeCLCIbXVAbxl3KAy03BHafkmGtVqOILF8FZKonaSxqIPCzK4j6i",
        # "secret": "n91lmhQJCOB1ZySmbuTeuefoFlytnnAkjivYazRF1DW4x22v34RN3LXEq5OlHZtR",
        "enableRateLimit": False,
    }
)
binance.load_markets()

is_entering = {}


global total_buy_count
global USDT_size


# a = ['FIL/BNB', 'SWRV/BNB', 'UNI/BNB', 'CHR/BNB', 'LTC/BNB', 'SUSHI/BNB', 'VET/BNB', 'EOS/BNB', 'DOT/BNB', 'SOL/BNB', 'XRP/BNB', 'ADA/BNB', 'CHZ/BNB', 'FTT/BNB', 'LUNA/BNB', 'CAKE/BNB', 'BAKE/BNB', 'SPARTA/BNB', 'IOTA/BNB', 'MATIC/BNB', 'AAVE/BNB', 'BCH/BNB', 'ENJ/BNB', 'INJ/BNB', 'THETA/BNB', 'TRX/BNB', 'HARD/BNB', 'ATA/BNB', 'NEO/BNB', 'ATOM/BNB', 'ETC/BNB', 'SAND/BNB', 'CTSI/BNB', 'ICP/BNB', 'XLM/BNB', 'COS/BNB', 'BTT/BNB', 'ANT/BNB', 'FTM/BNB', 'ZIL/BNB', 'OGN/BNB', 'ANKR/BNB', 'MBL/BNB', 'ALGO/BNB', 'KSM/BNB', 'XVS/BNB', 'C98/BNB', 'SXP/BNB', 'DGB/BNB', 'EGLD/BNB', 'AXS/BNB', 'ONE/BNB', 'BAT/BNB', 'WABI/BNB', 'ICX/BNB', 'WAVES/BNB', 'BLZ/BNB']
# b = ['ETH/BTC', 'ETC/BTC', 'BNB/BTC', 'SOL/BTC', 'ADA/BTC', 'LINK/BTC', 'DOT/BTC', 'UNI/BTC', 'THETA/BTC', 'LIT/BTC', 'LUNA/BTC', 'AVAX/BTC', 'ONT/BTC', 'LTC/BTC', 'RUNE/BTC', 'XRP/BTC', 'GRT/BTC', 'BAT/BTC', '1INCH/BTC', 'WTC/BTC', 'MATIC/BTC', 'SKY/BTC', 'ENJ/BTC', 'BCD/BTC', 'ADX/BTC', 'XMR/BTC', 'OCEAN/BTC', 'ICX/BTC', 'ALGO/BTC', 'GAS/BTC', 'SUSHI/BTC', 'AUDIO/BTC', 'CRV/BTC', 'ATOM/BTC', 'FIL/BTC', 'WAVES/BTC', 'EVX/BTC', 'SXP/BTC', 'REN/BTC', 'HIVE/BTC', 'TFUEL/BTC', 'BAND/BTC', 'RLC/BTC', 'KAVA/BTC', 'SNX/BTC', 'TOMO/BTC', 'ALPHA/BTC', 'CAKE/BTC', 'KNC/BTC', 'OXT/BTC', 'FTT/BTC', 'OGN/BTC', 'IOTA/BTC', 'XLM/BTC', 'LSK/BTC', 'CHZ/BTC', 'ZRX/BTC', 'SRM/BTC', 'SAND/BTC', 'DASH/BTC', 'MANA/BTC', 'POLY/BTC', 'LRC/BTC', 'GXS/BTC', 'NEAR/BTC', 'AXS/BTC', 'FTM/BTC', 'QTUM/BTC', 'CTK/BTC', 'MTL/BTC', 'DOGE/BTC', 'NAV/BTC', 'CTSI/BTC', 'ICP/BTC', 'GVT/BTC', 'ALICE/BTC', 'VIDT/BTC', 'OMG/BTC', 'CELO/BTC', 'POWR/BTC', 'EOS/BTC', 'BAR/BTC', 'PNT/BTC', 'KMD/BTC', 'SUSD/BTC', 'BNT/BTC', 'WING/BTC', 'POLS/BTC', 'TLM/BTC', 'NEO/BTC', 'FET/BTC', 'XEM/BTC', 'WABI/BTC', 'PERP/BTC', 'TKO/BTC', 'STORJ/BTC', 'ONG/BTC', 'PHA/BTC', 'C98/BTC', 'MDX/BTC', 'XTZ/BTC', 'CVC/BTC', 'INJ/BTC', 'DREP/BTC', 'GTC/BTC', 'NANO/BTC', 'ASR/BTC', 'REP/BTC', 'FIS/BTC', 'CHR/BTC', 'HNT/BTC', 'AST/BTC', 'SCRT/BTC', 'OM/BTC', 'COTI/BTC', 'TVK/BTC', 'NULS/BTC', 'WRX/BTC', 'ANT/BTC', 'UMA/BTC', 'JUV/BTC', 'FIRO/BTC', 'LTO/BTC', 'AION/BTC']
# c = ['BTC/USDT', 'ETH/USDT', 'MATIC/USDT', 'BCH/USDT', 'BNB/USDT', 'XMR/USDT', 'DOT/USDT', 'ADA/USDT', 'AUD/USDT', 'EUR/USDT', 'TFUEL/USDT', 'BUSD/USDT', 'PAX/USDT', 'TUSD/USDT', 'USDC/USDT', 'OMG/USDT', 'EOS/USDT', 'COCOS/USDT', 'GBP/USDT', 'DOGE/USDT', 'ROSE/USDT', 'XRP/USDT', 'RVN/USDT', 'TRX/USDT', 'THETA/USDT', 'PAXG/USDT', 'XLM/USDT', 'ZEC/USDT', 'FIL/USDT', 'LTC/USDT', 'ICP/USDT', 'VET/USDT', 'AVAX/USDT', 'LTO/USDT', 'LINK/USDT', 'REEF/USDT', 'ETC/USDT', 'NEO/USDT', 'BTCUP/USDT', 'CVC/USDT', 'COMP/USDT', 'SLP/USDT', 'BTT/USDT', 'DASH/USDT', 'BAT/USDT', 'AAVE/USDT', 'BEL/USDT', 'LINKUP/USDT', 'CAKE/USDT', 'UNI/USDT', 'ATOM/USDT', 'ONT/USDT', 'OCEAN/USDT', 'ALGO/USDT', 'CHZ/USDT', 'COTI/USDT', 'BZRX/USDT', 'DENT/USDT', 'TKO/USDT', 'ANKR/USDT', 'GRT/USDT', 'ZIL/USDT', 'SAND/USDT', 'SNX/USDT', 'AXS/USDT', 'DEGO/USDT', 'IOST/USDT', 'FIO/USDT', 'YFI/USDT', 'SXP/USDT', 'SC/USDT', 'XTZ/USDT', 'SOL/USDT', 'ALICE/USDT', 'TLM/USDT', 'XEM/USDT', 'NEAR/USDT', 'GTO/USDT', 'FTM/USDT', 'STMX/USDT', 'BAKE/USDT', 'FTT/USDT', 'GXS/USDT', 'WAVES/USDT', 'HNT/USDT', 'C98/USDT', 'LUNA/USDT', 'MANA/USDT', 'KSM/USDT', 'EGLD/USDT', 'BLZ/USDT', 'KNC/USDT', 'SUSHI/USDT', 'ENJ/USDT', 'CELR/USDT', 'BTCDOWN/USDT', '1INCH/USDT', 'STORJ/USDT', 'CTK/USDT', 'SRM/USDT', 'QTUM/USDT', 'RUNE/USDT', 'INJ/USDT', 'REN/USDT', 'UMA/USDT', 'VTHO/USDT', 'AUDIO/USDT', 'HOT/USDT', 'WIN/USDT', 'NANO/USDT', 'PUNDIX/USDT', 'OGN/USDT', 'CELO/USDT', 'IOTA/USDT', 'ETHDOWN/USDT', 'YFII/USDT', 'DUSK/USDT', 'MKR/USDT', 'DGB/USDT', 'SUSHIUP/USDT', 'ZRX/USDT', 'CHR/USDT', 'TOMO/USDT', 'XVG/USDT', 'PERP/USDT', 'MITH/USDT']
# d = ['XRP/ETH', 'BNB/ETH', 'ETC/ETH', 'NEO/ETH', 'LTC/ETH', 'QLC/ETH', 'ADX/ETH', 'XLM/ETH', 'ADA/ETH', 'EOS/ETH', 'GRT/ETH', 'VET/ETH', 'THETA/ETH', 'ZIL/ETH', 'TRX/ETH', 'NANO/ETH', 'REP/ETH', 'OMG/ETH', 'LINK/ETH', 'IOST/ETH', 'SCRT/ETH', 'BLZ/ETH', 'QTUM/ETH', 'PIVX/ETH', 'ZRX/ETH', 'MTL/ETH', 'BAT/ETH', 'SNT/ETH', 'ENJ/ETH', 'MANA/ETH', 'WAVES/ETH', 'EZ/ETH', 'XVG/ETH', 'KMD/ETH', 'ONT/ETH', 'KEY/ETH', 'SLP/ETH', 'VIB/ETH', 'RLC/ETH', 'IOTX/ETH']
# ticker_list = ['BTC/USDT', 'ETH/USDT', 'BCH/USDT', 'XRP/USDT', 'EOS/USDT', 'LTC/USDT', 'TRX/USDT', 'ETC/USDT', 'LINK/USDT', 'XLM/USDT', 'ADA/USDT', 'XMR/USDT', 'DASH/USDT', 'ZEC/USDT', 'XTZ/USDT', 'BNB/USDT', 'ATOM/USDT', 'ONT/USDT', 'IOTA/USDT', 'BAT/USDT', 'VET/USDT', 'NEO/USDT', 'QTUM/USDT', 'IOST/USDT', 'THETA/USDT', 'ALGO/USDT', 'ZIL/USDT', 'KNC/USDT', 'ZRX/USDT', 'COMP/USDT', 'OMG/USDT', 'DOGE/USDT', 'SXP/USDT', 'KAVA/USDT', 'BAND/USDT', 'RLC/USDT', 'WAVES/USDT', 'MKR/USDT', 'SNX/USDT', 'DOT/USDT', 'YFI/USDT', 'BAL/USDT', 'CRV/USDT', 'TRB/USDT', 'YFII/USDT', 'RUNE/USDT', 'SUSHI/USDT', 'SRM/USDT', 'BZRX/USDT', 'EGLD/USDT', 'SOL/USDT', 'ICX/USDT', 'STORJ/USDT', 'BLZ/USDT', 'UNI/USDT', 'AVAX/USDT', 'FTM/USDT', 'HNT/USDT', 'ENJ/USDT', 'FLM/USDT', 'TOMO/USDT', 'REN/USDT', 'KSM/USDT', 'NEAR/USDT', 'AAVE/USDT', 'FIL/USDT', 'RSR/USDT', 'LRC/USDT', 'MATIC/USDT', 'OCEAN/USDT', 'CVC/USDT', 'BEL/USDT', 'CTK/USDT', 'AXS/USDT', 'ALPHA/USDT', 'ZEN/USDT', 'SKL/USDT', 'GRT/USDT', '1INCH/USDT', 'BTC/BUSD', 'AKRO/USDT', 'CHZ/USDT', 'SAND/USDT', 'ANKR/USDT', 'LUNA/USDT', 'BTS/USDT', 'LIT/USDT', 'UNFI/USDT', 'DODO/USDT', 'REEF/USDT', 'RVN/USDT', 'SFP/USDT', 'XEM/USDT', 'COTI/USDT', 'CHR/USDT', 'MANA/USDT', 'ALICE/USDT', 'HBAR/USDT', 'ONE/USDT', 'LINA/USDT', 'STMX/USDT', 'DENT/USDT', 'CELR/USDT', 'HOT/USDT', 'MTL/USDT', 'OGN/USDT', 'BTT/USDT', 'NKN/USDT', 'SC/USDT', 'DGB/USDT', 'ICP/USDT', 'BAKE/USDT']
# ticker_list = ticker_list + a + b + d

# ticker_list = ['BTC/USDT', 'ETH/USDT', 'BCH/USDT', 'XRP/USDT', 'EOS/USDT', 'LTC/USDT', 'TRX/USDT', 'ETC/USDT', 'LINK/USDT', 'XLM/USDT', 'ADA/USDT', 'XMR/USDT', 'DASH/USDT', 'ZEC/USDT', 'XTZ/USDT', 'BNB/USDT', 'ATOM/USDT', 'ONT/USDT', 'IOTA/USDT', 'BAT/USDT', 'VET/USDT', 'NEO/USDT', 'QTUM/USDT', 'IOST/USDT', 'THETA/USDT', 'ALGO/USDT', 'ZIL/USDT', 'KNC/USDT', 'ZRX/USDT', 'COMP/USDT', 'OMG/USDT', 'DOGE/USDT', 'SXP/USDT', 'KAVA/USDT', 'BAND/USDT', 'RLC/USDT', 'WAVES/USDT', 'MKR/USDT', 'SNX/USDT', 'DOT/USDT', 'YFI/USDT', 'BAL/USDT', 'CRV/USDT', 'TRB/USDT', 'YFII/USDT', 'RUNE/USDT', 'SUSHI/USDT', 'SRM/USDT', 'BZRX/USDT', 'EGLD/USDT', 'SOL/USDT', 'ICX/USDT', 'STORJ/USDT', 'BLZ/USDT', 'UNI/USDT', 'AVAX/USDT', 'FTM/USDT', 'HNT/USDT', 'ENJ/USDT', 'FLM/USDT', 'TOMO/USDT', 'REN/USDT', 'KSM/USDT', 'NEAR/USDT', 'AAVE/USDT', 'FIL/USDT', 'RSR/USDT', 'LRC/USDT', 'MATIC/USDT', 'OCEAN/USDT', 'CVC/USDT', 'BEL/USDT', 'CTK/USDT', 'AXS/USDT', 'ALPHA/USDT', 'ZEN/USDT', 'SKL/USDT', 'GRT/USDT', '1INCH/USDT', 'BTC/BUSD', 'AKRO/USDT', 'CHZ/USDT', 'SAND/USDT', 'ANKR/USDT', 'LUNA/USDT', 'BTS/USDT', 'LIT/USDT', 'UNFI/USDT', 'DODO/USDT', 'REEF/USDT', 'RVN/USDT', 'SFP/USDT', 'XEM/USDT', 'COTI/USDT', 'CHR/USDT', 'MANA/USDT', 'ALICE/USDT', 'HBAR/USDT', 'ONE/USDT', 'LINA/USDT', 'STMX/USDT', 'DENT/USDT', 'CELR/USDT', 'HOT/USDT', 'MTL/USDT', 'OGN/USDT', 'BTT/USDT', 'NKN/USDT', 'SC/USDT', 'DGB/USDT', 'ICP/USDT', 'BAKE/USDT']


if __name__ == "__main__":
    ticker_list = [
        "XEM/USDT",
        "NKN/USDT",
        "BAKE/USDT",
        "ZEC/USDT",
        "LRC/USDT",
        "LINA/USDT",
        "YFI/USDT",
        "RVN/USDT",
        "QTUM/USDT",
        "SXP/USDT",
        "REEF/USDT",
        "CVC/USDT",
        "CHZ/USDT",
        "FIL/USDT",
        "MTL/USDT",
        "XRP/USDT",
        "MATIC/USDT",
        "NEO/USDT",
        "COTI/USDT",
        "ALGO/USDT",
        "HBAR/USDT",
        "REN/USDT",
        "BAT/USDT",
        "HOT/USDT",
        "ADA/USDT",
        "AVAX/USDT",
        "AXS/USDT",
        "TRX/USDT",
        "SC/USDT",
        "AKRO/USDT",
        "KNC/USDT",
        "ALPHA/USDT",
        "CHR/USDT",
        "XTZ/USDT",
        "KSM/USDT",
        "DASH/USDT",
        "HNT/USDT",
        "BTS/USDT",
        "ICP/USDT",
        "DOGE/USDT",
        "DGB/USDT",
        "AAVE/USDT",
        "VET/USDT",
        "RLC/USDT",
        "SRM/USDT",
        "ONE/USDT",
        "EGLD/USDT",
        "STORJ/USDT",
        "GTC/USDT",
        "NEAR/USDT",
        "WAVES/USDT",
        "ETH/USDT",
        "1INCH/USDT",
        "EOS/USDT",
        "LUNA/USDT",
        "UNFI/USDT",
        "SUSHI/USDT",
        "OMG/USDT",
        "RSR/USDT",
        "DODO/USDT",
        "CRV/USDT",
        "IOTA/USDT",
        "ICX/USDT",
        "ALICE/USDT",
        "OGN/USDT",
        "BCH/USDT",
        "BLZ/USDT",
        "FTM/USDT",
        "BNB/USDT",
        "SKL/USDT",
        "KAVA/USDT",
        "SOL/USDT",
        "BTC/USDT",
        "OCEAN/USDT",
        "SAND/USDT",
        "LINK/USDT",
        "ZRX/USDT",
        "XLM/USDT",
        "MANA/USDT",
        "ANKR/USDT",
        "TRB/USDT",
        "BTT/USDT",
        "THETA/USDT",
        "UNI/USDT",
        "STMX/USDT",
        "KEEP/USDT",
        "IOST/USDT",
        "BAND/USDT",
        "ETC/USDT",
        "ZIL/USDT",
        "ENJ/USDT",
        "LTC/USDT",
        "BZRX/USDT",
        "RUNE/USDT",
        "CTK/USDT",
        "LIT/USDT",
        "ZEN/USDT",
        "ATOM/USDT",
        "SFP/USDT",
        "TOMO/USDT",
        "YFII/USDT",
        "FLM/USDT",
        "BEL/USDT",
        "COMP/USDT",
        "ONT/USDT",
        "GRT/USDT",
        "DOT/USDT",
        "TLM/USDT",
        "XMR/USDT",
        "BAL/USDT",
        "MKR/USDT",
        "CELR/USDT",
        "DENT/USDT",
        "SNX/USDT",
    ]

    while True:
        time.sleep(2)
        now = int(get_time()[1][-2:])
        if now % 15 == 0:
            break

    while 1:
        temp = []
        target_list = parmap.map(get_target, ticker_list, pm_pbar=False, pm_processes=4)
        target_list = list(set(target_list) - set([None]))
        total_buy_count = len(target_list)

        """
        USDT_size = float(binance.fetch_balance()['info']['availableBalance']) * 0.07
        for target in target_list:
            try:
                balance = binance.fetch_balance()['info']
                if float(balance['totalInitialMargin']) / float(balance['totalWalletBalance']) > 0.4:
	                break
                # buy_order(target)
                print(f'buy : {target}')
            except:
                time.sleep(2)
                continue
        """

        for target in target_list:
            price = get_ohlcv(target, "1m", 3)[-1][4]
            print(f"buy : {target}, price : {price},  {int(get_time()[1])}")
            is_entering[target] = 100

        time.sleep(59)

        while True:
            time.sleep(1)
            now = int(get_time()[1][-2:])
            if now % 15 == 0:
                break

        for i in range(len(is_entering)):
            try:
                ticker = list(is_entering.keys())[i]
                ohlcv_temp = get_ohlcv(ticker, "15m", 250)
                # df = pd.DataFrame(data=np.array(ohlcv_temp), columns=['0','0', '0', 'close', '0', '0','0', '0', '0','0', '0', '0']) ## rsi(7, low)
                # rsi_exit = df.ta.rsi(length=8).tolist()
                # if rsi_exit[-2] > 39:

                df = pd.DataFrame(
                    data=np.array(ohlcv_temp),
                    columns=[
                        "0",
                        "0",
                        "0",
                        "0",
                        "close",
                        "0",
                        "0",
                        "0",
                        "0",
                        "0",
                        "0",
                        "0",
                    ],
                )
                ema_25 = (df["close"].ewm(50).mean()).tolist()  # 50
                ema_50 = (df["close"].ewm(100).mean()).tolist()  # 100
                ema_100 = (df["close"].ewm(200).mean()).tolist()  # 200

                if ohlcv_temp[-2][4] > ema_25[-2]:
                    sell_amount = is_entering[ticker]
                    # binance.create_order(ticker , 'limit', 'sell', sell_amount, binance.fetch_order_book(ticker)['bids'][0][0])
                    price = get_ohlcv(ticker, "1m", 3)[-1][4]
                    print(f"sell : {ticker}, price : {price}   {int(get_time()[1])}")
                    temp.append(ticker)
            except:
                time.sleep(5)
                continue

        for i in range(len(temp)):
            del is_entering[temp[i]]
