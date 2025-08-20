using CSV, DataFrames
using Dates
include("./../../2022/julia_test/utils.jl")
using Statistics

data = CSV.read("./E6_1h.CSV", DataFrame)

ohlcvs = []
for i=1:nrow(data)
    ohlcv = values( data[i, :] )
    push!(ohlcvs, ohlcv)
end

function log_maker(ohlcv)
    global total_buy_sell_log
    buy_sell_log = []
    # slippage = 0.9994 * 0.9994
    slippage = 1
    for j=length(ohlcv)-5:-1:2
        
        high = ohlcv[end-(j)][3]
        low = ohlcv[end-(j)][4]
        close = ohlcv[end-(j)][5]

        if high - low == 0
            continue
        end
        ibs = (close - low) / (high - low)
        
        # if ibs > 0.9  #1d
        # if ibs < 0.05 #1d
        if ibs < 0.08 #1h

            entry_price= ohlcv[end-j+1][2]
            exit_price = ohlcv[end-j+2][2]
            # earning = -100(exit_price/entry_price-1) *47
            earning = 100(exit_price/entry_price-1) *47
            entry_time= ohlcv[end-j][1]
            exit_time = ohlcv[end-j+1][1]
            print("$(entry_time)  ")
            text = string(exit_time ,"   buy :", "$(entry_price)", "// sell :", string(exit_price), "  ",string(earning))
            println(text)
            push!(buy_sell_log, earning)
            push!(total_buy_sell_log, earning)

            if earning > 15
                entry_price= ohlcv[end-j+2][2]
                exit_price = ohlcv[end-j+3][2]
                earning = 100(exit_price/entry_price-1) *47
                text = string(exit_time ,"   buy :", "$(entry_price)", "// sell :", string(exit_price), "  ",string(earning))
                println(text)
                push!(buy_sell_log, earning)
                push!(total_buy_sell_log, earning)
            end

            if earning < -10
                entry_price= ohlcv[end-j+2][2]
                exit_price = ohlcv[end-j+3][2]
                earning = -100(exit_price/entry_price-1) *47
                text = string(exit_time ,"   buy :", "$(entry_price)", "// sell :", string(exit_price), "  ",string(earning))
                println(text)
                push!(buy_sell_log, earning)
                push!(total_buy_sell_log, earning)
            end

        end
    end
    get_performance(buy_sell_log, true)
    empty!(buy_sell_log)
    get_performance(total_buy_sell_log, true, 264)
    return nothing
end


total_buy_sell_log = []

log_maker(ohlcvs)





