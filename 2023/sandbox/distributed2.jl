using Distributed

addprocs(4) 


@everywhere using Data_loader
@everywhere using strategy_1
@everywhere using strategy_2
@everywhere using strategy_3



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




result = remotecall_fetch(MyModule.myfunction, 2, args...)


