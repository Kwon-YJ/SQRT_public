using Dates
include("./../../2022/julia_test/utils.jl")

mutable struct data_struct
    ohlc::Dict{String, Any}
    order_dict::Dict{String, String}
    weight1::Float64
    weight2::Float64
    time_frame::Int8
    money::Float64
end

function get_ohlc(time_frame::String)
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

function main()
    @async _1h_data = data_struct(get_ohlc("1h"), Dict(), 1.945, 1.94, 1, 300)
    @async _2h_data = data_struct(get_ohlc("2h"), Dict(), 1.94, 1.935, 2, 325)
    @async _4h_data = data_struct(get_ohlc("4h"), Dict(), 1.955, 1.95, 4, 425)
    @async _6h_data = data_struct(get_ohlc("6h"), Dict(), 1.93, 1.925, 6, 450)
    @async _8h_data = data_struct(get_ohlc("8h"), Dict(), 1.94, 1.935, 8, 500)
    @async _12h_data = data_struct(get_ohlc("12h"), Dict(), 1.93, 1.9325, 12, 550)

    @async _1h_data = data_struct(get_ohlc("1h"), Dict(), 1.945, 1.94, 1, 300)
    @async _2h_data = data_struct(get_ohlc("2h"), Dict(), 1.94, 1.935, 2, 325)
    @async _4h_data = data_struct(get_ohlc("4h"), Dict(), 1.955, 1.95, 4, 425)
    @async _6h_data = data_struct(get_ohlc("6h"), Dict(), 1.93, 1.925, 6, 450)
    @async _8h_data = data_struct(get_ohlc("8h"), Dict(), 1.94, 1.935, 8, 500)
    @async _12h_data = data_struct(get_ohlc("12h"), Dict(), 1.93, 1.9325, 12, 550)

    _1h_data = data_struct(get_ohlc("1h"), Dict(), 1.945, 1.94, 1, 300)
    _2h_data = data_struct(get_ohlc("2h"), Dict(), 1.94, 1.935, 2, 325)

end


ticker_list = get_tickers()

sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))

@time main()


