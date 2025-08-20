from random import randint
import datetime
import ccxt
import time


def get_decimal(ticker):
    ticker = ticker[:-5]
    Group_14 = [
        "XRP",
        "ONT",
        "IOTA",
        "BAT",
        "LEND",
        "SXP",
        "OMG",
        "ZRX",
        "ALGO",
        "THETA",
        "KAVA",
        "BAND",
        "RLC",
        "WAVES",
    ]
    Group_13 = [
        "EOS",
        "XTZ",
        "QTUM",
        "SNX",
        "DOT",
        "BAL",
        "CRV",
        "TRB",
        "NEO",
        "LIT",
        "ALICE",
        "KSM",
        "DODO",
        "UNFI",
        "EGLD",
        "FIL",
        "AAVE",
    ]
    Group_05 = ["TRX", "XLM", "ADA", "KNC", "ZIL", "RUNE", "SUSHI", "SRM", "BZRX"]
    Group_06 = ["VET", "IOST", "DOGE"]
    Group_23 = ["LINK", "COMP", "ETC", "BNB", "ATOM", "ZEN"]
    Group_31 = ["DEFI", "YFI", "YFII", "XMR"]
    Group_32 = ["MKR", "BTC", "ETH", "BCH", "LTC", "DASH", "ZEC"]
    Group_0X = [
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
        "NEAR/USDT",
        "RSR/USDT",
        "LRC/USDT",
        "MATIC/USDT",
        "OCEAN/USDT",
        "CVC/USDT",
        "BEL/USDT",
        "CTK/USDT",
        "AXS/USDT",
        "ALPHA/USDT",
        "SKL/USDT",
        "GRT/USDT",
        "1INCH/USDT",
        "AKRO/USDT",
        "CHZ/USDT",
        "SAND/USDT",
        "ANKR/USDT",
        "LUNA/USDT",
        "BTS/USDT",
        "REEF/USDT",
        "RVN/USDT",
        "SFP/USDT",
        "XEM/USDT",
        "COTI/USDT",
        "CHR/USDT",
        "MANA/USDT",
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
    ]

    if any(ticker in i for i in Group_14):
        return 1, 4
    elif any(ticker in i for i in Group_13):
        return 1, 3
    elif any(ticker in i for i in Group_05):
        return 0, 5
    elif any(ticker in i for i in Group_06):
        return 0, 6
    elif any(ticker in i for i in Group_23):
        return 2, 3
    elif any(ticker in i for i in Group_31):
        return 3, 1
    elif any(ticker in i for i in Group_32):
        return 3, 2
    elif any(ticker in i for i in Group_0X):
        return 0, 3
    else:
        return ticker


if __name__ == "__main__":
    binance = ccxt.binance(
        {"enableRateLimit": True, "options": {"defaultType": "future"}}
    )
    binance.enableRateLimit = True
    binance.RateLimit = 10000
    binance.apiKey = "Wofk7BIStGtvLeCLCIbXVAbxl3KAy03BHafkmGtVqOILF8FZKonaSxqIPCzK4j6i"
    binance.secret = "n91lmhQJCOB1ZySmbuTeuefoFlytnnAkjivYazRF1DW4x22v34RN3LXEq5OlHZtR"
    binance.load_markets()

    tickers = list(binance.fetch_tickers().keys())
    tickers = [ticker for ticker in tickers if "/USDT" in ticker]

    result = []

    for ticker in tickers:
        temp = get_decimal(ticker)
        if type(temp) == str:
            result.append(temp + "/USDT")

    for ticker in result:
        a = binance.fetch_order_book(ticker)["bids"][-1]
        print(ticker[:-5], a[0])

    print(result)
