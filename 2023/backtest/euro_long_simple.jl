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


Moving_average(var, n::Int64) = [sum(@view var[i:(i+n-1)]) / n for i in 1:(length(var) - (n - 1))]

True_range(ohlcv) = [(i == 1) ? var[3] - var[4] : maximum([var[3] - var[4], abs(var[3] - ohlcv[i-1][5]), abs(var[4] - ohlcv[i-1][5])]) for (i, var) in enumerate(ohlcv)]

function rma(data::Vector{T}, period::Int) where T
    alpha = 1 / period
    ema_values = similar(data, T)
    sma = sum(@view data[1:period]) / period
    ema_values[period] = sma
    @fastmath @simd for i in (period+1):length(data)
        ema_values[i] = (data[i] - ema_values[i-1]) * alpha + ema_values[i-1]
    end
    return ema_values
end

function rsi(data::Vector{T}, period::Int) where T
    delta = diff(data)
    gain = [max(delta[i], 0) for i in 1:length(delta)]
    loss = [max(-delta[i], 0) for i in 1:length(delta)]
    avg_gain = rma(gain, period)
    avg_loss = rma(loss, period)
    rs = avg_gain ./ avg_loss
    rsi_values = 100 .- (100 ./ (1 .+ rs))
    return rsi_values
end


function log_maker(ohlcv)
    global total_buy_sell_log
    buy_sell_log = []
    # slippage = 0.9994 * 0.9994
    slippage = 1

    global temp_result

    close = map(x -> x[5], ohlcv)
    ma5 = Moving_average(close, 5)[end-(length(close)-210):end]
    ma200 = Moving_average(close, 200)[end-(length(close)-210):end]
    rsi_ = rsi(close, 2)[end-(length(close)-210):end]

    # for j=length(rsi_)-2:-1:2
    for j=length(rsi_)-8:-1:2
        # if rsi_[end-j] < 5 && close[end-j] < ma5[end-j] && close[end-j] > ma200[end-j]
        if rsi_[end-j] < 5 #&& close[end-j] > ma200[end-j]
            entry_price= ohlcv[end-j+1][2]
            exit_price = ohlcv[end-j+2][2]
            earning = 100(exit_price/entry_price*slippage-1) 
            entry_time= ohlcv[end-j+1][1]
            exit_time = ohlcv[end-j+1][1]
            print("$(entry_time)  ")
            text = string(exit_time ,"   buy :", string(ohlcv[end-j+1][2]), "// sell :", string(exit_price), "  ",string(earning))
            println(text)
            push!(buy_sell_log, earning)
            push!(total_buy_sell_log, earning)
        end
    end


    get_performance(buy_sell_log, true)
    empty!(buy_sell_log)
    get_performance(total_buy_sell_log, true, 15000)
    return nothing
end



total_buy_sell_log = []

log_maker(ohlcvs)





