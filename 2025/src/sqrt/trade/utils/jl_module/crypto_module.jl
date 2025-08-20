using Statistics
using DataFrames
using CSV
using Dates
using ArgParse
include("utils.jl")




function get_all_ohlcv(ticker::String, start_time::String, end_time::String, time_frame)
    # sleep(0.0495)
    sleep(0.0101)

    interval = 499

    new_ohlcv = fetch_ohlcv(ticker, time_frame, "$(interval)" , start_time, end_time, "spot")
    new_ohlcv = [ohlc[1:6] for ohlc in new_ohlcv]
    new_start = string(new_ohlcv[end][1])

    if cmp(end_time, new_start) == 0
        df = DataFrame(Time=Float64[], Name=[] ,Temperature1=Float32[], Temperature2=Float32[], Temperature3=Float32[], Temperature4=Float32[], Temperature5=[])
        for row in new_ohlcv[2:end]
            # push!(df, (row[1], row[2], row[3], row[4], row[5], unix2datetime(row[1] / 1000)))
            push!(df, (row[1], ticker, row[2], row[3], row[4], row[5], row[6]))
        end
        CSV.write("./data/binance/$(time_frame)/$(ticker)_$(time_frame).csv", df, append=true)
        println("finish1 " * "$(ticker)_$(time_frame).csv")
    else
        df = DataFrame(Time=Float64[], Name=[] ,Temperature1=Float32[], Temperature2=Float32[], Temperature3=Float32[], Temperature4=Float32[], Temperature5=[])
        for row in new_ohlcv[2:end]
            # push!(df, (row[1], row[2], row[3], row[4], row[5], unix2datetime(row[1] / 1000)))
            push!(df, (row[1], ticker, row[2], row[3], row[4], row[5], row[6]))
        end

        CSV.write("./data/binance/$(time_frame)/$(ticker)_$(time_frame).csv", df, append=true)

        if length(new_ohlcv[2:end]) < interval -1
            df = DataFrame(Time=Float64[], Name=[] ,Temperature1=Float32[], Temperature2=Float32[], Temperature3=Float32[], Temperature4=Float32[], Temperature5=[])
            for row in new_ohlcv[2:end]
                # push!(df, (row[1], row[2], row[3], row[4], row[5], unix2datetime(row[1] / 1000)))
                push!(df, (row[1], ticker, row[2], row[3], row[4], row[5], row[6]))
            end
            CSV.write("./data/binance/$(time_frame)/$(ticker)_$(time_frame).csv", df, append=true)
            println("finish2 " * "$(ticker)_$(time_frame).csv")
            return nothing
        end

        try
            get_all_ohlcv(ticker, new_start, end_time, time_frame)
        catch e
            println("finish2 " * "$(ticker)_$(time_frame).csv \n $(e)")
        end
    end
end


function parse_commandline()
    s = ArgParseSettings()
    ArgParse.@add_arg_table s begin
        "--ticker"
        help = "ticker select"
        required = true
        arg_type = String
        default = ""
    end
    return parse_args(s)

end


args = parse_commandline()


# time_frames = ["1m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d"]
# time_frames = ["12h", "1d", "3d"]
time_frames = ["1m"]

mkdir_exist_ok("./data/binance")

_ = [mkdir_exist_ok("./data/binance/$(time_frame)") for time_frame in time_frames]





end_time = "$(fetch_ohlcv("BTCUSDT", "1d", "5")[end][1])"
start_time = "$(fetch_ohlcv("BTCUSDT", "1w", "1000")[1][1])"

for time_frame in time_frames
    get_all_ohlcv(args["ticker"], start_time, end_time, time_frame)
end


