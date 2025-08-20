using Statistics
using Dates
include("./../../2022/julia_test/utils.jl")


function get_syntehtic_ticker_list(since_day=100::Int64)
    btc_ohlcv = fetch_ohlcv("BTCUSDT", "1d", "1000")
    start_time = string(btc_ohlcv[end-since_day][1])
    end_time = string(btc_ohlcv[end-since_day+100][1])
    ticker_list = get_tickers()
    deleteat!(ticker_list, findall(x->x=="BTCDOMUSDT",ticker_list))
    deleteat!(ticker_list, findall(x->x=="BTCUSDT",ticker_list))
    del_list = []
    for ticker in ticker_list
        if length(fetch_ohlcv(ticker, "1d", string(since_day), start_time, end_time)) != since_day
            push!(del_list, ticker)
        end
    end
    ticker_list=setdiff!(ticker_list, del_list)
    ticker_list, nP2(ticker_list)
end

function one_per_day_init()
    All_ohlcv = Dict()
    ticker_list, syntehtic_ticker_list = get_syntehtic_ticker_list()
    btc_ohlcv = fetch_ohlcv("BTCUSDT", "1d", "2")
    start_time = string(btc_ohlcv[1][1])
    end_time = string(btc_ohlcv[end][1])
    for (i, ticker) in enumerate(ticker_list)
        All_ohlcv[ticker] = fetch_ohlcv(ticker,"1m","1440",start_time,end_time)
        sleep(0.9)
    end
    ticker_list, syntehtic_ticker_list, All_ohlcv
end

function get_fifth_element(data)
    n = length(data)
    selected_data = Vector{typeof(data[1][5])}(undef, n)
    @inbounds @simd for i in 1:n
        selected_data[i] = data[i][5]
    end
    return selected_data
end

function get_spread(first_ohlcv::Vector, second_ohlcv::Vector)
    first_price = get_fifth_element(first_ohlcv)
    second_price = get_fifth_element(second_ohlcv)
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

function get_elastic(n)
    result = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11.5, 14.0, 16.5, 19.0, 21.5, 24.0, 26.5, 29.0, 31.5, 34.0, 39.0, 44.0, 49.0, 54.0, 59.0, 64.0, 69.0, 74.0, 79.0, 84.0, 89.0, 94.0, 99.0, 104.0, 109.0, 114.0, 119.0, 124.0, 129.0, 134.0, 139.0, 144.0, 149.0, 154.0, 159.0, 164.0, 169.0, 174.0, 179.0, 184.0, 189.0, 194.0, 199.0, 204.0, 209.0, 214.0, 219.0, 224.0, 229.0, 234.0, 239.0, 244.0, 249.0, 254.0, 259.0, 264.0, 269.0, 274.0, 279.0, 284.0, 289.0, 294.0, 299.0, 304.0, 309.0, 314.0, 319.0, 324.0, 329.0, 334.0, 339.0, 344.0, 349.0, 354.0, 359.0, 364.0, 369.0, 374.0, 379.0, 384.0, 389.0, 394.0, 399.0, 404.0, 409.0, 414.0, 419.0, 424.0, 429.0, 434.0, 439.0]
    return result[n+1]
end

function exit_side(ticker1, ticker2, trade_amount1, trade_amount2, orderd_list)
    wait_next_day()
    create_order(ticker1, "SELL", "MARKET",trade_amount1)
    create_order(ticker2, "BUY", "MARKET",trade_amount2)
    deleteat!(orderd_list, findall(x->x=="$(ticker1)$(ticker2)",orderd_list))
end

function main()
    orderd_list = Vector{String}([])
    ticker_list, syntehtic_ticker_list, All_ohlcv = one_per_day_init()
    sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
    while true
        utcurrentime = now(Dates.UTC)
        hours = parse(Int8, Dates.format(utcurrentime, "HH"))
        minute = parse(Int8, Dates.format(utcurrentime, "MM"))
        if hours==23 && minute==55 # UTC 기준 날짜 변경 5분 전
            sleep(600)
            ticker_list, syntehtic_ticker_list, All_ohlcv = one_per_day_init()
            orderd_list = Vector{String}([])
        end
        orderd_list = entry_side(ticker_list, syntehtic_ticker_list, deepcopy(All_ohlcv), orderd_list)
        sleep(3)
    end
end

main()

