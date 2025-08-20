include("pivot.jl")
import .Pivot
import JSON
using Dates
using HTTP
using HTTP.WebSockets: open, send, receive



function run_ws(channel::Channel, url, batch_num)
    while true
        sleep(0.01)
        try
            open(url[1:end-1], suppress_close_error=true) do ws
                @info "Binance WebSocket에 연결되었습니다. batch_num : $(batch_num), (UTC $(now(Dates.UTC)))"
                for msg in ws
                    data = JSON.parse(String(msg))
                    put!(channel, data)
                end
            end
        catch e
            @info "재연결 시도 $(batch_num)번 웹소켓 (UTC $(now(Dates.UTC)))"
        end
    end
end


# 실제로 멈추는 건 아니고, 해당 구간 동안 수신된 모든 데이터를 그냥 버림 (지연 방지)
function pause_ws()
    while true
        if parse(Int8, Dates.format(now(Dates.UTC), "MM")) == 2
            break
        end
        take!(data_channel)
    end
end


function get_ws_url(ticker_list)
    BINANCE_API_WS = "wss://fstream.binance.com/stream?streams="
    for ticker in ticker_list
        ticker = lowercase(ticker)
        BINANCE_API_WS *= "$(ticker)@bookTicker/"
    end
    return BINANCE_API_WS
end

function main()
    data_channel = Channel(10000)
    ticker_list = Pivot.all_ticker_list["pivot"]["all"]

    @async run_ws(data_channel, get_ws_url(ticker_list), 1)

    temp_dict = Dict() # verbose

    pivot_dict = Pivot.get_pivot_dict()
    @info("(UTC $(now(Dates.UTC))) pivot_dict $(pivot_dict)") # verbose


    while true
        verbose = false
        minute = parse(Int8, Dates.format(now(Dates.UTC), "MM"))
        if minute == 59
            @async pause_ws()
            sleep(60.5 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
            pivot_dict = Pivot.exit_side(pivot_dict)
            @info("(UTC $(now(Dates.UTC))) pivot_dict $(pivot_dict)") # verbose
        end
        data = take!(data_channel)
        ticker = uppercase(split(data["stream"], "@")[1])
        price = parse(Float32, data["data"]["b"])
        time_ = data["data"]["T"]

        # println(data)
        # dt = DateTime(1970, 1, 1) + Millisecond(time_)
        # println(dt)


        # verbose >>
        if haskey(temp_dict, ticker)
            if temp_dict[ticker] > price
                temp_dict[ticker] = price
                @info("(UTC $(now(Dates.UTC))) UPDATE $(ticker) $(price)")
                @info(temp_dict)
                verbose = true
            end
        else
            temp_dict[ticker] = price
            @info("(UTC $(now(Dates.UTC))) ADD $(ticker) $(price)")
            @info(temp_dict)
            verbose = true
        end
        # verbose <<

        pivot_dict = Pivot.entry_side(pivot_dict, price, ticker, time_, verbose)
    end
end

main()


