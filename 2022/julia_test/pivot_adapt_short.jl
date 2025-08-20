using Statistics
include("./utils.jl")


function get_sum_value(limit, All_ohlcv, weight, day_value)
    total_buy_sell_log = []
    weight = weight
    slippage = 0.9992 * 0.9992
    
    for day in limit-2:-1:0
        for (i, ohlcv) in enumerate(All_ohlcv)
            high = ohlcv[end-(day+1)][2+1]
            low = ohlcv[end-(day+1)][3+1]
            close = ohlcv[end-(day+1)][4+1]
            PP = (high + low + 4*close) / 6
            # S2 = weight * PP - high 
            R2 = weight * PP -low
            # if ohlcv[end-day][3+1] < S2
            if ohlcv[end-day][3] > R2
                # entry_price = S2
                entry_price = R2
                exit_price = ohlcv[end-day][4+1]
                # earning = 100(exit_price / entry_price - 1)
                earning = 100(entry_price /exit_price  * slippage - 1) # short
                push!(total_buy_sell_log, earning)
            end
        end
    end
    if length(total_buy_sell_log)!=0
        return sum(total_buy_sell_log)    
    end
end

function get_optimized_weight(ticker, day_value, start_time, end_time, length_btc)
    All_ohlcv = []
    interval = "4h"
    limit = "1499"
    #temp_ohlcv = fetch_ohlcv("BTCUSDT", "1d", 85+day_value, "", "", "spot")
    #start_time = string(temp_ohlcv[1][1])
    # end_time = string(temp_ohlcv[end-day_value][1])
    ohlcv = fetch_ohlcv(ticker, interval, limit, start_time, end_time)
    
    if length_btc != length(ohlcv)
        return nothing
    end


    close_price = Float64[close[5] for close in ohlcv]

    close_std = std(close_price, corrected=false) / close_price[end]

    push!(All_ohlcv, ohlcv)
    weight_space = [i for i in 1.96:0.0001:2.1]
    result = Dict()

    # @inbounds for weight in weight_space
    for weight in weight_space
        sum_value = get_sum_value(length(All_ohlcv[1]), All_ohlcv, weight, day_value)
        if sum_value != nothing && sum_value > 0
            result[weight] = sum_value
        end
    end
    
    

    #result_sort = sort(collect(result), by=x->x[1])
    #[println(data) for data in result_sort]
    

    result_keys = [key for key in keys(result)]

    if length(result_keys) == 0
        println("")
        return nothing
    end
    
    med = 0
    if length(result_keys)%2 == 0
        med = median(result_keys[1:end-1])
    else
        med = median(result_keys)
    end
    

    # avg_value = [result[data] for data in result_keys]
    # println(minimum(result_keys))
    # println("med : $(med) med_value : $(result[round(med, digits = 4)]) avg_value : $(round(mean(avg_value), digits = 4)) std : $(close_std)")
    # println("med : $(med) std : $(close_std)")

    #println("med : $(med)")
    #println("")

    # return med
    # return minimum(result_keys)
    return maximum(result_keys)
end





function log_maker(limit, All_ohlcv, ticker_list, result)
    total_buy_sell_log = []
    buy_sell_log = []
    slippage = 0.9992 * 0.9992
    for day in limit-2:-1:0
        for (i, ohlcv) in enumerate(All_ohlcv)
            weight = result[ticker_list[i]]
            high = ohlcv[end-(day+1)][2+1]
            low = ohlcv[end-(day+1)][3+1]
            close = ohlcv[end-(day+1)][4+1]
            PP = (high + low + 4*close) / 6
            # S2 = weight * PP - high 
            R2 = weight * PP -low
            # if ohlcv[end-day][3+1] < S2
            if ohlcv[end-day][3] > R2
                # entry_price = S2
                entry_price = R2
                exit_price = ohlcv[end-day][4+1]
                # earning = 100(exit_price / entry_price * slippage - 1) # long
                earning = 100(entry_price /exit_price  * slippage - 1) # short
                trade_time = unix2datetime((ohlcv[end-day][0+1]+3600000*9)/1000)
                text = string(ticker_list[i]," " ,trade_time ,"   buy :", string(entry_price), "// sell :", string(exit_price), "  ",string(earning))
                #println(text)
                push!(buy_sell_log, earning)
                push!(total_buy_sell_log, earning)
            end
        end
        #get_performance(buy_sell_log)
        empty!(buy_sell_log)
    end
    get_performance(total_buy_sell_log)
    return nothing
end



