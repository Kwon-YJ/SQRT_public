using HTTP
import JSON
using Statistics
using Dates
include("./../../2022/julia_test/utils.jl")

using Random

All_ohlcv = Dict()
limit = 40
ticker = "BNBUSDT"




function _1d_calc()  
    ohlcvs = fetch_ohlcv(ticker, "1d", 40)

    result = []

    win = 0
    lose = 0

    for ohlcv in ohlcvs
        if ohlcv[5] > ohlcv[2]
            win += 1
            push!(result, true)
        elseif ohlcv[5] < ohlcv[2]
            lose += 1
            push!(result, false)
        end
    end

    println("total : $(win + lose)")
    println("winrate : $(win/(win+lose)*100)%")
    println("win : $(win)")
    println("lose : $(lose)")

    println("")

    new_win = 0
    new_lose= 0

    for (i, ohlcv) in enumerate(ohlcvs) 
        if i == 1
            continue
        end

        if ohlcvs[i-1][5] < ohlcvs[i-1][2]
            if ohlcv[5] > ohlcv[2]
                new_win += 1
            elseif ohlcv[5] < ohlcv[2]
                new_lose += 1
            end
        end
    end

    println("total : $(new_win + new_lose)")
    println("winrate : $(new_win/(new_win+new_lose)*100)%")
    println("new_win : $(new_win)")
    println("new_lose : $(new_lose)")

    println("")

    return result

end



_1d_data = _1d_calc()


function _12_calc(data)  
    ohlcvs = fetch_ohlcv(ticker, "12h", 80)

    result = []

    win = 0
    lose = 0

    for ohlcv in ohlcvs
        if ohlcv[5] > ohlcv[2]
            win += 1
            push!(result, true)
        elseif ohlcv[5] < ohlcv[2]
            lose += 1
            push!(result, false)
        end
    end

    println("total : $(win + lose)")
    println("winrate : $(win/(win+lose)*100)%")
    println("win : $(win)")
    println("lose : $(lose)")

    println("")

    new_win = 0
    new_lose= 0

    for (i, ohlcv) in enumerate(ohlcvs) 
        if i == 1
            continue
        end

        if ohlcvs[i-1][5] < ohlcvs[i-1][2]
            if ohlcv[5] > ohlcv[2]
                new_win += 1
            elseif ohlcv[5] < ohlcv[2]
                new_lose += 1
            end
        end
    end

    println("total : $(new_win + new_lose)")
    println("winrate : $(new_win/(new_win+new_lose)*100)%")
    println("new_win : $(new_win)")
    println("new_lose : $(new_lose)")

    println("")


    new_win = 0
    new_lose= 0

    for (i, ohlcv) in enumerate(ohlcvs) 
        if i < 3
            continue
        end

        if ohlcvs[i-1][5] < ohlcvs[i-1][2] && data[round(Int, i*0.5)-1] == true
            if ohlcv[5] > ohlcv[2]
                new_win += 1
            elseif ohlcv[5] < ohlcv[2]
                new_lose += 1
            end
        end
    end

    println("total : $(new_win + new_lose)")
    println("winrate : $(new_win/(new_win+new_lose)*100)%")
    println("new_win : $(new_win)")
    println("new_lose : $(new_lose)")

    println("")

    return result

end


_12_data = _12_calc(_1d_data)

