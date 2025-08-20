import ccxt
import time
import urllib
import json


def get_round_up_price(num):
    if num < 1:
        if num < 0.0000001:
            return 0.0000001
        elif num < 0.000001:
            return 0.000001
        elif num < 0.00001:
            return 0.00001
        elif num < 0.0001:
            return 0.0001
        elif num < 0.001:
            return 0.001
        elif num < 0.01:
            return 0.01
        elif num < 0.1:
            return 0.1
        return 1
    else:
        return (num - float(str(num)[1:])) / float(str(num)[0]) * 10


def Validate(ticker):
    ohlcv = binance.fetch_ohlcv(ticker, "1M")
    ATH_price = max([ohlcv[s][2] for s in range(len(ohlcv))])
    round_up_price = get_round_up_price(ohlcv[-1][4])
    if ATH_price < round_up_price:
        ticker_result.append(ticker)
        price_result.append(round(round_up_price / ohlcv[-1][4], 3))


def get_ohlcv(ticker="BTC/KRW", interval="1m", limit=200):
    try:
        temp = ticker.split("/")
        ticker = f"{temp[1]}-{temp[0]}"
        url = "https://api.upbit.com/v1/candles/months?market=KRW-BTC&count=50"
        text_data = urllib.request.urlopen(url).read().decode("utf-8")
        output = json.loads(text_data)
    except Exception as e:
        print(f"{e}\n{ticker}")
        return None
    # output = [list(map(float,output[i])) for i in range(len(output))]
    return output


exchange_class = getattr(ccxt, "binance")
binance = exchange_class()
binance.enableRateLimit = False
binance.RateLimit = 10000
# binance.apiKey =
# binance.secret =
binance.load_markets()

ticker_result = []
price_result = []


def print_result():
    del_list = []
    for i in range(len(price_result)):
        if price_result[i] == min(price_result):
            # if price_result[i] == max(price_result):
            print(f"ticker = {ticker_result[i]}, value = {price_result[i]}\n\n")
            del_list.append(ticker_result[i])
            del_list.append(price_result[i])
    ticker_result.remove(del_list[0])
    price_result.remove(del_list[1])


