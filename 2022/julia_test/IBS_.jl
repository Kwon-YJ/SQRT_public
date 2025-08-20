include("./utils.jl")
using HTTP
import JSON
using Statistics
using Dates
using Base.Threads


function get_all_ibs(All_ohlcv, day)
    ibs_min = ["none", 1.1]
    ibs_max = ["none", 0]
    result = Dict()
    for ticker in keys(All_ohlcv)
        ibs = All_ohlcv[ticker][end-day+1][end]
        result[ticker] = ibs
        if ibs < ibs_min[2]
            ibs_min[1] = ticker
            ibs_min[2] = ibs
        end
        if ibs > ibs_max[2]
            ibs_max[1] = ticker
            ibs_max[2] = ibs
        end
    end
    return result, ibs_max, ibs_min
end

function log_maker(days, All_ohlcv, ticker_list)
    total_buy_sell_log = []
    buy_sell_log = []
    result = []
    slippage = 0.9982 * 0.9982
    for day in days:-1:2
        all_ibs, ibs_max, ibs_min = get_all_ibs(All_ohlcv, day)
        if ibs_min[2] > 0.1
            continue
        else
        
        long_ohlcv = All_ohlcv[ibs_min[1]][end-day+1:end]
        long_close = [close[5] for close in long_ohlcv]
        short_ohlcv= All_ohlcv[ibs_max[1]][end-day+1:end]
        short_close= [close[5] for close in short_ohlcv]
        
        long_earning = long_close/long_close[1]

        short_earning = [item/short_close[1] for item in short_close]


        earning_list = (long_earning + short_earning)/2

        println(ibs_max[1])
        println(ibs_min[1])

        println( unix2datetime((long_ohlcv[1][1]+3600000*33)/1000) )
        
        

        println(earning_list,"    /earning_list/    " ,length(earning_list))

        continue




        end
        


        # earning = 
        println("$ticker / short : $(y_max) / exit : $(ohlcv[end][5]) / time : $(unix2datetime( (ohlcv[end-1][1]+3600000*33) /1000)) /  earn : $(y_max/ohlcv[end][5])")
        earning = 100(y_max/ohlcv[end][5]*slippage-1)



    end
end


#=
function log_maker(days, All_ohlcv, ticker_list)
    total_buy_sell_log = []
    buy_sell_log = []
    result = []
    slippage = 0.9982 * 0.9982
    for day in days:-1:1
        println("\n$day")
        for (idx, ticker) in enumerate(ticker_list)
            ohlcv = All_ohlcv[ticker][end-day+1]
            ibs = get_all_ibs(All_ohlcv, day)
            
            if minimum(ibs) > 0.1
                continue

            if ibs[ticker] < 0.1

            

            if highs[end] == local_max && y_highs[1] != y_max
                println("$ticker / short : $(y_max) / exit : $(ohlcv[end][5]) / time : $(unix2datetime( (ohlcv[end-1][1]+3600000*33) /1000)) /  earn : $(y_max/ohlcv[end][5])")
                earning = 100(y_max/ohlcv[end][5]*slippage-1)
                push!(buy_sell_log, earning)
                push!(total_buy_sell_log, earning)
            end
        end
        push!(result, get_performance(buy_sell_log))
        empty!(buy_sell_log)
    end
    get_performance(total_buy_sell_log)
    return result
end
=#

function main()
    ticker_list = get_tickers()
    All_ohlcv = Dict()
    del_list = []
    backtest_boundaries = 200

    #time_ = fetch_ohlcv("BTCUSDT")[end][1]
    #start_time = string( time_ - (86400000*480) )
    #end_time = string( time_ - (86400000*350) )

    time_frame = "1d"
    for ticker in ticker_list
        # ohlcv = fetch_ohlcv(ticker, time_frame, string(backtest_boundaries), start_time, end_time)
        ohlcv = fetch_ohlcv(ticker, time_frame, string(backtest_boundaries))
        println(length(ohlcv))
        if length(ohlcv) != backtest_boundaries
            push!(del_list,ticker)
            continue
        end
        ibs_data = []
        for ohlcv_data in ohlcv
            high_ = ohlcv_data[3]
            low_ = ohlcv_data[4]
            close_ = ohlcv_data[5]
            ibs = (close_ - low_) / (high_ - low_)
            push!(ibs_data, ibs)
        end
        for (i, ibs) in enumerate(ibs_data)
            push!(ohlcv[i], ibs)
        end
        All_ohlcv[ticker] = ohlcv
    end
    ticker_list=setdiff!(ticker_list, del_list)


    result = log_maker(backtest_boundaries, All_ohlcv, ticker_list)

    pos = 0
    neg = 0
    for earning in result        
        try
            if earning > 0
                pos+=1
            else
                neg+=1
            end
        catch
            pos+=1
        end
    end
    println("pos : $pos // neg : $neg")

end

main()
