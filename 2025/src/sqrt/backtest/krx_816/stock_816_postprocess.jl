using Statistics
using DataFrames
using CSV
using Dates

include("../../utils/utils.jl")


function csv_init(input_data, file_name)


    df = DataFrame(A=[input_data[1]], B=[input_data[2]], C=[input_data[3]], D=[input_data[4]])
    # CSV.write(file_name, df, append=true)
    try
        CSV.write("./post_result/" * file_name, df, append=false)
    catch
        return nothing
    end
end


function shortest_distance_(ratio, winrate)
    lins = [i / 10000 for i in 0:100000]
    y = [-log(0.99) / (log(1 + 0.01 * i) - log(0.99)) for i in lins]
    least_distance = 100
    for i in 1:100000
        dx = lins[i] - ratio
        dy = y[i] - winrate
        distance = sqrt(dx^2 + dy^2)
        if distance < least_distance
            least_distance = distance
        end
    end
    base_line = -log(0.99) / (log(1 + 0.01 * ratio) - log(0.99))
    if winrate > base_line
        return least_distance
    else
        return -least_distance
    end
end


function get_performance_(trade_log)
    if length(trade_log) == 0
        return 0
    else
        trade_count = length(trade_log)
    end
    win = []
    lose = []
    for value in trade_log
        if value > 0
            push!(win, value)
        else
            push!(lose, value)
        end
    end

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

    avg_w_l_ratio = -1 * avg_win / avg_lose
    if avg_w_l_ratio < 0
        total_perform = "Nan"
    else
        total_perform = shortest_distance_(avg_w_l_ratio, win_count / trade_count)
    end
    return total_perform
end


function load_data(data_dir="./../data/", file_name="E6_1d.CSV")
    csv_data = CSV.read(data_dir * file_name, DataFrame)
    return csv_data
    cleaned_data = filter(row -> !any(x -> ismissing(x) || (typeof(x) <: AbstractFloat && isnan(x)), row), csv_data)
    return cleaned_data
end










@inbounds function ema(data::Vector{T}, period::Int) where {T}
    alpha = 2 / (period + 1)
    ema_values = similar(data, T)
    sma = sum(@view data[1:period]) / period
    ema_values[period] = sma
    @fastmath @simd for i in (period+1):length(data)
        ema_values[i] = (data[i] - ema_values[i-1]) * alpha + ema_values[i-1]
    end
    return ema_values
end





function replace_missing_with_zero(nested_array)
    # 배열의 각 요소에 대해 함수 적용
    result = map(sub_array -> map(x -> ismissing(x) || (typeof(x) <: AbstractFloat && isnan(x)) ? 0 : x, sub_array), nested_array)
    return result
end



function mkdir_exist_ok(dir_path)
    if isdir(dir_path) != true
        mkdir(dir_path)
    end
end

mkdir_exist_ok("./post_result")

data_dir = "./result/"
for file_name = readdir(data_dir)
    println(file_name)
    ohlc = 0
    try
        ohlc = load_data(data_dir, file_name)
    catch
        println("load_fail $(file_name)")
        continue
    end



    ohlc_col = [ohlc[!, col] for col in names(ohlc)]
    # ohlc_col = replace_missing_with_zero(ohlc_col)

    param_1 = ohlc_col[1]
    param_2 = ohlc_col[2]
    trade_count = ohlc_col[3]
    distance = ohlc_col[4]




    trade_count_sort = sort(trade_count, rev=true) # 내림차순으로 정렬

    if length(trade_count_sort) <= 1
        continue
    end

    top_10per_var = trade_count_sort[1:ceil(Int, length(trade_count_sort) * 0.1)][1]


    ohlc_row = [Vector(row) for row in eachrow(ohlc)]
    # ohlc_row = replace_missing_with_zero(ohlc_row)



    step_1_result = []
    for row in ohlc_row
        try
            if row[3] >= top_10per_var
                push!(step_1_result, row)
            end
        catch
            continue
        end
    end



    step_2_max = maximum(map(x -> x[4], step_1_result))

    step_2_result = []
    try
        step_2_result = [x for x in step_1_result if x[4] == step_2_max][1]
    catch
        step_2_result = ohlc_row[1]
        println("$(file_name) has only NaN")
    end

    csv_init(step_2_result, file_name)


end