using CSV
using DataFrames
using Plots

using Statistics
using LinearAlgebra

include("../../utils/utils.jl")




function calculate_trend_score(data)
    n = length(data)
    if n < 2
        return 0.0 # Not enough data to determine trend
    end

    x = collect(1.0:n)
    y = data

    # Linear Regression
    # y = mx + b
    # m = (n * sum(xy) - sum(x) * sum(y)) / (n * sum(x^2) - sum(x)^2)
    # b = (sum(y) - m * sum(x)) / n

    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(x .* y)
    sum_x_sq = sum(x .^ 2)

    numerator = n * sum_xy - sum_x * sum_y
    denominator = n * sum_x_sq - sum_x^2

    if denominator == 0
        return 0.0 # Avoid division by zero if all x values are the same (shouldn't happen with 1:n)
    end

    slope = numerator / denominator

    # Pearson Correlation Coefficient
    # r = sum((x - mean(x)) .* (y - mean(y))) / (sqrt(sum((x - mean(x)).^2)) * sqrt(sum((y - mean(y)).^2)))

    mean_x = mean(x)
    mean_y = mean(y)

    diff_x = x .- mean_x
    diff_y = y .- mean_y

    numerator_corr = sum(diff_x .* diff_y)
    denominator_corr_x = sqrt(sum(diff_x .^ 2))
    denominator_corr_y = sqrt(sum(diff_y .^ 2))

    correlation = 0.0
    if denominator_corr_x != 0 && denominator_corr_y != 0
        correlation = numerator_corr / (denominator_corr_x * denominator_corr_y)
    end

    # Scoring Logic
    # A higher positive slope and a higher positive correlation indicate a stronger upward trend.
    # Normalize slope and correlation to a 0-1 range and combine them.
    # Slope can be very large or very small, so we need to scale it.
    # Correlation is already between -1 and 1.

    # For slope, we need a reference. Let's assume a reasonable range for 'good' upward trend.
    # This part is subjective and might need adjustment based on typical data ranges.
    # For now, let's consider a simple approach: scale slope based on its sign and magnitude.
    # If slope is negative, score is low. If positive, higher slope means higher score.

    # Let's try to map slope to a 0-1 range. This is tricky without knowing the expected range of slopes.
    # For now, let's use a sigmoid-like function or simply cap it.
    # A simple approach: if slope is positive, score is proportional to slope, capped at some max.
    # If slope is negative, score is 0.

    # Let's define a maximum reasonable slope for scoring purposes. This will need to be tuned.
    # For now, let's assume a slope of 100 (meaning, on average, each step increases by 100 units) is a very strong upward trend.
    # This is a placeholder and should be refined based on actual data characteristics.
    max_meaningful_slope = 100.0 # This needs to be determined based on data scale

    # Score based on slope (0 to 0.5 contribution)
    slope_score = 0.0
    if slope > 0
        slope_score = min(1.0, slope / max_meaningful_slope) * 0.5 # Max 0.5 contribution
    end

    # Score based on correlation (0 to 0.5 contribution)
    # We only care about positive correlation for 'upward' trend.
    correlation_score = 0.0
    if correlation > 0
        correlation_score = correlation * 0.5 # Max 0.5 contribution
    end

    total_score = (slope_score + correlation_score) * 100.0

    return round(total_score, digits=2)
end









function fig_result(initial_capital, returns)
    equity_curve = []
    returns = map(x -> x * 1 / 100 * initial_capital, returns)
    for earn in returns
        initial_capital += earn
        push!(equity_curve, initial_capital)
    end

    # step = (equity_curve[end] - 1000) / length(equity_curve)
    # ideal_vec = [1000 + x * step for x = 1:length(equity_curve)]

    # result = abs.(equity_curve - ideal_vec)
    # result = sum(result) / length(result)
    # result = round(result, digits=2)

    # println(equity_curve)
    # println("")
    # readline()

    result = calculate_trend_score(equity_curve)
    if result < 50
        return false
    end

    plot(
        equity_curve,
        xlabel="Period",
        ylabel="Equity (USD)",
        title="Equity Curve (Initial capital = \$$(round(Int, initial_capital))) $(result) ",
        legend=false,
        linewidth=2
    )
