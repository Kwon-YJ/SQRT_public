include("../../../../2022/julia_test/utils.jl")


for ticker in get_tickers()
    run(`julia crypto_data_save_module.jl --ticker $(ticker)`)
end
