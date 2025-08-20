include("../../../utils/utils.jl")

ticker_list = get_tickers_listed_over_1year() 


for ticker in ticker_list
    println(ticker)
    try
        run(`julia crypto_module.jl --ticker $(ticker)`)
    catch e
        println("$(ticker) : $(e)")
        continue
    end
end