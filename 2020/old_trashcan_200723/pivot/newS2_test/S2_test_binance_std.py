import ccxt
import time
from pprint import pprint
import datetime
import random
import numpy


def log_maker(day, max_num):
    return 0, 0, 0


def trade_tester(start_day, end_day):
    for i in range(start_day, end_day):
        random.shuffle(ticker_list)
        a, b, c = log_maker(i, 3)
        # print(c)
        # print('day',i,': ','count =' ,a,'   earining =' , b, '    total = ', c)


def get_perfomance(trade_log):
    win = []
    lose = []
    risk_free = 0.038 / 365
    avg = numpy.mean(trade_log)
    std = numpy.std(trade_log)
    size = (avg - risk_free) / (std * std)

    for i in range(len(trade_log)):
        if trade_log[i] > 0:
            win.append(trade_log[i])
        elif trade_log[i] < 0:
            lose.append(trade_log[i])

    print("총거래 : ", len(trade_log))
    print("수익거래수 :", len(win))
    print("손실거래수 :", len(lose))
    print("평균거래 :", avg)
    print("평균수익거래 :", numpy.mean(win))
    print("평균손실거래 :", numpy.mean(lose))
    print("평균손익비 :", -1 * numpy.mean(win) / numpy.mean(lose))
    print("승률 :", len(win) / len(trade_log))
    print("포지션 사이징 :", size)
    print("")


"""
binance = ccxt.binance({
    'apiKey': '3pFJ5lblk8ff8brlz2plOG2o',
    'secret': 'KKFk0a-YvtW8aEcS33HbQlxJ63rHpdA95D7IWNALSOTVraB1',
    # 'enableRateLimit': True,
    'enableRateLimit': False,
    # 'RateLimit' : 10000
})
binance.load_markets()
"""

binance = ccxt.binance(
    {
        "options": {"defaultType": "future"},
        "timeout": 30000,
        "apiKey": "f6LEy0POPdaukqwlrnC4KvJbGWkcXRfVmKbsPmFAaPlyL2Rytswf7ilTa3kAjnQh",
        "secret": "sLvrd7ZT6c49yZVlnFRhPvJcIg8z39S6dVwZcIfPhFueA5BAy5UpTT3ZbVZg9zA2",
        "enableRateLimit": False,
    }
)
binance.load_markets()


