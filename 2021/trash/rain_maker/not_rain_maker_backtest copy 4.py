import numpy as np
import datetime
import urllib
import ccxt
import json


def TW(odd):
    return np.round(-np.log(0.99) / (np.log(1 + 0.01 * odd) - np.log(0.99)), 4)


def shortest_distance(odd, winrate, n=100000):
    lins = np.linspace(0, 10, n)
    y = TW(lins)
    least_distance = 1e100
    for i in range(n):
        dx = lins[i] - odd
        dy = y[i] - winrate
        distance = np.sqrt(dx**2 + dy**2)
        if distance < least_distance:
            least_distance = distance
    if winrate > TW(odd):
        return np.round(least_distance, 10)
    else:
        return -1 * np.round(least_distance, 10)


def get_perfomance(trade_log):
    if len(trade_log) == 0:
        return None
    win = []
    lose = []
    risk_free = 0.038 / 365
    avg = np.mean(trade_log)
    std = np.std(trade_log)
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
    print("평균수익거래 :", np.mean(win))
    print("평균손실거래 :", np.mean(lose))
    avg_W_L_ratio = -1 * np.mean(win) / np.mean(lose)
    print("평균손익비 :", avg_W_L_ratio)
    win_rate = int(round(len(win) / len(trade_log), 2) * 100)

    print("승률 :", win_rate, "%")
    print("포지션 사이징 :", size)
    if len(lose) > 0:
        # print(lose)
        print("최대 손실 :", min(lose))
    total_perform = shortest_distance(avg_W_L_ratio, len(win) / len(trade_log))
    print(total_perform)
    perform_value.append(total_perform)
    winrate.append(win_rate)
    print("")


def timestamp_to_datetime(timestamp):
    datetimeobj = datetime.datetime.fromtimestamp(timestamp / 1000)
    original_time_data = str(datetimeobj)
    entry_time_data = str(datetimeobj)[11:-3]
    exit_time_data = str(datetimeobj)[5:-3]
    return entry_time_data, exit_time_data, original_time_data


def log_maker():
    buy_sell_log = []
    all_names = []
    all_ohlcvs = []
    all_dict = {}

    time_size = 1000
    for i in range(len(ticker_list)):
        temp = get_ohlcv(ticker_list[i], time_frame, time_size)
        if len(temp) != time_size:
            print(ticker_list[i])
            continue
        all_names.append(ticker_list[i])
        all_ohlcvs.append(temp)
        all_dict[ticker_list[i]] = temp

    print(len(all_names))

    for magic_number in range(len(all_ohlcvs[0])):
        a = {}
        b = {}
        c = {}
        for i in range(len(all_ohlcvs)):

            ohlcv = all_ohlcvs[i]
            open_ = ohlcv[magic_number][1]
            close_ = ohlcv[magic_number][4]

            a[all_names[i]] = close_ / open_

            open_ = ohlcv[magic_number - 1][1]
            close_ = ohlcv[magic_number - 1][4]

            b[all_names[i]] = close_ / open_

            open_ = ohlcv[magic_number - 2][1]
            close_ = ohlcv[magic_number - 2][4]

            c[all_names[i]] = close_ / open_

        # if len(a) == 0 or len(b) == 0 or len(c) == 0:
        #    buy_sell_log.append(None)
        #    continue

        sort_total = sorted(a.items(), key=lambda item: item[1])

        sort_total2 = sorted(b.items(), key=lambda item: item[1])

        sort_total3 = sorted(c.items(), key=lambda item: item[1])

        if (
            sort_total[0][1] < sort_total2[0][1]
            and sort_total[0][1] < sort_total3[0][1]
        ):
            buy_sell_log.append(sort_total[0][0])

        else:
            buy_sell_log.append(None)

    temp = [sort_total[i][1] for i in range(len(sort_total))]
    print(sum(temp) / len(temp))

    temp2 = [sort_total2[i][1] for i in range(len(sort_total2))]
    print(sum(temp2) / len(temp2))

    temp3 = [sort_total3[i][1] for i in range(len(sort_total3))]
    print(sum(temp3) / len(temp3))

    # buy_sell_log.reverse()
    print(buy_sell_log)
    for i in range(0, len(buy_sell_log)):
        # if i == 998:
        #    break
        if buy_sell_log[i] != None:
            try:
                base_ohlcv = all_dict[buy_sell_log[i]]
                entry_price = base_ohlcv[i + 1][1]
                exit_price = base_ohlcv[i + 1][4]
                earning = 100 * (exit_price / entry_price * Slippage - 1)
                all_earn.append(earning)

                print(
                    buy_sell_log[i],
                    timestamp_to_datetime(base_ohlcv[i + 1][0])[1],
                    round(earning, 2),
                    entry_price,
                    exit_price,
                )
            except:
                base_ohlcv = all_dict[buy_sell_log[i]]
                entry_price = base_ohlcv[i][1]
                entry_price = base_ohlcv[i][4]
                earning = 100 * (exit_price / entry_price * Slippage - 1)
                print(
                    buy_sell_log[i],
                    timestamp_to_datetime(base_ohlcv[i][0])[1],
                    round(earning, 2),
                    entry_price,
                    exit_price,
                )
            continue


