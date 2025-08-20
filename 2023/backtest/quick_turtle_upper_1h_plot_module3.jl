include("./../../2022/julia_test/utils.jl")
using HTTP
import JSON
using Statistics
using Dates
# using Base.Threads


using Telegram, Telegram.API
using Nettle
using Formatting
using Logging

using Base.Threads


result = Vector{Float64}([])

function log_maker(days, All_ohlcv, ticker_list, param ,weight)
    total_buy_sell_log = []
    buy_sell_log = []
    slippage = 0.9982 * 0.9982
    std_len = length(All_ohlcv["ETHUSDT"])
    for day in days:-1:1
        momentum = Atomic{Float64}(0)
        momentum_count = Atomic{Int64}(0)

        if day%24 == 0
        # if day%1 == 0
            get_performance(buy_sell_log, true, money)
            println("********************************************************************************************************************************")
            println("Press Enter!")
            empty!(buy_sell_log)
            readline()
        end

        # Threads.@threads for ticker in ticker_list
        for ticker in ticker_list
            if length(All_ohlcv[ticker]) != std_len
                continue
            end
            if length(All_ohlcv[ticker])-day-param+1 < 1
                continue
            end 
            ohlcv = All_ohlcv[ticker][end-day-param+1:end-day+1]
            y_max = maximum( map(x->x[3], ohlcv[1:end-1]) )
            max_tr = maximum( map(x->abs(x[2]-x[5]), ohlcv[1:end-1]) )
            atomic_2_regular = momentum[]
            entry_price = y_max + max_tr * (weight+atomic_2_regular)
            if ohlcv[end][3] > entry_price
                if momentum_count[] > 4
                    atomic_add!(momentum, 0.04)
                else
                    atomic_add!(momentum, 0.01)
                end
                atomic_add!(momentum_count, 1)
                earning = -100(ohlcv[end][5] / entry_price / slippage - 1)
                text = "$ticker / short : $(convert(Float16,entry_price)) / exit : $(ohlcv[end][5]) / time : $(unix2datetime( (ohlcv[end-1][1])/1000)) /  earn : $(convert(Float16,earning))"
                println(text)
                #@info(text)
                push!(buy_sell_log, earning)
                push!(total_buy_sell_log, earning)
                global result
                push!(result, earning)
            end
        end
        #get_performance(buy_sell_log, true)
        #empty!(buy_sell_log)
    end
    get_performance(total_buy_sell_log, true, money)
    return nothing
end




function get_performance(file_name::String, trade_log::Vector{Float64}, verbose, money = 1)
    io = open(file_name, "a")
    logger = SimpleLogger(io)
    global_logger(logger)

    if length(trade_log) == 0
        return 0, 0
    else
        trade_count = length(trade_log)
    end


    win = [value for value in trade_log if value > 0]
    lose = [value for value in trade_log if value < 0]

    risk_free = 0.038/365
    avg = mean(trade_log)

    if length(lose) == 0
        avg_lose = 10^-6
        std_lose = 10^-6
    else
        avg_lose = mean(lose)
        std_lose = std(lose, corrected=false)
    end

    if length(win) == 0
        avg_win = 10^-6
        win_count = 0
    else
        avg_win = mean(win)
        win_count = length(win)
    end
    
    std_value = std(trade_log, corrected=false)
    avg_w_l_ratio = -1 * avg_win / avg_lose
    win_rate = 100*length(win)/length(trade_log)
    sharp = (avg - risk_free) / std_value
    sortino = (avg - risk_free) / std_lose
    if avg_w_l_ratio < 0
        total_perform = "Nan"
    else
        total_perform = shortest_distance(avg_w_l_ratio, win_count / trade_count)
    end
    size = (avg - risk_free) / std_value^2
    if verbose == true

        @info("총 거래 수 : $(trade_count)")
        @info("수익 거래 수 : $(win_count)")
        @info("손실 거래 수 : $(length(lose))")
        @info("평균 손익률 : $(avg)%")
        @info("평균 수익률 : $(avg_win)%")
        @info("평균 손실률 : $(avg_lose)%")
        @info("평균 손익비 : $(avg_w_l_ratio)")
        @info("승 률 : $(win_rate)%")
        @info("포지션 사이징 : $(size)")
        @info("sharp ratio : $(sharp)%")
        @info("sortino ratio : $(sortino)")
        if length(lose) != 0
            @info("최대 손실 : $(minimum(lose))%")
        end
        @info(sum(trade_log) * money * 0.01)
        @info("$(total_perform)\n")
        @info("")
    end
    flush(io)
    return total_perform, trade_count
end



i = 6
j = 1.0
file_name = "$(i)_$(j)"
money = 100

io = open("./$(file_name).txt", "a")
logger = SimpleLogger(io)
global_logger(logger)

for k in range(1,24)
    
    print(k)
    #@info(k)
    println("##########################################################################################################################################################################################################################################################################################")
    #@info("##########################################################################################################################################################################################################################################################################################")
    #flush(io)
    
    log_maker(960+i, All_ohlcvs[k], ticker_lists[k], i, j)
end
get_performance("./$(file_name).txt", result, true, money)
empty!(result)
log_post_processing("./$(file_name).txt")


