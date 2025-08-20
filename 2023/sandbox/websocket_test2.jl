using PyCall
using Dates


@async begin
    py"""
    from pybit.unified_trading import WebSocket
    from time import sleep
    result = []
    ws = WebSocket(
        testnet=False,
        channel_type="linear",
    )
    def handle_message(message):
        result.append(message)
    def return_data():
        count = len(result)
        return_data = []
        for i in range(count):
            return_data.append(result.pop())
        return return_data
    ticker_list =  ["TRXUSDT", "BAKEUSDT", "SOLUSDT", "SPELLUSDT", "RADUSDT", "SSVUSDT", "ARUSDT", "TOMOUSDT", "ARBUSDT", "LRCUSDT", "DOGEUSDT", "NEOUSDT", "GALAUSDT", "SUIUSDT", "MANAUSDT", "LTCUSDT", "LEVERUSDT", "BLURUSDT", "COMPUSDT", "VETUSDT", "LUNA2USDT", "CTKUSDT", "MASKUSDT", "PEOPLEUSDT", "TRUUSDT", "DARUSDT", "C98USDT", "ENSUSDT", "AAVEUSDT", "COMBOUSDT", "CKBUSDT", "KSMUSDT", "ALPHAUSDT", "CRVUSDT", "LDOUSDT", "SKLUSDT", "HFTUSDT", "OPUSDT", "DGBUSDT", "QNTUSDT", "ADAUSDT", "HOTUSDT", "IOSTUSDT", "IOTXUSDT", "CTSIUSDT", "ACHUSDT", "UMAUSDT", "MATICUSDT", "PERPUSDT", "THETAUSDT", "STORJUSDT", "SANDUSDT", "JOEUSDT", "HBARUSDT", "BNBUSDT", "INJUSDT", "ZRXUSDT", "DASHUSDT", "REEFUSDT", "GALUSDT", "AMBUSDT", "FETUSDT", "FLOWUSDT", "WAVESUSDT", "RVNUSDT", "CFXUSDT", "SXPUSDT", "EGLDUSDT", "API3USDT", "ROSEUSDT", "EOSUSDT", "XTZUSDT", "AVAXUSDT", "ICPUSDT", "SNXUSDT", "RENUSDT", "XLMUSDT", "1000PEPEUSDT", "FTMUSDT", "WOOUSDT", "KAVAUSDT", "ZENUSDT", "AUDIOUSDT", "IDUSDT", "ONEUSDT", "OGNUSDT", "ARPAUSDT", "RDNTUSDT", "BCHUSDT", "CHZUSDT", "MKRUSDT", "KLAYUSDT", "KEYUSDT", "UNIUSDT", "HOOKUSDT", "CELOUSDT", "ETCUSDT", "STGUSDT", "LINAUSDT", "ONTUSDT", "ATOMUSDT", "ASTRUSDT", "BATUSDT", "QTUMUSDT", "SFPUSDT", "ATAUSDT", "MINAUSDT", "SUSHIUSDT", "RUNEUSDT", "RSRUSDT", "ZECUSDT", "TLMUSDT", "RLCUSDT", "FXSUSDT", "APTUSDT", "ANTUSDT", "BLZUSDT", "DENTUSDT", "XEMUSDT", "BALUSDT", "MTLUSDT", "HIGHUSDT", "DUSKUSDT", "JASMYUSDT", "GTCUSDT", "XVSUSDT", "ANKRUSDT", "PHBUSDT", "COTIUSDT", "XMRUSDT", "DOTUSDT", "KNCUSDT", "OMGUSDT", "GMTUSDT", "UNFIUSDT", "AGIXUSDT", "TRBUSDT", "GRTUSDT", "BELUSDT", "ENJUSDT", "AXSUSDT", "FILUSDT", "ALGOUSDT", "DYDXUSDT", "CVXUSDT", "LPTUSDT", "STXUSDT", "TUSDT", "RNDRUSDT", "APEUSDT", "IDEXUSDT", "BANDUSDT", "1000XECUSDT", "IMXUSDT", "LQTYUSDT", "LINKUSDT", "1000FLOKIUSDT", "OCEANUSDT", "ZILUSDT", "IOTAUSDT", "EDUUSDT", "FLMUSDT", "STMXUSDT", "CELRUSDT", "NEARUSDT", "GMXUSDT", "1INCHUSDT", "ALICEUSDT", "XRPUSDT", "MAGICUSDT", "ICXUSDT", "LITUSDT", "BNXUSDT", "ETHUSDT", "1000LUNCUSDT", "CHRUSDT", "NKNUSDT"]
    ws.trade_stream(ticker_list, handle_message)
    sleep(86400 * 3)
    """
end


println("start")
while true
    try
        snapshots = py"return_data()"

        for snapshot in snapshots

            ts = snapshot["ts"]

            ticker = snapshot["data"][1]["s"]
            
            price = 10^9
            for data_seq in snapshot["data"]
                temp_price = parse(Float32, data_seq["p"])
                if price > temp_price
                    price = temp_price
                end
            end

            println("$(ticker)\n$(unix2datetime(ts/1000))\n$(now(Dates.UTC))\n$(price)")
            
        end

    catch e
        print("$e  : ")
        println(now(Dates.UTC))
        continue
    end
end