end







function rma(series::Vector{Float64}, len::Int)
    result = fill(NaN, size(series))
    if isempty(series) || len <= 0
        return result
    end

    alpha = 1.0 / len

    # Initialize the first non-NaN value
    first_valid_idx = findfirst(!isnan, series)
    if isnothing(first_valid_idx)
        return result
    end

    current_rma = series[first_valid_idx]
    result[first_valid_idx] = current_rma

    for i in (first_valid_idx+1):Base.length(series)
        if isnan(series[i])
            result[i] = NaN
        else
            current_rma = (series[i] * alpha) + (current_rma * (1 - alpha))
            result[i] = current_rma
        end
    end
    return result
end

# function rsi(close::Vector{Any}; length::Int=14, scalar::Float64=100.0, drift::Int=1, offset::Int=0)
function rsi(close; length::Int=14, scalar::Float64=100.0, drift::Int=1, offset::Int=0)
    if isempty(close) || length <= 0
        return fill(NaN, size(close))
    end

    # Calculate differences
    diffs = diff(close, dims=1)

    # Pad diffs to match original length for easier indexing
    padded_diffs = vcat([NaN], diffs)

    positive_diffs = [d > 0 ? d : 0.0 for d in padded_diffs]
    negative_diffs = [d < 0 ? abs(d) : 0.0 for d in padded_diffs]

    positive_avg = rma(positive_diffs, length)
    negative_avg = rma(negative_diffs, length)

    rsi_values = fill(NaN, size(close))
    for i in 1:Base.length(close)
        if !isnan(positive_avg[i]) && !isnan(negative_avg[i])
            if (positive_avg[i] + negative_avg[i]) == 0
                rsi_values[i] = scalar * 0.5 # Handle division by zero, assuming 50 when no movement
            else
                rsi_values[i] = scalar * positive_avg[i] / (positive_avg[i] + negative_avg[i])
            end
        end
    end

    # Handle offset (Julia's circshift is similar to pandas shift)
    if offset != 0
        rsi_values = circshift(rsi_values, offset)
        # Fill the shifted-in values with NaN, as pandas shift does
        if offset > 0
            rsi_values[1:offset] .= NaN
        elseif offset < 0
            rsi_values[end+offset+1:end] .= NaN
        end
    end

    return rsi_values
end



function load_csv_no_header(file_dir::String)
    try
        df = CSV.read(file_dir, DataFrame, header=false)
        rows = []
        for i in 1:nrow(df)
            row = [df[i, j] for j in 1:ncol(df)]
            # 나중에 지워야함

            index_to_remove = findfirst(x -> x == row[2], row)
            deleteat!(row, index_to_remove)

            push!(rows, row)
        end
        return rows
    catch e
        println("Error reading CSV file: $e")
        return nothing
    end
end


function is_bullish(ohlcv)
    if ohlcv[2] < ohlcv[5]
        return true
    elseif ohlcv[2] > ohlcv[5]
        return false
    end
    return nothing
end



# 1. 현재 캔들은 양봉 (닫힌 캔들, 다음 캔들 시가에 진입)
# 2. D-1 캔들은 음봉
# 3. D-1 RSI(close, 14)의 값은 30보다 낮음
# 4. D-1 RSI(close, 14)의 값보다 낮은 캔들을 직전 100캔들에서 서치, 없으면 패스


function check_candle_color(current_ohlcv, prev_ohlcv)
    # 현재 캔들은 양봉
    if is_bullish(current_ohlcv) == true
        # D-1 캔들은 음봉
        if is_bullish(prev_ohlcv) == false
            return true
        end
    end
    return false
end


# function find_prev_low_rsi(partial_ohlcvs, partial_rsi, min_rsi)
#     count = 0
#     for var in partial_rsi
#         if var + 10 < min_rsi
#             count += 1
#         end
#     end
#     if count > 2
#         return true
#     end
#     return false
# end



function find_prev_low_rsi(partial_ohlcvs, partial_rsi, min_rsi)
    if minimum(partial_rsi) + 5 < min_rsi
        return true
    end
    # perv_min_rsi 와 min_rsi의 간격을 thes 값으로 활용하기
    return false

    # for i=-1*length(partial_rsi):1
    #     println(i)
    #     if partial_rsi[length(partial_rsi)+i] + 5 < min_rsi
    #         return true
    #     end
    # end
    # return nothing