# ccxt ex.fetch_ohlcv() 보다 훨씬 빠르게 ohlcv 얻기
def get_ohlcv(ticker="BTC/USDT", interval="1m", limit=200):
    # cdef int i = 0
    try:
        temp = ticker.split("/")
        ticker = f"{temp[0]}{temp[1]}"
        url = f"https://api.binance.com/api/v3/klines?symbol={ticker}&interval={interval}&limit={str(limit)}"
        # url = f'https://fapi.binance.com/fapi/v1/klines?symbol={ticker}&interval={interval}&limit={str(limit)}'
        text_data = urllib.request.urlopen(url).read().decode("utf-8")
        buy_sell_log = json.loads(text_data)
    # except Exception as e:
    except Exception as e:
        print(
            e,
            "\n",
            "ccxt.base.errors.BadSymbol: binance does not have market symbol {0}".format(
                ticker
            ),
        )
        return [[0]]
    buy_sell_log = [list(map(float, buy_sell_log[i])) for i in range(len(buy_sell_log))]
    return buy_sell_log


binance = ccxt.binance(
    {
        # "options": {"defaultType": "future"},
        "timeout": 30000,
        # "apiKey":"",
        # "secret": "",
        "enableRateLimit": False,
    }
)
binance.load_markets()

# ticker_list = ['FIO/USDT', 'WAVES/USDT', 'BNT/USDT', 'TKO/USDT', 'DODO/USDT', 'MANA/USDT', 'YFI/USDT', 'SOL/USDT', 'ZEC/USDT', 'RVN/USDT', 'CRV/USDT', 'NEO/USDT', 'SXP/USDT', 'SNX/USDT', 'SRM/USDT', 'MIR/USDT', 'IOTX/USDT', 'ETC/USDT', 'ADA/USDT', 'COTI/USDT', 'WRX/USDT', 'AVAX/USDT', 'EGLD/USDT', 'DASH/USDT', 'OGN/USDT', 'PAXG/USDT', 'ROSE/USDT', 'DOT/USDT', 'TLM/USDT', 'MKR/USDT', 'KSM/USDT', 'STMX/USDT', 'COMP/USDT', 'KNC/USDT', 'CHR/USDT', 'ZEN/USDT', 'LUNA/USDT', 'THETA/USDT', 'ALICE/USDT', 'NEAR/USDT', 'RLC/USDT', 'BCH/USDT', 'XEM/USDT', '1INCH/USDT', 'BAND/USDT', 'SUSHI/USDT', 'TRX/USDT', 'ALGO/USDT', 'BTS/USDT', 'RSR/USDT', 'LIT/USDT', 'LRC/USDT', 'CHZ/USDT', 'SKL/USDT', 'GRT/USDT', 'FTM/USDT', 'ANKR/USDT', 'ETH/USDT', 'RUNE/USDT', 'DOGE/USDT', 'OCEAN/USDT', 'FTT/USDT', 'ATOM/USDT', 'XRP/USDT', 'AXS/USDT', 'RAMP/USDT', 'TWT/USDT', 'PUNDIX/USDT', 'MATIC/USDT', 'EOS/USDT', 'HOT/USDT', 'IOTA/USDT', 'BTT/USDT', 'STORJ/USDT', 'QTUM/USDT', 'ALPHA/USDT', 'ONE/USDT', 'REEF/USDT', 'SFP/USDT', 'KAVA/USDT', 'XMR/USDT', 'ONT/USDT', 'FUN/USDT', 'HBAR/USDT', 'AAVE/USDT', 'XLM/USDT', 'LINK/USDT', 'UNI/USDT', 'DEGO/USDT', 'TRU/USDT', 'BZRX/USDT', 'OXT/USDT', 'BNB/USDT', 'STX/USDT', 'LTC/USDT', 'BTCUP/USDT', 'OMG/USDT', 'FIL/USDT', 'BAT/USDT', 'CAKE/USDT', 'XTZ/USDT', 'CELR/USDT', 'ZIL/USDT', 'BTC/USDT', 'PERP/USDT', 'ENJ/USDT', 'VET/USDT']

