from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
from scipy.signal import argrelextrema
import Utils
import pandas_ta as ta


# get_plt(ticker, 'Close')
# get_plt(ticker, 'rsi')
def get_plt(ticker_name, index_name):
    Ohlcv = binance.fetch_ohlcv(ticker_name, "1d", None, 100)
    if len(Ohlcv) < 100:
        return None
    data = pd.DataFrame(
        data=np.array(Ohlcv), columns=["Time", "Open", "High", "Low", "Close", "V"]
    )  ## rsi(15, high)
    rsi_entry = data.ta.rsi(length=14).tolist()
    data.insert(6, "rsi", rsi_entry, True)

    colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    max_idx = argrelextrema(data[index_name].values, np.greater, order=5)[0]
    min_idx = argrelextrema(data[index_name].values, np.less, order=5)[0]

    plt.figure(figsize=(15, 8))
    plt.plot(data[index_name], zorder=0)
    plt.scatter(
        data.iloc[max_idx].index,
        data.iloc[max_idx][index_name],
        label="Maxima",
        s=100,
        color=colors[1],
        marker="^",
    )
    plt.scatter(
        data.iloc[min_idx].index,
        data.iloc[min_idx][index_name],
        label="Minima",
        s=100,
        color=colors[2],
        marker="v",
    )

    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.title(f"Local Maxima and Minima for {ticker_name}")
    plt.legend()
    plt.show()


def get_target(ticker_name, timeframe):
    Ohlcv = binance.fetch_ohlcv(ticker_name, timeframe, None, 100)
    data = pd.DataFrame(
        data=np.array(Ohlcv), columns=["Time", "Open", "High", "Low", "Close", "V"]
    )  ## rsi(15, high)
    rsi_entry = data.ta.rsi(length=14).tolist()

    if rsi_entry[-1] > 30 and rsi_entry[-1] < 70:
        return None

    data.insert(6, "rsi", rsi_entry, True)
    data = data.fillna(0)

    max_price = argrelextrema(data["Close"].values, np.greater, order=5)[0][-2:]
    min_price = argrelextrema(data["Close"].values, np.less, order=5)[0][-2:]
    max_rsi = argrelextrema(data["rsi"].values, np.greater, order=5)[0][-2:]
    min_rsi = argrelextrema(data["rsi"].values, np.less, order=5)[0][-2:]

    if len(max_price) > 1:
        max_before = data.iloc[max_price[0]]
        max_after = data.iloc[max_price[1]]
        if max_price[-1] > 97:
            if (
                np.array_equal(max_price, max_rsi)
                and data["rsi"][max_rsi[0]] > 80
                and data["rsi"][max_rsi[1]] > 70
            ):
                if (
                    max_before["rsi"] > max_after["rsi"]
                    and max_before["Close"] < max_after["Close"]
                ):
                    print("overbuy", ticker_name)

    if len(min_price) > 1:
        min_before = data.iloc[min_price[0]]
        min_after = data.iloc[min_price[1]]
        if min_price[-1] > 97:
            if (
                np.array_equal(min_price, min_rsi)
                and data["rsi"][min_rsi[0]] < 20
                and data["rsi"][min_rsi[1]] < 30
            ):
                if (
                    min_before["rsi"] < min_after["rsi"]
                    and min_before["Close"] > min_after["Close"]
                ):
                    print("oversell", ticker_name)
                    print("")


