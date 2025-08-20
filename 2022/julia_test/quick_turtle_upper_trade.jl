using Dates
using Random
using Distributed
using Base.Threads
include("./utils.jl")


mutable struct all_data
    ticker_list
    target_price
    order_list
end

function exit_side(ticker, amount)
    hours, minute = parse(Int8, Dates.format(now(Dates.UTC), "HH")), parse(Int8, Dates.format(now(Dates.UTC), "MM"))
    sleep(1442 - (60(hours)+minute))
    sleep(rand()*10)
    create_order(ticker, "BUY", "MARKET", amount)
end

function get_target_price(ticker_list)
    result = Dict()
    for ticker in ticker_list
        ohlcv = fetch_ohlcv(ticker, "1d", "6")
        if length(ohlcv) != 6
            result[ticker] = 10^9
            continue
        end
        highs = [high[3] for high in ohlcv]
        result[ticker] = maximum(highs[1:end-1])
    end
    return result
end

function get_struct_data()
    ticker_list = get_tickers()
    sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
    result = all_data(ticker_list, get_target_price(ticker_list), [])
    return result
end

function main()
    struct_data = get_struct_data()

    while true
        sleep(4)
        utcurrentime = now(Dates.UTC)
        hours = parse(Int8, Dates.format(utcurrentime, "HH"))
        minute = parse(Int8, Dates.format(utcurrentime, "MM"))
        if hours==0 && minute==0 # UTC 기준 00:00분 
            struct_data = get_struct_data()
        end

        current_price = get_current_price()

        for ticker in struct_data.ticker_list
            if ticker in struct_data.order_list
                continue
            end
            if current_price[ticker] > struct_data.target_price[ticker]
                println("short $(ticker) // Q_turtle_U")
                trade_amount, price = get_amount(ticker, 350)
                order_resp = create_order(ticker, "SELL", "MARKET", trade_amount, price)
                push!(struct_data.order_list, ticker)
                @async exit_side(ticker, order_resp["origQty"])
            end
        end
    end
end



main()