time_frame = "1d"
# ticker_list = ['ETH/USDT', 'NEO/USDT', 'LTC/USDT', 'QTUM/USDT', 'ADA/USDT', 'XRP/USDT', 'EOS/USDT',  'IOTA/USDT', 'XLM/USDT', 'ONT/USDT', 'TRX/USDT', 'ETC/USDT', 'ICX/USDT', 'NULS/USDT', 'VET/USDT', 'LINK/USDT', 'WAVES/USDT', 'BTT/USDT', 'ONG/USDT', 'HOT/USDT', 'ZIL/USDT', 'ZRX/USDT', 'FET/USDT', 'BAT/USDT', 'XMR/USDT', 'ZEC/USDT', 'IOST/USDT', 'CELR/USDT', 'DASH/USDT', 'NANO/USDT', 'OMG/USDT', 'THETA/USDT', 'ENJ/USDT', 'MITH/USDT', 'MATIC/USDT', 'ATOM/USDT', 'TFUEL/USDT', 'ONE/USDT', 'FTM/USDT', 'ALGO/USDT', 'GTO/USDT', 'ERD/USDT', 'DOGE/USDT', 'DUSK/USDT', 'ANKR/USDT', 'WIN/USDT', 'COS/USDT', 'NPXS/USDT', 'COCOS/USDT', 'MTL/USDT', 'TOMO/USDT', 'PERL/USDT', 'DENT/USDT', 'MFT/USDT', 'KEY/USDT', 'DOCK/USDT', 'WAN/USDT', 'FUN/USDT', 'CVC/USDT', 'CHZ/USDT', 'BAND/USDT', 'BEAM/USDT', 'XTZ/USDT', 'REN/USDT', 'RVN/USDT', 'HC/USDT', 'HBAR/USDT', 'NKN/USDT', 'STX/USDT', 'KAVA/USDT', 'ARPA/USDT', 'IOTX/USDT', 'RLC/USDT', 'MCO/USDT', 'CTXC/USDT', 'TROY/USDT', 'VITE/USDT', 'FTT/USDT',  'OGN/USDT', 'DREP/USDT', 'TCT/USDT', 'WRX/USDT', 'BTS/USDT', 'LSK/USDT', 'BNT/USDT', 'LTO/USDT', 'STRAT/USDT', 'AION/USDT', 'MBL/USDT', 'COTI/USDT', 'STPT/USDT', 'WTC/USDT', 'DATA/USDT', 'XZC/USDT', 'CTSI/USDT', 'HIVE/USDT', 'CHR/USDT', 'GXS/USDT', 'ARDR/USDT', 'LEND/USDT', 'MDT/USDT', 'STMX/USDT', 'KNC/USDT', 'REP/USDT', 'LRC/USDT', 'PNT/USDT']
ticker_list = [
    "BAKE/USDT",
    "NKN/USDT",
    "XEM/USDT",
    "LRC/USDT",
    "ZEC/USDT",
    "LINA/USDT",
    "YFI/USDT",
    "RVN/USDT",
    "QTUM/USDT",
    "SXP/USDT",
    "CVC/USDT",
    "CHZ/USDT",
    "REEF/USDT",
    "FIL/USDT",
    "MTL/USDT",
    "XRP/USDT",
    "MATIC/USDT",
    "COTI/USDT",
    "NEO/USDT",
    "ALGO/USDT",
    "HBAR/USDT",
    "BAT/USDT",
    "REN/USDT",
    "ADA/USDT",
    "AVAX/USDT",
    "HOT/USDT",
    "TRX/USDT",
    "AXS/USDT",
    "AKRO/USDT",
    "SC/USDT",
    "ALPHA/USDT",
    "KNC/USDT",
    "CHR/USDT",
    "AUDIO/USDT",
    "XTZ/USDT",
    "KSM/USDT",
    "BTS/USDT",
    "HNT/USDT",
    "DASH/USDT",
    "ICP/USDT",
    "DGB/USDT",
    "DOGE/USDT",
    "VET/USDT",
    "AAVE/USDT",
    "IOTX/USDT",
    "SRM/USDT",
    "ONE/USDT",
    "RLC/USDT",
    "NEAR/USDT",
    "GTC/USDT",
    "STORJ/USDT",
    "EGLD/USDT",
    "WAVES/USDT",
    "ETH/USDT",
    "1INCH/USDT",
    "EOS/USDT",
    "LUNA/USDT",
    "UNFI/USDT",
    "SUSHI/USDT",
    "RSR/USDT",
    "OMG/USDT",
    "IOTA/USDT",
    "DODO/USDT",
    "CRV/USDT",
    "ICX/USDT",
    "ALICE/USDT",
    "OGN/USDT",
    "RAY/USDT",
    "BCH/USDT",
    "FTM/USDT",
    "BLZ/USDT",
    "BNB/USDT",
    "KAVA/USDT",
    "SKL/USDT",
    "SOL/USDT",
    "OCEAN/USDT",
    "BTC/USDT",
    "BTCDOM/USDT",
    "LINK/USDT",
    "SAND/USDT",
    "ZRX/USDT",
    "C98/USDT",
    "XLM/USDT",
    "ANKR/USDT",
    "MANA/USDT",
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
    "SFP/USDT",
    "ATOM/USDT",
    "ZEN/USDT",
    "TOMO/USDT",
    "YFII/USDT",
    "DEFI/USDT",
    "FLM/USDT",
    "BEL/USDT",
    "COMP/USDT",
    "ONT/USDT",
    "1000SHIB/USDT",
    "TLM/USDT",
    "DOT/USDT",
    "GRT/USDT",
    "XMR/USDT",
    "MKR/USDT",
    "CELR/USDT",
    "BAL/USDT",
    "DENT/USDT",
    "SNX/USDT",
]

name = []

for i in range(1):
    buy_and_sell = []
    trade_tester(0, 20)
    get_perfomance(buy_and_sell)


"""
j = 0

for k in range(len(ticker_list)):
    j = 0
    
    for i in range(len(name)):
        if ticker_list[k] == name[i]:
            j += 1
    
    print(ticker_list[k], ':', j)
"""
