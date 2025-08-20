# %%cython


import datetime
import urllib
import ccxt
import json


# ccxt ex.fetch_ohlcv() 보다 훨씬 빠르게 ohlcv 얻기
def get_ohlcv(ticker="BTC/USDT", interval="1m", limit=200):
    # cdef int i = 0
    try:
        temp = ticker.split("/")
        ticker = f"{temp[0]}{temp[1]}"
        url = f"https://api.binance.com/api/v3/klines?symbol={ticker}&interval={interval}&limit={str(limit)}"
        text_data = urllib.request.urlopen(url).read().decode("utf-8")
        result = json.loads(text_data)
    # except Exception as e:
    except:
        # print(e, '\n', 'ccxt.base.errors.BadSymbol: binance does not have market symbol {0}'.format(ticker))
        return [[0]]
    result = [list(map(float, result[i])) for i in range(len(result))]
    return result


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

is_entering = {}


def timestamp_to_datetime(timestamp):
    datetimeobj = datetime.datetime.fromtimestamp(timestamp / 1000)
    original_time_data = str(datetimeobj)
    entry_time_data = str(datetimeobj)[11:-3]
    exit_time_data = str(datetimeobj)[5:-3]
    return entry_time_data, exit_time_data, original_time_data


# ticker_list = ['BTC/USDT', 'ETH/USDT', 'MATIC/USDT', 'DOGE/USDT', 'BNB/USDT', 'AUD/USDT', 'LTC/USDT', 'ADA/USDT', 'ZEC/USDT', 'EOS/USDT', 'GBP/USDT', 'VET/USDT', 'EUR/USDT', 'XRP/USDT', 'USDC/USDT', 'BUSD/USDT', 'PAX/USDT', 'TUSD/USDT', 'THETA/USDT', 'GRT/USDT', 'FIL/USDT', 'DOT/USDT', 'DASH/USDT', 'BCH/USDT', 'OMG/USDT', 'TRX/USDT', 'ETC/USDT', 'ONT/USDT', 'CKB/USDT', 'XLM/USDT', 'SOL/USDT', 'XMR/USDT', 'ZEN/USDT', 'CAKE/USDT', 'UNI/USDT', 'NEAR/USDT', 'ENJ/USDT', 'BAKE/USDT', 'AR/USDT', 'NEO/USDT', 'SXP/USDT', 'CHZ/USDT', 'RVN/USDT', 'ZIL/USDT', 'XEM/USDT', 'TKO/USDT', 'XTZ/USDT', 'LINK/USDT', 'WRX/USDT', 'PUNDIX/USDT', 'MDX/USDT', 'KAVA/USDT', 'YFI/USDT', 'HOT/USDT', 'DENT/USDT', 'FTM/USDT', 'NANO/USDT', 'SLP/USDT', 'PAXG/USDT', 'QTUM/USDT', 'BAT/USDT', 'ICP/USDT', 'IOST/USDT', 'KSM/USDT', 'STX/USDT', '1INCH/USDT', 'SUSHI/USDT', 'BAND/USDT', 'AAVE/USDT', 'PSG/USDT', 'HBAR/USDT', 'MANA/USDT', 'ANKR/USDT', 'SKL/USDT', 'CRV/USDT', 'BNT/USDT', 'OGN/USDT', 'COTI/USDT', 'AUDIO/USDT', 'NMR/USDT', 'ATOM/USDT', 'FTT/USDT', 'WAVES/USDT', 'SNX/USDT', 'RLC/USDT', 'ALPHA/USDT', 'BAL/USDT', 'COMP/USDT', 'ADAUP/USDT', 'ONE/USDT', 'ZRX/USDT', 'BTT/USDT', 'REEF/USDT', 'SAND/USDT', 'MIR/USDT', 'SC/USDT', 'MKR/USDT', 'STMX/USDT', 'CHR/USDT', 'BADGER/USDT', 'EGLD/USDT', 'SHIB/USDT', 'ALGO/USDT', 'CVC/USDT', 'LPT/USDT', 'CELO/USDT', 'BEL/USDT', 'YFII/USDT', 'ALICE/USDT', 'REN/USDT', 'RUNE/USDT', 'WING/USDT', 'AXS/USDT', 'MITH/USDT', 'DATA/USDT', 'LUNA/USDT', 'AVAX/USDT', 'BTS/USDT', 'KNC/USDT', 'ONG/USDT', 'RSR/USDT', 'TOMO/USDT', 'IOTA/USDT', 'FORTH/USDT', 'LTO/USDT', 'XVS/USDT', 'HNT/USDT', 'FLM/USDT', 'ICX/USDT', 'WIN/USDT', 'ANT/USDT', 'CELR/USDT', 'IOTX/USDT', 'DGB/USDT', 'GTO/USDT', 'PERP/USDT', 'BZRX/USDT', 'DEGO/USDT', 'SFP/USDT', 'LINKUP/USDT', 'NKN/USDT', 'OCEAN/USDT', 'TLM/USDT', 'TRB/USDT', 'BURGER/USDT', 'HARD/USDT', 'STORJ/USDT', 'FIO/USDT', 'BLZ/USDT', 'TFUEL/USDT', 'SXPUP/USDT', 'JST/USDT', 'OXT/USDT', 'DODO/USDT', 'BNBDOWN/USDT', 'SRM/USDT', 'VTHO/USDT', 'GXS/USDT', 'CTK/USDT', 'AKRO/USDT', 'AION/USDT', 'JUV/USDT', 'PNT/USDT', 'FUN/USDT', 'LRC/USDT', 'INJ/USDT', 'COS/USDT', 'UNFI/USDT', 'ROSE/USDT', 'AAVEUP/USDT', 'EPS/USDT', 'FIS/USDT', 'BTCDOWN/USDT', 'HIVE/USDT', 'POND/USDT', 'BNBUP/USDT', 'POLS/USDT', 'LINA/USDT', 'FIRO/USDT', 'XRPUP/USDT', 'FET/USDT', 'KEY/USDT', 'ARPA/USDT', 'TWT/USDT', 'DNT/USDT', 'SUPER/USDT', 'BAR/USDT', 'SUN/USDT', 'BTCUP/USDT', 'NULS/USDT', 'MTL/USDT', 'YFIDOWN/USDT', 'CTSI/USDT']
# ticker_list = list(set(ticker_list) - set(['BUSD/USDT', 'AUD/USDT', 'BRL/USDT', 'EUR/USDT', 'GBP/USDT', 'RUB/USDT', 'TRY/USDT', 'TUSD/USDT', 'USDC/USDT', 'PAX/USDT', 'BIDR/USDT', 'DAI/USDT', 'IDRT/USDT', 'UAH/USDT', 'NGN/USDT', 'VAI/USDT', 'BNVD/USDT']))
time_frame = "1h"