# ticker_list = ['BTC/USDT', 'AUD/USDT', 'ETH/USDT', 'BNB/USDT', 'DOGE/USDT', 'ATA/USDT', 'BCH/USDT', 'LTC/USDT', 'GBP/USDT', 'EUR/USDT', 'PAXG/USDT', 'PAX/USDT', 'USDC/USDT', 'TUSD/USDT', 'BUSD/USDT', 'TRX/USDT', '1INCH/USDT', 'XLM/USDT', 'THETA/USDT', 'UNFI/USDT', 'FIL/USDT', 'NEO/USDT', 'MATIC/USDT', 'EOS/USDT', 'BTT/USDT', 'ZEC/USDT', 'LINK/USDT', 'XRP/USDT', 'CTSI/USDT', 'DASH/USDT', 'ADA/USDT', 'ONT/USDT', 'DOT/USDT', 'CRV/USDT', 'XMR/USDT', 'OMG/USDT', 'AAVE/USDT', 'ATOM/USDT', 'UNI/USDT', 'CELR/USDT', 'RVN/USDT', 'YFI/USDT', 'NEAR/USDT', 'CHZ/USDT', 'DIA/USDT', 'TWT/USDT', 'XTZ/USDT', 'TLM/USDT', 'BAND/USDT', 'SUSHI/USDT', 'VET/USDT', 'GRT/USDT', 'BADGER/USDT', 'BAT/USDT', 'ETC/USDT', 'REEF/USDT', 'HOT/USDT', 'BAKE/USDT', 'LPT/USDT', 'WAVES/USDT', 'EGLD/USDT', 'ZIL/USDT', 'ZEN/USDT', 'KSM/USDT', 'ANKR/USDT', 'ALGO/USDT', 'FTM/USDT', 'INJ/USDT', 'QTUM/USDT', 'LUNA/USDT', 'ICP/USDT', 'STRAX/USDT', 'IOTA/USDT', 'RAMP/USDT', 'NU/USDT', 'BNT/USDT', 'BTS/USDT', 'KNC/USDT', 'BEAM/USDT', 'SOL/USDT', 'RUNE/USDT', 'KAVA/USDT', 'LTO/USDT', 'SXP/USDT', 'TRU/USDT', 'AVAX/USDT', 'WRX/USDT', 'MKR/USDT', 'TFUEL/USDT', 'COMP/USDT', 'WIN/USDT', 'JST/USDT', 'IOST/USDT', 'ALPHA/USDT', 'TKO/USDT', 'CVC/USDT', 'SFP/USDT', 'ARPA/USDT', 'OXT/USDT', 'CAKE/USDT', 'XEM/USDT', 'ENJ/USDT', 'BTCDOWN/USDT', 'RSR/USDT', 'LINKUP/USDT', 'ONE/USDT', 'IOTX/USDT', 'MANA/USDT', 'HBAR/USDT', 'PERP/USDT', 'REN/USDT', 'FLM/USDT', 'UMA/USDT', 'SNX/USDT', 'COS/USDT', 'MIR/USDT', 'DODO/USDT', 'SHIB/USDT', 'ADAUP/USDT', 'LIT/USDT', 'STORJ/USDT', 'ZRX/USDT']

