using Statistics
using DataFrames
using CSV
using Dates
using ArgParse
include("../../../../2022/julia_test/utils.jl")





function get_all_ohlcv(ticker::String, start_time::String, end_time::String, time_frame::String, save_path::String)
    #=
    save_dir = "./"
    end_time = "$(fetch_ohlcv("BTCUSDT", "1d", "5")[end][1])" 
    start_time = "$(fetch_ohlcv("BTCUSDT", "1w", "1000")[1][1])" 
    =#

    if cmp(start_time, "") == 0
        start_time = "$(fetch_ohlcv("BTCUSDT", "1w", "1000")[1][1])"
    end

    if cmp(end_time, "") == 0
        end_time = "$(fetch_ohlcv("BTCUSDT", "1d", "5")[end][1])"
    end

    function csv_save(new_ohlcv)
        df = DataFrame(Time=Float64[], Temperature1=Float32[], Temperature2=Float32[], Temperature3=Float32[], Temperature4=Float32[], Temperature5=[])
        for row in new_ohlcv[2:end]
            push!(df, (row[1], row[2], row[3], row[4], row[5], unix2datetime(row[1] / 1000)))
        end
        CSV.write("save_path/$(time_frame)/$(ticker)_$(time_frame).csv", df, append=true)
    end

    sleep(0.2)
    new_ohlcv = fetch_ohlcv(ticker, time_frame, "1500", start_time, end_time)
    new_ohlcv = [ohlc[1:5] for ohlc in new_ohlcv]
    new_start = string(new_ohlcv[end][1])

    csv_save(new_ohlcv)
    if cmp(end_time, new_start) == 0
        println("finish1 " * "$(ticker)_$(time_frame).csv")
        return nothing
    elseif length(new_ohlcv[2:end]) < 1450
        println("finish2 " * "$(ticker)_$(time_frame).csv")
        return nothing
    else
        try
            get_all_ohlcv(ticker, new_start, end_time, time_frame, save_path)
        catch e
            println("finish2 " * "$(ticker)_$(time_frame).csv")
        end
    end
end





# get_all_ohlcv(args["ticker"], start_time, end_time, time_frame, save_dir)





get_all_ohlcv("BTCUSDT", start_time, end_time, "1d", "./")



