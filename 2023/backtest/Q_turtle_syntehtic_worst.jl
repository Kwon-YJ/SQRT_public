using HTTP
import JSON
using Dates
using Plots
using Pickle
using Random
using Statistics
using Base.Threads
include("./../../2022/julia_test/utils.jl")


function get_spread(first_ohlcv::Vector{Any}, second_ohlcv::Vector{Any})
    first_price = map(x->x[2], first_ohlcv)
    second_price = map(x->x[2], second_ohlcv)
    first_price_for_calc = first_price[1:1200]
    second_price_for_calc = second_price[1:1200]
    first_avg = mean(first_price_for_calc)
    second_avg = mean(second_price_for_calc)
    first_std = std(first_price_for_calc, corrected=false)    
    second_std = std(second_price_for_calc, corrected=false)
    first_norm = map(x -> (x-first_avg)/first_std, first_price)
    second_norm = map(x -> (x-second_avg)/second_std, second_price)
    -(first_norm,second_norm)
end

function get_max_tr(data_for_calc)
    data_for_calc = [abs(x) for x in data_for_calc]
    @fastmath max_tr = maximum(abs(data_for_calc[val-1] - data_for_calc[val]) for val = 2:length(data_for_calc))
end

@inbounds function log_maker(limit::Int64, All_ohlcv::Dict{Any, Any}, ticker_list::Vector{Any})
    total_buy_sell_log = Vector{Float64}([])


    shuffle!(ticker_list)

    for day::Int64 in limit-2:-1:0
        println("day : $(day)")  

        println(All_ohlcv["XRPUSDT"][end-day][1])


        #println("계속 하려면 Enter 버튼을 입력")
        #temp_ = readline()


        buy_sell_log = Vector{Float64}([])
        daily_log = []
        
        @inbounds for (ticker1::String, ticker2::String) in ticker_list
            first_ohlcv = All_ohlcv[ticker1]
            first_ohlcv = [first_ohlcv[end-day-1];first_ohlcv[end-day]]
            second_ohlcv = All_ohlcv[ticker2]
            second_ohlcv = [second_ohlcv[end-day-1];second_ohlcv[end-day]]

            len_of_data = length(first_ohlcv)
            spread = get_spread(first_ohlcv[240:end], second_ohlcv[240:end]) # first, k=1441, k-1200=241~end, len(k)=2639, for_calc(k)=241~1440,
            
            data_for_calc  = spread[1:1200]
            data_for_trade = spread[1201:end]

            y_min = minimum( data_for_calc )

            max_tr = get_max_tr(data_for_calc)

            # weight = 25

            weight = 34

            entry_price = y_min - max_tr * weight
            low_trade = minimum(data_for_trade)

            if low_trade < entry_price
                idx = 0
                @inbounds for (i::Int64, data::Float64) in enumerate(data_for_trade)
                    if data < entry_price
                        idx = i
                        break
                    end
                end
                if idx ==1441
                    idx = 1440
                end

                long_entry_price = All_ohlcv[ticker1][end-day][idx][2]
                long_exit_price = All_ohlcv[ticker1][end-day][end][2]
                @fastmath long_earning = 100(long_exit_price / long_entry_price * slippage - 1)

                short_entry_price = All_ohlcv[ticker2][end-day][idx][2]
                short_exit_price = All_ohlcv[ticker2][end-day][end][2]
                @fastmath short_earning = -100(short_exit_price / short_entry_price / slippage - 1)

                @fastmath entry_time = string(unix2datetime((All_ohlcv[ticker1][end-day-1][idx][1][1]+3600000*9)/1000))[6:end]
                
                #text = "$(entry_time[1:end-2])/L:$(ticker1[1:end-4]) $(Float16(long_entry_price))~$(Float16(long_exit_price))/S:$(ticker2[1:end-4]) $(Float16(short_entry_price))~$(Float16(short_exit_price)) $(Float16(long_earning)) $(Float16(short_earning)))"
                #println(text)

                trade_data = [entry_time[1:end-2], ticker1, long_entry_price, long_exit_price, ticker2, short_entry_price, short_exit_price, long_earning, short_earning]
                push!(daily_log, trade_data)
            end
        end

        get_total_result(daily_log)
        global total_result
        

        for data in total_result
            data = data[1]
            text = " $(data[1])/L:$(data[2][1:end-4]) $(Float16(data[3]))~$(Float16(data[4]))/S:$(data[5][1:end-4]) $(Float16(data[6]))~$(Float16(data[7])) $(Float16(data[8])) $(Float16(data[9])))"
            println(text)


            push!(total_buy_sell_log, data[end])
            push!(total_buy_sell_log, data[end-1])
            push!(buy_sell_log, data[end])
            push!(buy_sell_log, data[end-1])
        end

        get_performance(buy_sell_log, true, 450)
        
        empty!(total_result)
    end
    get_performance(total_buy_sell_log, true, 450)
    return nothing
end


function get_total_result(daily_log)
    if length(daily_log) == 0
        return nothing
    end
    global total_result

    min_earn = minimum([data[end-1:end] for data in daily_log])
    min_data = [data for data in daily_log if min_earn == data[end-1:end]]
    push!(total_result, min_data)
        
    next_result = [data for data in daily_log if !(min_data[1][2] in data) && !(min_data[1][5] in data)]
    if length(next_result) == 0
        return nothing
    end
    get_total_result(next_result)
end






@inbounds function main()   

    
    println("load start")
    All_ohlcv = @time load(".//test.pkl")
    println("load finish")

    

    ticker_list =[key for (key,value) in All_ohlcv]
    syntehtic_ticker_list = nP2(ticker_list)
    limit = length(All_ohlcv["BNBUSDT"])
    println(length(syntehtic_ticker_list))
    println(limit)
    log_maker(limit, All_ohlcv, syntehtic_ticker_list)

end

const slippage = 0.9982 * 0.9982

total_result = []

@time main()



