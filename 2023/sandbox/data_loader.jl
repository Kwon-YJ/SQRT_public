include("./../../2022/julia_test/utils.jl")
using Distributed
addprocs(1)


function get_ohlc(time_frame::String)
    global ticker_list
    result = Dict{String, Any}()
    for ticker in ticker_list
        ohlcv = fetch_ohlcv(ticker, time_frame, 45)
        if length(ohlcv) !=45
            continue
        end
        result[ticker] = ohlcv
    end
    return result
end

all_ohlcv = Dict()

hours = parse(Int8, Dates.format(now(Dates.UTC), "HH"))
all_ohlcv["1h"] = get_ohlc("1h")


if hours%2 == 0
    all_ohlcv["2h"] = get_ohlc("2h")
end
if hours%4 == 0
    all_ohlcv["4h"] = get_ohlc("4h")
end
if hours%6 == 0
    all_ohlcv["6h"] = get_ohlc("6h")
end
if hours%8 == 0
    all_ohlcv["8h"] = get_ohlc("8h")
end
if hours%12 == 0
    all_ohlcv["12h"] = get_ohlc("12h")
end

@everywhere @eval all_ohlcv = $all_ohlcv

println(ticker_list)

println(all_ohlcv["12h"]["XRPUSDT"][end])


