using CSV, DataFrames
using Dates

include("./../../2022/julia_test/utils.jl")


# data = CSV.read("./E6_full_1min.CSV", DataFrame)
# data = CSV.read("./E6_full_1h.CSV", DataFrame)
data = CSV.read("./E6_full_1d.CSV", DataFrame)
ohlcvs = []
for i=1:nrow(data)
    ohlcv = values( data[i, :] )
    push!(ohlcvs, ohlcv)
end

#println(ohlcvs[end-2])
#println(ohlcvs[end-1])
#println(ohlcvs[end])
#println(typeof(ohlcvs[end][end]))



#############################################################################
#############################################################################


result = Vector{Float64}([])

# function log_maker(days, All_ohlcv, ticker_list, param ,weight)
function log_maker(ohlcvs,param ,weight)
    total_buy_sell_log = []
    buy_sell_log = []
    slippage = 0.99993 * 0.99993
    
    for day=length(ohlcvs)-5:-1:1
        ohlcv = ohlcvs[end-day-param+1:end-day+1]
        lows = [low[4] for low in ohlcv]
        y_min = minimum( lows[1:end-1] )
        max_tr = maximum( map(x->abs(x[2]-x[5]), ohlcv[1:end-1]) )
        entry_price = y_min - max_tr * weight
        if ohlcv[end][4] < entry_price
            earning = 100(ohlcv[end][5]/entry_price*slippage-1)
            text = "long : $(convert(Float16,entry_price)) / exit : $(ohlcv[end][5]) / time : $(ohlcv[end-1][1]) /  earn : $(convert(Float16,earning))"
            println(text)
            # @info(text)
            push!(buy_sell_log, earning)
            push!(total_buy_sell_log, earning)
            global result
            push!(result, earning)
        end
        # get_performance(buy_sell_log, true, 200)
        empty!(buy_sell_log)
    end
    get_performance(total_buy_sell_log, true, 1)
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
    #close(io)
    return total_perform, trade_count
end




i = 4
j = 0.45
# j = 1.2




file_name = "$(i)_$(j)"

io = open("./$(file_name).txt", "a")
logger = SimpleLogger(io)
global_logger(logger)


log_maker(ohlcvs, i, j)


get_performance("./$(file_name).txt", result, true, 200)

if length(result) < 1
    log_post_processing("./$(file_name).txt")
    return nothing
end

empty!(result)
log_post_processing("./$(file_name).txt")

