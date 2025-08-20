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

function elastic_pivot(n)
    values = [0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.09, 0.13, 0.17, 0.21, 0.25, 0.29, 0.33, 0.37, 0.41, 0.45, 0.49, 0.53, 0.57, 0.61, 0.65, 0.69, 0.73, 0.77, 0.81]
    return values[n+1]
end

function elastic_Q(n, time_frame)
    if time_frame == 8
        values = [0, 0.04, 0.08, 0.12, 0.16, 0.2, 0.33, 0.46, 0.59, 0.72, 0.85, 1.04, 1.23, 1.42, 1.61, 1.8, 1.99, 2.18, 2.37, 2.56, 2.75, 2.94, 3.13, 3.32, 3.51, 3.7, 3.89, 4.08, 4.27, 4.46, 4.65, 4.84, 5.03, 5.22, 5.41, 5.6, 5.79, 5.98, 6.17, 6.36, 6.55, 6.74, 6.93, 7.12, 7.31, 7.5, 7.69, 7.88, 8.07, 8.26, 8.45, 8.64, 8.83, 9.02]
        return values[n+1]
    elseif time_frame == 4 || time_frame == 6
        values = [0, 0.04, 0.08, 0.12, 0.16, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1, 1.05, 1.1, 1.15, 1.2, 1.25, 1.3, 1.35, 1.4, 1.45, 1.5, 1.55, 1.6, 1.65, 1.7, 1.75, 1.8, 1.85, 1.9, 1.95, 2, 2.05, 2.1, 2.15, 2.2, 2.25, 2.3, 2.35, 2.4, 2.45, 2.5]
        return values[n+1]
    else
        values = [0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.79, 0.98, 1.17, 1.36, 1.55, 1.74, 1.93, 2.12, 2.31, 2.5, 2.69, 2.88, 3.07, 3.26, 3.45, 3.64, 3.83, 4.02, 4.21, 4.4, 4.59, 4.78, 4.97, 5.16, 5.35, 5.54, 5.73, 5.92, 6.11, 6.3, 6.49, 6.68, 6.87, 7.06, 7.25, 7.44, 7.63, 7.82, 8.01, 8.2, 8.39, 8.58, 8.77, 8.96, 9.15, 9.34, 9.53, 9.72, 9.91, 10.1, 10.29, 10.48, 10.67, 10.86, 11.05, 11.24, 11.43, 11.62, 11.81, 12.00, 12.19, 12.38, 12.57, 12.76, 12.95, 13.14]
        return values[n+1]
    end   
end 

function get_ohlc_pivot(time_frame::String)
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

function get_ohlc_Q(time_frame::String)
    ticker_list = get_tickers()
    result = Dict{String, Any}()
    for ticker in ticker_list
        ohlcv = fetch_ohlcv(ticker, time_frame, 41)
        if length(ohlcv) !=41
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

function entry_side_pivot(data, current_price, double_ohlcv, ticker_list)
    for ticker in setdiff!(ticker_list, data.ordered)
        ohlc = data.ohlc[ticker]
        if double_ohlcv == true
            high = maximum((ohlc[1][3], ohlc[2][3]))
            low = minimum((ohlc[1][4], ohlc[2][4]))
        else
            high = ohlc[2][3]
            low = ohlc[2][4]
        end
        open = ohlc[2][2]
        close = ohlc[2][5]
        if high < 10^-5
            continue
        end
        weight = 10^6
        if open < close
            weight = data.weight1 - elastic_pivot(length(data.ordered))
        else
            weight = data.weight2 - elastic_pivot(length(data.ordered))
        end
        PP = (high + low + 4*close) / 6
        target_price = (weight + 0.00715) * PP - high
        limit_target_price = weight * PP - high
        if current_price[ticker] < target_price && fetch_available_balance("USDT")
            try
                trade_amount, price = get_amount(ticker, data.money)
                price = same_decimal(price, limit_target_price)
                order_resp = create_order(ticker, "BUY", "LIMIT", trade_amount, price)
                push!(data.ordered, ticker)
                push!(data.orderids, order_resp)
            catch e
                telegram_send("1_pivot_s2_all_H_trade_new_limit.jl entry_side error $(ticker) $(data.time_frame)h $(e)")
                sleep(1)
            end
        end
    end
