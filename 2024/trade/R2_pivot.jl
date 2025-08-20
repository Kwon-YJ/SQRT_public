using Dates
include("./../../2022/julia_test/utils.jl")


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


function exit_side()
    global _4h_data
    utcurrentime = now(Dates.UTC)
    minute = parse(Int8, Dates.format(utcurrentime, "MM"))
    hours = parse(Int8, Dates.format(utcurrentime, "HH"))
    if hours%_4h_data.time_frame == 0 && minute == 0
        for ticker in keys(_4h_data.order_dict)
            create_order(ticker, "BUY", "MARKET", _4h_data.order_dict[ticker])
            # @async telegram_send("BUY exit (R2) : $(ticker) // $(_4h_data.time_frame)h // $(utcurrentime)")
        end
        _4h_data.order_dict = Dict{String,String}()
        _4h_data.ohlc = get_target_price("$(_4h_data.time_frame)h")
    end
    sleep(120)
end

function main()
    global ticker_list
    while true
        #try
            sleep(3.5)
            current_price = get_current_price_old()
            entry_side(current_price, true)
            exit_side()
        #catch e
        #    @async telegram_send("R2_pivot.jl error $(e)")
        #end
    end
end



ticker_list = get_tickers()
_4h_data = data_struct(get_target_price("4h"), Dict(), 0, 2.305, 2.155, 4)

main()



