using HTTP
import JSON
using Statistics
using Dates
include("./../../2022/julia_test/utils.jl")

result = []

function log_maker(limit, All_ohlcv, ticker_list)
    
    global  total_buy_sell_log
    buy_sell_log = []
    slippage = 0.9982 * 0.9982
    for day in limit-3:-1:0
        for (i, ohlcv) in enumerate(All_ohlcv)
            high = maximum((ohlcv[end-(day+1)][3], ohlcv[end-(day+2)][3]))
            low = minimum((ohlcv[end-(day+1)][4], ohlcv[end-(day+2)][4]))
            open = ohlcv[end-(day+1)][2]
            close = ohlcv[end-(day+1)][5]

            value = 10^5
            if open < close # 양봉
                value = 2.305
            else
                value = 2.155
            end

            PP = (high + low + 4*close) / 6
            R2 = value * PP - low 
            if ohlcv[end-day][3] > R2
                entry_price = R2
                exit_price = ohlcv[end-day][4+1]
                earning = -100(exit_price / entry_price / slippage - 1)
                trade_time = unix2datetime((ohlcv[end-day][0+1]+3600000*9)/1000)
                #text = string(ticker_list[i]," " ,trade_time ,"   buy :", string(entry_price), "// sell :", string(exit_price), "  ",string(earning))
                #println(text)
                push!(buy_sell_log, earning)
                push!(total_buy_sell_log, earning)

                global result
                push!(result, earning)

            end
        end
        
    end
    get_performance(buy_sell_log, true)
    empty!(buy_sell_log)
    get_performance(total_buy_sell_log, true)
    return nothing
end



#4h = [2.3, 2.15, 0, true]


# ticker_list = ["MKRUSDT", "C98USDT", "SFPUSDT", "1000XECUSDT", "XEMUSDT", "ZENUSDT", "ETHUSDT", "MTLUSDT", "BATUSDT", "LDOUSDT", "ENJUSDT", "RSRUSDT", "OMGUSDT", "ATAUSDT", "IOSTUSDT", "STGUSDT", "DOGEUSDT", "ALGOUSDT", "ANKRUSDT", "CHZUSDT", "ZRXUSDT", "AVAXUSDT", "TOMOUSDT", "ARUSDT", "CELOUSDT", "SXPUSDT", "OCEANUSDT", "DOTUSDT", "UNFIUSDT", "ALPHAUSDT", "SPELLUSDT", "ONEUSDT", "EGLDUSDT", "INJUSDT", "DUSKUSDT", "RENUSDT", "KAVAUSDT", "NEOUSDT", "BCHUSDT", "SUSHIUSDT", "LPTUSDT", "SOLUSDT", "WOOUSDT", "NKNUSDT", "FILUSDT", "AAVEUSDT", "HOTUSDT", "FOOTBALLUSDT", "GTCUSDT", "QNTUSDT", "APEUSDT", "GALAUSDT", "VETUSDT", "ANTUSDT", "BELUSDT", "SNXUSDT", "BAKEUSDT", "STMXUSDT", "LUNA2USDT", "REEFUSDT", "OGNUSDT", "GALUSDT", "RLCUSDT", "XTZUSDT", "EOSUSDT", "CVXUSDT", "COTIUSDT", "STORJUSDT", "HNTUSDT", "IMXUSDT", "OPUSDT", "ARPAUSDT", "DASHUSDT", "MANAUSDT", "CELRUSDT", "GRTUSDT", "1INCHUSDT", "BLUEBIRDUSDT", "ROSEUSDT", "DEFIUSDT", "KSMUSDT", "LINAUSDT", "ATOMUSDT", "CHRUSDT", "XMRUSDT", "FTMUSDT", "IOTAUSDT", "BTCDOMUSDT", "CTKUSDT", "UNIUSDT", "TRXUSDT", "CRVUSDT", "KNCUSDT", "THETAUSDT", "ICXUSDT", "SKLUSDT", "API3USDT", "KLAYUSDT", "WAVESUSDT", "ADAUSDT", "ALICEUSDT", "1000LUNCUSDT", "FLOWUSDT", "MASKUSDT", "LRCUSDT", "NEARUSDT", "DARUSDT", "PEOPLEUSDT", "CTSIUSDT", "MATICUSDT", "BALUSDT", "ZILUSDT", "ENSUSDT", "DGBUSDT", "XLMUSDT", "JASMYUSDT", "QTUMUSDT", "LTCUSDT", "FLMUSDT", "RUNEUSDT", "ZECUSDT", "1000SHIBUSDT", "AXSUSDT", "BANDUSDT", "GMTUSDT", "ETCUSDT", "TRBUSDT", "ICPUSDT", "COMPUSDT", "LINKUSDT", "HBARUSDT", "XRPUSDT", "BNXUSDT", "DYDXUSDT", "YFIUSDT", "BTCUSDT", "APTUSDT", "LITUSDT", "SANDUSDT", "BLZUSDT", "BNBUSDT"]
ticker_list = get_tickers()

total_buy_sell_log = []

for i in range(1, 24)
    print(i)
    println("##########################################################################################################################################################################################################################################################################################")
    global ticker_list

    if i%5==0
        sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
    end

    All_ohlcv = []
    del_list = []
    interval = "4h"
    limit = "240"
    time_flag = 40
    multiple = i # 1~10

    btc_ohlcv = fetch_ohlcv("BTCUSDT", "1d", "1000")
    start_time = string(btc_ohlcv[end-time_flag*multiple][1])
    end_time = string(btc_ohlcv[end-time_flag*(multiple-1)][1])


    for ticker = ticker_list
        ohlcv = fetch_ohlcv(ticker, interval, limit, start_time, end_time)   
        if length(ohlcv) == 240
            push!(All_ohlcv, ohlcv)
        else
            push!(del_list, ticker)
        end
    end
    ticker_list=setdiff!(ticker_list, del_list)
    log_maker(parse(Int64, limit), All_ohlcv, ticker_list)

    get_performance(result, true)

end