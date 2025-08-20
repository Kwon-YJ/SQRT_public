using Dates
include("./../../2022/julia_test/utils.jl")

using Base.Threads

function r2j(response)
    JSON.parse(String(response))
end

function ws_run(channel::Channel)
    HTTP.WebSockets.open(string(BINANCE_API_WS, "!bookTicker"); verbose=false) do io
        while !eof(io);
            # put!(channel, r2j(readavailable(io)))
            print(r2j(readavailable(io))["T"])
        end
    end
end

BINANCE_API_WS = "wss://fstream.binance.com/ws/"

data_channel = Channel(10000)
ws_run(data_channel)

