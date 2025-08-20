import ccxt
import time
import pandas as pd
import datetime


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


def get_amount(ticker):
    price = binance.fetch_ohlcv(ticker)[-1][4]
    today_money_BTC = binance.fetch_balance()["BTC"]["total"]
    size = [
        0.0045,
        0.004520342,
        0.004540868,
        0.004561581,
        0.004582485,
        0.004603581,
        0.004624872,
        0.00464636,
        0.00466805,
        0.004689943,
        0.004712042,
        0.00473435,
        0.004756871,
        0.004779607,
        0.004802561,
        0.004825737,
        0.004849138,
        0.004872767,
        0.004896627,
        0.004920722,
        0.004945055,
        0.00496963,
        0.004994451,
        0.00501952,
        0.005044843,
        0.005070423,
        0.005096263,
        0.005122368,
        0.005148741,
        0.005175388,
        0.005202312,
        0.005229518,
        0.005257009,
        0.005284792,
        0.005312869,
        0.005341246,
        0.005369928,
        0.00539892,
        0.005428227,
        0.005457853,
        0.005487805,
        0.005518087,
        0.005548705,
        0.005579665,
        0.005610973,
        0.005642633,
        0.005674653,
        0.005707039,
        0.005739796,
        0.005772931,
        0.005806452,
        0.005840363,
        0.005874674,
        0.005909389,
        0.005944518,
        0.005980066,
        0.006016043,
        0.006052455,
        0.00608931,
        0.006126617,
        0.006164384,
        0.006202619,
        0.006241331,
        0.00628053,
        0.006320225,
        0.006360424,
        0.006401138,
        0.006442377,
        0.00648415,
        0.006526468,
        0.006569343,
        0.006612785,
        0.006656805,
        0.006701415,
        0.006746627,
        0.006792453,
        0.006838906,
        0.006885998,
        0.006933744,
        0.006982157,
        0.00703125,
        0.007081039,
        0.007131537,
        0.007182761,
        0.007234727,
        0.007287449,
        0.007340946,
        0.007395234,
        0.007450331,
        0.007506255,
        0.007563025,
        0.00762066,
        0.007679181,
        0.007738607,
        0.00779896,
        0.007860262,
        0.007922535,
        0.007985803,
        0.008050089,
        0.008115419,
        0.008181818,
        0.008249313,
        0.00831793,
        0.008387698,
        0.008458647,
        0.008530806,
        0.008604207,
        0.008678881,
        0.008754864,
        0.008832188,
        0.008910891,
        0.008991009,
        0.009072581,
        0.009155646,
        0.009240246,
        0.009326425,
        0.009414226,
        0.009503696,
        0.009594883,
        0.009687836,
        0.009782609,
        0.009879254,
        0.009977827,
        0.010078387,
        0.010180995,
        0.010285714,
        0.01039261,
        0.01050175,
        0.010613208,
        0.010727056,
        0.010843373,
        0.010962241,
        0.011083744,
        0.01120797,
        0.011335013,
        0.011464968,
        0.011597938,
        0.011734029,
        0.011873351,
        0.012016021,
        0.012162162,
        0.012311902,
        0.012465374,
        0.012622721,
        0.012784091,
        0.01294964,
        0.013119534,
        0.013293944,
        0.013473054,
        0.013657056,
        0.013846154,
        0.014040562,
        0.014240506,
        0.014446228,
        0.01465798,
        0.014876033,
        0.015100671,
        0.015332198,
        0.015570934,
        0.015817223,
        0.016071429,
        0.016333938,
        0.016605166,
        0.016885553,
        0.017175573,
        0.017475728,
        0.017786561,
        0.018108652,
        0.018442623,
        0.018789144,
        0.019148936,
        0.019522777,
        0.019522777,
        0.019522777,
    ]
    return (today_money_BTC * size[len(is_entering)]) / price


def buy_order(ticker):
    buy_amount = get_amount(ticker)
    order = binance.create_order(ticker, "market", "buy", buy_amount)
    is_entering[ticker] = float(order["amount"]) * 0.998


def ATR(data, length):
    TR = []
    for i in range(length):
        TR.append(
            max(
                (data[i - length][2] - data[i - length][3]),
                abs(data[i - length][2] - data[i - length - 1][4]),
                abs(data[i - length][3] - data[i - length - 1][4]),
            )
        )
    ATR = pd.Series(TR).rolling(length).mean()
    return ATR.tolist()[-1]


