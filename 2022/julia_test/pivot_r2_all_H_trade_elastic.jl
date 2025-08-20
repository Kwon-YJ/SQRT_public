using Dates
include("./utils.jl")


mutable struct data_struct
    ohlc::Dict{String, Any}
    order_dict::Dict{String, String}
    elastic::Float64
    weight1::Float64
    weight2::Float64
    time_frame::Int8
end

function get_target_price(time_frame::String)
    global ticker_list
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

function entry_side(data, current_price, double_ohlcv)
    global ticker_list
    order_keys = [key for (key, value) in data.order_dict]
    for ticker in ticker_list
        if ticker in order_keys
            continue
        end
        weight = 2.35
        ohlc = data.ohlc[ticker]
        open = ohlc[2][2]
        if double_ohlcv == true
            high = maximum((ohlc[1][3], ohlc[2][3]))
            low = minimum((ohlc[1][4], ohlc[2][4]))
        else
            high = ohlc[2][3]
            low = ohlc[2][4]
        end
        close = ohlc[2][5]
        PP = (high + low + 4*close) / 6
        if open < close
            weight = data.weight1 + (length(data.order_dict) * data.elastic)
        else
            weight = data.weight2 + (length(data.order_dict) * data.elastic)
        end
        target_price = weight * PP - low 
        if current_price[ticker] > target_price
            trade_amount, price = get_amount(ticker, 277)
            order_resp = create_order(ticker, "SELL", "MARKET", trade_amount, price)
            data.order_dict[ticker] = order_resp["origQty"]
            println("SELL : $(ticker) // $(data.time_frame)h ")
        end
    end
end

function exit_side(data)
    utcurrentime = now(Dates.UTC)
    minute = parse(Int8, Dates.format(utcurrentime, "MM"))
    hours = parse(Int8, Dates.format(utcurrentime, "HH"))
    if hours%data.time_frame == 0 && minute == 0
        for ticker in keys(data.order_dict)
            create_order(ticker, "BUY", "MARKET", data.order_dict[ticker])
            println("BUY : $(ticker) // $(data.time_frame)h // $(utcurrentime)")
        end
        data.order_dict = Dict{String,String}()
        data.ohlc = get_target_price("$(data.time_frame)h")
    end
end

function main()
    _1h_data = data_struct(get_target_price("1h"), Dict(), 0, 2.3, 2.15 ,1)
    _2h_data = data_struct(get_target_price("2h"), Dict(), 0, 2.3, 2.15, 2)    
    _4h_data = data_struct(get_target_price("4h"), Dict(), 0, 2.3, 2.15, 4)
    _8h_data = data_struct(get_target_price("8h"), Dict(), 0.0025, 2.24, 2.24, 8)

    while true

        sleep(4)
        current_price = get_current_price()

        entry_side(_1h_data, current_price, false)
        entry_side(_2h_data, current_price, true)
        entry_side(_4h_data, current_price, true)
        entry_side(_8h_data, current_price, true)
        
        exit_side(_1h_data)
        exit_side(_2h_data)
        exit_side(_4h_data)
        exit_side(_8h_data)
        
    end
end

ticker_list = get_tickers()

main()