# ticker_list = ['ADA/BTC', 'BNB/BTC', 'ETH/BTC', 'LTC/BTC', 'DOT/BTC', 'POLS/BTC', 'EPS/BTC', 'SUSHI/BTC', 'ETC/BTC', 'UNI/BTC', 'ZEC/BTC', 'XRP/BTC', 'MDA/BTC', 'SOL/BTC', 'SNX/BTC', 'LINK/BTC', 'XLM/BTC', 'SUSD/BTC', 'ORN/BTC', 'DOGE/BTC', 'THETA/BTC', 'LPT/BTC', 'ALGO/BTC', 'LRC/BTC', 'ICP/BTC', 'TOMO/BTC', 'FET/BTC', 'FTM/BTC', 'MATIC/BTC', 'BZRX/BTC', 'CAKE/BTC', 'BAND/BTC', 'SXP/BTC', 'FLM/BTC', 'GAS/BTC', 'CELO/BTC', 'ATOM/BTC', 'OMG/BTC', 'ENJ/BTC', 'OG/BTC', 'EOS/BTC', 'AVAX/BTC', 'NEO/BTC', 'LUNA/BTC', 'POWR/BTC', 'MANA/BTC', 'CHZ/BTC', 'QTUM/BTC', 'NANO/BTC', 'REN/BTC', 'ALPHA/BTC', 'WAVES/BTC', 'ZRX/BTC', 'WTC/BTC', 'BAT/BTC', 'FIL/BTC', 'SRM/BTC', 'LTO/BTC', 'RDN/BTC', 'CRV/BTC', 'BNT/BTC', 'MIR/BTC', 'HBAR/BTC', 'UMA/BTC', 'FTT/BTC', 'AUDIO/BTC', 'KNC/BTC', 'CTSI/BTC', 'ICX/BTC', 'COTI/BTC', 'STORJ/BTC', 'CTK/BTC', 'OCEAN/BTC', 'ONT/BTC', 'HIVE/BTC', 'WRX/BTC', 'IOTA/BTC', 'RIF/BTC', 'TFUEL/BTC', 'NULS/BTC', 'SYS/BTC', 'GRT/BTC', 'INJ/BTC', 'NAV/BTC', 'SKL/BTC', 'XTZ/BTC', 'KAVA/BTC', 'RLC/BTC', 'BCD/BTC', 'AST/BTC', 'DNT/BTC', 'OAX/BTC', 'LSK/BTC', 'NU/BTC', 'FRONT/BTC', '1INCH/BTC', 'BRD/BTC', 'NEAR/BTC', 'UTK/BTC', 'ATA/BTC', 'OGN/BTC', 'CVC/BTC', 'GLM/BTC', 'BQX/BTC', 'AVA/BTC', 'HNT/BTC', 'RUNE/BTC', 'PIVX/BTC', 'ONG/BTC', 'ACM/BTC', 'PERP/BTC', 'GVT/BTC', 'ADX/BTC', 'MDX/BTC', 'POLY/BTC', 'XVS/BTC', 'ELF/BTC', 'EZ/BTC', 'VET/BTC', 'STX/BTC', 'WABI/BTC', 'PHA/BTC', 'ZIL/BTC', 'DUSK/BTC', 'BEL/BTC', 'STRAX/BTC', 'KMD/BTC', 'AXS/BTC', 'ALICE/BTC', 'STEEM/BTC', 'ARDR/BTC', 'SFP/BTC', 'POND/BTC', 'TRU/BTC', 'ANKR/BTC', 'SAND/BTC', 'ANT/BTC', 'CTXC/BTC', 'CHR/BTC', 'DEGO/BTC', 'GXS/BTC', 'ONE/BTC', 'AION/BTC', 'PNT/BTC', 'CFX/BTC', 'BLZ/BTC', 'ARK/BTC', 'SUN/BTC', 'XEM/BTC', 'DIA/BTC', 'SNT/BTC', 'FIO/BTC', 'DREP/BTC', 'VITE/BTC', 'NKN/BTC', 'DLT/BTC', 'OM/BTC', 'REQ/BTC', 'DODO/BTC', 'BEAM/BTC', 'APPC/BTC', 'TLM/BTC', 'PSG/BTC', 'TKO/BTC', 'RAMP/BTC', 'TRX/BTC', 'LIT/BTC', 'RVN/BTC', 'WAN/BTC', 'GRS/BTC', 'ROSE/BTC', 'OXT/BTC', 'BADGER/BTC', 'SKY/BTC', 'LOOM/BTC', 'PPT/BTC', 'REP/BTC', 'JUV/BTC', 'ATM/BTC', 'TWT/BTC', 'NXS/BTC', 'RCN/BTC', 'VIDT/BTC', 'FIRO/BTC', 'DGB/BTC', 'SCRT/BTC', 'UNFI/BTC', 'GTO/BTC', 'AERGO/BTC', 'HARD/BTC', 'VIA/BTC', 'MTL/BTC', 'NEBL/BTC', 'ASR/BTC', 'EVX/BTC']

