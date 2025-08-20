using Dates, DataFrames, Plots
include("./temp_binance.jl")



function Channel_test()
    global data_channel
    data_channel = Channel(10000)
    global num
    put!(data_channel, num)
end


data_channel = Channel(10000)




num = 1
Channel_test()

num = 2
Channel_test()

num = 3
Channel_test()



function print_ch()
    global data_channel
    println(take!(data_channel))
    println(take!(data_channel))
    println(take!(data_channel))
    println(take!(data_channel))
    println(take!(data_channel))
end

print_ch()