using HTTP
include("./../../2022/julia_test/utils.jl")

function get_depth(ticker)
    url = "https://fapi.binance.com/fapi/v1/depth?symbol=$(ticker)&limit=5"
    raw = HTTP.request("GET", url; verbose=0)
    
    header_data = raw.headers
    for i in range(1, length(header_data))
        if occursin("X-MBX-USED-WEIGHT", header_data[i][1])
            used_weight = parse(Float64, header_data[i][2])
            println(used_weight)
        end
    end
    
    json_data = JSON.parse(String(raw.body))
    return json_data
end
