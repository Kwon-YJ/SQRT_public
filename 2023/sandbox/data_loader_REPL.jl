include("./../../2022/julia_test/utils.jl")

ticker_list = get_current_price_old()
while true
    minute = parse(Int8, Dates.format(now(Dates.UTC), "MM"))
    if minute == 59
        sleep()
    end
    global ticker_list
    ticker_list = get_current_price_old()
end

