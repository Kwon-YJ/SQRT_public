using Dates
include("./../../2022/julia_test/utils.jl")

function get_ohlc(time_frame::String)
    ticker_list = get_tickers()
    result = Dict{String, Any}()
    for ticker in ticker_list
        ohlcv = fetch_ohlcv(ticker, time_frame, 200)
        result[ticker] = ohlcv
    end
    return result
end

Moving_average(var, n::Int64) = [sum(@view var[i:(i+n-1)]) / n for i in 1:(length(var) - (n - 1))]

True_range(ohlcv) = [(i == 1) ? var[3] - var[4] : maximum([var[3] - var[4], abs(var[3] - ohlcv[i-1][5]), abs(var[4] - ohlcv[i-1][5])]) for (i, var) in enumerate(ohlcv)]

function rma(data::Vector{T}, period::Int) where T
    alpha = 1 / period
    ema_values = similar(data, T)
    sma = sum(@view data[1:period]) / period
    ema_values[period] = sma
    @fastmath @simd for i in (period+1):length(data)
        ema_values[i] = (data[i] - ema_values[i-1]) * alpha + ema_values[i-1]
    end
    return ema_values
end

function rsi(data::Vector{T}, period::Int) where T
    delta = diff(data)
    gain = [max(delta[i], 0) for i in 1:length(delta)]
    loss = [max(-delta[i], 0) for i in 1:length(delta)]
    avg_gain = rma(gain, period)
    avg_loss = rma(loss, period)
    rs = avg_gain ./ avg_loss
    rsi_values = 100 .- (100 ./ (1 .+ rs))
    return rsi_values
end


function main()

    ticker_list = get_tickers()

    order_dict = Dict()

    while true
        sleep(0.5)
        minute = parse(Int8, Dates.format(now(Dates.UTC), "MM"))
        if minute%5 == 0
            all_ohlcv = get_ohlc("5m")

            # exit
            for ticker ∈ keys(order_dict)
                ohlcv = all_ohlcv[ticker][1:end-1]
                close = map(x -> x[5], ohlcv)
                ma = Moving_average(close, 20)[end]
                tr2 = (Moving_average(True_range(ohlcv), 4) .* 1.5)[end]
                exit_target = ma + tr2
                if exit_target < (ohlcv[end][2] + ohlcv[end][5]) / 2
                    try
                        create_order(ticker, "SELL", "MARKET", order_dict[ticker])
                        pop!(order_dict, ticker)
                    catch e
                        telegram_send("5m_long.jl exit_side error $(ticker) $(e)")
                        sleep(1)
                    end
                end
            end

            # entry 
            for ticker ∈ setdiff!(ticker_list, keys(order_dict))
                ohlcv = all_ohlcv[ticker][1:end-1]
                rsi_ = rsi(map(x -> x[3], ohlcv), 15)[end]
                if rsi_ < 7
                    # trade_amount, price = get_amount(ticker, 300)
                    trade_amount, price = get_amount(ticker, 30)
                    create_order(ticker, "BUY", "MARKET", trade_amount, price)
                    order_dict[ticker] = trade_amount   
                    @async println(ticker)
                    @async println("$(unix2datetime(time_data/1000))")
                    @async println(now(Dates.UTC))
                end

            end
            sleep(61)
        end
    end
end


main()