def ma(data, length):
    result = []
    for i in range(len(data)):
        result.append(data[i][4])
    return pd.Series(result).rolling(length).mean().tolist()[-1]


ticker_list = [
    "NEO/BTC",
    "DOT/BTC",
    "STORJ/BTC",
    "EOS/BTC",
    "XMR/BTC",
    "DASH/BTC",
    "BNT/BTC",
    "PNT/BTC",
    "NMR/BTC",
    "TOMO/BTC",
    "ZEN/BTC",
    "MCO/BTC",
    "LRC/BTC",
    "RUNE/BTC",
    "KAVA/BTC",
    "CRV/BTC",
    "COMP/BTC",
    "REN/BTC",
    "LEND/BTC",
    "KNC/BTC",
    "BAND/BTC",
    "ZEC/BTC",
    "REP/BTC",
    "MKR/BTC",
    "IOTA/BTC",
    "ICX/BTC",
    "XZC/BTC",
    "OGN/BTC",
    "BZRX/BTC",
    "WNXM/BTC",
    "DCR/BTC",
    "ALGO/BTC",
    "NANO/BTC",
    "ZRX/BTC",
    "SXP/BTC",
    "TRB/BTC",
    "BAT/BTC",
    "LINK/BTC",
    "YFII/BTC",
    "ANT/BTC",
    "ETH/BTC",
    "GXS/BTC",
    "SOL/BTC",
    "THETA/BTC",
    "BAL/BTC",
    "XTZ/BTC",
    "LUNA/BTC",
    "SRM/BTC",
    "MTL/BTC",
    "WAVES/BTC",
    "RLC/BTC",
    "ETC/BTC",
    "OMG/BTC",
    "EGLD/BTC",
    "NULS/BTC",
    "YFI/BTC",
    "ONT/BTC",
    "OCEAN/BTC",
    "QTUM/BTC",
    "PAXG/BTC",
    "LTC/BTC",
    "LSK/BTC",
    "STRAT/BTC",
    "WAN/BTC",
    "BNB/BTC",
    "FTT/BTC",
    "BCH/BTC",
    "WTC/BTC",
    "ATOM/BTC",
    "HC/BTC",
    "SNX/BTC",
    "XRP/BTC",
    "SUSHI/BTC",
    "KMD/BTC",
]

exchange_class = getattr(ccxt, "binance")
binance = exchange_class()
binance.enableRateLimit = True
binance.RateLimit = 10000
binance.apiKey = "FRbVseExyAWjQUtYFnS4memLnPCcgNAeRW7HEBrrw9qyIyPUMCTzUKxZKOJIHcfV"
binance.secret = "CbDX3DE5r9ErdLBOphDB4rjCaAaKbUqITbNK05YIitktZ24VfcNrvVRbIgfK6L87"
binance.load_markets()
is_entering = {}
time_frame = "5m"


while 1:
    time_ = get_time()[1][3:]
    if time_ == "0" or time_ == "5":
        break
    else:
        time.sleep(27)


while True:
    time.sleep(0.01)
    ban_list = []
    time_ = get_time()[1][3:]
    if time_ == "0" or time_ == "5":
        for i, item in enumerate(ticker_list):
            try:
                if item not in list(is_entering.keys()):  # not buy
                    # buy_side
                    ohlcv = binance.fetch_ohlcv(item, time_frame)
                    target_price = ma(ohlcv[-10:-1], 9) - (1.5 * ATR(ohlcv[-7:-1], 5))
                    if ohlcv[-2][2] <= target_price:
                        buy_order(item)
                        continue
            except:
                time.sleep(0.1)
                continue

    for i in range(len(is_entering)):
        try:
            # sell_side
            ohlcv = binance.fetch_ohlcv(item, time_frame)
            target_price = ma(ohlcv[-10:-1], 9) + (1.5 * ATR(ohlcv[-7:-1], 5))
            if ohlcv[-2][3] >= target_price:
                sell_amount = is_entering[item]
                binance.create_order(item, "market", "sell", sell_amount)
                ban_list.append(item)
        except:
            time.sleep(0.1)
            continue

    for i in range(len(ban_list)):
        del is_entering[ban_list[i]]
