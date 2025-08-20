using Telegram, Telegram.API
using HTTP
import JSON
using Statistics
using Dates
using Nettle
using Formatting
using Logging


function get_current_price(option = "futures")
    url = "https://fapi.binance.com/fapi/v1/ticker/price"
    if cmp(option, "futures") != 0
        url = "https://api.binance.com/api/v3/ticker/price"
    end
    raw = HTTP.request("GET", url; verbose=0)
    json_data = JSON.parse(String(raw.body))
    Dict((ticker["symbol"], parse(Float64,ticker["price"])) for ticker in json_data if occursin("USDT", ticker["symbol"]) && occursin("_", ticker["symbol"])==false)
end

function precision_optimize(ticker::String, amount, price)
    market_info_row = HTTP.request("GET", "https://fapi.binance.com/fapi/v1/exchangeInfo"; verbose=0)
    market_info = JSON.parse(String(market_info_row.body))["symbols"]
    for values in market_info
        if values["symbol"] == ticker
            return round(amount, digits=values["quantityPrecision"]), round(price, digits=values["pricePrecision"])
        end
    end
end

function precision_optimize_spot(ticker::String, amount, price)
    market_info_row = HTTP.request("GET", "https://api.binance.com/api/v3/exchangeInfo"; verbose=0)
    market_info = JSON.parse(String(market_info_row.body))["symbols"]
    for values in market_info
        if values["symbol"] == ticker
            return round(amount, digits=values["quantityPrecision"]), round(price, digits=values["pricePrecision"])
        end
    end
end

function get_amount(ticker::String, money)
    price = fetch_ohlcv(ticker)[end][5]
    amount = money / price
    amount, price = precision_optimize(ticker, amount, price)
    if occursin("e", string(amount))
        amount = format(amount)
    end
    return amount, price
end

function get_amount_spot(ticker::String, money)
    price = fetch_ohlcv(ticker,"1m", 2, "", "", "spot")[end][5]
    amount = money / price
    amount, price = precision_optimize(ticker, amount, price)
    if occursin("e", string(amount))
        amount = format(amount)
    end
    return amount, price
end

function get_tickers()
    sever_time_raw = HTTP.request("GET", "https://fapi.binance.com/fapi/v1/time"; verbose=0)
    sever_time = JSON.parse(String(sever_time_raw.body))["serverTime"]
    url = "https://fapi.binance.com/fapi/v1/ticker/price"
    raw = HTTP.request("GET", url; verbose=0)
    json_data = JSON.parse(String(raw.body))
    [ticker["symbol"] for ticker in json_data if occursin("USDT", ticker["symbol"]) && occursin("_", ticker["symbol"]) == false && abs(sever_time-ticker["time"]) < 86400.00]
end

function get_tickers_spot(market)
    sever_time_raw = HTTP.request("GET", "https://fapi.binance.com/fapi/v1/time"; verbose=0)
    sever_time = JSON.parse(String(sever_time_raw.body))["serverTime"]
    url = "https://api.binance.com/api/v3/ticker/price"
    raw = HTTP.request("GET", url; verbose=0)
    json_data = JSON.parse(String(raw.body))
    raw_ticker_list = [ticker["symbol"] for ticker in json_data if cmp(ticker["symbol"][end-2:end], market) == 0]
    result = []
    for ticker in raw_ticker_list
        last_ticker_time = fetch_ohlcv(ticker, "1m", 30,"$(sever_time-3600000)","$(sever_time)","spot")
        if length(last_ticker_time) == 30
            push!(result, ticker)
        end
    end
    sleep(60 - parse(Int8, Dates.format(now(Dates.UTC), "SS")))
    return result
end


function fetch_ohlcv(ticker="BTCUSDT"::String,
                    interval="1m"::String, 
                    limit="605"::String, 
                    start_time=""::String, 
                    end_time=""::String, 
                    option="future"::String) 
    if cmp(option, "future") == 0
        base_url = "https://fapi.binance.com/fapi/v1/klines?symbol="
    else
        base_url = "https://api.binance.com/api/v3/klines?symbol="
    end
    if cmp(start_time, "") == 0 || cmp(end_time, "") == 0
        url = "$base_url$ticker&interval=$interval&limit=$limit"
    else
        url = "$base_url$ticker&interval=$interval&limit=$limit&startTime=$start_time&endTime=$end_time"
    end
    raw = HTTP.request("GET", url; verbose=0)
    ohlcv_string = JSON.parse(String(raw.body))
    ohlcv_float = [Array(map(x -> typecasting_support(x), ohlcv)) for ohlcv in ohlcv_string]
end


function typecasting_support(x)
    if typeof(x) == String
        parse(Float32, x)
    else
        x
    end
end

###################### [⬆️ public], [⬇️ private] ######################

function get_key(exchange)
    key_ring = Dict(
                    )
    return key_ring[exchange]
end

function get_server_time()
    sever_time_raw = HTTP.request("GET", "https://fapi.binance.com/fapi/v1/time"; verbose=0)
    JSON.parse(String(sever_time_raw.body))["serverTime"]
end

