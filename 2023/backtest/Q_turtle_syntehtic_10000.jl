using HTTP
import JSON
using Dates
using Plots
using Pickle
using Random
using Statistics
using Base.Threads
include("./../../2022/julia_test/utils.jl")

using Profile

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


function get_performance_simplification(trade_log, money = 1)
    return sum(trade_log) * money * 0.01
end

function get_max_tr(data_for_calc)
    data_for_calc = [abs(x) for x in data_for_calc]
    @fastmath max_tr = maximum(abs(data_for_calc[val-1] - data_for_calc[val]) for val = 2:length(data_for_calc))
end

@inbounds function log_maker(limit::Int64, All_ohlcv::Dict{Any, Any}, ticker_list::Vector{Any})
    # total_buy_sell_log = Vector{Float64}([])
    for day::Int64 in limit-2:-1:0
        println("day : $(day)")  
        println(All_ohlcv["XRPUSDT"][end-day][1])

        # _10000_ticker_list = []
        _10000_buy_sell_log = []

        # for i in range(1, 100)
        for i in range(1, 50)
            println(i)
            shuffle!(ticker_list)
            # push!(_10000_ticker_list, ticker_list)

            _1_buy_sell_log = Vector{Any}([])
            
            elastic::Float64 = 35
            elastic_count::Int64 = 0

            # Threads.@threads for (ticker1::String, ticker2::String) in ticker_list  
            for (ticker1::String, ticker2::String) in ticker_list
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
                weight = 25 + elastic
                entry_price = y_min - max_tr * weight
                low_trade = minimum(data_for_trade)

                if low_trade < entry_price
                    if elastic_count > 18
                        elastic += 5    
                    elseif elastic_count > 8
                        elastic += 2.5
                    else
                        elastic += 1
                    end
                    elastic_count += 1    
                            
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
                    @fastmath short_earning = -100(short_exit_price / short_entry_price * slippage - 1)
                    
                    push!(_1_buy_sell_log, long_earning)
                    push!(_1_buy_sell_log, short_earning)

                end
            end
            push!(_10000_buy_sell_log, _1_buy_sell_log)
        end

        println(typeof(_10000_buy_sell_log))

        _10000_result = map(x -> get_performance_simplification(x), _10000_buy_sell_log)

        min_result = minimum(_10000_result)

        for (i, result) in enumerate(_10000_result)
            if result == min_result
                get_performance(_10000_buy_sell_log[i], true, 35)
            end
        end
    end
    return nothing
end



@inbounds function main()   
    println("load start")
    # All_ohlcv = @time load("./test.pkl")
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



@time main()

