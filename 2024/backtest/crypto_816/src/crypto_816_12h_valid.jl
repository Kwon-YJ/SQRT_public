using Statistics
using DataFrames
using CSV
using Dates

include("../../../../2022/julia_test/utils.jl")


function csv_init(input_data, file_name)
    if isempty(input_data)
        return nothing
    end
    if length(input_data) < 4
        return nothing
    end
    try 
        if input_data[4] < 0.15
            return nothing
        end
    catch
        if parse(Float64, input_data[4])  < 0.15
            return nothing
        end
    end

    df = DataFrame(A = [input_data[1]], B = [input_data[2]], C = [input_data[3]], D = [input_data[4]])
    CSV.write(file_name, df, append=true)
end


function shortest_distance_(ratio, winrate)
    lins = [i/10000 for i in 0:100000]
    y = [-log(0.99) / (log(1+0.01*i) - log(0.99)) for i in lins]
    least_distance = 100
    for i in 1:100000
        dx = lins[i] - ratio
        dy = y[i] - winrate
        distance = sqrt(dx^2 + dy^2)
        if distance < least_distance
            least_distance = distance
        end
    end
    base_line = -log(0.99) / (log(1+0.01*ratio) - log(0.99))
    if winrate > base_line
        return least_distance
    else
        return -least_distance
    end
end


function load_data(data_dir="../../data/", file_name="E6_1d.CSV")
    csv_data = CSV.read(data_dir*file_name, DataFrame)
    csv_data = csv_data[2:end, :]
    try
        rename!(csv_data, [:t, :o, :h, :l, :c, :v, :s, :real_v])
    catch
        rename!(csv_data, [:t, :o, :h, :l, :c, :v])
    end
    #only_close = csv_data[!, "c"]
    #ema_8 = ema(only_close, 8)
    #ema_16 = ema(only_close, 16)
    #return csv_data, ema_8, ema_16
    return csv_data
end








function back_test(open_data, high_data, low_data, close_data, time_data,ema_8,ema_16,tail_d,body_d, param_1::Float64, param_2::Float64, file_name::String)

    is_long = false
    slippage = 1
    long_entry_price = Vector{Float64}([])
    trade_log = Vector{Float64}([])
    long_sl = Vector{Float64}([])
    long_tp = Vector{Float64}([])

    for i::Int64=1:length(close_data)-1
        low_::Float64 = low_data[i]
        close_::Float64 = close_data[i]
        short_ema::Float64 = ema_8[i]
        open_::Float64 = open_data[i]

        if is_long == false
            if low_ < short_ema && min(close_, open_) > short_ema && short_ema > ema_16[i]
                if body_d[i] * param_1 < tail_d[i]
                    is_long = true
                    push!(long_entry_price, open_data[i+1])
                    push!(long_sl, low_)
                    push!(long_tp, open_data[i+1] + param_2* abs((low_-max(close_, open_))))

                    println("entry : $(unix2datetime(time_data[i]/1000)) $(long_entry_price[end])")

                    long_entry_time = time_data[i+1]
                end
            end
        else
            if low_ < long_sl[end]
                is_long = false
                earning = 100 * (long_sl[end] / long_entry_price[end] * slippage -1)
                println("exit : $(unix2datetime(time_data[i]/1000)) $(earning)")
                push!(trade_log, earning)
            elseif high_data[i] > long_tp[end]
                is_long = false
                earning = 100 * (long_tp[end] / long_entry_price[end] * slippage -1)
                println("exit : $(unix2datetime(time_data[i]/1000)) $(earning)")
                push!(trade_log, earning)
            end
        end
    end
        
    result = get_performance(trade_log, true)
    # csv_init([param_1, param_2, length(trade_log), result], file_name)
end




@inbounds function ema(data::Vector{T}, period::Int) where T
    alpha = 2 / (period + 1)
    ema_values = similar(data, T)
    sma = sum(@view data[1:period]) / period
    ema_values[period] = sma
    @fastmath @simd for i in (period+1):length(data)
        ema_values[i] = (data[i] - ema_values[i-1]) * alpha + ema_values[i-1]
    end
    return ema_values
end



data_dir = "../data/12h/"


ticker = "AAVE"
file_name = ticker * "USDT_12h.csv"


println(file_name)

ohlc = load_data(data_dir, file_name)

open_data = ohlc.o
high_data = ohlc.h
low_data = ohlc.l
close_data = ohlc.c
time_data = ohlc.t


ema_8 = ema(close_data, 8)
ema_16 = ema(close_data, 16)


tail_d = Vector{Float64}([])
body_d = Vector{Float64}([])


for i::Int64=1:length(close_data)
    low_::Float64 = low_data[i]
    close_::Float64 = close_data[i]
    open_::Float64 = open_data[i]
    push!(tail_d, min(close_, open_) - low_)
    push!(body_d, abs(close_ - open_))
end

println("start : $(file_name)")



back_test(open_data, high_data, low_data, close_data, time_data,ema_8,ema_16,tail_d,body_d , 4.382352941176471, 1.0470588235294118, file_name)










