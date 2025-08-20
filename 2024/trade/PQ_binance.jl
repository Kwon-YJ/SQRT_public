using Dates
include("./../../2022/julia_test/utils.jl")

using Base.Threads

using Logging

Logging.global_logger(ConsoleLogger(stderr, Logging.Debug))

module all_weight
    global_dict = Dict( "1h" => [], 
                        "2h" => [], 
                        "4h" => [], 
                        "6h" => [], 
                        "8h" => [], 
                        "12h"=> []
                        )
end

mutable struct data_struct
    target_price::Dict{Any, Any}
    order_dict
    money::Float64
end

function get_ohlc(time_frame::String)
    ticker_list = get_tickers()
    result = Dict{String, Any}()
    for ticker in ticker_list
        ohlcv = fetch_ohlcv(ticker, time_frame, 3)
        result[ticker] = ohlcv
    end
    return result
end

function get_ohlc_Q(time_frame::String)
    ticker_list = get_tickers()
    result = Dict{String, Any}()
    for ticker in ticker_list
        # ohlcv = fetch_ohlcv(ticker, time_frame, 5)
        ohlcv = fetch_ohlcv(ticker, time_frame, 6+1) # last 6 days ohlcv
        result[ticker] = ohlcv
    end
    return result
end



function exit_side(data::data_struct, time_frame::Int64, double_ohlcv)
    utcurrentime = now(Dates.UTC)
    hours = parse(Int8, Dates.format(utcurrentime, "HH"))
    if hours%time_frame == 0
        for ticker in keys(data.order_dict)
            try
                create_order(ticker, "SELL", "MARKET", data.order_dict[ticker])
            catch e
                telegram_send("1_pivot_s2_all_H_trade_new_limit.jl exit_side error $(ticker) $(data.time_frame)h $(e)")
                sleep(1)
            end
        end
    end
end

function r2j(response)
    JSON.parse(String(response))
end

function ws_run(channel::Channel)
    try
        global BINANCE_API_WS

        # HTTP.WebSockets.open(string(BINANCE_API_WS, "!bookTicker"); verbose=false) do io
        HTTP.WebSockets.open(BINANCE_API_WS[1:end-1]; verbose=false) do io
            while !eof(io);
                put!(channel, r2j(readavailable(io)))
            end
        end
    catch e
        @info "reconnection at $(now(Dates.UTC)) cuz : $(e)"
        ws_run(channel)
    end
    @info "reconnection at $(now(Dates.UTC))"
    ws_run(channel)
end


function main()

    _1h_data = data_struct(data_init_P("1h", true), Dict(), 715)
    _6h_data = data_struct(data_init_P("6h", true), Dict(), 1100)

    _12h_data = data_struct(data_init_Q("12h"), Dict(), 200)

    ticker_list = get_tickers()

    data_channel = Channel(10000)
    @async ws_run(data_channel)

    while true
        @info "binance $(now(Dates.UTC))"
        while true
            minute = parse(Int8, Dates.format(now(Dates.UTC), "MM"))
            if minute == 59
                @async while true
                    if parse(Int8, Dates.format(now(Dates.UTC), "MM")) == 3
                        break
                    end
                    take!(data_channel)
                end
                sleep(60.5 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
                
                exit_side(_1h_data, 1, true)
                exit_side(_6h_data, 6, true)
                exit_side(_12h_data, 12, true)

                sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
                hours = parse(Int8, Dates.format(now(Dates.UTC), "HH"))
                if hours%12 == 0
                    @info "exit at $(now(Dates.UTC))"
                    exit()
                    #_12h_data.order_dict = Dict()
                    #_12h_data.target_price = data_init_Q("12h")
                end
                sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
                if hours%6 == 0
                    @info "half at $(now(Dates.UTC))"
                    _6h_data.order_dict = Dict()
                    _6h_data.target_price = data_init_P("6h", true)
                end
                sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
                
                @info "_1h_data_update $(now(Dates.UTC))"
                _1h_data.order_dict = Dict()
                _1h_data.target_price = data_init_P("1h", true)

                sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
                if hours == 0
                    exit()
                end
                break
            end      
            data = take!(data_channel)

            ticker = uppercase(split(data["stream"],"@")[1]) 

            #if !(ticker in ticker_list)
            #    continue
            #end

            price = parse(Float32, data["data"]["b"])
            time_ = data["data"]["T"]

            entry_side_P(_6h_data, price, ticker, time_)
            entry_side_Q(_12h_data,price, ticker, time_)
        end
    end
end

# BINANCE_API_WS = "wss://fstream.binance.com/ws/" # futures

BINANCE_API_WS = "wss://fstream.binance.com/stream?streams="

ticker_list = get_tickers()

for ticker in ticker_list
    global BINANCE_API_WS
    ticker = lowercase(ticker)
    BINANCE_API_WS *= "$(ticker)@bookTicker/"
end

# elastic_data_Q = [1+0.2*(i-1) for i in range(1,200)]
elastic_data_Q = [1+0.205*(i-1) for i in range(1,200)]

elastic_data_P = [0.0004, 0.0004, 0.0004, 0.0004, 0.0004, 0.0024, 0.0028, 0.0032, 0.0036, 0.004, 0.0044, 0.02, 0.0217, 0.0232, 0.0247, 0.0262, 0.0277, 0.0292, 0.0307, 0.0322, 0.0337, 0.0352, 0.0367, 0.0382, 0.0397, 0.196, 0.202, 0.208, 0.214, 0.22, 0.226, 0.232, 0.238, 0.244, 0.25, 0.256, 0.262, 0.268, 0.274, 0.28, 0.286, 0.292, 0.298, 0.304, 0.31, 0.316, 0.322, 0.328, 0.334, 0.34, 0.346, 0.352, 0.358, 0.364, 0.37, 0.376, 0.382, 0.388, 0.394, 0.4, 0.406, 0.412, 0.418, 0.424, 0.43, 0.436, 0.442, 0.448, 0.454, 0.46, 0.466, 0.472, 0.478, 0.484, 0.49, 0.496, 0.502, 0.508, 0.514, 0.52, 0.526, 0.532, 0.538, 0.544, 0.55, 0.556, 0.562, 0.568, 0.574, 0.58, 0.586, 0.592, 0.598, 0.604, 0.61, 0.616, 0.622, 0.628, 0.634, 0.64]
elastic_data_P = elastic_data_P .*1.5 .+1

main()



