include("../../utils/utils.jl")
using HTTP
import JSON
using Statistics
using Dates
using Telegram, Telegram.API
using Nettle
using Formatting
using Logging
using Base.Filesystem



function log_maker(days, ohlcv_law, param, weight)
    for day in days:-1:1
        if length(ohlcv_law) - day - param + 1 < 1
            continue
        end

        ohlcv = ohlcv_law[end-day-param+1:end-day+1]
        y_min = minimum(map(x -> x[4], ohlcv[1:end-1]))
        max_tr = maximum(map(x -> abs(x[2] - x[5]), ohlcv[1:end-1]))
        # entry_price = y_min - max_tr * (weight + momentum)
        entry_price = y_min - max_tr * weight
        if ohlcv[end][4] < entry_price
            if entry_price < 10^-5
                continue
            end
            earning = 100(ohlcv[end][5] / entry_price * slippage - 1)
            push!(result, earning)
        end
    end
    return nothing
end



function get_performance(file_name::String, trade_log::Vector{Float64}, verbose, money=1)
    # io = open(file_name, "a")
    # logger = SimpleLogger(io)
    # global_logger(logger)

    if length(trade_log) == 0
        return 0, 0
        elseabout:blank#blocked
    end

    win = [value for value in trade_log if value > 0]
    lose = [value for value in trade_log if value < 0]

    risk_free = 0.038 / 365
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
    win_rate = 100 * length(win) / length(trade_log)
    sharp = (avg - risk_free) / std_value
    sortino = (avg - risk_free) / std_lose
    if avg_w_l_ratio < 0
        # total_perform = "Nan"
        total_perform = 0.0
    else
        total_perform = shortest_distance(avg_w_l_ratio, win_count / length(trade_log))
    end
    size = (avg - risk_free) / std_value^2
    if verbose == true

        @info("총 거래 수 : $(length(trade_log))")
        @info("수익 거래 수 : $(win_count)")
        @info("손실 거래 수 : $(length(lose))")
        @info("평균 손익률 : $(avg)%")
        @info("평균 수익률 : $(avg_win)%")
        @info("평균 손실률 : $(avg_lose)%")
        @info("평균 손익비 : $(avg_w_l_ratio)")
        @info("승 률 : $(win_rate)%")
        @info("포지션 사이징 : $(size)")
        @info("sharp ratio : $(sharp)%")
        @info("sortino ratio : $(sortino)")
        if length(lose) != 0
            @info("최대 손실 : $(minimum(lose))%")
        end
        @info(sum(trade_log) * money * 0.01)
        @info("$(total_perform)\n")
        @info("")
    end
    # flush(io)
    #close(io)
    return total_perform, length(trade_log)
end







function ohlcv_init(price_ch_interval, interval, limit, time_flag)
    All_ohlcvs = []
    ticker_lists = []

    for i in range(1, 24)
        if time_flag == 52 && i == 19
            break
        end

        All_ohlcv = Dict()
        del_list = []

        btc_ohlcv = fetch_ohlcv("BTCUSDT", "1d", "1000")

        start_time = string(btc_ohlcv[end-time_flag*i][1])
        end_time = string(btc_ohlcv[end-time_flag*(i-1)][1])

        global ticker_list
        for ticker in ticker_list
            ohlcv = fetch_ohlcv(ticker, interval, string(limit + price_ch_interval), start_time, end_time)
            All_ohlcv[ticker] = ohlcv
            sleep(0.09)
        end
        ticker_list = setdiff!(ticker_list, del_list)
        push!(All_ohlcvs, All_ohlcv)
        push!(ticker_lists, ticker_list)

    end
    return All_ohlcvs, ticker_lists
end


# need update
ticker_list = get_tickers_listed_over_1year()

function get_perfom_by_ticker(i::Int64, j, All_ohlcvs, interval, time_frame)
    result_dict = Dict()
    for ticker in ticker_list
        file_name = "$(ticker)_$(time_frame)_$(i)_$(j)"
        io = open("./$(file_name).txt", "a")
        logger = SimpleLogger(io)
        global_logger(logger)

        for k in range(1, 24)
            if time_frame == "2h" && k == 19
                break
            end
            log_maker(interval + i, All_ohlcvs[k][ticker], i, j)
        end
        total_perform, _ = get_performance("./$(file_name).txt", result, false, 200)
        result_dict[ticker] = total_perform
        if length(result) < 1000
            log_post_processing("./$(file_name).txt")
        end
        empty!(result)
        log_post_processing("./$(file_name).txt")
    end

    # println("$(time_frame) : $(rank_by_val(result_dict)) \n\n")

    io = open("./result/$(time_frame)_result.txt", "a")
    logger = SimpleLogger(io)
    global_logger(logger)
    @info("$(i) : $j \n")
    @info("$(time_frame) : $(rank_by_val(result_dict)) \n\n")
    flush(io)
    log_post_processing("./result/$(time_frame)_result.txt")

    return [k for (k, v) in rank_by_val(result_dict)]