function fetch_available_balance(ticker, exchange = "binance")
    pub, sec = get_key(exchange)
    body = "&recvWindow=5000&timestamp=$(get_server_time())"
    signature = hexdigest("sha256", sec, body)
    url = "https://fapi.binance.com/fapi/v2/balance"
    headers = ["X-MBX-APIKEY" => pub]
    resp = HTTP.request("GET", "$url?$body&signature=$signature", headers=headers)
    result = JSON.parse(String(resp.body))
    for i=eachindex(result)
        if cmp(result[i]["asset"], ticker) == 0
            return parse(Float64, result[i]["maxWithdrawAmount"])
        end
    end
end

function cancel_order(ticker, order_id, exchange = "binance")
    pub, sec = get_key(exchange)
    body = "symbol=$ticker&orderId=$order_id&recvWindow=5000&timestamp=$(get_server_time())"
    signature = hexdigest("sha256", sec, body)
    url = "https://fapi.binance.com/fapi/v1/order"
    headers = ["X-MBX-APIKEY" => pub]
    resp = HTTP.request("DELETE", "$url?$body&signature=$signature", headers=headers)
    result = JSON.parse(String(resp.body))
end

function create_order(ticker, side, type, quantity, price="0", exchange = "binance")
    pub, sec = get_key(exchange)
    cmp(type, "LIMIT") == 0 ? body = "symbol=$ticker&side=$side&type=$type&timeInForce=GTC&quantity=$quantity&price=$price&recvWindow=5000&timestamp=$(get_server_time())" : body = "symbol=$ticker&side=$side&type=$type&quantity=$quantity&recvWindow=5000&timestamp=$(get_server_time())"
    signature = hexdigest("sha256", sec, body)
    url = "https://fapi.binance.com/fapi/v1/order"
    headers = ["X-MBX-APIKEY" => pub]
    resp = HTTP.request("POST", "$url?$body&signature=$signature", headers=headers)
    JSON.parse(String(resp.body))
end

function transfer_coin(from, to, coin, amount, exchange = "binance")
    pub, sec = get_key(exchange)
    type = 0
    if from=="spot" && to=="futures"
        type=1
    elseif from=="futures" && to=="spot"
        type=2
    elseif from=="spot" && to=="coin-m"
        type=3
    elseif from=="coin-m" && to=="spot"
        type=4
    else
        error("""Invalid specification: enter valid parameters for "from" and "to", example: from="spot", to="coin-m" """)
    end
    body = "&recvWindow=5000&asset=$(coin)&amount=$(amount)&type=$(type)&timestamp=$(get_server_time())"
    signature = hexdigest("sha256", sec, body)
    url = "https://api.binance.com/sapi/v1/futures/transfer"
    headers = ["X-MBX-APIKEY" => pub]
    resp = HTTP.request("POST", "$url?$body&signature=$signature", headers=headers)
    JSON.parse(String(resp.body))
end

function cancel_all(ticker, exchange = "binance")
    pub, sec = get_key(exchange)
    body = "symbol=$ticker&recvWindow=5000&timestamp=$(get_server_time())"
    signature = hexdigest("sha256", sec, body)
    url = "https://fapi.binance.com/fapi/v1/allOpenOrders"
    headers = ["X-MBX-APIKEY" => pub]
    resp = HTTP.request("DELETE", "$url?$body&signature=$signature", headers=headers)
    result = JSON.parse(String(resp.body))
end

function check_order(ticker, orderid, exchange = "binance")
    pub, sec = get_key(exchange)
    body = "symbol=$ticker&orderId=$orderid&recvWindow=5000&timestamp=$(get_server_time())"
    signature = hexdigest("sha256", sec, body)
    url = "https://fapi.binance.com/fapi/v1/order"
    headers = ["X-MBX-APIKEY" => pub]
    resp = HTTP.request("GET", "$url?$body&signature=$signature", headers=headers)
    result = JSON.parse(String(resp.body))
end

function fetch_spot_balance(ticker, exchange = "binance")
    pub, sec = get_key(exchange)
    body = "recvWindow=5000&timestamp=$(get_server_time())"
    signature = hexdigest("sha256", sec, body)
    url = "https://api.binance.com/sapi/v3/asset/getUserAsset"
    headers = ["X-MBX-APIKEY" => pub]
    resp = HTTP.request("POST", "$url?$body&signature=$signature", headers=headers)
    json_result = JSON.parse(String(resp.body))
    for dict_ in json_result
        if cmp(dict_["asset"], ticker) == 0
            return parse(Float64, dict_["free"])
        end
    end
end

function create_order_spot(ticker, side, type, quantity, price="0", exchange = "binance")
    pub, sec = get_key(exchange)  
    cmp(type, "LIMIT") == 0 ? body = "symbol=$ticker&side=$side&type=$type&timeInForce=GTC&quantity=$quantity&price=$price&recvWindow=5000&timestamp=$(get_server_time())" : body = "symbol=$ticker&side=$side&type=$type&quantity=$quantity&recvWindow=5000&timestamp=$(get_server_time())"
    signature = hexdigest("sha256", sec, body)
    url = "https://api.binance.com/api/v3/order"
    headers = ["X-MBX-APIKEY" => pub]
    resp = HTTP.request("POST", "$url?$body&signature=$signature", headers=headers)
    JSON.parse(String(resp.body))
end