if __name__ == "__main__":
    binance = Utils.use_binance()
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
        "ICP/USDT",
        "BAKE/USDT",
        "GTC/USDT",
        "KEEP/USDT",
    ]

    # ticker_list = ['BTC/USDT', 'ETH/USDT', 'BETA/USDT', 'SAND/USDT', 'DAR/USDT', 'AVAX/USDT', 'DYDX/USDT', 'AXS/USDT', 'DREP/USDT', 'SUSHI/USDT', 'XRP/USDT', 'TRX/USDT', 'GTC/USDT', 'AUD/USDT', 'RAY/USDT', 'NEAR/USDT', 'GRT/USDT', 'OMG/USDT', 'ANT/USDT', 'BNB/USDT', 'FIRO/USDT', 'LINA/USDT', 'UST/USDT', 'WIN/USDT', 'QTUM/USDT', 'ZIL/USDT', 'CELR/USDT', 'FXS/USDT', 'ALGO/USDT', 'FIL/USDT', 'FLM/USDT', 'SOL/USDT', 'SHIB/USDT', 'ETC/USDT', 'ONT/USDT', 'GALA/USDT', 'MANA/USDT', 'FTM/USDT', 'RVN/USDT', 'ZEN/USDT', 'EOS/USDT', 'RSR/USDT', 'CHZ/USDT', 'GTO/USDT', 'ONE/USDT', 'VET/USDT', 'KSM/USDT', 'BTT/USDT', 'LUNA/USDT', 'DOT/USDT', 'MBOX/USDT', 'ENJ/USDT', 'XLM/USDT', 'AR/USDT', 'EGLD/USDT', 'ATOM/USDT', 'LAZIO/USDT', 'HOT/USDT', 'MATIC/USDT', 'IOTX/USDT', 'THETA/USDT', 'COS/USDT', 'ICP/USDT', 'RNDR/USDT', 'AKRO/USDT', 'BLZ/USDT', 'BCH/USDT', 'OGN/USDT', 'MTL/USDT', 'COMP/USDT', 'XMR/USDT', 'FLUX/USDT', 'ANKR/USDT', 'LTO/USDT', 'BAT/USDT', 'BTCDOWN/USDT', 'ENS/USDT', 'FTT/USDT', 'SNX/USDT', 'COTI/USDT', 'TOMO/USDT', 'AVA/USDT', 'REEF/USDT', 'IOTA/USDT', 'KAVA/USDT', 'SRM/USDT', 'CHESS/USDT', 'PAXG/USDT', 'YGG/USDT', 'DOGE/USDT', 'BTS/USDT', 'CVC/USDT', 'CRV/USDT', 'IOST/USDT', 'YFI/USDT', 'LRC/USDT', 'OM/USDT', 'BEL/USDT', 'XVS/USDT', 'VOXEL/USDT', 'TROY/USDT', 'QI/USDT', 'ZEC/USDT', 'CHR/USDT', 'WAVES/USDT', 'REN/USDT', 'RUNE/USDT', 'LTC/USDT', 'HBAR/USDT', 'POND/USDT', 'ADA/USDT', 'JST/USDT', 'YFII/USDT', 'UNFI/USDT', 'DASH/USDT', 'NEO/USDT', 'GBP/USDT', 'ZRX/USDT', 'LPT/USDT', 'ALICE/USDT', 'KNC/USDT', '1INCH/USDT', 'XEM/USDT', 'TKO/USDT', 'KLAY/USDT', 'AAVE/USDT', 'OCEAN/USDT', 'HNT/USDT', 'DOTUP/USDT', 'MITH/USDT', 'CAKE/USDT', 'STORJ/USDT', 'MINA/USDT', 'MIR/USDT', 'WRX/USDT', 'HARD/USDT', 'DGB/USDT', 'ARPA/USDT', 'SPELL/USDT', 'XTZ/USDT', 'EUR/USDT', 'SUN/USDT', 'DUSK/USDT', 'STMX/USDT', 'XEC/USDT', 'BAKE/USDT', 'SKL/USDT', 'DENT/USDT', 'RLC/USDT', 'TVK/USDT', 'NU/USDT', 'CTXC/USDT', 'LIT/USDT', 'LINK/USDT', 'ALPHA/USDT', 'ROSE/USDT', 'SFP/USDT', 'CTSI/USDT', 'TFUEL/USDT', 'QUICK/USDT', 'MDT/USDT', 'FORTH/USDT', 'QNT/USDT', 'UNI/USDT', 'PORTO/USDT', 'POLS/USDT', 'DODO/USDT', 'KEEP/USDT', 'C98/USDT', 'PERP/USDT', 'AUDIO/USDT', 'NULS/USDT', 'ETHUP/USDT', 'INJ/USDT', 'BAND/USDT', 'FLOW/USDT', 'PHA/USDT', 'SUPER/USDT', 'ETHDOWN/USDT', 'ATA/USDT', 'CTK/USDT', 'XRPUP/USDT', 'HIVE/USDT', 'MKR/USDT', 'ADX/USDT', 'UTK/USDT', 'BAL/USDT', 'MASK/USDT', 'TWT/USDT', 'FIO/USDT', 'ICX/USDT', 'DOCK/USDT', 'SC/USDT', 'CELO/USDT', 'OXT/USDT', 'BTCST/USDT', 'DATA/USDT', 'WAXP/USDT', 'JASMY/USDT', 'BTCUP/USDT', 'SXP/USDT', 'KEY/USDT', 'GXS/USDT', 'TLM/USDT', 'VIDT/USDT', 'CLV/USDT', 'STRAX/USDT', 'TCT/USDT', 'POLY/USDT', 'ILV/USDT', 'TRB/USDT', 'BNX/USDT', 'DNT/USDT', 'FET/USDT', 'PEOPLE/USDT', 'DIA/USDT', 'PERL/USDT', 'DEGO/USDT', 'AMP/USDT', 'PNT/USDT', 'BOND/USDT', 'EPS/USDT', 'NKN/USDT', 'FOR/USDT', 'VTHO/USDT', 'WAN/USDT', 'NANO/USDT', 'FARM/USDT', 'VGX/USDT', 'MLN/USDT', 'XVG/USDT', 'JOE/USDT', 'FUN/USDT', 'HIGH/USDT']
    # ticker_list = ticker_list + ['ETH/BTC', 'BNB/BTC', 'MATIC/BTC', 'MTL/BTC', 'LINK/BTC', 'SAND/BTC', 'SOL/BTC', 'LTC/BTC', 'DOT/BTC', 'ADA/BTC', 'AAVE/BTC', 'LUNA/BTC', 'CAKE/BTC', 'AVAX/BTC', 'XTZ/BTC', 'NEAR/BTC', 'XMR/BTC', 'FTT/BTC', 'AXS/BTC', 'UNI/BTC', 'ENJ/BTC', 'SUSHI/BTC', 'OCEAN/BTC', 'MANA/BTC', 'XRP/BTC', 'FTM/BTC', 'ZEC/BTC', 'LRC/BTC', 'ONT/BTC', 'ATOM/BTC', 'DYDX/BTC', 'ALICE/BTC', 'OMG/BTC', 'BAT/BTC', 'EGLD/BTC', 'GAS/BTC', 'CELO/BTC', 'ADX/BTC', 'LPT/BTC', 'ICX/BTC', 'FLUX/BTC', 'TRIBE/BTC', '1INCH/BTC', 'THETA/BTC', 'SXP/BTC', 'IOTA/BTC', 'MIR/BTC', 'MDA/BTC', 'GALA/BTC', 'QTUM/BTC', 'REP/BTC', 'FLOW/BTC', 'TKO/BTC', 'LTO/BTC', 'NULS/BTC', 'WRX/BTC', 'AR/BTC', 'CRV/BTC', 'C98/BTC', 'TOMO/BTC', 'WAVES/BTC', 'DAR/BTC', 'ALGO/BTC', 'BAKE/BTC', 'FIL/BTC', 'STRAX/BTC', 'CTSI/BTC', 'AGLD/BTC', 'ETC/BTC', 'NAV/BTC', 'VOXEL/BTC', 'WAN/BTC', 'GRT/BTC', 'UTK/BTC', 'BAL/BTC', 'KNC/BTC', 'UMA/BTC', 'KEEP/BTC', 'OGN/BTC', 'EOS/BTC', 'EPS/BTC', 'DODO/BTC', 'STORJ/BTC', 'CHZ/BTC', 'REN/BTC', 'HBAR/BTC', 'BCD/BTC', 'ENS/BTC', 'BNT/BTC', 'POLS/BTC', 'ACM/BTC', 'XLM/BTC', 'UNFI/BTC', 'NEO/BTC', 'MC/BTC', 'RLC/BTC', 'BAND/BTC', 'ZRX/BTC', 'IDEX/BTC', 'FET/BTC', 'ANT/BTC', 'KLAY/BTC', 'OG/BTC', 'VGX/BTC', 'AUCTION/BTC', 'NXS/BTC', 'KMD/BTC', 'ICP/BTC', 'NU/BTC', 'POLY/BTC', 'CHR/BTC', 'RUNE/BTC', 'ONE/BTC', 'ALPHA/BTC', 'CTK/BTC', 'SUPER/BTC', 'EZ/BTC', 'PSG/BTC', 'WAXP/BTC', 'JUV/BTC', 'AUDIO/BTC', 'BLZ/BTC', 'XVS/BTC', 'TLM/BTC', 'SKL/BTC', 'SYS/BTC', 'PLA/BTC', 'STEEM/BTC', 'TVK/BTC', 'AVA/BTC', 'CTXC/BTC', 'OAX/BTC', 'AGIX/BTC', 'MBOX/BTC', 'TFUEL/BTC', 'LAZIO/BTC', 'BEAM/BTC', 'GXS/BTC', 'RIF/BTC', 'HIVE/BTC', 'SNX/BTC', 'BADGER/BTC', 'OXT/BTC', 'FORTH/BTC', 'SCRT/BTC', 'COTI/BTC', 'SFP/BTC', 'MDX/BTC', 'ROSE/BTC', 'NKN/BTC', 'FRONT/BTC', 'KAVA/BTC', 'DIA/BTC', 'NANO/BTC', 'DCR/BTC', 'SRM/BTC', 'INJ/BTC', 'GRS/BTC', 'REQ/BTC', 'YGG/BTC', 'DOGE/BTC', 'STX/BTC', 'FIS/BTC', 'CVC/BTC', 'ALPACA/BTC', 'RAD/BTC', 'HNT/BTC', 'HARD/BTC', 'WTC/BTC', 'RNDR/BTC', 'FIO/BTC', 'BICO/BTC', 'DUSK/BTC', 'PORTO/BTC', 'GTC/BTC', 'PYR/BTC', 'GLM/BTC', 'SSV/BTC', 'CLV/BTC', 'POWR/BTC', 'PHA/BTC', 'NEBL/BTC', 'AST/BTC', 'ANY/BTC', 'PNT/BTC', 'DNT/BTC', 'VIDT/BTC', 'ATA/BTC', 'ARK/BTC', 'FIRO/BTC', 'SNM/BTC', 'BETA/BTC', 'DREP/BTC', 'LIT/BTC']
    # ticker_list = ticker_list + ['ADA/ETH', 'MATIC/ETH', 'MANA/ETH', 'TRX/ETH', 'IOTX/ETH', 'ADX/ETH', 'BNB/ETH', 'LINK/ETH', 'LTC/ETH', 'SAND/ETH', 'XRP/ETH', 'FTM/ETH', 'AVAX/ETH', 'XMR/ETH', 'GRT/ETH', 'SOL/ETH', 'VET/ETH', 'LUNA/ETH', 'NEO/ETH', 'ZIL/ETH', 'DOT/ETH', 'THETA/ETH', 'WAVES/ETH', 'AXS/ETH', 'ENJ/ETH', 'LRC/ETH', 'OMG/ETH', 'BAT/ETH', 'SCRT/ETH', 'GALA/ETH', 'QTUM/ETH', 'ZRX/ETH', 'EOS/ETH', 'VGX/ETH', 'STRAX/ETH', 'XLM/ETH', 'NANO/ETH', 'GXS/ETH', 'XEM/ETH', 'FUN/ETH', 'IOST/ETH', 'CVP/ETH', 'KMD/ETH', 'RLC/ETH', 'DATA/ETH', 'DEXE/ETH', 'GHST/ETH', 'BRD/ETH', 'XVG/ETH', 'NAS/ETH', 'IOTA/ETH', 'BLZ/ETH']
    # ticker_list = ticker_list + ['SPARTA/BNB', 'UNI/BNB', 'SAND/BNB', 'CAKE/BNB', 'XRP/BNB', 'LTC/BNB', 'DOT/BNB', 'SOL/BNB', 'LUNA/BNB', 'MATIC/BNB', 'ADA/BNB', 'VET/BNB', 'OCEAN/BNB', 'CHZ/BNB', 'AAVE/BNB', 'GALA/BNB', 'FTM/BNB', 'XLM/BNB', 'AVAX/BNB', 'TRX/BNB', 'KAVA/BNB', 'FIL/BNB', 'MINA/BNB', 'AXS/BNB', 'ENJ/BNB', 'SUSHI/BNB', 'EGLD/BNB', 'C98/BNB', 'ONE/BNB', 'ATOM/BNB', 'ALGO/BNB', 'XTZ/BNB', 'COS/BNB', 'ZIL/BNB', 'HOT/BNB', 'CHR/BNB', 'THETA/BNB', 'RUNE/BNB', 'CTSI/BNB', 'WAXP/BNB', 'WAVES/BNB', 'VOXEL/BNB', 'HBAR/BNB', 'DAR/BNB', 'WRX/BNB', 'ANT/BNB', 'MBOX/BNB', 'AR/BNB', 'PERL/BNB', 'IOTA/BNB', 'POLS/BNB', 'CELR/BNB']

    a = datetime.now()

    print(len(ticker_list))

    print("15m")
    for ticker in ticker_list:
        get_target(ticker, "15m")

    print("30m")
    for ticker in ticker_list:
        get_target(ticker, "30m")

    print("1h")
    for ticker in ticker_list:
        get_target(ticker, "1h")

    print("2h")
    for ticker in ticker_list:
        get_target(ticker, "2h")

    print("4h")
    for ticker in ticker_list:
        get_target(ticker, "4h")

    print("6h")
    for ticker in ticker_list:
        get_target(ticker, "6h")

    print("12h")
    for ticker in ticker_list:
        get_target(ticker, "12h")

    print("1d")
    for ticker in ticker_list:
        get_target(ticker, "1d")

    print(datetime.now() - a)