end




function sort_by_val(dict)
    return sort(collect(dict), by=x -> x[2], rev=true)
end

function rank_by_val(dict)
    sorted = sort_by_val(dict)
    return sorted[1:70]
end


const result = Vector{Float64}([])
const slippage = 0.9982 * 0.9982




function get_final_txt_val(time_frame)
    i = 0
    j = 0
    files = readdir(time_frame)[1]
    for var in split(files, "_")
        if var == "" || var == time_frame
            continue
        end
        if i == 0
            i = var
        else
            j = split(var, ".txt")[1]
        end
    end
    return parse(Int64, i), parse(Float64, j)
end


function get_final_txt_vals(time_frame)
    result = []
    i = 0
    j = 0
    files = readdir(time_frame)

    for file in files
        var = split(file, "_")
        i = var[end-1]
        j = split(var[end], ".txt")[1]
        push!(result, [i, parse(Float64, j)])
    end
    return result
end






# time_frame = "1h"
# All_ohlcvs, ticker_lists = ohlcv_init(35, time_frame, 960, 41)
# i_j_vars = get_final_txt_vals(time_frame)
# for i_j_var in i_j_vars
#     i::Int64 = parse(Int64, i_j_var[1])
#     j::Float64 = i_j_var[end]
#     println(i_j_var)
#     _1h_reuslt = get_perfom_by_ticker(i, j, All_ohlcvs, 960, time_frame)
#     run(`sh -c "rm *.txt"`)
# end







# time_frame = "2h"
# All_ohlcvs, ticker_lists = ohlcv_init(35, time_frame, 605, 52)
# i_j_vars = get_final_txt_vals(time_frame)
# for i_j_var in i_j_vars
#     i::Int64 = parse(Int64, i_j_var[1])
#     j::Float64 = i_j_var[end]
#     println(i_j_var)
#     _2h_reuslt = get_perfom_by_ticker(i, j, All_ohlcvs, 605, time_frame)
#     run(`sh -c "rm *.txt"`)
# end



time_frame = "4h"
All_ohlcvs, ticker_lists = ohlcv_init(35, time_frame, 240, 41)
i_j_vars = get_final_txt_vals(time_frame)
for i_j_var in i_j_vars
    i::Int64 = parse(Int64, i_j_var[1])
    j::Float64 = i_j_var[end]
    println(i_j_var)
    _4h_reuslt = get_perfom_by_ticker(i, j, All_ohlcvs, 240, time_frame)
    run(`sh -c "rm *.txt"`)
end


exit()

time_frame = "6h"
All_ohlcvs, ticker_lists = ohlcv_init(35, time_frame, 160, 40)
i_j_vars = get_final_txt_vals(time_frame)
for i_j_var in i_j_vars
    i::Int64 = parse(Int64, i_j_var[1])
    j::Float64 = i_j_var[end]
    println(i_j_var)
    _6h_reuslt = get_perfom_by_ticker(i, j, All_ohlcvs, 160, time_frame)
    run(`sh -c "rm *.txt"`)
end



time_frame = "8h"
All_ohlcvs, ticker_lists = ohlcv_init(35, time_frame, 123, 41)
i_j_vars = get_final_txt_vals(time_frame)
for i_j_var in i_j_vars
    i::Int64 = parse(Int64, i_j_var[1])
    j::Float64 = i_j_var[end]
    println(i_j_var)
    _8h_reuslt = get_perfom_by_ticker(i, j, All_ohlcvs, 123, time_frame)
    run(`sh -c "rm *.txt"`)
end

time_frame = "12h"
All_ohlcvs, ticker_lists = ohlcv_init(35, time_frame, 80, 40)
i_j_vars = get_final_txt_vals(time_frame)
for i_j_var in i_j_vars
    i::Int64 = parse(Int64, i_j_var[1])
    j::Float64 = i_j_var[end]
    println(i_j_var)
    _12h_reuslt = get_perfom_by_ticker(i, j, All_ohlcvs, 80, time_frame)
    run(`sh -c "rm *.txt"`)
end



println(_1h_reuslt)
println(_2h_reuslt)
println(_4h_reuslt)
println(_6h_reuslt)
println(_8h_reuslt)
println(_12h_reuslt)



