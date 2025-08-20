using Dates
using Random
using Distributed
using Base.Threads
include("./../../2022/julia_test/utils.jl")


mutable struct all_data
    ticker_list
    target_price
    order_list
end

function exit_side(ticker, amount)
    wait_next("4h")
    create_order(ticker, "BUY", "MARKET", amount)
end

function get_target_price(ticker_list)
    result = Dict()
    for ticker in ticker_list
        ohlcv = fetch_ohlcv(ticker, "4h", "11")
        if length(ohlcv) != 11
            result[ticker] = 10^9
            continue
        end
        highs = [high[3] for high in ohlcv]
        result[ticker] = maximum(highs[1:end-1])
        y_max = maximum( map(x->x[3], ohlcv[1:end-1]) )
        max_tr = maximum( map(x->abs(x[2]-x[5]), ohlcv[1:end-1]) )
        result[ticker] = y_max + max_tr * 3.9
    end
    return result
end

function get_struct_data()
    ticker_list = get_tickers()
    deleteat!(ticker_list, findall(x->x=="BTCUSDT",ticker_list))
    deleteat!(ticker_list, findall(x->x=="FXSUSDT",ticker_list))
    sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
    result = all_data(ticker_list, get_target_price(ticker_list), [])
    return result
end

function main()
    struct_data = get_struct_data()

    while true
        sleep(59)
        utcurrentime = now(Dates.UTC)
        hours = parse(Int8, Dates.format(utcurrentime, "HH"))
        minute = parse(Int8, Dates.format(utcurrentime, "MM"))
        if hours%4 == 0 && minute == 0 # UTC 기준 4시간 마다
            sleep(120)
            struct_data = get_struct_data()
        end

        current_price = get_current_price()

        for ticker in struct_data.ticker_list
            if ticker in struct_data.order_list
                continue
            end
            if current_price[ticker] > struct_data.target_price[ticker] && fetch_available_balance() > 100
                telegram_send("short $(ticker) // Q_turtle_U")
                trade_amount, price = get_amount(ticker, 350)
                order_resp = create_order(ticker, "SELL", "MARKET", trade_amount, price)
                push!(struct_data.order_list, ticker)
                @async exit_side(ticker, order_resp["origQty"])
            end
        end
    end
end

main()

