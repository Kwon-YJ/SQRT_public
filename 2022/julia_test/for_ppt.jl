include("./utils.jl")

function log_maker(days, All_ohlcv, ticker_list)
    total_buy_sell_log = []
    buy_sell_log = []
    for day in days-4:-1:1
        println("\n$day")
        for (idx, ticker) in enumerate(ticker_list)
            A_candle, B_candle, C_candle, D_candle, target_candel = All_ohlcv[ticker][end-day-3:end-day+1]
            if A_candle[2] < A_candle[5]
                continue
            end
            if B_candle[2] > B_candle[5] || C_candle[2] > C_candle[5] || D_candle[2] > D_candle[5]
                continue
            end
            if A_candle[2] < D_candle[5]
                continue
            end
            earning = 100(target_candel[2]/target_candel[5]-1)
            println("$ticker : $(unix2datetime( (target_candel[1]+3600000*9) /1000)) $earning")
            push!(buy_sell_log, earning)
            push!(total_buy_sell_log, earning)
        end
        get_performance(buy_sell_log)
        empty!(buy_sell_log)
    end
    get_performance(total_buy_sell_log)
end

function main()
    ticker_list = get_tickers()
    All_ohlcv = Dict()
    backtest_boundaries = 200
    time_frame = "8h"
    for ticker in ticker_list
        ohlcv = fetch_ohlcv(ticker, time_frame, string(backtest_boundaries))
        if length(ohlcv) == backtest_boundaries
            All_ohlcv[ticker] = ohlcv
        end
    end
    log_maker(backtest_boundaries, All_ohlcv, keys(All_ohlcv))
end

main()




