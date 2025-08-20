using HTTP
import JSON
using Statistics
using Dates
using Pickle
include("./../../2022/julia_test/utils.jl")


function get1440(ticker::String, start_time::String, end_time::String, result=[])
    # sleep(0.69)
    sleep(0.188)
    new_ohlcv = fetch_ohlcv(ticker,"1m","1440",start_time,end_time)
    # new_ohlcv = [ohlc[1:5] for ohlc in new_ohlcv]
    new_start = string(new_ohlcv[end][1] + 60)
    new_ohlcv = [[ohlc[1], ohlc[5]] for ohlc in new_ohlcv]

    if cmp(end_time, new_start) == 0
        return result
    else
        push!(result, new_ohlcv)
        
        try
            get1440(ticker, new_start, end_time, result)
        catch e
            pop!(result)
            return result
        end  
    end
end




function make_pickle(start_time, end_time, file_name)
    temp_ticker_list = get_tickers()
    ticker_list = []

    std_len = length(fetch_ohlcv("BTCUSDT", "1d", 100, start_time, end_time))

    for ticker in temp_ticker_list
        if length(fetch_ohlcv(ticker, "1d", 1000, start_time, end_time)) == std_len
            push!(ticker_list, ticker)
        end
    end

    sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
    All_ohlcv = Dict()
    for (i, ticker) in enumerate(ticker_list)
        println(i, " ", ticker)
        All_ohlcv[ticker] = get1440(ticker, start_time, end_time)
    end
    # store("./test.pkl", All_ohlcv)
    store(file_name, All_ohlcv)
end


#=
# 23년 7월
start_time = "1688169600000"
end_time = "1690848000000"

@time make_pickle(start_time, end_time, "./23_07.pkl")

# 23년 6월

start_time = "1685545200000"
end_time = "1688169600000"

@time make_pickle(start_time, end_time, "./23_06.pkl")

# 23년 5월 
start_time = "1682866800000"
end_time = "1685545200000"
@time make_pickle(start_time, end_time, "./23_5.pkl")

# 23년 4월 
start_time = "1680274800000"
end_time = "1682866800000"
@time make_pickle(start_time, end_time, "./23_4.pkl")

# 23년 3월 
start_time = "1677596400000"
end_time = "1680274800000"
@time make_pickle(start_time, end_time, "./23_3.pkl")

# 23년 2월 
start_time = "1675177200000"
end_time = "1677596400000"
@time make_pickle(start_time, end_time, "./23_2.pkl")

# 23년 1월 
start_time = "1672498800000"
end_time = "1675177200000"
@time make_pickle(start_time, end_time, "./23_1.pkl")



# 22년 8월 
start_time = "1659279600000"
end_time = "1661958000000"
@time make_pickle(start_time, end_time, "./22_8.pkl")

# 22년 7월 
start_time = "1656601200000"
end_time = "1659279600000"
@time make_pickle(start_time, end_time, "./22_7.pkl")

# 22년 6월 
start_time = "1654009200000"
end_time = "1656601200000"
@time make_pickle(start_time, end_time, "./22_6.pkl")

# 22년 5월 
start_time = "1651330800000"
end_time = "1654009200000"
@time make_pickle(start_time, end_time, "./22_5.pkl")

# 22년 4월 
start_time = "1648738800000"
end_time = "1651330800000"
@time make_pickle(start_time, end_time, "./22_4.pkl")

# 22년 3월 
start_time = "1646060400000"
end_time = "1648738800000"
@time make_pickle(start_time, end_time, "./22_3.pkl")

# 22년 2월 
start_time = "1643641200000"
end_time = "1646060400000"
@time make_pickle(start_time, end_time, "./22_2.pkl")

# 22년 1월 
start_time = "1640962800000"
end_time = "1643641200000"
@time make_pickle(start_time, end_time, "./22_1.pkl")

# 21년 12월 
start_time = "1638284400000"
end_time = "1640962800000"
@time make_pickle(start_time, end_time, "./21_12.pkl")
=#

# 21년 11월 
start_time = "1635692400000"
end_time = "1638284400000"
@time make_pickle(start_time, end_time, "./21_11.pkl")

# 21년 10월 
start_time = "1633014000000"
end_time = "1635692400000"
@time make_pickle(start_time, end_time, "./21_10.pkl")

# 21년 9월 
start_time = "1630422000000"
end_time = "1633014000000"
@time make_pickle(start_time, end_time, "./21_9.pkl")

# 21년 8월 
start_time = "1627743600000"
end_time = "1630422000000"
@time make_pickle(start_time, end_time, "./21_8.pkl")

# 21년 7월 
start_time = "1625065200000"
end_time = "1627743600000"
@time make_pickle(start_time, end_time, "./21_7.pkl")

# 21년 6월 
start_time = "1622473200000"
end_time = "1625065200000"
@time make_pickle(start_time, end_time, "./21_6.pkl")

# 21년 5월 
start_time = "1619794800000"
end_time = "1622473200000"
@time make_pickle(start_time, end_time, "./21_5.pkl")

# 21년 4월 
start_time = "1617202800000"
end_time = "1619794800000"
@time make_pickle(start_time, end_time, "./21_4.pkl")

# 21년 3월 
start_time = "1614524400000"
end_time = "1617202800000"
@time make_pickle(start_time, end_time, "./21_3.pkl")

# 21년 2월 
start_time = "1612105200000"
end_time = "1614524400000"
@time make_pickle(start_time, end_time, "./21_2.pkl")

# 21년 1월 
start_time = "1609426800000"
end_time = "1612105200000"
@time make_pickle(start_time, end_time, "./21_1.pkl")

# 20년 12월 
start_time = "1606748400000"
end_time = "1609426800000"
@time make_pickle(start_time, end_time, "./20_12.pkl")

# 20년 11월 
start_time = "1604156400000"
end_time = "1606748400000"
@time make_pickle(start_time, end_time, "./20_11.pkl")

# 20년 10월 
start_time = "1601478000000"
end_time = "1604156400000"
@time make_pickle(start_time, end_time, "./20_10.pkl")

# 20년 9월 
start_time = "1598886000000"
end_time = "1601478000000"
@time make_pickle(start_time, end_time, "./20_9.pkl")

# 20년 8월 
start_time = "1596207600000"
end_time = "1598886000000"
@time make_pickle(start_time, end_time, "./20_8.pkl")

# 20년 7월 
start_time = "1593529200000"
end_time = "1596207600000"
@time make_pickle(start_time, end_time, "./20_7.pkl")

# 20년 6월 
start_time = "1590937200000"
end_time = "1593529200000"
@time make_pickle(start_time, end_time, "./20_6.pkl")

# 20년 5월 
start_time = "1588258800000"
end_time = "1590937200000"
@time make_pickle(start_time, end_time, "./20_5.pkl")

# 20년 4월 
start_time = "1585666800000"
end_time = "1588258800000"
@time make_pickle(start_time, end_time, "./20_4.pkl")

# 20년 3월 
start_time = "1582988400000"
end_time = "1585666800000"
@time make_pickle(start_time, end_time, "./20_3.pkl")

# 20년 2월 
start_time = "1580482800000"
end_time = "1582988400000"
@time make_pickle(start_time, end_time, "./20_2.pkl")

# 20년 1월 
start_time = "1577804400000"
end_time = "1580482800000"
@time make_pickle(start_time, end_time, "./20_1.pkl")