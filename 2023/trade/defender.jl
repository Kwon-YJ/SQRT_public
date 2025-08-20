using HTTP
import JSON
using Nettle
include("./../../2022/julia_test/utils.jl")

while true
    sleep(10)
    utcurrentime = now(Dates.UTC)
    hours = parse(Int8, Dates.format(utcurrentime, "HH"))
    minute = parse(Int8, Dates.format(utcurrentime, "MM"))
    if hours==0 && minute==3 # UTC 기준 00:03분 
        sleep(30)

        base_line = 2000

        try 
            f_bnb = fetch_available_balance("BNB")
            f_usdt = fetch_available_balance("USDT")
            bnb = fetch_spot_balance("BNB")
            usdt = fetch_spot_balance("USDT")
            margin = trunc(Int, f_usdt-base_line)
            if f_usdt > base_line+1
                #telegram_send("You got $(margin)usdt yesterday.")
                # println("You got $(margin)usdt yesterday.")
                transfer_coin("futures", "spot", "USDT", margin)
            else
                #telegram_send("You lose $(margin)usdt yesterday.")
                # println("You lose $(margin)usdt yesterday.")
                sleep(1)
            end
            if usdt < fetch_ohlcv("BNBUSDT", "1m", 2)[end][5] * 0.11
                #telegram_send("WARNING : Not Enough Minerals!")
                # println("WARNING : Not Enough Minerals!")
                sleep(31)
                exit()
            end
            if bnb < 0.05
                create_order_spot("BNBUSDT", "BUY", "MARKET", 0.05)
            end
            
            if f_bnb < 0.05
                create_order_spot("BNBUSDT", "BUY", "MARKET", 0.05)
                transfer_coin("spot", "futures", "BNB", 0.05)
            end
        catch
            sleep(31)
            telegram_send("WARNING : The defender is broken")
        end
        sleep(3600 * 24 - 200)
    end
end