# ticker_list = ['LTC/ETH', 'BNB/ETH', 'ADA/ETH', 'VET/ETH', 'XRP/ETH', 'ZIL/ETH', 'XLM/ETH', 'TRX/ETH', 'EOS/ETH', 'LINK/ETH', 'QTUM/ETH', 'ETC/ETH', 'PUNDIX/ETH', 'NEO/ETH', 'DEXE/ETH', 'ENJ/ETH', 'GRT/ETH', 'OMG/ETH', 'THETA/ETH', 'FUN/ETH', 'MTL/ETH', 'RLC/ETH', 'HOT/ETH', 'ELF/ETH', 'ZRX/ETH', 'IOTX/ETH', 'BAT/ETH', 'STMX/ETH', 'GXS/ETH', 'SCRT/ETH', 'NAV/ETH', 'NANO/ETH', 'XVG/ETH', 'LSK/ETH', 'IOTA/ETH', 'IOST/ETH', 'LOOM/ETH', 'SC/ETH', 'WAVES/ETH', 'SLP/ETH', 'XEM/ETH', 'ICX/ETH', 'WAN/ETH', 'BQX/ETH', 'MFT/ETH', 'KNC/ETH', 'STRAX/ETH', 'ONT/ETH', 'MANA/ETH', 'KMD/ETH', 'STEEM/ETH', 'CDT/ETH', 'QKC/ETH', 'BNT/ETH', 'UFT/ETH', 'GLM/ETH', 'KEY/ETH', 'PROS/ETH', 'ADX/ETH', 'BLZ/ETH', 'BRD/ETH', 'NCASH/ETH', 'VIB/ETH', 'NEBL/ETH', 'QLC/ETH', 'FRONT/ETH', 'QSP/ETH']

