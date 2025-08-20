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
    values = [0, 0.01, 0.02, 0.03, 0.04, 0.08, 0.12, 0.16, 0.2, 0.24, 0.28, 0.32, 0.36, 0.4, 0.44, 0.48, 0.52, 0.56, 0.6, 0.64, 0.68, 0.72, 0.76, 0.80, 0.84, 0.88, 0.92, 0.96, 1.0, 1.04, 1.08, 1.12, 1.16, 1.2, 1.24, 1.28, 1.32, 1.36, 1.40, 1.44, 1.48, 1.52, 1.56, 1.6, 1.64, 1.68, 1.72, 1.76, 1.8, 1.84]
    return values[n+1]
end

function get_ohlc(time_frame::String)
    global ticker_list
    result = Dict{String, Any}()
    for ticker in ticker_list
        ohlcv = fetch_ohlcv(ticker, time_frame, 7)
        if length(ohlcv) !=7
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

function entry_side(data, current_price)
    global ticker_list
    for ticker in setdiff!(ticker_list, data.ordered)
        ohlc = data.ohlc[ticker]
        if ohlc[end][3] < 10^-5
            continue
        end

        y_max = maximum( map(x->x[3], ohlc[1:end-1]) )
        max_tr = maximum( map(x->abs(x[2]-x[5]), ohlc[1:end-1]) )      
        
        target_price = y_max + max_tr * (data.weight2+0.01+elastic(length(data.ordered)))
        limit_target_price = y_max + max_tr * (data.weight2+elastic(length(data.ordered)))
        
        if current_price[ticker] > target_price && fetch_available_balance("USDT") > 2500
            try
                trade_amount, price = get_amount(ticker, data.money)
                price = same_decimal(price, limit_target_price)
                order_resp = create_order(ticker, "SELL", "LIMIT", trade_amount, price)
                sleep(1)
                push!(data.ordered, ticker)
                push!(data.orderids, order_resp)
            catch e
                telegram_send("error Upper_Q : $(ticker) $(data.time_frame)h $(e)")
                sleep(60)
            end
        end
    end
end

function exit_side(order_results)
    for order_result in order_results
        query_result = check_order(order_result["symbol"], order_result["orderId"])
        if cmp(query_result["executedQty"], order_result["origQty"]) == 0
            create_order(query_result["symbol"], "BUY", "MARKET", order_result["origQty"])
            continue
        end
        cancel_order(order_result["symbol"], order_result["orderId"])
        if cmp(query_result["executedQty"], "0") != 0
            create_order(query_result["symbol"], "BUY", "MARKET", query_result["executedQty"])
        end
    end
end

function main()
    _1h_data = data_struct(get_ohlc("1h"), Vector(), 6, 1.01, 1, 95, Vector())
    sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))

    while true
        current_price = get_current_price()
        minute = parse(Int8, Dates.format(now(Dates.UTC), "MM"))
        if minute == 59
            sleep(55)
            exit_side(_1h_data.orderids)
            sleep(5)
            _1h_data.ohlc = get_ohlc("1h")
            empty!(_1h_data.ordered)
            empty!(_1h_data.orderids)
            sleep(120 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
        end
        entry_side(_1h_data, current_price)
        sleep(3)
    end
end

ticker_list = get_tickers()
sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
del_list = []
for ticker in ticker_list
    if length(fetch_ohlcv(ticker, "1d", 7)) != 7
        push!(del_list, ticker)
    end
end
ticker_list=setdiff!(ticker_list, del_list)
deleteat!(ticker_list, findall(x->x=="BTCUSDT",ticker_list))
deleteat!(ticker_list, findall(x->x=="BTCDOMUSDT",ticker_list))

main()
