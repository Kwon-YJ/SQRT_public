using Dates
using Random
using Distributed
using Base.Threads
include("./../../2022/julia_test/utils.jl")


mutable struct all_data
    ticker_list
    target_price
    order_list
    weight
    time_frame::String
end

function exit_side(ticker, amount, time_frame)
    wait_next(time_frame)
    telegram_send("short exit $(ticker) // Q_turtle_U // $(time_frame)")
    create_order(ticker, "BUY", "MARKET", amount)
end

function get_target_price(ticker_list, length, weight, time_frame)
    result = Dict()
    for ticker in ticker_list
        ohlcv = fetch_ohlcv(ticker, time_frame, length)
        highs = [high[3] for high in ohlcv]
        result[ticker] = maximum(highs[1:end-1])
        y_max = maximum( map(x->x[3], ohlcv[1:end-1]) )
        max_tr = maximum( map(x->abs(x[2]-x[5]), ohlcv[1:end-1]) )
        result[ticker] = y_max + max_tr * weight
    end
    return result
end

function entry_side(struct_data, current_price)
    for ticker in struct_data.ticker_list
        if ticker in struct_data.order_list
            continue
        end
        if current_price[ticker] > struct_data.target_price[ticker] && fetch_available_balance() > 100
            telegram_send("short $(ticker) // Q_turtle_U // $(struct_data.time_frame)")
            trade_amount, price = get_amount(ticker, 35)
            order_resp = create_order(ticker, "SELL", "MARKET", trade_amount, price)
            push!(struct_data.order_list, ticker)
            @async exit_side(ticker, order_resp["origQty"], struct_data.time_frame)
        end
    end
end

function main()
    _4h = all_data(ticker_list, get_target_price(ticker_list, 11, 3.9, "4h"), [], 3.9, "4h")
    _1d = all_data(ticker_list, get_target_price(ticker_list, 4, 1.9, "1d"), [], 1.9, "1d")

    while true
        sleep(3)
        current_price = get_current_price()

        entry_side(_4h, current_price)
        entry_side(_1d, current_price)

        utcurrentime = now(Dates.UTC)
        minute = parse(Int8, Dates.format(utcurrentime, "MM"))
        hours = parse(Int8, Dates.format(utcurrentime, "HH"))
        if hours%4 == 0 && minute == 0
            sleep(60)
            _4h = all_data(ticker_list, get_target_price(ticker_list, 11, 3.9, "4h"), [], 3.9, "4h")        
            if hours == 0
                _1d = all_data(ticker_list, get_target_price(ticker_list, 4, 1.9, "4h"), [], 1.9, "1d")
            end
        end
    end
end


ticker_list = get_tickers()
deleteat!(ticker_list, findall(x->x=="BTCDOMUSDT",ticker_list))
deleteat!(ticker_list, findall(x->x=="BTCUSDT",ticker_list))
del_list = []
for ticker in ticker_list
    if length(fetch_ohlcv(ticker, "1d", 13)) != 13
        push!(del_list, ticker)
    end
end
ticker_list=setdiff!(ticker_list, del_list)


main()