# ticker_list = ['PROM/BNB', 'ZIL/BNB', 'ADA/BNB', 'ETC/BNB', 'XRP/BNB', 'MATIC/BNB', 'LTC/BNB', 'BTT/BNB', 'TRX/BNB', 'DOT/BNB', 'ICP/BNB', 'CAKE/BNB', 'VET/BNB', 'FIL/BNB', 'LUNA/BNB', 'EOS/BNB', 'UNI/BNB', 'IOTA/BNB', 'CHR/BNB', 'AAVE/BNB', 'SUSHI/BNB', 'CTSI/BNB', 'BAKE/BNB', 'ATA/BNB', 'RUNE/BNB', 'CHZ/BNB', 'STX/BNB', 'XLM/BNB', 'AVAX/BNB', 'ZEN/BNB', 'SOL/BNB', 'INJ/BNB', 'ALGO/BNB', 'KSM/BNB', 'THETA/BNB', 'AVA/BNB', 'NEO/BNB', 'SPARTA/BNB', 'ATOM/BNB', 'ENJ/BNB', 'WRX/BNB', 'OGN/BNB', 'OCEAN/BNB', 'FTM/BNB', 'SXP/BNB', 'ONE/BNB', 'XVS/BNB', 'XTZ/BNB', 'ICX/BNB', 'ALPHA/BNB', 'WAVES/BNB', 'ONT/BNB', 'NU/BNB', 'RVN/BNB', 'FIO/BNB', 'HBAR/BNB', 'WABI/BNB', 'COCOS/BNB', 'NEAR/BNB', 'IOST/BNB', 'DGB/BNB', 'CELR/BNB', 'MBL/BNB', 'COTI/BNB', 'VTHO/BNB', 'KAVA/BNB', 'ANT/BNB', 'RSR/BNB', 'CTK/BNB', 'PERL/BNB', 'EGLD/BNB', 'SAND/BNB', 'AXS/BNB', 'SNX/BNB', 'SRM/BNB', 'SWRV/BNB', 'BLZ/BNB', 'ANKR/BNB', 'BURGER/BNB', 'HOT/BNB', 'COS/BNB', 'CRV/BNB', 'JST/BNB', 'BAT/BNB', 'ARPA/BNB', 'DIA/BNB']

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
    "COMP/USDT",
    "OMG/USDT",
    "DOGE/USDT",
    "SXP/USDT",
    "KAVA/USDT",
    "BAND/USDT",
    "RLC/USDT",
    "WAVES/USDT",
    "MKR/USDT",
    "SNX/USDT",
    "DOT/USDT",
    "DEFI/USDT",
    "YFI/USDT",
    "BAL/USDT",
    "CRV/USDT",
    "TRB/USDT",
    "YFII/USDT",
    "RUNE/USDT",
    "SUSHI/USDT",
    "SRM/USDT",
    "BZRX/USDT",
    "EGLD/USDT",
    "SOL/USDT",
    "ICX/USDT",
    "STORJ/USDT",
    "BLZ/USDT",
    "UNI/USDT",
    "AVAX/USDT",
    "FTM/USDT",
    "HNT/USDT",
    "ENJ/USDT",
    "FLM/USDT",
    "TOMO/USDT",
    "REN/USDT",
    "KSM/USDT",
    "NEAR/USDT",
    "AAVE/USDT",
    "FIL/USDT",
    "RSR/USDT",
    "LRC/USDT",
    "MATIC/USDT",
    "OCEAN/USDT",
    "CVC/USDT",
    "BEL/USDT",
    "CTK/USDT",
    "AXS/USDT",
    "ALPHA/USDT",
    "ZEN/USDT",
    "SKL/USDT",
    "GRT/USDT",
    "1INCH/USDT",
    "BTC/BUSD",
    "AKRO/USDT",
    "CHZ/USDT",
    "SAND/USDT",
    "ANKR/USDT",
    "LUNA/USDT",
    "BTS/USDT",
    "LIT/USDT",
    "UNFI/USDT",
    "DODO/USDT",
    "REEF/USDT",
    "RVN/USDT",
    "SFP/USDT",
    "XEM/USDT",
    "COTI/USDT",
    "CHR/USDT",
    "MANA/USDT",
    "ALICE/USDT",
    "HBAR/USDT",
    "ONE/USDT",
    "LINA/USDT",
    "STMX/USDT",
    "DENT/USDT",
    "CELR/USDT",
    "HOT/USDT",
    "MTL/USDT",
    "OGN/USDT",
    "BTT/USDT",
    "NKN/USDT",
    "SC/USDT",
    "DGB/USDT",
    "1000SHIB/USDT",
    "ICP/USDT",
    "BAKE/USDT",
]


Slippage = 0.9982 * 0.9982
time_frame = "1h"
perform_value = []
winrate = []


print(len(ticker_list))


success = []
fail = []
lose_earn = []
all_earn = []

print("")
aaaa = log_maker()
print("")
get_perfomance(all_earn)