end

function entry_side_Q(data, current_price)
    ticker_list = get_tickers()
    for ticker in setdiff!(ticker_list, data.ordered)
        ohlc = data.ohlc[ticker][end-convert(Int8, data.weight1):end]
        if ohlc[end][3] < 10^-5
            continue
        end

        lows = [low[4] for low in ohlc]
        y_min = minimum( lows[1:end-1] )

        max_tr = maximum( map(x->abs(x[2]-x[5]), ohlc[1:end-1]) )      
        target_price = y_min - max_tr * (data.weight2+0.01+elastic_Q(length(data.ordered), data.time_frame))
        limit_target_price = y_min - max_tr * (data.weight2+elastic_Q(length(data.ordered), data.time_frame))
        
        if current_price[ticker] < target_price && fetch_available_balance("USDT")
            try
                trade_amount, price = get_amount(ticker, data.money)
                price = same_decimal(price, limit_target_price)
                order_resp = create_order(ticker, "BUY", "LIMIT", trade_amount, price)
                sleep(0.5)
                push!(data.ordered, ticker)
                push!(data.orderids, order_resp)
            catch e
                telegram_send("Q_lower_all_H_trade_limit.jl entry_side error $(ticker) $(data.time_frame)h $(e)")
                sleep(60)
            end
        end
    end
end

function exit_side_Q(order_results, interval)
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
            telegram_send("Q_lower_all_H_trade_limit.jl exit_side error $(e)")
            sleep(5)
        end
    end
end

