using HTTP
import JSON
using Statistics
using Dates
include("./../../2022/julia_test/utils.jl")




function log_maker(limit, All_ohlcv, ticker_list)
    global total_buy_sell_log
    buy_sell_log = []
    slippage = 0.9994 * 0.9994


    for (i, ohlcv) in enumerate(All_ohlcv)
        ticker = ticker_list[i]

        close = map(x -> x[5], ohlcv)
        ma = Moving_average(close, 20)[end-1439:end]
        tr2 = (Moving_average(True_range(ohlcv), 4) .* 1.5)[end-1439:end]
        rsi_ = rsi(map(x -> x[3], ohlcv), 15)[end-1439:end]
        exit_target = ma + tr2

        long_entry_price = []
        long_entry_time_buffer = []

        for j=length(rsi_)-1:-1:1
            if rsi_[end-j] < 7 && length(long_entry_price) == 0
                push!(long_entry_price, ohlcv[end-j+1][2])
                push!(long_entry_time_buffer, "$(unix2datetime(ohlcv[end-j+1][1]/1000))")
                continue
            end
            if length(long_entry_price) != 0
                if exit_target[end-j] < (ohlcv[end-j][2] + ohlcv[end-j][5]) / 2
                    exit_price = ohlcv[end-j+1][2]
                    earning = 100(exit_price/long_entry_price[end]*slippage-1)
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
            earning = 100(exit_price/long_entry_price[end]*slippage-1)
            exit_time = "$(unix2datetime(ohlcv[end][1]/1000))"

            #print("$(long_entry_time_buffer[end])  ")
            #text = string(ticker," " ,exit_time ,"   buy :", string(long_entry_price[end]), "// sell :", string(exit_price), "  ",string(earning))
            #println(text)

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




function get_HA_ohlcv(ohlcv)
    ha_ohlcv = [ohlcv[1]]
    ha_open = -1
    for i in range(2, length(ohlcv))
        if i == 2
            ha_open = (ohlcv[i-1][2] + ohlcv[i-1][5]) / 2
        else
            ha_open = (ha_ohlcv[i-2][2] + ha_ohlcv[i-2][5]) / 2
        end
        result = ohlcv[i]
        time_stamp = result[1]
        ha_close = (result[2] + result[3] + result[4] + result[5]) / 4
		ha_high = maximum([result[3], ha_close, ha_open])
		ha_low = minimum([result[4], ha_close, ha_open])
        push!(ha_ohlcv, [time_stamp, ha_open, ha_high, ha_low, ha_close])
    end
    return ha_ohlcv
end


ticker = "BTCUSDT"
btc_ohlcv = fetch_ohlcv(ticker, "1d", "1500")

ha_ohlcv = get_HA_ohlcv(btc_ohlcv)

buy_sell_log = []

position_handler = Dict()

slippage = 0.9994 * 0.9994

compounding = [1]

for (i, ohlcv) in enumerate(btc_ohlcv)
    T, O, H, L, C = ohlcv[1:5]
    global compounding
    if length(position_handler) == 0
        if O < C
            position_handler["long"] = C
        else
            position_handler["short"] = C
        end
    else
        if haskey(position_handler, "long")
            earning = 100(position_handler["long"]/C*slippage-1) * compounding[1]
            println(earning)
            push!(buy_sell_log, earning)
            if O > C #손절 분기
                #compounding[1] = compounding[1] * 2
                compounding[1] = compounding[1] + 1
                empty!(position_handler)
                position_handler["short"] = C
                continue
            end
        else
            earning = -100(position_handler["short"]/C/slippage-1) * compounding[1]
            println(earning)
            push!(buy_sell_log, earning)
            if O < C #손절 분기
                #compounding[1] = compounding[1] * 2
                compounding[1] = compounding[1] + 1
                empty!(position_handler)
                position_handler["long"] = C
                continue
            end
        end
        
        compounding[1] = 1
        empty!(position_handler)
        # 익절 분기, HA 
        T, O, H, L, C = ha_ohlcv[i][1:5]
        if O < C
            position_handler["long"] = ohlcv[5]
        else
            position_handler["short"] = ohlcv[5]
        end
    end
end
println(length(buy_sell_log))
get_performance(buy_sell_log, true, 100)











