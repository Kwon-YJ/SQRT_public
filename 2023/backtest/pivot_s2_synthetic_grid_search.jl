using HTTP
import JSON
using Statistics
using Dates
using Pickle
include("./../../2022/julia_test/utils.jl")
using Random
using Plots


function get_spread(first_ohlcv::Vector{Any}, second_ohlcv::Vector{Any})
    first_price = map(x->x[2], first_ohlcv)
    second_price = map(x->x[2], second_ohlcv)
    first_price_for_calc = first_price[1:1440]
    second_price_for_calc = second_price[1:1440]
    first_avg = mean(first_price_for_calc)
    second_avg = mean(second_price_for_calc)
    first_std = std(first_price_for_calc, corrected=false)    
    second_std = std(second_price_for_calc, corrected=false)
    first_norm = map(x -> (x-first_avg)/first_std, first_price)
    second_norm = map(x -> (x-second_avg)/second_std, second_price)
    -(first_norm,second_norm)
end


@inbounds function log_maker(limit::Int64, All_ohlcv::Dict{Any, Any}, ticker_list::Vector{Any}, weight::Float64)

end

@inbounds function main()   
    println("load start")
    All_ohlcv = @time load("./test.pkl")
    println("load finish")

    ticker_list =[key for (key,value) in All_ohlcv]
    syntehtic_ticker_list = nP2(ticker_list)
    limit = length(All_ohlcv["BNBUSDT"])

    result = Dict()
    idx = 1
    # for weight in range(1.95, 1.98, length=50) # 1번
    # for weight in range(1.3, 1.70, length=50) # 2번
    # for weight in range(1.2, 1.65, length=50) # 3번
    for weight in range(1.1, 1.5, length=25) # 4번
    # for weight in range(1.69, 1.85, length=50) # 5번
        println(idx)
        earn, count = log_maker(limit, All_ohlcv, syntehtic_ticker_list, weight)
        result[string(idx)] = [weight, earn, count]
        idx+=1
    end
    println(result)
    #for i in range(1,50)
    #    print(i, "  ");println(result[string(i)])
    #end
    telegram_send(string(result))
    return nothing
end


const slippage = 0.9982 * 0.9982

@time main()




