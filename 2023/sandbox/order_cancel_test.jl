using Dates
include("./../../2022/julia_test/utils.jl")


ticker = "BTCUSDT"
price = "26123"
order_resp = create_order(ticker, "BUY", "LIMIT", 0.001, price)


sleep(60)


cancel_order(order_resp["symbol"], order_resp["orderId"])