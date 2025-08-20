include("./utils.jl")
using HTTP
import JSON
using Statistics
using Dates
using Base.Threads


function log_maker(days, All_ohlcv, ticker_list, param)
    total_buy_sell_log = []
    buy_sell_log = []
    result = []
    slippage = 0.9982 * 0.9982
    for day in days-1:-1:1
        println("\n$day")
        for (idx, ticker) in enumerate(ticker_list)
            ohlcv = All_ohlcv[ticker][end-day-param+1:end-day+1]
            highs = [high[3] for high in ohlcv]
            local_max = maximum(highs)
            y_max = maximum(highs[1:end-1])
            if highs[end] == local_max
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

function main()
    ticker_list = get_tickers()
    All_ohlcv = Dict()
    del_list = []
    backtest_boundaries = 100
    # price_ch_interval = 44
    price_ch_interval = 5
    
    #backtest_boundaries = 130
    #time_ = fetch_ohlcv("BTCUSDT")[end][1]
    #start_time = string( time_ - (86400000*480) )
    #end_time = string( time_ - (86400000*350) )

    time_frame = "1d"
    for ticker in ticker_list
        # ohlcv = fetch_ohlcv(ticker, time_frame, string(backtest_boundaries), start_time, end_time)
        ohlcv = fetch_ohlcv(ticker, time_frame, string(backtest_boundaries))
        if length(ohlcv) != backtest_boundaries
            push!(del_list,ticker)
            continue
        end
        All_ohlcv[ticker] = ohlcv
    end
    ticker_list=setdiff!(ticker_list, del_list)
    result = log_maker(backtest_boundaries-price_ch_interval, All_ohlcv, ticker_list, price_ch_interval)
    println(price_ch_interval)
    
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
