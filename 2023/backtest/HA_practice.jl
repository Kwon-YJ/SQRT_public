include("./../../2022/julia_test/utils.jl")
using HTTP
import JSON
using Statistics
using Dates

function get_HA_ohlcv(ohlcv)
    ha_ohlcv = []
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

moving_average(vs, n) = [sum(@view vs[i:(i+n-1)]) / n for i in 1:(length(vs) - (n - 1))]

function get_rolling_std(data, mean_data, n)
    squared_diff = [(data[i:(i+n-1)] .- mean_data[i]) .^ 2 for i in 1:length(data) - (n - 1)]
    std_data = sqrt.(sum.(squared_diff) ./ n)  # 표준편차 계산
    return std_data
end

function get_bollinger(ohlcvs, interval, k)
    close_data = map(x->x[5], ohlcvs)
    mbb = moving_average(close_data, interval)
    std = get_rolling_std(close_data, mbb, interval)
    lbb = mbb - k * std
    ubb = mbb + k * std
    return ubb, mbb, lbb
end


function get_all_ohlcv()
    ticker_list = get_tickers()
    All_ohlcvs = []
    ticker_lists = []

    for i in 24:-1:1
        All_ohlcv = Dict()
        del_list = []
        if i%2==0
            sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
        end
        interval = "1h"
        limit::Int64 = 960
        time_flag = 41
        btc_ohlcv = fetch_ohlcv("BTCUSDT", "1d", "1000")
        start_time = string(btc_ohlcv[end-time_flag*i][1])
        end_time = string(btc_ohlcv[end-time_flag*(i-1)][1])

        for ticker in ticker_list
            ohlcv = fetch_ohlcv(ticker, interval, string(limit), start_time, end_time)
            All_ohlcv[ticker] = ohlcv
        end

        ticker_list=setdiff!(ticker_list, del_list)
        push!(All_ohlcvs, All_ohlcv)
        push!(ticker_lists, ticker_list)
    end

    result_dict = Dict()

    for key in ticker_list
        result_dict[key] = []
    end

    for (i,data) in enumerate(All_ohlcvs)
        for ticker in keys(data)
            result_dict[ticker] = [result_dict[ticker] ; data[ticker]]
        end
    end
    for ticker in keys(result_dict)
        for i in range(1, length(result_dict["ETHUSDT"]) - length(result_dict[ticker]) )
            result_dict[ticker] = [[[result_dict["ETHUSDT"][i][1], -1, -1, -1, -1]] ; result_dict[ticker]]
        end
    end
    return result_dict, ticker_lists
end

function log_maker(All_ohlcvs, All_HA, All_ubb, All_mbb, All_lbb)
    slippage = 0.9982 * 0.9982
    buy_sell_log = []
    

    for ticker in keys(All_ohlcvs)
        long_entry_price = 0
        short_entry_price = 0
        long_entry_time_buffer = []
        short_entry_time_buffer = []

        canlde_count = 0


        for i in range(3, length(All_ohlcvs[ticker])-1)
            target_candle = All_HA[ticker][i-2:i]
            d_3 = target_candle[1]
            d_2 = target_candle[2]
            d_1 = target_candle[3]

            
            if long_entry_price == 0
                # if d_3[2] > d_3[5] && d_2[2] < d_2[5] && d_1[2] < d_1[5] && All_ohlcvs[ticker][i][5] < All_mbb[ticker][i]
                # if d_3[2] > d_3[5] && d_2[2] < d_2[5] && d_1[2] < d_1[5] && All_ohlcvs[ticker][i][5] < 0.491*(All_mbb[ticker][i]+All_lbb[ticker][i])
                # if d_3[2] > d_3[5] && d_2[2] > d_2[5] && d_1[2] < d_1[5] && All_ohlcvs[ticker][i][5] < 0.4897*(All_mbb[ticker][i]+All_lbb[ticker][i]) # && All_ohlcvs[ticker][i][5] < All_mbb[ticker][i]
                # if d_1[2] < d_1[5] && All_ohlcvs[ticker][i][5] < 0.489*(All_mbb[ticker][i]+All_lbb[ticker][i])   # && All_ohlcvs[ticker][i][5] < All_mbb[ticker][i]
                if d_3[2] > d_3[5] && d_2[2] < d_2[5] && d_1[2] < d_1[5] && All_ohlcvs[ticker][i][5] > All_mbb[ticker][i] #&& All_ohlcvs[ticker][i][5] < 0.5*(All_mbb[ticker][i]+All_lbb[ticker][i])
                    long_entry_price = All_ohlcvs[ticker][i+1][2]
                    push!(long_entry_time_buffer, "$(unix2datetime(All_ohlcvs[ticker][i+1][1]/1000))")
                    continue
                end
            else
                
                # if All_ubb[ticker][i] < All_ohlcvs[ticker][i][5] || All_lbb[ticker][i] > All_ohlcvs[ticker][i][5]
                # if All_ubb[ticker][i] < All_ohlcvs[ticker][i][5] 
                # if All_mbb[ticker][i] > All_ohlcvs[ticker][i][5] 
                
                if All_lbb[ticker][i] > All_ohlcvs[ticker][i][5]

                    exit_price = All_ohlcvs[ticker][i][5]
                    earning = 100(exit_price/long_entry_price*slippage-1)
                    push!(buy_sell_log, earning)
                    exit_time = "$(unix2datetime(All_ohlcvs[ticker][i][1]/1000))"
                    text = "L entry:$(long_entry_time_buffer[end])/exit=$(exit_time)/$ticker/long:$(long_entry_price)/exit:$(exit_price)/earn:$(convert(Float16,earning))"
                    println(text)
                    empty!(long_entry_time_buffer) 
                    long_entry_price = 0
                end
            end
        end


        if long_entry_price !=0
            exit_price = All_ohlcvs[ticker][end][5]
            earning = 100(exit_price/long_entry_price*slippage-1)
            push!(buy_sell_log, earning)
            exit_time = "$(unix2datetime(All_ohlcvs[ticker][end][1]/1000))"
            text = "S entry:$(long_entry_time_buffer[end])/exit=$(exit_time)/$ticker/long:$(long_entry_price)/exit:$(exit_price)/earn:$(convert(Float16,earning))"
            println(text)
            long_entry_price = 0
            canlde_count = 0
            
        end

    
    end

    get_performance(buy_sell_log, true, 100)
