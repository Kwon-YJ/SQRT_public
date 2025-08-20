using CSV, DataFrames
using Dates
include("./../../2022/julia_test/utils.jl")
using Statistics

# data = CSV.read("./E6_1m.CSV", DataFrame)
# data = CSV.read("./E6_5m.CSV", DataFrame)
# data = CSV.read("./E6_30m.CSV", DataFrame)
# data = CSV.read("./E6_1h.CSV", DataFrame)
# data = CSV.read("./E6_1d.CSV", DataFrame)


ohlcvs = []
for i=1:nrow(data)
    ohlcv = values( data[i, :] )
    push!(ohlcvs, ohlcv)
end

function log_maker(ohlcv)
    global total_buy_sell_log
    buy_sell_log = []
    slippage = 1

    for j=length(ohlcv)-3:-1:2
        
        high = ohlcv[end-j-1][3]
        low = ohlcv[end-j-1][4]
        TR = high - low


        entry_price = ohlcv[end-j][2] + .5*TR
        if ohlcv[end-j][3] > entry_price

            # 돌파 진입
            entry_price = ohlcv[end-j][2] + .5*TR
            exit_price = ohlcv[end-j+1][2]
            
            # 컨펌 후 진입
            # entry_price = ohlcv[end-j+1][2]
            # exit_price = ohlcv[end-j+2][2]

            earning = 100(exit_price/entry_price-1) *47
            entry_time= ohlcv[end-j][1]
            exit_time = ohlcv[end-j+1][1]
            print("$(entry_time)  ")
            text = string(exit_time ,"   buy :", "$(entry_price)", "// sell :", string(exit_price), "  ",string(earning))
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