function exit_side_pivot(order_results)
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

    _1h_data_pivot = data_struct(get_ohlc_pivot("1h"), Vector(), 1.945, 1.94, 1, 75, Vector())
    _2h_data_pivot = data_struct(get_ohlc_pivot("2h"), Vector(), 1.94, 1.935, 2, 150, Vector())
    sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
    _4h_data_pivot = data_struct(get_ohlc_pivot("4h"), Vector(), 1.955, 1.95, 4, 200, Vector())
    _6h_data_pivot = data_struct(get_ohlc_pivot("6h"), Vector(), 1.93, 1.925, 6, 225, Vector())
    sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
    _8h_data_pivot = data_struct(get_ohlc_pivot("8h"), Vector(), 1.94, 1.935, 8, 250, Vector())
    _12h_data_pivot = data_struct(get_ohlc_pivot("12h"), Vector(), 1.93, 1.925, 12, 300, Vector())
    sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))

    _1h_data_Q = data_struct(get_ohlc_Q("1h"), Vector(), 37, 2.1, 1, 75, Vector())
    _2h_data_Q = data_struct(get_ohlc_Q("2h"), Vector(), 10, 2.9, 2, 150, Vector())
    sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
    _4h_data_Q = data_struct(get_ohlc_Q("4h"), Vector(), 15, 0.63, 4, 200, Vector())
    _6h_data_Q = data_struct(get_ohlc_Q("6h"), Vector(), 40, 0.09, 6, 225, Vector())
    sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
    _8h_data_Q = data_struct(get_ohlc_Q("8h"), Vector(), 36, 0.1, 8, 250, Vector())
    _12h_data_Q = data_struct(get_ohlc_Q("12h"), Vector(), 6, 1.43, 12, 300, Vector())
    sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
    
    while true
        try
            current_price = get_current_price(ticker_list)
            minute = parse(Int8, Dates.format(now(Dates.UTC), "MM"))
            if minute == 59
                sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
                hours = parse(Int8, Dates.format(now(Dates.UTC), "HH"))
                exit_side_pivot(_1h_data_pivot.orderids)
                empty!(_1h_data_pivot.ordered)
                empty!(_1h_data_pivot.orderids)

                exit_side_Q(_1h_data_Q.orderids, "1h")
                empty!(_1h_data_Q.ordered)
                empty!(_1h_data_Q.orderids)

                if hours%_2h_data_pivot.time_frame == 0
                    exit_side_pivot(_2h_data_pivot.orderids)
                    empty!(_2h_data_pivot.ordered)
                    empty!(_2h_data_pivot.orderids)

                    exit_side_Q(_2h_data_Q.orderids, "2h")
                    empty!(_2h_data_Q.ordered)
                    empty!(_2h_data_Q.orderids)
                end
                if hours%_4h_data_pivot.time_frame == 0
                    exit_side_pivot(_4h_data_pivot.orderids)
                    empty!(_4h_data_pivot.ordered)
                    empty!(_4h_data_pivot.orderids)

                    exit_side_Q(_4h_data_Q.orderids, "4h")
                    empty!(_4h_data_Q.ordered)
                    empty!(_4h_data_Q.orderids)
                end
                if hours%_6h_data_pivot.time_frame == 0
                    exit_side_pivot(_6h_data_pivot.orderids)
                    empty!(_6h_data_pivot.ordered)
                    empty!(_6h_data_pivot.orderids)

                    exit_side_Q(_6h_data_Q.orderids, "6h")
                    empty!(_6h_data_Q.ordered)
                    empty!(_6h_data_Q.orderids)
                end
                if hours%_8h_data_pivot.time_frame == 0
                    exit_side_pivot(_8h_data_pivot.orderids)
                    empty!(_8h_data_pivot.ordered)
                    empty!(_8h_data_pivot.orderids)

                    exit_side_Q(_8h_data_Q.orderids, "8h")
                    empty!(_8h_data_Q.ordered)
                    empty!(_8h_data_Q.orderids)
                end
                if hours%_12h_data_pivot.time_frame == 0
                    exit_side_pivot(_12h_data_pivot.orderids)
                    empty!(_12h_data_pivot.ordered)
                    empty!(_12h_data_pivot.orderids)

                    exit_side_Q(_12h_data_Q.orderids, "12h")
                    empty!(_12h_data_Q.ordered)
                    empty!(_12h_data_Q.orderids)
                end

                sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))

                _1h_data_pivot.ohlc = get_ohlc_pivot("1h")
                _1h_data_Q.ohlc = get_ohlc_Q("1h")
                if hours%_2h_data_pivot.time_frame == 0
                    _2h_data_pivot.ohlc = get_ohlc_pivot("2h")
                    _2h_data_Q.ohlc = get_ohlc_Q("2h")
                end
                if hours%_4h_data_pivot.time_frame == 0
                    _4h_data_pivot.ohlc = get_ohlc_pivot("4h")
                    _4h_data_Q.ohlc = get_ohlc_Q("4h")
                end
                if hours%_6h_data_pivot.time_frame == 0
                    _6h_data_pivot.ohlc = get_ohlc_pivot("6h")
                    _6h_data_Q.ohlc = get_ohlc_Q("6h")
                end
                if hours%_8h_data_pivot.time_frame == 0
                    _8h_data_pivot.ohlc = get_ohlc_pivot("8h")
                    _8h_data_Q.ohlc = get_ohlc_Q("8h")
                end
                if hours%_12h_data_pivot.time_frame == 0
                    _12h_data_pivot.ohlc= get_ohlc_pivot("12h")
                    _12h_data_Q.ohlc= get_ohlc_Q("12h")
                end
                if hours == 0
                    telegram_send("all_in_1.jl is operating normally.")
                    sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
                end
            end
            entry_side_pivot(_1h_data_pivot, current_price, true, ticker_list)
            entry_side_pivot(_2h_data_pivot, current_price, false, ticker_list)
            entry_side_pivot(_4h_data_pivot, current_price, false, ticker_list)
            entry_side_pivot(_6h_data_pivot, current_price, true, ticker_list)
            entry_side_pivot(_8h_data_pivot, current_price, true, ticker_list)
            entry_side_pivot(_12h_data_pivot, current_price, true, ticker_list)
            
            entry_side_Q(_1h_data_Q, current_price)
            entry_side_Q(_2h_data_Q, current_price)
            entry_side_Q(_4h_data_Q, current_price)
            entry_side_Q(_6h_data_Q, current_price)
            entry_side_Q(_8h_data_Q, current_price)
            entry_side_Q(_12h_data_Q, current_price)
            
            sleep(1)
        catch e
            telegram_send("all_in_1.jl main error $(e)")
            sleep(60)
            continue
        end
    end
end

main()