if __name__ == "__main__":
    # all_ticker = list(binance.fetch_tickers().keys())
    # all_ticker = [all_ticker[s] for s in range(len(all_ticker)) if '/ETH' in all_ticker[s]]

    all_ticker = [
        "BTC/USDT",
        "ETH/USDT",
        "BNB/USDT",
        "BCC/USDT",
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
        "VEN/USDT",
        "NULS/USDT",
        "VET/USDT",
        "PAX/USDT",
        "BCH/USDT",
        "BSV/USDT",
        "USDC/USDT",
        "LINK/USDT",
        "WAVES/USDT",
        "BTT/USDT",
        "USDS/USDT",
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
        "USDSB/USDT",
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
        "STORM/USDT",
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
        "BULL/USDT",
        "BEAR/USDT",
        "ETHBULL/USDT",
        "ETHBEAR/USDT",
        "TCT/USDT",
        "WRX/USDT",
        "BTS/USDT",
        "LSK/USDT",
        "BNT/USDT",
        "LTO/USDT",
        "EOSBULL/USDT",
        "EOSBEAR/USDT",
        "XRPBULL/USDT",
        "XRPBEAR/USDT",
        "STRAT/USDT",
        "AION/USDT",
        "MBL/USDT",
        "COTI/USDT",
        "BNBBULL/USDT",
        "BNBBEAR/USDT",
        "STPT/USDT",
        "WTC/USDT",
        "DATA/USDT",
        "XZC/USDT",
        "SOL/USDT",
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
        "COMP/USDT",
        "BKRW/USDT",
        "SC/USDT",
        "ZEN/USDT",
        "SNX/USDT",
        "ETHUP/USDT",
        "ETHDOWN/USDT",
        "ADAUP/USDT",
        "ADADOWN/USDT",
        "LINKUP/USDT",
        "LINKDOWN/USDT",
        "VTHO/USDT",
        "DGB/USDT",
        "GBP/USDT",
        "SXP/USDT",
        "MKR/USDT",
        "DAI/USDT",
        "DCR/USDT",
        "STORJ/USDT",
        "BNBUP/USDT",
        "BNBDOWN/USDT",
        "XTZUP/USDT",
        "XTZDOWN/USDT",
        "MANA/USDT",
        "AUD/USDT",
        "YFI/USDT",
        "BAL/USDT",
        "BLZ/USDT",
        "IRIS/USDT",
        "KMD/USDT",
        "JST/USDT",
        "SRM/USDT",
        "ANT/USDT",
        "CRV/USDT",
        "SAND/USDT",
        "OCEAN/USDT",
        "NMR/USDT",
        "DOT/USDT",
        "LUNA/USDT",
        "RSR/USDT",
        "PAXG/USDT",
        "WNXM/USDT",
        "TRB/USDT",
        "BZRX/USDT",
        "SUSHI/USDT",
        "YFII/USDT",
        "KSM/USDT",
        "EGLD/USDT",
        "DIA/USDT",
        "RUNE/USDT",
        "FIO/USDT",
        "UMA/USDT",
        "EOSUP/USDT",
        "EOSDOWN/USDT",
        "TRXUP/USDT",
        "TRXDOWN/USDT",
        "XRPUP/USDT",
        "XRPDOWN/USDT",
        "DOTUP/USDT",
        "DOTDOWN/USDT",
        "BEL/USDT",
        "WING/USDT",
        "LTCUP/USDT",
        "LTCDOWN/USDT",
        "UNI/USDT",
        "NBS/USDT",
        "OXT/USDT",
        "SUN/USDT",
        "AVAX/USDT",
        "HNT/USDT",
        "FLM/USDT",
        "UNIUP/USDT",
        "UNIDOWN/USDT",
        "ORN/USDT",
        "UTK/USDT",
        "XVS/USDT",
        "ALPHA/USDT",
        "AAVE/USDT",
        "NEAR/USDT",
        "SXPUP/USDT",
        "SXPDOWN/USDT",
        "FIL/USDT",
        "FILUP/USDT",
        "FILDOWN/USDT",
        "YFIUP/USDT",
        "YFIDOWN/USDT",
        "INJ/USDT",
        "AUDIO/USDT",
        "CTK/USDT",
        "BCHUP/USDT",
        "BCHDOWN/USDT",
        "AKRO/USDT",
        "AXS/USDT",
        "HARD/USDT",
        "DNT/USDT",
        "STRAX/USDT",
        "UNFI/USDT",
        "ROSE/USDT",
        "AVA/USDT",
        "XEM/USDT",
        "AAVEUP/USDT",
        "AAVEDOWN/USDT",
        "SKL/USDT",
        "SUSD/USDT",
        "SUSHIUP/USDT",
        "SUSHIDOWN/USDT",
        "XLMUP/USDT",
        "XLMDOWN/USDT",
        "GRT/USDT",
        "JUV/USDT",
        "PSG/USDT",
        "1INCH/USDT",
        "REEF/USDT",
        "OG/USDT",
        "ATM/USDT",
        "ASR/USDT",
        "CELO/USDT",
        "RIF/USDT",
        "BTCST/USDT",
        "TRU/USDT",
        "CKB/USDT",
        "TWT/USDT",
        "FIRO/USDT",
        "LIT/USDT",
        "SFP/USDT",
        "DODO/USDT",
        "CAKE/USDT",
        "ACM/USDT",
        "BADGER/USDT",
        "FIS/USDT",
        "OM/USDT",
        "POND/USDT",
        "DEGO/USDT",
        "ALICE/USDT",
        "LINA/USDT",
        "PERP/USDT",
        "RAMP/USDT",
        "SUPER/USDT",
        "CFX/USDT",
        "EPS/USDT",
        "AUTO/USDT",
        "TKO/USDT",
        "PUNDIX/USDT",
        "TLM/USDT",
        "1INCHUP/USDT",
        "1INCHDOWN/USDT",
        "BTG/USDT",
        "MIR/USDT",
        "BAR/USDT",
        "FORTH/USDT",
        "BAKE/USDT",
        "BURGER/USDT",
        "SLP/USDT",
        "SHIB/USDT",
        "ICP/USDT",
        "AR/USDT",
        "POLS/USDT",
        "MDX/USDT",
        "MASK/USDT",
        "LPT/USDT",
        "NU/USDT",
        "XVG/USDT",
        "ATA/USDT",
        "GTC/USDT",
        "TORN/USDT",
        "KEEP/USDT",
        "ERN/USDT",
        "KLAY/USDT",
        "PHA/USDT",
        "BOND/USDT",
        "MLN/USDT",
        "DEXE/USDT",
        "C98/USDT",
        "CLV/USDT",
        "QNT/USDT",
        "FLOW/USDT",
        "TVK/USDT",
        "MINA/USDT",
        "RAY/USDT",
        "FARM/USDT",
        "ALPACA/USDT",
        "QUICK/USDT",
        "MBOX/USDT",
        "FOR/USDT",
        "REQ/USDT",
        "GHST/USDT",
        "WAXP/USDT",
        "TRIBE/USDT",
        "GNO/USDT",
        "XEC/USDT",
        "ELF/USDT",
        "DYDX/USDT",
        "POLY/USDT",
        "IDEX/USDT",
        "VIDT/USDT",
        "USDP/USDT",
        "GALA/USDT",
        "ILV/USDT",
        "YGG/USDT",
        "SYS/USDT",
        "DF/USDT",
        "FIDA/USDT",
        "FRONT/USDT",
        "CVP/USDT",
        "AGLD/USDT",
        "RAD/USDT",
        "BETA/USDT",
        "RARE/USDT",
        "LAZIO/USDT",
        "CHESS/USDT",
        "ADX/USDT",
        "AUCTION/USDT",
        "DAR/USDT",
        "BNX/USDT",
        "RGT/USDT",
        "MOVR/USDT",
        "CITY/USDT",
        "ENS/USDT",
        "KP3R/USDT",
        "QI/USDT",
        "PORTO/USDT",
        "POWR/USDT",
    ]

    # all_ticker = ['VEN/BNB', 'YOYOW/BNB', 'POWR/BNB', 'NULS/BNB', 'RCN/BNB', 'RDN/BNB', 'DLT/BNB', 'WTC/BNB', 'AMB/BNB', 'BCC/BNB', 'BAT/BNB', 'BCPT/BNB', 'NEO/BNB', 'QSP/BNB', 'BTS/BNB', 'XZC/BNB', 'LSK/BNB', 'IOTA/BNB', 'ADX/BNB', 'CMT/BNB', 'XLM/BNB', 'CND/BNB', 'WABI/BNB', 'LTC/BNB', 'WAVES/BNB', 'GTO/BNB', 'ICX/BNB', 'OST/BNB', 'AION/BNB', 'NEBL/BNB', 'BRD/BNB', 'MCO/BNB', 'NAV/BNB', 'TRIG/BNB', 'APPC/BNB', 'RLC/BNB', 'PIVX/BNB', 'STEEM/BNB', 'NANO/BNB', 'VIA/BNB', 'BLZ/BNB', 'AE/BNB', 'RPX/BNB', 'NCASH/BNB', 'POA/BNB', 'ZIL/BNB', 'ONT/BNB', 'STORM/BNB', 'QTUM/BNB', 'XEM/BNB', 'WAN/BNB', 'SYS/BNB', 'QLC/BNB', 'ADA/BNB', 'GNT/BNB', 'LOOM/BNB', 'BCN/BNB', 'REP/BNB', 'TUSD/BNB', 'ZEN/BNB', 'SKY/BNB', 'EOS/BNB', 'CVC/BNB', 'THETA/BNB', 'XRP/BNB', 'AGI/BNB', 'NXS/BNB', 'ENJ/BNB', 'TRX/BNB', 'ETC/BNB', 'SC/BNB', 'NAS/BNB', 'MFT/BNB', 'ARDR/BNB', 'VET/BNB', 'POLY/BNB', 'PHX/BNB', 'GO/BNB', 'PAX/BNB', 'RVN/BNB', 'DCR/BNB', 'USDC/BNB', 'MITH/BNB', 'REN/BNB', 'BTT/BNB', 'ONG/BNB', 'HOT/BNB', 'ZRX/BNB', 'FET/BNB', 'XMR/BNB', 'ZEC/BNB', 'IOST/BNB', 'CELR/BNB', 'DASH/BNB', 'OMG/BNB', 'MATIC/BNB', 'ATOM/BNB', 'PHB/BNB', 'TFUEL/BNB', 'ONE/BNB', 'FTM/BNB', 'ALGO/BNB', 'ERD/BNB', 'DOGE/BNB', 'DUSK/BNB', 'ANKR/BNB', 'WIN/BNB', 'COS/BNB', 'COCOS/BNB', 'TOMO/BNB', 'PERL/BNB', 'CHZ/BNB', 'BAND/BNB', 'BEAM/BNB', 'XTZ/BNB', 'HBAR/BNB', 'NKN/BNB', 'STX/BNB', 'KAVA/BNB', 'ARPA/BNB', 'CTXC/BNB', 'BCH/BNB', 'TROY/BNB', 'VITE/BNB', 'FTT/BNB', 'OGN/BNB', 'DREP/BNB', 'TCT/BNB', 'WRX/BNB', 'LTO/BNB', 'STRAT/BNB', 'MBL/BNB', 'COTI/BNB', 'STPT/BNB', 'SOL/BNB', 'CTSI/BNB', 'HIVE/BNB', 'CHR/BNB', 'MDT/BNB', 'STMX/BNB', 'IQ/BNB', 'DGB/BNB', 'COMP/BNB', 'SXP/BNB', 'SNX/BNB', 'VTHO/BNB', 'IRIS/BNB', 'MKR/BNB', 'DAI/BNB', 'RUNE/BNB', 'FIO/BNB', 'AVA/BNB', 'BAL/BNB', 'YFI/BNB', 'JST/BNB', 'SRM/BNB', 'ANT/BNB', 'CRV/BNB', 'SAND/BNB', 'OCEAN/BNB', 'NMR/BNB', 'DOT/BNB', 'LUNA/BNB', 'RSR/BNB', 'PAXG/BNB', 'WNXM/BNB', 'TRB/BNB', 'BZRX/BNB', 'SUSHI/BNB', 'YFII/BNB', 'KSM/BNB', 'EGLD/BNB', 'DIA/BNB', 'BEL/BNB', 'WING/BNB', 'SWRV/BNB', 'CREAM/BNB', 'UNI/BNB', 'AVAX/BNB', 'BAKE/BNB', 'BURGER/BNB', 'FLM/BNB', 'CAKE/BNB', 'SPARTA/BNB', 'XVS/BNB', 'ALPHA/BNB', 'AAVE/BNB', 'NEAR/BNB', 'FIL/BNB', 'INJ/BNB', 'CTK/BNB', 'KP3R/BNB', 'AXS/BNB', 'HARD/BNB', 'UNFI/BNB', 'PROM/BNB', 'BIFI/BNB', 'ICP/BNB', 'AR/BNB', 'POLS/BNB', 'MDX/BNB', 'MASK/BNB', 'LPT/BNB', 'NU/BNB', 'ATA/BNB', 'GTC/BNB', 'TORN/BNB', 'KEEP/BNB', 'ERN/BNB', 'KLAY/BNB', 'BOND/BNB', 'MLN/BNB', 'QUICK/BNB', 'C98/BNB', 'CLV/BNB', 'QNT/BNB', 'FLOW/BNB', 'MINA/BNB', 'RAY/BNB', 'FARM/BNB', 'ALPACA/BNB', 'MBOX/BNB', 'WAXP/BNB', 'TRIBE/BNB', 'GNO/BNB', 'DYDX/BNB', 'GALA/BNB', 'ILV/BNB', 'YGG/BNB', 'FIDA/BNB', 'AGLD/BNB', 'RAD/BNB', 'BETA/BNB', 'RARE/BNB', 'CHESS/BNB', 'DAR/BNB', 'BNX/BNB', 'RGT/BNB', 'MOVR/BNB', 'CITY/BNB', 'ENS/BNB', 'QI/BNB']

    # all_ticker = ['ETH/BTC', 'LTC/BTC', 'BNB/BTC', 'NEO/BTC', 'BCC/BTC', 'GAS/BTC', 'HSR/BTC', 'MCO/BTC', 'WTC/BTC', 'LRC/BTC', 'QTUM/BTC', 'YOYOW/BTC', 'OMG/BTC', 'ZRX/BTC', 'STRAT/BTC', 'SNGLS/BTC', 'BQX/BTC', 'KNC/BTC', 'FUN/BTC', 'SNM/BTC', 'IOTA/BTC', 'LINK/BTC', 'XVG/BTC', 'SALT/BTC', 'MDA/BTC', 'MTL/BTC', 'SUB/BTC', 'EOS/BTC', 'SNT/BTC', 'ETC/BTC', 'MTH/BTC', 'ENG/BTC', 'DNT/BTC', 'ZEC/BTC', 'BNT/BTC', 'AST/BTC', 'DASH/BTC', 'OAX/BTC', 'ICN/BTC', 'BTG/BTC', 'EVX/BTC', 'REQ/BTC', 'VIB/BTC', 'TRX/BTC', 'POWR/BTC', 'ARK/BTC', 'XRP/BTC', 'MOD/BTC', 'ENJ/BTC', 'STORJ/BTC', 'VEN/BTC', 'KMD/BTC', 'RCN/BTC', 'NULS/BTC', 'RDN/BTC', 'XMR/BTC', 'DLT/BTC', 'AMB/BTC', 'BAT/BTC', 'BCPT/BTC', 'ARN/BTC', 'GVT/BTC', 'CDT/BTC', 'GXS/BTC', 'POE/BTC', 'QSP/BTC', 'BTS/BTC', 'XZC/BTC', 'LSK/BTC', 'TNT/BTC', 'FUEL/BTC', 'MANA/BTC', 'BCD/BTC', 'DGD/BTC', 'ADX/BTC', 'ADA/BTC', 'PPT/BTC', 'CMT/BTC', 'XLM/BTC', 'CND/BTC', 'LEND/BTC', 'WABI/BTC', 'TNB/BTC', 'WAVES/BTC', 'GTO/BTC', 'ICX/BTC', 'OST/BTC', 'ELF/BTC', 'AION/BTC', 'NEBL/BTC', 'BRD/BTC', 'EDO/BTC', 'WINGS/BTC', 'NAV/BTC', 'LUN/BTC', 'TRIG/BTC', 'APPC/BTC', 'VIBE/BTC', 'RLC/BTC', 'INS/BTC', 'PIVX/BTC', 'IOST/BTC', 'CHAT/BTC', 'STEEM/BTC', 'NANO/BTC', 'VIA/BTC', 'BLZ/BTC', 'AE/BTC', 'RPX/BTC', 'NCASH/BTC', 'POA/BTC', 'ZIL/BTC', 'ONT/BTC', 'STORM/BTC', 'XEM/BTC', 'WAN/BTC', 'WPR/BTC', 'QLC/BTC', 'SYS/BTC', 'GRS/BTC', 'CLOAK/BTC', 'GNT/BTC', 'LOOM/BTC', 'BCN/BTC', 'REP/BTC', 'TUSD/BTC', 'ZEN/BTC', 'SKY/BTC', 'CVC/BTC', 'THETA/BTC', 'IOTX/BTC', 'QKC/BTC', 'AGI/BTC', 'NXS/BTC', 'DATA/BTC', 'SC/BTC', 'NPXS/BTC', 'KEY/BTC', 'NAS/BTC', 'MFT/BTC', 'DENT/BTC', 'ARDR/BTC', 'HOT/BTC', 'VET/BTC', 'DOCK/BTC', 'POLY/BTC', 'PHX/BTC', 'HC/BTC', 'GO/BTC', 'PAX/BTC', 'RVN/BTC', 'DCR/BTC', 'MITH/BTC', 'BCH/BTC', 'BSV/BTC', 'REN/BTC', 'BTT/BTC', 'ONG/BTC', 'FET/BTC', 'CELR/BTC', 'MATIC/BTC', 'ATOM/BTC', 'PHB/BTC', 'TFUEL/BTC', 'ONE/BTC', 'FTM/BTC', 'BTCB/BTC', 'ALGO/BTC', 'ERD/BTC', 'DOGE/BTC', 'DUSK/BTC', 'ANKR/BTC', 'WIN/BTC', 'COS/BTC', 'COCOS/BTC', 'TOMO/BTC', 'PERL/BTC', 'CHZ/BTC', 'BAND/BTC', 'BEAM/BTC', 'XTZ/BTC', 'HBAR/BTC', 'NKN/BTC', 'STX/BTC', 'KAVA/BTC', 'ARPA/BTC', 'CTXC/BTC', 'TROY/BTC', 'VITE/BTC', 'FTT/BTC', 'OGN/BTC', 'DREP/BTC', 'TCT/BTC', 'WRX/BTC', 'LTO/BTC', 'MBL/BTC', 'COTI/BTC', 'STPT/BTC', 'SOL/BTC', 'CTSI/BTC', 'HIVE/BTC', 'CHR/BTC', 'MDT/BTC', 'STMX/BTC', 'PNT/BTC', 'DGB/BTC', 'COMP/BTC', 'SXP/BTC', 'SNX/BTC', 'IRIS/BTC', 'MKR/BTC', 'DAI/BTC', 'RUNE/BTC', 'FIO/BTC', 'AVA/BTC', 'BAL/BTC', 'YFI/BTC', 'JST/BTC', 'SRM/BTC', 'ANT/BTC', 'CRV/BTC', 'SAND/BTC', 'OCEAN/BTC', 'NMR/BTC', 'DOT/BTC', 'LUNA/BTC', 'IDEX/BTC', 'RSR/BTC', 'PAXG/BTC', 'WNXM/BTC', 'TRB/BTC', 'BZRX/BTC', 'WBTC/BTC', 'SUSHI/BTC', 'YFII/BTC', 'KSM/BTC', 'EGLD/BTC', 'DIA/BTC', 'UMA/BTC', 'BEL/BTC', 'WING/BTC', 'UNI/BTC', 'NBS/BTC', 'OXT/BTC', 'SUN/BTC', 'AVAX/BTC', 'HNT/BTC', 'FLM/BTC', 'SCRT/BTC', 'ORN/BTC', 'UTK/BTC', 'XVS/BTC', 'ALPHA/BTC', 'VIDT/BTC', 'AAVE/BTC', 'NEAR/BTC', 'FIL/BTC', 'INJ/BTC', 'AERGO/BTC', 'AUDIO/BTC', 'CTK/BTC', 'BOT/BTC', 'AKRO/BTC', 'AXS/BTC', 'HARD/BTC', 'RENBTC/BTC', 'STRAX/BTC', 'FOR/BTC', 'UNFI/BTC', 'ROSE/BTC', 'SKL/BTC', 'SUSD/BTC', 'GLM/BTC', 'GRT/BTC', 'JUV/BTC', 'PSG/BTC', '1INCH/BTC', 'REEF/BTC', 'OG/BTC', 'ATM/BTC', 'ASR/BTC', 'CELO/BTC', 'RIF/BTC', 'BTCST/BTC', 'TRU/BTC', 'CKB/BTC', 'TWT/BTC', 'FIRO/BTC', 'LIT/BTC', 'SFP/BTC', 'FXS/BTC', 'DODO/BTC', 'FRONT/BTC', 'EASY/BTC', 'CAKE/BTC', 'ACM/BTC', 'AUCTION/BTC', 'PHA/BTC', 'TVK/BTC', 'BADGER/BTC', 'FIS/BTC', 'OM/BTC', 'POND/BTC', 'DEGO/BTC', 'ALICE/BTC', 'LINA/BTC', 'PERP/BTC', 'RAMP/BTC', 'SUPER/BTC', 'CFX/BTC', 'EPS/BTC', 'AUTO/BTC', 'TKO/BTC', 'TLM/BTC', 'MIR/BTC', 'BAR/BTC', 'FORTH/BTC', 'EZ/BTC', 'ICP/BTC', 'AR/BTC', 'POLS/BTC', 'MDX/BTC', 'LPT/BTC', 'AGIX/BTC', 'NU/BTC', 'ATA/BTC', 'GTC/BTC', 'TORN/BTC', 'BAKE/BTC', 'KEEP/BTC', 'KLAY/BTC', 'BOND/BTC', 'MLN/BTC', 'QUICK/BTC', 'C98/BTC', 'CLV/BTC', 'QNT/BTC', 'FLOW/BTC', 'MINA/BTC', 'FARM/BTC', 'ALPACA/BTC', 'MBOX/BTC', 'VGX/BTC', 'WAXP/BTC', 'TRIBE/BTC', 'GNO/BTC', 'PROM/BTC', 'DYDX/BTC', 'GALA/BTC', 'ILV/BTC', 'YGG/BTC', 'FIDA/BTC', 'AGLD/BTC', 'RAD/BTC', 'BETA/BTC', 'RARE/BTC', 'SSV/BTC', 'LAZIO/BTC', 'CHESS/BTC', 'DAR/BTC', 'BNX/BTC', 'RGT/BTC', 'MOVR/BTC', 'CITY/BTC', 'ENS/BTC', 'QI/BTC', 'PORTO/BTC']
    # all_ticker = ['QTUM/ETH', 'EOS/ETH', 'SNT/ETH', 'BNT/ETH', 'BNB/ETH', 'OAX/ETH', 'DNT/ETH', 'MCO/ETH', 'ICN/ETH', 'WTC/ETH', 'LRC/ETH', 'OMG/ETH', 'ZRX/ETH', 'STRAT/ETH', 'SNGLS/ETH', 'BQX/ETH', 'KNC/ETH', 'FUN/ETH', 'SNM/ETH', 'NEO/ETH', 'IOTA/ETH', 'LINK/ETH', 'XVG/ETH', 'SALT/ETH', 'MDA/ETH', 'MTL/ETH', 'SUB/ETH', 'ETC/ETH', 'MTH/ETH', 'ENG/ETH', 'ZEC/ETH', 'AST/ETH', 'DASH/ETH', 'BTG/ETH', 'EVX/ETH', 'REQ/ETH', 'VIB/ETH', 'HSR/ETH', 'TRX/ETH', 'POWR/ETH', 'ARK/ETH', 'YOYOW/ETH', 'XRP/ETH', 'MOD/ETH', 'ENJ/ETH', 'STORJ/ETH', 'VEN/ETH', 'KMD/ETH', 'RCN/ETH', 'NULS/ETH', 'RDN/ETH', 'XMR/ETH', 'DLT/ETH', 'AMB/ETH', 'BCC/ETH', 'BAT/ETH', 'BCPT/ETH', 'ARN/ETH', 'GVT/ETH', 'CDT/ETH', 'GXS/ETH', 'POE/ETH', 'QSP/ETH', 'BTS/ETH', 'XZC/ETH', 'LSK/ETH', 'TNT/ETH', 'FUEL/ETH', 'MANA/ETH', 'BCD/ETH', 'DGD/ETH', 'ADX/ETH', 'ADA/ETH', 'PPT/ETH', 'CMT/ETH', 'XLM/ETH', 'CND/ETH', 'LEND/ETH', 'WABI/ETH', 'LTC/ETH', 'TNB/ETH', 'WAVES/ETH', 'GTO/ETH', 'ICX/ETH', 'OST/ETH', 'ELF/ETH', 'AION/ETH', 'NEBL/ETH', 'BRD/ETH', 'EDO/ETH', 'WINGS/ETH', 'NAV/ETH', 'LUN/ETH', 'TRIG/ETH', 'APPC/ETH', 'VIBE/ETH', 'RLC/ETH', 'INS/ETH', 'PIVX/ETH', 'IOST/ETH', 'CHAT/ETH', 'STEEM/ETH', 'NANO/ETH', 'VIA/ETH', 'BLZ/ETH', 'AE/ETH', 'RPX/ETH', 'NCASH/ETH', 'POA/ETH', 'ZIL/ETH', 'ONT/ETH', 'STORM/ETH', 'XEM/ETH', 'WAN/ETH', 'WPR/ETH', 'QLC/ETH', 'SYS/ETH', 'GRS/ETH', 'CLOAK/ETH', 'GNT/ETH', 'LOOM/ETH', 'BCN/ETH', 'REP/ETH', 'TUSD/ETH', 'ZEN/ETH', 'SKY/ETH', 'CVC/ETH', 'THETA/ETH', 'IOTX/ETH', 'QKC/ETH', 'AGI/ETH', 'NXS/ETH', 'DATA/ETH', 'SC/ETH', 'NPXS/ETH', 'KEY/ETH', 'NAS/ETH', 'MFT/ETH', 'DENT/ETH', 'ARDR/ETH', 'HOT/ETH', 'VET/ETH', 'DOCK/ETH', 'PHX/ETH', 'HC/ETH', 'PAX/ETH', 'STMX/ETH', 'WBTC/ETH', 'SCRT/ETH', 'AAVE/ETH', 'EASY/ETH', 'RENBTC/ETH', 'SLP/ETH', 'CVP/ETH', 'STRAX/ETH', 'FRONT/ETH', 'HEGIC/ETH', 'SUSD/ETH', 'COVER/ETH', 'GLM/ETH', 'GHST/ETH', 'DF/ETH', 'GRT/ETH', 'DEXE/ETH', 'FIRO/ETH', 'BETH/ETH', 'PROS/ETH', 'UFT/ETH', 'PUNDIX/ETH', 'EZ/ETH', 'VGX/ETH', 'AXS/ETH', 'FTM/ETH', 'SOL/ETH', 'SSV/ETH', 'SAND/ETH', 'DOT/ETH', 'MATIC/ETH']

    for ticker in all_ticker:
        Validate(ticker)

    print_result()
    print_result()
    print_result()
    print_result()
    print_result()

    print(get_ohlcv()[0])