end


function log_maker(ticker, ohlcvs, rsi_var)
    flag[1] = false
    empty!(flag[2])
    empty!(flag[3])


    println(ticker)
    buy_sell_log = []

    for i = 200:length(ohlcvs)

        if i == 1
            continue
        end


        current_ohlcv = ohlcvs[i]
        prev_ohlcv = ohlcvs[i-1]

        if flag[1] == true && rsi_var[i] > exit_rsi
            println("compounding count : $(length(flag[2]))")
            for j = 1:length(flag[2])

                entry_price = flag[2][j]
                exit_price = current_ohlcv[5]
                entry_time = unix2datetime((flag[3][j]) / 1000)
                exit_time = unix2datetime((current_ohlcv[1]) / 1000)
                # earning = 100(exit_price / entry_price * slippage - 1)
                earning = 100(exit_price / entry_price * slippage - 1) * j

                text = string(ticker, " ", entry_time, " ~ ", exit_time, " buy :", string(entry_price), "// sell :", string(exit_price), "  ", string(earning))

                println(text, " $j")

                push!(buy_sell_log, earning)
                # push!(total_buy_sell_log, earning)
                # push!(result, earning)
            end

            flag[1] = false
            empty!(flag[2])
            empty!(flag[3])

            continue
        end


        if check_candle_color(current_ohlcv, prev_ohlcv) && rsi_var[i-1] < entry_rsi
            if find_prev_low_rsi(ohlcvs[i-200:i-1], rsi_var[i-200:i-1], rsi_var[i-1])
                flag[1] = true
                # flag[2] = ohlcvs[i+1][2] # entry_price
                # flag[3] = ohlcvs[i+1][1] # entry_time
                push!(flag[2], ohlcvs[i+1][2]) # entry_price
                push!(flag[3], ohlcvs[i+1][1]) # entry_price
            end
        end

    end

    total_perform, trade_count = get_performance(buy_sell_log, true, 100)
    println("\n")
    if total_perform < 0
        return false
    end
    return buy_sell_log
end



function main()
    folder_name = "15m"
    for file_name in readdir(folder_name)
        try
            ticker = split(file_name, "_")[1]
            ohlcvs = load_csv_no_header("./$(folder_name)/$(file_name)")
            close_data = [x[5] for x in ohlcvs]

            rsi_var = rsi(close_data; length=14, scalar=100.0, drift=1, offset=0)
            result = log_maker(ticker, ohlcvs, rsi_var)
            # println(map(x -> Float16(x), result[1:200]))
            if result != false
                f_result = fig_result(1000.0, result)
                savefig(f_result, "fig_result/$(file_name).png")
            end

            # readline()

        catch e
            continue
        end

    end
end

# flag = [is_orderd, entry_price, entry_time]
const flag = [false, [], []]

# const slippage = 0.9982 * 0.9982
# const slippage = 1
const slippage = 0.9985

const entry_rsi = 31
const exit_rsi = 50


mkdir_exist_ok("./fig_result")

main()





# function get_order_book()
#     base_url = config["binance"]["future"]["rest_base_url"]
#     end_point = "/ticker/bookTicker"
#     type = "GET"
#     json_data = request(type, base_url * end_point)
#     result = Dict()
#     for data in json_data
#         result[data["symbol"]] = parse(Float64, data["askPrice"]) / parse(Float64, data["bidPrice"])
#     end
#     return result
# end


# function sort_by_val(dict)
#     return sort(collect(dict), by=x -> x[2], rev=false)
# end

# # 거래 종목 서치
# function get_ticker_list()
#     results = sort_by_val(get_order_book())
#     for key in keys(results)
#         # USDT
#         if occursin("USDT", results[key][1])
#             @info("$(results[key][1]) : $(results[key][2])")
#         end

#         # USDC
#         # if key > 100
#         #     break
#         # end
#         #if occursin("USDC", results[key][1])
#         #    @info("$(results[key][1]) : $(results[key][2])")
#         #end
#     end
# end

