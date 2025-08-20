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
        high = maximum((ohlcv[end-(j+1)][3], ohlcv[end-(j+2)][3]))
        low = minimum((ohlcv[end-(j+1)][4], ohlcv[end-(j+2)][4]))

        open = ohlcv[end-(j)][2]
        close = ohlcv[end-(j+1)][5]

        
        PP = (high + low + 6.1*close) / 8.1
        S2 = 1.997 * PP - high # 1h
        

        if ohlcv[end-j][4] < S2
            entry_price= S2
            exit_price = ohlcv[end-j+1][2]
            earning = -100(exit_price/entry_price-1) *47
            entry_time= ohlcv[end-j][1]
            exit_time = ohlcv[end-j+1][1]
            print("$(entry_time)  ")
            text = string(exit_time ,"   buy :", "$(S2)", "// sell :", string(exit_price), "  ",string(earning))
            println(text)
            push!(buy_sell_log, earning)
            push!(total_buy_sell_log, earning)
        end
    end
    get_performance(buy_sell_log, true)
    empty!(buy_sell_log)
    get_performance(total_buy_sell_log, true, 264)
    return nothing
end


total_buy_sell_log = []

log_maker(ohlcvs)





