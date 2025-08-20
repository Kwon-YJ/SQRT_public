using HTTP
import JSON
using Statistics
using Dates
include("./../../2022/julia_test/utils.jl")

using BenchmarkTools

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










function log_maker(limit, All_ohlcv, ticker_list)
    global total_buy_sell_log
    buy_sell_log = []
    # slippage = 0.9982 * 0.9982
    slippage = 0.9994 * 0.9994


    for (i, ohlcv) in enumerate(All_ohlcv)
        ticker = ticker_list[i]

        close = map(x -> x[5], ohlcv)
        ma = Moving_average(close, 20)[end-1439:end]
        tr2 = (Moving_average(True_range(ohlcv), 4) .* 1.5)[end-1439:end]
        rsi_ = rsi(close, 14)[end-1439:end]
        exit_target = ma - tr2

        #for idx=1:10
        #    println("$(unix2datetime(ohlcv[end-idx][1]/1000)) ma:$(ma[end-idx]) tr2:$(tr2[end-idx]) rsi:$(rsi_[end-idx])")
        #end
        #exit()

        long_entry_price = []
        long_entry_time_buffer = []

        for j=length(rsi_)-2:-1:2
        # for j=length(rsi_)-1:-1:1
            # if rsi_[end-j] > 80 && rsi_[end-j-1] > 80 && length(long_entry_price) == 0
            
            if rsi_[end-j] > 90 && rsi_[end-j-1] > 90 && length(long_entry_price) == 0

            # if rsi_[end-j] > 80 && length(long_entry_price) == 0
                #println(rsi_[end-j])
                #println("$(unix2datetime(ohlcv[end-j+1][1]/1000))")
                #exit()
                push!(long_entry_price, ohlcv[end-j+1][2])
                push!(long_entry_time_buffer, "$(unix2datetime(ohlcv[end-j+1][1]/1000))")
                continue
            end
            if length(long_entry_price) != 0
                if exit_target[end-j] > (ohlcv[end-j][2] + ohlcv[end-j][5]) / 2
                    exit_price = ohlcv[end-j+1][2]
                    earning = -100(exit_price/long_entry_price[end]/slippage-1)
                    exit_time = "$(unix2datetime(ohlcv[end-j+1][1]/1000))"
                    print("$(long_entry_time_buffer[end])  ")
                    text = string(ticker," " ,exit_time ,"   buy :", string(long_entry_price[end]), "// sell :", string(exit_price), "  ",string(earning))
                    println(text)
                    push!(buy_sell_log, earning)
                    push!(total_buy_sell_log, earning)

                    exit_time_for_daily = ohlcv[end-j+1][1]
                    global daily_time_array
                    global daily_buy_sell_log
                    
                    for t = 2:length(daily_time_array)
                        t0 = daily_time_array[t-1]
                        t1 = daily_time_array[t]
                        if t0 < exit_time_for_daily < t1
                            push!(daily_buy_sell_log, earning)
                        end
                    end
                    empty!(long_entry_price)
                    empty!(long_entry_time_buffer)
                end
            end
        end

        if length(long_entry_price) != 0
            exit_price = ohlcv[end][2]
            earning = -100(exit_price/long_entry_price[end]/slippage-1)
            exit_time = "$(unix2datetime(ohlcv[end][1]/1000))"
            print("$(long_entry_time_buffer[end])  ")
            text = string(ticker," " ,exit_time ,"   buy :", string(long_entry_price[end]), "// sell :", string(exit_price), "  ",string(earning))
            println(text)
            push!(buy_sell_log, earning)
            push!(total_buy_sell_log, earning)
            exit_time_for_daily = ohlcv[end][1]
            global daily_time_array
            global daily_buy_sell_log
            for t = 2:length(daily_time_array)
                t0 = daily_time_array[t-1]
                t1 = daily_time_array[t]
                if t0 < exit_time_for_daily < t1
                    push!(daily_buy_sell_log, earning)
                end
            end
        end
    end
    get_performance(buy_sell_log, true)
    empty!(buy_sell_log)
    get_performance(total_buy_sell_log, true)
    return nothing
end



daily_time_array = fetch_ohlcv("BTCUSDT", "1d", 1500)
daily_time_array = map(x->x[1], daily_time_array)
total_buy_sell_log = []

daily_buy_sell_log = similar(daily_time_array, Float32)

println(length(daily_time_array))

for i in range(1, 295)
    ticker_list = get_tickers()
    # ticker_list = ["BTCUSDT"]
    print(i)
    println("##########################################################################################################################################################################################################################################################################################")

    
    
    

    All_ohlcv = []
    del_list = []
    interval = "5m"
    limit = "1500"
    time_flag = 5
    multiple = i

    btc_ohlcv = fetch_ohlcv("BTCUSDT", "1d", "1500")
    start_time = string(btc_ohlcv[end-time_flag*multiple][1])
    end_time = string(btc_ohlcv[end-time_flag*(multiple-1)][1])
    
    for ticker = ticker_list
        sleep(0.33)
        ohlcv = fetch_ohlcv(ticker, interval, limit, start_time, end_time)
        if length(ohlcv) == 1441
            p_start_time = string(btc_ohlcv[end-time_flag*multiple-1][1])
            p_ohlcv = fetch_ohlcv(ticker, interval, limit, p_start_time, start_time)
            push!(All_ohlcv, [p_ohlcv;ohlcv])
        else
            push!(del_list, ticker)
        end
    end
    ticker_list=setdiff!(ticker_list, del_list)
    log_maker(parse(Int64, limit), All_ohlcv, ticker_list)

end







