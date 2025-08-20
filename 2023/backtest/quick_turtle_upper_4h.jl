include("./../../2022/julia_test/utils.jl")
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
        println("$day")

        @inbounds for (idx, ticker) in enumerate(ticker_list)
            ohlcv = All_ohlcv[ticker][end-day-param+1:end-day+1]
            y_max = maximum( map(x->x[3], ohlcv[1:end-1]) )
            max_tr = maximum( map(x->abs(x[2]-x[5]), ohlcv[1:end-1]) )
            entry_price = y_max + max_tr * 3.9
            if ohlcv[end][3] > entry_price
                # println("$ticker / short : $(entry_price) / exit : $(ohlcv[end][5]) / time : $(unix2datetime( (ohlcv[end-1][1]+3600000*33) /1000)) /  earn : $(y_max/ohlcv[end][5])")
                earning = -100(ohlcv[end][5] / entry_price * slippage - 1)
                push!(buy_sell_log, earning)
                push!(total_buy_sell_log, earning)
            end
        end
        push!(result, get_performance(buy_sell_log, true))
        empty!(buy_sell_log)
    end
    get_performance(total_buy_sell_log, true)
    return result
end

function main()
    ticker_list = get_tickers()
    All_ohlcv = Dict()
    del_list = []
    backtest_boundaries = 1499
    price_ch_interval = 11
    
    #backtest_boundaries = 130
    #time_ = fetch_ohlcv("BTCUSDT")[end][1]
    #start_time = string( time_ - (86400000*480) )
    #end_time = string( time_ - (86400000*350) )

    time_frame = "4h"
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
end

main()
