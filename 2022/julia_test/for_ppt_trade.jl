using Dates
include("./utils.jl")

function main()
    orderd_dict = Dict()
    while true
        sleep(60)
        utcurrentime = now(Dates.UTC)
        hours = parse(Int8, Dates.format(utcurrentime, "HH"))
        # UTC 기준 8시간 마다
        if hours==17 && hours==1 && hours==9
            println(utcurrentime)
            all_ticker_price = get_current_price()
            for ticker in keys(orderd_dict)
                create_order(ticker, "BUY", "MARKET",orderd_dict[ticker])
                price = all_ticker_price[ticker]
                println("$ticker // exit price : $price ")
            end
            orderd_dict = Dict()
            ticker_list = get_tickers()
            for ticker in ticker_list
                ohlcv = fetch_ohlcv(ticker, "8H", "5")
                if length(ohlcv) != 5
                    continue
                end
                A_candle, B_candle, C_candle, D_candle, target_candel = ohlcv[ticker:end-1]
                if A_candle[2] < A_candle[5]
                    continue
                end
                if B_candle[2] > B_candle[5] || C_candle[2] > C_candle[5] || D_candle[2] > D_candle[5]
                    continue
                end
                if A_candle[2] < D_candle[5]
                    continue
                end
                trade_amount, price = get_amount(ticker)
                println(ticker," // " ,maximum(highs[end-(interval-1):end-1]), " // " ,ohlcv[end][5])
                order_resp = create_order(ticker, "SELL", "MARKET", trade_amount, price)
                orderd_dict[ticker] = order_resp["origQty"]
            end
        else
            continue
        end
        
    end
end

# main()