for day_value in 100:-1:0
    println(day_value)
    #pahse 1

    result = Dict()
    interval = "4h"
    limit = "1499"


    # ticker_list = get_tickers()
    ticker_list = ["MKRUSDT", "C98USDT", "SFPUSDT", "1000XECUSDT", "XEMUSDT", "ZENUSDT", "ETHUSDT", "MTLUSDT", "BATUSDT", "LDOUSDT", "ENJUSDT", "RSRUSDT", "OMGUSDT", "ATAUSDT", "IOSTUSDT", "STGUSDT", "DOGEUSDT", "ALGOUSDT", "ANKRUSDT", "CHZUSDT", "ZRXUSDT", "AVAXUSDT", "TOMOUSDT", "ARUSDT", "CELOUSDT", "SXPUSDT", "OCEANUSDT", "DOTUSDT", "UNFIUSDT", "ALPHAUSDT", "SPELLUSDT", "ONEUSDT", "EGLDUSDT", "INJUSDT", "DUSKUSDT", "RENUSDT", "KAVAUSDT", "NEOUSDT", "BCHUSDT", "CVCUSDT", "SUSHIUSDT", "LPTUSDT", "SOLUSDT", "WOOUSDT", "NKNUSDT", "FILUSDT", "AAVEUSDT", "HOTUSDT", "FOOTBALLUSDT", "GTCUSDT", "QNTUSDT", "APEUSDT", "GALAUSDT", "VETUSDT", "ANTUSDT", "BELUSDT", "SNXUSDT", "BAKEUSDT", "STMXUSDT", "LUNA2USDT", "REEFUSDT", "OGNUSDT", "GALUSDT", "RLCUSDT", "XTZUSDT", "EOSUSDT", "CVXUSDT", "COTIUSDT", "STORJUSDT", "HNTUSDT", "IMXUSDT", "OPUSDT", "ARPAUSDT", "DASHUSDT", "MANAUSDT", "CELRUSDT", "GRTUSDT", "1INCHUSDT", "BLUEBIRDUSDT", "ROSEUSDT", "DEFIUSDT", "KSMUSDT", "LINAUSDT", "ATOMUSDT", "CHRUSDT", "IOTXUSDT", "XMRUSDT", "FTMUSDT", "IOTAUSDT", "BTCDOMUSDT", "CTKUSDT", "UNIUSDT", "TRXUSDT", "ONTUSDT", "CRVUSDT", "KNCUSDT", "RVNUSDT", "THETAUSDT", "ICXUSDT", "SKLUSDT", "API3USDT", "KLAYUSDT", "WAVESUSDT", "ADAUSDT", "ALICEUSDT", "1000LUNCUSDT", "FLOWUSDT", "MASKUSDT", "LRCUSDT", "NEARUSDT", "DARUSDT", "AUDIOUSDT", "PEOPLEUSDT", "CTSIUSDT", "MATICUSDT", "BALUSDT", "ZILUSDT", "ENSUSDT", "DGBUSDT", "XLMUSDT", "JASMYUSDT", "DENTUSDT", "QTUMUSDT", "LTCUSDT", "FLMUSDT", "RUNEUSDT", "ZECUSDT", "1000SHIBUSDT", "AXSUSDT", "BANDUSDT", "GMTUSDT", "ETCUSDT", "TRBUSDT", "ICPUSDT", "COMPUSDT", "LINKUSDT", "HBARUSDT", "XRPUSDT", "BNXUSDT", "DYDXUSDT", "YFIUSDT", "BTCUSDT", "APTUSDT", "LITUSDT", "SANDUSDT", "BLZUSDT", "BNBUSDT"]
    

    

    temp_ohlcv = fetch_ohlcv("BTCUSDT", "1d", 85+day_value, "", "", "spot")
    start_time = string(temp_ohlcv[1][1])
    end_time = string(temp_ohlcv[end-day_value][1])
    btc_ohlcv = fetch_ohlcv("BTCUSDT", interval, limit, start_time, end_time)
    
    for ticker in ticker_list
        sleep(1.5)
        med = get_optimized_weight(ticker, day_value, start_time, end_time, length(btc_ohlcv))
        if med != nothing
            result[ticker] = med
        end
    end




    #pahse 2

    All_ohlcv = []
    

    ticker_list = [key for key in keys(result)]
    # ticker_list = ["1000SHIBUSDT"]

    temp_ohlcv = fetch_ohlcv("BTCUSDT", "1d", 2+day_value, "", "", "spot")
    start_time = string(temp_ohlcv[1][1])

    # temp_ohlcv = fetch_ohlcv("BTCUSDT", "1m", 1, "", "", "spot")
    end_time = string(temp_ohlcv[3][1])


    for ticker = ticker_list
        sleep(1.5)
        ohlcv = fetch_ohlcv(ticker, interval, limit, start_time,end_time)
        push!(All_ohlcv, ohlcv)
    end

    # log_maker(parse(Int64, limit), All_ohlcv, ticker_list)

    log_maker(length(All_ohlcv[1]), All_ohlcv, ticker_list, result)

    sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))

end