ticker_list = [
    "FIO/USDT",
    "WAVES/USDT",
    "BNT/USDT",
    "TKO/USDT",
    "DODO/USDT",
    "MANA/USDT",
    "YFI/USDT",
    "SOL/USDT",
    "ZEC/USDT",
    "RVN/USDT",
    "CRV/USDT",
    "NEO/USDT",
    "SXP/USDT",
    "SNX/USDT",
    "SRM/USDT",
    "MIR/USDT",
    "IOTX/USDT",
    "ETC/USDT",
    "ADA/USDT",
    "COTI/USDT",
    "WRX/USDT",
    "AVAX/USDT",
    "EGLD/USDT",
    "DASH/USDT",
    "OGN/USDT",
    "PAXG/USDT",
    "ROSE/USDT",
    "DOT/USDT",
    "TLM/USDT",
    "MKR/USDT",
    "KSM/USDT",
    "STMX/USDT",
    "COMP/USDT",
    "KNC/USDT",
    "CHR/USDT",
    "ZEN/USDT",
    "LUNA/USDT",
    "THETA/USDT",
    "ALICE/USDT",
    "NEAR/USDT",
    "RLC/USDT",
    "BCH/USDT",
    "XEM/USDT",
    "1INCH/USDT",
    "BAND/USDT",
    "SUSHI/USDT",
    "TRX/USDT",
    "ALGO/USDT",
    "BTS/USDT",
    "RSR/USDT",
    "LIT/USDT",
    "LRC/USDT",
    "CHZ/USDT",
    "SKL/USDT",
    "GRT/USDT",
    "FTM/USDT",
    "ANKR/USDT",
    "ETH/USDT",
    "RUNE/USDT",
    "DOGE/USDT",
    "OCEAN/USDT",
    "FTT/USDT",
    "ATOM/USDT",
    "XRP/USDT",
    "AXS/USDT",
    "RAMP/USDT",
    "TWT/USDT",
    "PUNDIX/USDT",
    "MATIC/USDT",
    "EOS/USDT",
    "HOT/USDT",
    "IOTA/USDT",
    "BTT/USDT",
    "STORJ/USDT",
    "QTUM/USDT",
    "ALPHA/USDT",
    "ONE/USDT",
    "REEF/USDT",
    "SFP/USDT",
    "KAVA/USDT",
    "XMR/USDT",
    "ONT/USDT",
    "FUN/USDT",
    "HBAR/USDT",
    "AAVE/USDT",
    "XLM/USDT",
    "LINK/USDT",
    "UNI/USDT",
    "DEGO/USDT",
    "TRU/USDT",
    "BZRX/USDT",
    "OXT/USDT",
    "BNB/USDT",
    "STX/USDT",
    "LTC/USDT",
    "BTCUP/USDT",
    "OMG/USDT",
    "FIL/USDT",
    "BAT/USDT",
    "CAKE/USDT",
    "XTZ/USDT",
    "CELR/USDT",
    "ZIL/USDT",
    "BTC/USDT",
    "PERP/USDT",
    "ENJ/USDT",
    "VET/USDT",
]

