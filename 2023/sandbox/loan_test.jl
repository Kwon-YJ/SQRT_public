using Dates
include("./../../2022/julia_test/utils.jl")



function borrow_order(loan_coin, amount, collateral_coin="USDT", term="7")
    pub = "bOHcvOmxqFVGN6FPsJwcnh4QOxw0D6oaFGHjEhpU2pby1bt7EJDb6t9TExauOccU"
    sec = "Yece0g5APcAZR4sXJl1M007tLL9w9bB7Qp2o3fGFYJjN3f6tfx6lOCq1LdmRk4Ob"
    sever_time_raw = HTTP.request("GET", "https://fapi.binance.com/fapi/v1/time"; verbose=0)
    sever_time = JSON.parse(String(sever_time_raw.body))["serverTime"]
    body = "loanCoin=$loan_coin&collateralCoin=$collateral_coin&collateralAmount=$amount&loanTerm=$term&recvWindow=5000&timestamp=$sever_time"
    signature = hexdigest("sha256", sec, body)
    url = "https://api.binance.com/sapi/v1/loag/borrow"
    headers = ["X-MBX-APIKEY" => pub]
    resp = HTTP.request("POST", "$url?$body&signature=$signature", headers=headers)
    JSON.parse(String(resp.body))
end


function repay_btc_loan(order_id::Int64, amount::Float64)
    endpoint = "/sapi/v1/loan/repay"
    parameters = [
        ("orderId", order_id),
        ("amount", amount),
        ("type", 1)  # 1: 대출한 코인으로 상환, 2: 담보로 상환
    ]
    response = create_signed_request("POST", endpoint, parameters)
    return JSON.parse(String(response.body))
end


loan_data = borrow_order("ETH", 150)

println(loan_data)





