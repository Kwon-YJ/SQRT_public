include("./../../2022/julia_test/utils.jl")
using HTTP
import JSON
using Statistics
using Dates

using Nettle
using Formatting
using Logging


result = Vector{Float64}([])

function log_maker(days, All_ohlcv, ticker_list, param)
    total_buy_sell_log = []
    buy_sell_log = []
    # slippage = 0.9982 * 0.9982
    slippage = 0.9994 * 0.9994

    std_len = length(All_ohlcv["ETHUSDT"])
    for day in days:-1:1

        
        for ticker in ticker_list
            try

                ohlcv = All_ohlcv[ticker][end-day-param+6:end-day+1]
                



                #if ohlcv[end-2][2] < ohlcv[end-2][5]
                #    continue
                #end
                
                entry_price = ohlcv[end-1][2] * 1.085

                exit_price = ohlcv[end-1][2] * 1.99999999

                #println(entry_price)
                #error()

                #=
                if ohlcv[end-1][3] > entry_price
                    earning = 100(ohlcv[end-1][5]/entry_price*slippage-1)
                    
                    text = "$ticker / long : $(convert(Float16,entry_price)) / exit : $(ohlcv[end][5]) / time : $(unix2datetime( (ohlcv[end-1][1]+3600000*33) /1000)) /  earn : $(convert(Float16,earning))"
                    #println(text)
                    push!(buy_sell_log, earning)
                    push!(total_buy_sell_log, earning)
                    global result
                    push!(result, earning)
                end
                =#


                
                if ohlcv[end-1][3] > entry_price && ohlcv[end-1][3] > exit_price
                    earning = 100(exit_price/entry_price*slippage-1)
                    text = "$ticker / long : $(convert(Float16,entry_price)) / exit : $(ohlcv[end][5]) / time : $(unix2datetime( (ohlcv[end-1][1]+3600000*33) /1000)) /  earn : $(convert(Float16,earning))"
                    #println(text)
                    push!(buy_sell_log, earning)
                    push!(total_buy_sell_log, earning)
                    global result
                    push!(result, earning)

                elseif ohlcv[end-1][3] > entry_price && ohlcv[end-1][3] < exit_price

                    earning = 100(ohlcv[end-1][5]/entry_price*slippage-1)
                    text = "$ticker / long : $(convert(Float16,entry_price)) / exit : $(ohlcv[end][5]) / time : $(unix2datetime( (ohlcv[end-1][1]+3600000*33) /1000)) /  earn : $(convert(Float16,earning))"
                    #println(text)
                    push!(buy_sell_log, earning)
                    push!(total_buy_sell_log, earning)
                    global result
                    push!(result, earning)
                

                end
                


            catch
                # continue
            end
        end
        #get_performance_local(buy_sell_log, true, 100)
        empty!(buy_sell_log)
    end
    get_performance_local(total_buy_sell_log, true, 100)
    return nothing
end



function get_performance_local(trade_log, verbose, money = 1)
    if length(trade_log) == 0
        return 0, 0
    else
        trade_count = length(trade_log)
    end


    win = [value for value in trade_log if value > 0]
    lose = [value for value in trade_log if value < 0]

    risk_free = 0.038/365
    avg = mean(trade_log)

    if length(lose) == 0
        avg_lose = 10^-6
        std_lose = 10^-6
    else
        avg_lose = mean(lose)
        std_lose = std(lose, corrected=false)
    end

    if length(win) == 0
        avg_win = 10^-6
        win_count = 0
    else
        avg_win = mean(win)
        win_count = length(win)
    end
    
    std_value = std(trade_log, corrected=false)
    avg_w_l_ratio = -1 * avg_win / avg_lose
    win_rate = 100*length(win)/length(trade_log)
    sharp = (avg - risk_free) / std_value
    sortino = (avg - risk_free) / std_lose
    if avg_w_l_ratio < 0
        total_perform = "Nan"
    else
        total_perform = shortest_distance(avg_w_l_ratio, win_count / trade_count)
    end
    size = (avg - risk_free) / std_value^2
    if verbose == true

        println("총 거래 수 : $(trade_count)")
        println("수익 거래 수 : $(win_count)")
        println("손실 거래 수 : $(length(lose))")
        println("평균 손익률 : $(avg)%")
        println("평균 수익률 : $(avg_win)%")
        println("평균 손실률 : $(avg_lose)%")
        println("평균 손익비 : $(avg_w_l_ratio)")
        println("승 률 : $(win_rate)%")
        println("포지션 사이징 : $(size)")
        println("sharp ratio : $(sharp)%")
        println("sortino ratio : $(sortino)")
        if length(lose) != 0
            println("최대 손실 : $(minimum(lose))%")
        end
        println(sum(trade_log) * money * 0.01)
        println("$(total_perform)\n")
        println("")
    end
    return total_perform, trade_count
end



i = 6
for k in range(1,24)
    log_maker(80+i, All_ohlcvs[k], ticker_lists[k], i)
end

get_performance(result, true, 100)