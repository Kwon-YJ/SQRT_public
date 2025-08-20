using Dates
include("./../../2022/julia_test/utils.jl")

mutable struct data_struct
    ohlc::Dict{String, Any}
    ordered::Vector{String}
    weight1::Float64
    weight2::Float64
    time_frame::Int8
    money::Float64
    orderids
end

function elastic(n)
    values = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.09, 0.13, 0.17, 0.21, 0.25, 0.29, 0.33, 0.37, 0.41, 0.45, 0.49, 0.53, 0.57, 0.61, 0.65, 0.69, 0.73, 0.77, 0.81]
    return values[n+1]
end

function get_ohlc(time_frame::String)
    ticker_list = get_tickers()
    result = Dict{String, Any}()
    for ticker in ticker_list
        ohlcv = fetch_ohlcv(ticker, time_frame, 3)
        if length(ohlcv) !=3
            continue
        end
        result[ticker] = ohlcv
    end
    return result
end

function same_decimal(A, B)
    isinteger(A) && return 0
    str_A = string(A)
    places = length(str_A) - findfirst('.', str_A)
    return floor(B, digits=places)
end

function exit_side(order_results)
    for order_result in order_results
        try
            query_result = check_order(order_result["symbol"], order_result["orderId"])
            if cmp(query_result["executedQty"], order_result["origQty"]) == 0
                create_order(query_result["symbol"], "SELL", "MARKET", order_result["origQty"])
                continue
            end
            cancel_order(order_result["symbol"], order_result["orderId"])
            if cmp(query_result["executedQty"], "0") != 0
                create_order(query_result["symbol"], "SELL", "MARKET", query_result["executedQty"])
            end
        catch e
            telegram_send("1_pivot_s2_all_H_trade_new_limit.jl exit_side error $(e)")
            sleep(1)
            continue
        end
    end
end

function main()
    ticker_list = get_tickers()
    # _1h_data = data_struct(get_ohlc("1h"), Vector(), 1.945, 1.94, 1, 549, Vector())
    _1h_data = data_struct(get_ohlc("1h"), Vector(), 1.945, 1.94, 1, 1000, Vector())
    _2h_data = data_struct(get_ohlc("2h"), Vector(), 1.94, 1.935, 2, 599, Vector())
    _4h_data = data_struct(get_ohlc("4h"), Vector(), 1.955, 1.95, 4, 849, Vector())
    _6h_data = data_struct(get_ohlc("6h"), Vector(), 1.93, 1.925, 6, 899, Vector())
    _8h_data = data_struct(get_ohlc("8h"), Vector(), 1.94, 1.935, 8, 999, Vector())
    _12h_data = data_struct(get_ohlc("12h"), Vector(), 1.93, 1.925, 12, 1099, Vector())
    
    sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
    
    

    while true
        try
            # current_price = get_current_price(ticker_list)
            current_price = get_current_price_new(ticker_list)
            minute = parse(Int8, Dates.format(now(Dates.UTC), "MM"))

            if minute == 59
                sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
                hours = parse(Int8, Dates.format(now(Dates.UTC), "HH"))
                exit_side(_1h_data.orderids)
                empty!(_1h_data.ordered)
                empty!(_1h_data.orderids)
                if hours%_2h_data.time_frame == 0
                    exit_side(_2h_data.orderids)
                    empty!(_2h_data.ordered)
                    empty!(_2h_data.orderids)
                end
                if hours%_4h_data.time_frame == 0
                    exit_side(_4h_data.orderids)
                    empty!(_4h_data.ordered)
                    empty!(_4h_data.orderids)
                end
                if hours%_6h_data.time_frame == 0
                    exit_side(_6h_data.orderids)
                    empty!(_6h_data.ordered)
                    empty!(_6h_data.orderids)
                end
                if hours%_8h_data.time_frame == 0
                    exit_side(_8h_data.orderids)
                    empty!(_8h_data.ordered)
                    empty!(_8h_data.orderids)
                end
                if hours%_12h_data.time_frame == 0
                    exit_side(_12h_data.orderids)
                    empty!(_12h_data.ordered)
                    empty!(_12h_data.orderids)
                end

                sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))

                _1h_data.ohlc = get_ohlc("1h")
                if hours%_2h_data.time_frame == 0
                    _2h_data.ohlc = get_ohlc("2h")
                end
                if hours%_4h_data.time_frame == 0
                    _4h_data.ohlc = get_ohlc("4h")
                end
                if hours%_6h_data.time_frame == 0
                    _6h_data.ohlc = get_ohlc("6h")
                end
                if hours%_8h_data.time_frame == 0
                    _8h_data.ohlc = get_ohlc("8h")
                end
                if hours%_12h_data.time_frame == 0
                    _12h_data.ohlc= get_ohlc("12h")
                end
                if hours == 0
                    telegram_send("1_pivot_s2_all_H_trade_new_limit.jl is operating normally.")
                    sleep(600)
                end
            end
            entry_side(_1h_data, current_price, true, ticker_list)
            #entry_side(_2h_data, current_price, false, ticker_list)
            #entry_side(_4h_data, current_price, false, ticker_list)
            #entry_side(_6h_data, current_price, true, ticker_list)
            #entry_side(_8h_data, current_price, true, ticker_list)
            #entry_side(_12h_data, current_price, true, ticker_list)
            sleep(0.05)
        catch e
            telegram_send("1_pivot_s2_all_H_trade_new_limit.jl main error $(e)")
            sleep(60)
            continue
        end
    end
end


main()

