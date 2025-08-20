using Statistics
using Dates
using Base.Threads
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
    end
    ticker_list, syntehtic_ticker_list, All_ohlcv
end

@inbounds function get_spread(first_ohlcv::Vector, second_ohlcv::Vector)
    first_price = map(x->x[5], first_ohlcv)
    second_price = map(x->x[5], second_ohlcv)
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

@inbounds function entry_side(ticker_list::Vector, syntehtic_ticker_list::Vector, All_ohlcv::Dict, orderd_list::Vector)

end

function exit_side(ticker1, ticker2, entry_price1, entry_price2, orderd_list, entry_time)
    wait_next_day()
    exit_price1 = fetch_ohlcv(ticker1)[end][5]
    exit_price2 = fetch_ohlcv(ticker2)[end][5]
    long_earning = 100(exit_price1 / entry_price1 * slippage - 1) 
    short_earning = -100(exit_price2 / entry_price2 * slippage - 1)
    text = "$(entry_time)/L:$(ticker1[1:end-4]) $(Float16(entry_price1))~$(Float16(exit_price1))/S:$(ticker2[1:end-4]) $(Float16(entry_price2))~$(Float16(exit_price2)) $(Float16(long_earning)) $(Float16(short_earning)))"
    println(text)
    push!(earning_log, long_earning)
    push!(earning_log, short_earning)
    deleteat!(orderd_list, findall(x->x=="$(ticker1)$(ticker2)",orderd_list))
end

function main()
    orderd_list = Vector([])
    ticker_list, syntehtic_ticker_list, All_ohlcv = one_per_day_init()
    sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
    while true
        utcurrentime = now(Dates.UTC)
        hours = parse(Int8, Dates.format(utcurrentime, "HH"))
        minute = parse(Int8, Dates.format(utcurrentime, "MM"))
        if hours==23 && minute==55 # UTC 기준 00:00분 
            sleep(600)
            ticker_list, syntehtic_ticker_list, All_ohlcv = one_per_day_init()
            get_performance(earning_log, true, 35)
            empty!(earning_log)
        end
        orderd_list = entry_side(ticker_list, syntehtic_ticker_list, deepcopy(All_ohlcv), orderd_list)
    end
end


weight::Float64 = 1.18
const elastic::Float64 = 0.0015
const money::Float64 = 35
const slippage::Float64 = 0.9982 * 0.9982
earning_log = [] 

main()

