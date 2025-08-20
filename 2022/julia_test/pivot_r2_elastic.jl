using HTTP
import JSON
using Statistics
using Dates
include("./utils.jl")

using Random


function log_maker(limit, All_ohlcv, ticker_list)
    total_buy_sell_log = []
    buy_sell_log = []
    slippage = 0.9982 * 0.9982
    for day in limit-3:-1:0
        for (i, ohlcv) in enumerate(All_ohlcv)
            high = maximum((ohlcv[end-(day+1)][3], ohlcv[end-(day+2)][3]))
            low = minimum((ohlcv[end-(day+1)][4], ohlcv[end-(day+2)][4]))
            open = ohlcv[end-(day+1)][2]
            close = ohlcv[end-(day+1)][5]
            if open < close # 양봉
                value = 2.3
            else
                value = 2.15
            end

            value = 2.3

            elastic = 0
            elastic_list = []
            while true

                if length(elastic_list) == 10
                    break
                end

                value = value + elastic
                PP = (high + low + 4*close) / 6
                R2 = value * PP - low 
                if ohlcv[end-day][3] > R2
                    elastic += 0.0025
                    push!(elastic_list, 0)
                    
                    entry_price = R2
                    exit_price = ohlcv[end-day][5]
                    earning = 100(entry_price / exit_price * slippage - 1)
                    trade_time = unix2datetime((ohlcv[end-day][0+1]+3600000*9)/1000)
                    # text = string(ticker_list[i]," " ,trade_time ,"   buy :", string(entry_price), "// sell :", string(exit_price), "  ",string(earning))
                    # println(text)
                    push!(buy_sell_log, earning)
                    push!(total_buy_sell_log, earning)
                else
                    break
                end



            end

        end
        # get_performance(buy_sell_log)
        empty!(buy_sell_log)
    end
    get_performance(total_buy_sell_log)
    return nothing
end




ticker_list = ["MKRUSDT", "C98USDT", "SFPUSDT", "1000XECUSDT", "XEMUSDT", "ZENUSDT", "ETHUSDT", "MTLUSDT", "BATUSDT", "LDOUSDT", "ENJUSDT", "RSRUSDT", "OMGUSDT", "ATAUSDT", "IOSTUSDT", "STGUSDT", "DOGEUSDT", "ALGOUSDT", "ANKRUSDT", "CHZUSDT", "ZRXUSDT", "AVAXUSDT", "TOMOUSDT", "ARUSDT", "CELOUSDT", "SXPUSDT", "OCEANUSDT", "DOTUSDT", "UNFIUSDT", "ALPHAUSDT", "SPELLUSDT", "ONEUSDT", "EGLDUSDT", "INJUSDT", "DUSKUSDT", "RENUSDT", "KAVAUSDT", "NEOUSDT", "BCHUSDT", "SUSHIUSDT", "LPTUSDT", "SOLUSDT", "WOOUSDT", "NKNUSDT", "FILUSDT", "AAVEUSDT", "HOTUSDT", "FOOTBALLUSDT", "GTCUSDT", "QNTUSDT", "APEUSDT", "GALAUSDT", "VETUSDT", "ANTUSDT", "BELUSDT", "SNXUSDT", "BAKEUSDT", "STMXUSDT", "LUNA2USDT", "REEFUSDT", "OGNUSDT", "GALUSDT", "RLCUSDT", "XTZUSDT", "EOSUSDT", "CVXUSDT", "COTIUSDT", "STORJUSDT", "HNTUSDT", "IMXUSDT", "OPUSDT", "ARPAUSDT", "DASHUSDT", "MANAUSDT", "CELRUSDT", "GRTUSDT", "1INCHUSDT", "BLUEBIRDUSDT", "ROSEUSDT", "DEFIUSDT", "KSMUSDT", "LINAUSDT", "ATOMUSDT", "CHRUSDT", "XMRUSDT", "FTMUSDT", "IOTAUSDT", "BTCDOMUSDT", "CTKUSDT", "UNIUSDT", "TRXUSDT", "CRVUSDT", "KNCUSDT", "THETAUSDT", "ICXUSDT", "SKLUSDT", "API3USDT", "KLAYUSDT", "WAVESUSDT", "ADAUSDT", "ALICEUSDT", "1000LUNCUSDT", "FLOWUSDT", "MASKUSDT", "LRCUSDT", "NEARUSDT", "DARUSDT", "PEOPLEUSDT", "CTSIUSDT", "MATICUSDT", "BALUSDT", "ZILUSDT", "ENSUSDT", "DGBUSDT", "XLMUSDT", "JASMYUSDT", "QTUMUSDT", "LTCUSDT", "FLMUSDT", "RUNEUSDT", "ZECUSDT", "1000SHIBUSDT", "AXSUSDT", "BANDUSDT", "GMTUSDT", "ETCUSDT", "TRBUSDT", "ICPUSDT", "COMPUSDT", "LINKUSDT", "HBARUSDT", "XRPUSDT", "BNXUSDT", "DYDXUSDT", "YFIUSDT", "BTCUSDT", "APTUSDT", "LITUSDT", "SANDUSDT", "BLZUSDT", "BNBUSDT"]
ticker_list = shuffle(ticker_list)


for i in range(1, 24)
    # for i in range(1, 3)
        print(i)
        println("##########################################################################################################################################################################################################################################################################################")
        global ticker_list
    
        if i%2==0
            sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
        end
    
        All_ohlcv = []
        del_list = []
        interval = "1h"
        limit = "960"
        time_flag = 40
        # multiple = 1 # 1~10
        multiple = i # 1~10
        
        # ticker_list = shuffle(ticker_list)
    
        btc_ohlcv = fetch_ohlcv("BTCUSDT", "1d", "1000")
        start_time = string(btc_ohlcv[end-time_flag*multiple][1])
        end_time = string(btc_ohlcv[end-time_flag*(multiple-1)][1])
    
    
        for ticker = ticker_list
            ohlcv = fetch_ohlcv(ticker, interval, limit, start_time, end_time)
            # ohlcv = fetch_ohlcv(ticker, interval, limit)
    
            if length(ohlcv) == 960
                push!(All_ohlcv, ohlcv)
            else
                # println(length(ohlcv))
                push!(del_list, ticker)
            end
        end
        ticker_list=setdiff!(ticker_list, del_list)
    
    
        log_maker(parse(Int64, limit), All_ohlcv, ticker_list)
    
    
    end