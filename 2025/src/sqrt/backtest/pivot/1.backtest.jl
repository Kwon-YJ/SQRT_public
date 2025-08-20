# nohup nice -n 10 julia 1.backtest.jl bybit_future > out.log 2>&1 &

include("../../utils/utils.jl")
include("backtest_module.jl")

function main(time_frame, option)
    exchange = ARGS[1]
    ticker_list = sort(get_tickers_listed_over_1year(exchange))
    for ticker in ticker_list
        # main_module("future", "USDT", time_frame, option, ticker)
        main_module(exchange, "future", "USDT", time_frame, option, ticker)
    end
    run(`mkdir $(time_frame)_$(option)`)
    run(`sh -c "mv *.txt './$(time_frame)_$(option)'"`)
end


time_frames = ["1h", "2h", "4h", "6h", "8h", "12h"]

option = "default"
for time_frame in time_frames
    main(time_frame, option)
end

option = "double"
for time_frame in time_frames
    main(time_frame, option)
end