all_names = []
all_ohlcvs = []
all_dict = {}

temp_time = get_ohlcv("BTC/USDT", time_frame, 1000)
all_times = [temp_time[i][0] for i in range(len(temp_time))]


for i in range(len(ticker_list)):
    temp = get_ohlcv(ticker_list[i], time_frame, 1000)
    all_names.append(ticker_list[i])
    all_ohlcvs.append(temp)
    all_dict[ticker_list[i]] = temp


for magic_number in range(0, 1000):
    a = {}
    b = {}
    for i in range(len(all_ohlcvs)):

        ohlcv = all_ohlcvs[i]
        open_ = ohlcv[-magic_number][1]
        high_ = ohlcv[-magic_number][2]
        low_ = ohlcv[-magic_number][3]
        close_ = ohlcv[-magic_number][4]

        if (high_ - low_) == 0:
            continue

        IBS = (close_ - low_) / (high_ - low_)
        if IBS < 0.1:
            a[all_names[i]] = close_ / open_

        open_ = ohlcv[-magic_number - 1][1]
        high_ = ohlcv[-magic_number - 1][2]
        low_ = ohlcv[-magic_number - 1][3]
        close_ = ohlcv[-magic_number - 1][4]

        if (high_ - low_) == 0:
            continue

        IBS = (close_ - low_) / (high_ - low_)

        if IBS < 0.1:
            b[all_names[i]] = close_ / open_

    if len(a) == 0 or len(b) == 0:
        # print('해당 없음')
        # exit()
        continue

    sort_total = sorted(a.items(), key=lambda item: item[1])

    sort_total2 = sorted(b.items(), key=lambda item: item[1])

    if sort_total[0][1] < sort_total2[0][1]:
        print(timestamp_to_datetime(all_times[-magic_number])[1])
        print(sort_total[0][0])
        # print(sort_total2[0])