end



function get_data(All_ohlcvs)
    All_HA = Dict()
    All_ubb = Dict()
    All_mbb = Dict()
    All_lbb = Dict()


    for ticker in keys(All_ohlcvs)
        ticker_HA = get_HA_ohlcv(All_ohlcvs[ticker])
        ubb, mbb, lbb = get_bollinger(All_ohlcvs[ticker], 20, 3)
        # ubb, mbb, lbb = get_bollinger(All_ohlcvs[ticker], 10, 1.5)
        # ubb, mbb, lbb = get_bollinger(All_ohlcvs[ticker], 40, 3)
        # ubb, mbb, lbb = get_bollinger(All_ohlcvs[ticker], 40, 1.9)



        All_ohlcvs[ticker] = All_ohlcvs[ticker][end-22900:end]
        All_HA[ticker] = ticker_HA[end-22900:end]
        All_ubb[ticker] = ubb[end-22900:end]
        All_mbb[ticker] = mbb[end-22900:end]
        All_lbb[ticker] = lbb[end-22900:end]


        fix_index = 0
        for (i, value) in enumerate(All_lbb[ticker]) 
            if value != -1
                fix_index = i + 100
                break
            end
        end
        for i in range(1, fix_index)
            All_HA[ticker][i] = [All_HA[ticker][i][1], -1, -1, -1, -1]
            All_ubb[ticker][i] = -1
            All_mbb[ticker][i] = -1
            All_lbb[ticker][i] = -1
        end
    end
    return All_ohlcvs, All_HA, All_ubb, All_mbb, All_lbb
end



# All_ohlcvs, ticker_lists = get_all_ohlcv()

temp_ohlcvs, All_HA, All_ubb, All_mbb, All_lbb = get_data(deepcopy(All_ohlcvs))

log_maker(temp_ohlcvs, All_HA, All_ubb, All_mbb, All_lbb)



#=
for temp_ticker in keys(All_ohlcvs)

    temp_ohlcvs = Dict(temp_ticker=>All_ohlcvs[temp_ticker])
    temp_HA = Dict(temp_ticker=>All_HA[temp_ticker])
    temp_ubb = Dict(temp_ticker=>All_ubb[temp_ticker])
    temp_mbb = Dict(temp_ticker=>All_mbb[temp_ticker])
    temp_lbb = Dict(temp_ticker=>All_lbb[temp_ticker])


    log_maker(temp_ohlcvs, temp_HA, temp_ubb, temp_mbb, temp_lbb)

    println(temp_ticker)
    readline()
end
=#


#=
for (i, ohlcv) in enumerate(All_ohlcvs["ETHUSDT"]) 
    if i % 24 == 0
        readline()
    end
    println("$(unix2datetime(ohlcv[1]/1000))")
end
=#

    