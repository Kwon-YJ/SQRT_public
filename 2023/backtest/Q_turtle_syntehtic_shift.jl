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

@inbounds function log_maker(limit::Int64, All_ohlcv::Dict{Any, Any}, ticker_list::Vector{Any})
    total_buy_sell_log = Vector{Float64}([])
    # for day::Int64 in limit-2:-1:0
    for day::Int64 in limit-2:-1:1
        println("day : $(day)")  

        println(All_ohlcv["XRPUSDT"][end-day][1])


        #println("계속 하려면 Enter 버튼을 입력")
        #temp_ = readline()


        buy_sell_log = Vector{Float64}([])

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

            max_tr = Vector{Float64}([])
            for val::Int64 = 2:length(data_for_calc)
                push!(max_tr, abs(abs(data_for_calc[val-1]) - abs(data_for_calc[val])))
            end
            max_tr = maximum(max_tr)


            # weight = 20
            weight = 30
            
            
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

                #@fastmath entry_time = string(unix2datetime((All_ohlcv[ticker1][end-day-1][idx][1][1]+3600000*9)/1000))[6:end]
                
                # text = "$(entry_time[1:end-2])/L:$(ticker1[1:end-4]) $(Float16(long_entry_price))~$(Float16(long_exit_price))/S:$(ticker2[1:end-4]) $(Float16(short_entry_price))~$(Float16(short_exit_price)) $(Float16(long_earning)) $(Float16(short_earning)))"
                
                # println(text)
                
                #=
                if long_earning < -5 && short_earning < -5

                    long_entry_price = All_ohlcv[ticker1][end-day+1][idx][2]
                    long_exit_price = All_ohlcv[ticker1][end-day+1][end][2]

                    short_entry_price = All_ohlcv[ticker2][end-day+1][idx][2]
                    short_exit_price = All_ohlcv[ticker2][end-day+1][end][2]

                    shifted_long_earning = 100(long_exit_price / long_entry_price * slippage - 1)
                    shifted_short_earning = -100(short_exit_price / short_entry_price / slippage - 1)

                    push!(total_buy_sell_log, shifted_long_earning)
                    push!(total_buy_sell_log, shifted_short_earning)
                    push!(buy_sell_log, shifted_long_earning)
                    push!(buy_sell_log, shifted_short_earning)
                end
                =#


                if long_earning < -5
                    short_entry_price = All_ohlcv[ticker1][end-day+1][idx][2]
                    short_exit_price = All_ohlcv[ticker1][end-day+1][end][2]
                    shifted_short_earning = -100(short_exit_price / short_entry_price / slippage - 1)
                    push!(total_buy_sell_log, shifted_short_earning)
                    push!(buy_sell_log, shifted_short_earning)
                end

                if long_earning > 5
                    long_entry_price = All_ohlcv[ticker1][end-day+1][idx][2]
                    long_exit_price = All_ohlcv[ticker1][end-day+1][end][2]
                    shifted_long_earning = 100(long_exit_price / long_entry_price * slippage - 1)
                    push!(total_buy_sell_log, shifted_long_earning)
                    push!(buy_sell_log, shifted_long_earning)

                end
                
                

                if short_earning < -5

                    long_entry_price = All_ohlcv[ticker2][end-day+1][idx][2]
                    long_exit_price = All_ohlcv[ticker2][end-day+1][end][2]


                    shifted_long_earning = 100(long_exit_price / long_entry_price * slippage - 1)
                    

                    push!(total_buy_sell_log, shifted_long_earning)
                    
                    push!(buy_sell_log, shifted_long_earning)
                    
                end

                if short_earning > 5

                    short_entry_price = All_ohlcv[ticker2][end-day+1][idx][2]
                    short_exit_price = All_ohlcv[ticker2][end-day+1][end][2]

                    
                    shifted_short_earning = -100(short_exit_price / short_entry_price / slippage - 1)

                    
                    push!(total_buy_sell_log, shifted_short_earning)
                    
                    push!(buy_sell_log, shifted_short_earning)
                end








            end
        end
        get_performance(buy_sell_log, true, 35)
    end
    get_performance(total_buy_sell_log, true, 35)
    return nothing
end

@inbounds function main()   

    
    


    ticker_list =[key for (key,value) in All_ohlcv]
    syntehtic_ticker_list = nP2(ticker_list)
    limit = length(All_ohlcv["BNBUSDT"])
    println(length(syntehtic_ticker_list))
    println(limit)
    log_maker(limit, All_ohlcv, syntehtic_ticker_list)

end

const slippage = 0.9982 * 0.9982



@time main()


#println("load start")
#All_ohlcv = @time load(".//test.pkl")
#All_ohlcv = @time load(".//11_9__12_29.pkl")
#println("load finish")

# main()


