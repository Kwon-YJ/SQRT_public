include("./../../2022/julia_test/utils.jl")


ticker_list = get_tickers()
current_price = get_current_price(ticker_list)
while true
    try
        minute = parse(Int8, Dates.format(now(Dates.UTC), "MM"))
        
        if minute == 59
            sleep(177)
        end

        global ticker_list
        global current_price
        current_price = get_current_price(ticker_list)
        sleep(0.1)
    catch
        telegram_send("data_loader error")
        sleep(180)
    end
end


