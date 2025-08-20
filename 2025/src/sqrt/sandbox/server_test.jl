using HTTP
import JSON

function use_ccxt(params::Dict)
    url = "http://127.0.0.1:8000/"
    resp = HTTP.get(url; query=params)
    if resp.status == 200
        return JSON.parse(String(resp.body))
    else
        error("HTTP request failed with status $(resp.status): $(String(resp.body))")
    end
end

# params = Dict(
#     "exchange" => "binance_future",
#     "method" => "fetch_ohlcv",
#     "args" => "'BTCUSDT','1h',1750550400000,960"
# )
# println(length(use_ccxt(params)))

params = Dict(
    "exchange" => "gateio_future",
    "method" => "fetch_ohlcv",
    "args" => "('1INCH/USDT','1w')",
    "kwargs" => "{'limit': 960}"
)

temp_ = use_ccxt(params)
println(temp_)
println(length(temp_))


# function get_tickers_listed_over_1year(exchange::String)
#     function USDT_filter(data)
#         return [x for x in data if x[end-3:end] == "USDT"]
#     end

#     function time_filter(data)
#         filter_result = []
#         params = Dict(
#             "exchange" => exchange,
#             "method" => "fetch_ohlcv",
#         )
#         option = split(exchange, "_")[end]
#         if option=="future"
#             params["args"] = "('BTC/USDT:USDT','1w')"
#         else
#             params["args"] = "('BTC/USDT','1w')"
#         end
#         last_time = use_ccxt(params)[end][1]
#         for ticker in data
#             params["args"] = "('$(ticker)','1w')"
#             ohlcv = use_ccxt(params)
#             if length(ohlcv) > 60 && last_time == ohlcv[end][1]
#                 push!(filter_result, ticker)
#             end
#         end
#         return filter_result
#     end
#     all_tikcer_data = use_ccxt(Dict("exchange" => exchange, "method" => "fetch_tickers"))
#     return all_tikcer_data |> keys |> USDT_filter |> time_filter
# end

# println(get_tickers_listed_over_1year("gateio_future"))
