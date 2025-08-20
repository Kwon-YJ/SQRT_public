using Dates
using Logging
include("./../../2022/julia_test/utils.jl")
Logging.global_logger(ConsoleLogger(stderr, Logging.Debug))


function is_bullish_candle(data)
    if data[5] > data[2]
        return true
    else
        return false
    end
end

function main()
    time_frame = "1d"
    ticker_list = ["ALTUSDT", "SANDUSDT", "ZETAUSDT", "MAVIAUSDT", "WUSDT"]

    [fetch_ohlcv(x) for x in ticker_list] # validation ticker_name

    budget = 400
    while true
        wait_next_day()
        sleep(120 - parse(Int8, Dates.format(now(Dates.UTC), "SS"))) # Maybe pass at UTC 00:01:00
        for ticker in ticker_list
            ohlcv = fetch_ohlcv(ticker, time_frame, 3)
            if is_bullish_candle(ohlcv[2]) # is yesterday bullish_candle?
                trade_amount, price = get_amount(ticker, budget)
                response = create_order(ticker, "SELL", "MARKET", trade_amount, price)
                if response == false
                    msg = "partial_short.jl error in entry order $(ticker) $(response)"
                    @info msg
                    telegram_send(msg)
                    continue
                end
                exit_price = minimum([ohlcv[1][4], ohlcv[2][4]])
                response = create_order(ticker, "BUY", "LIMIT", trade_amount, exit_price)
                if response == false
                    msg = "partial_short.jl error in exit order $(ticker) $(response)"
                    @info msg
                    telegram_send(msg)
                    continue
                end
            end
        end
    end
end


main()



