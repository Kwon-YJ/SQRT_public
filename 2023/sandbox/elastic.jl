
function _1h_2h_12h()
    result = []
    momentum_count, momentum = 0, 0
    for i in range(1, 20)
        if momentum_count > 9
            momentum += 0.18
        elseif momentum_count > 4
            momentum += 0.09
        else
            momentum += 0.01
        end
        momentum += 0.01
        momentum_count += 1
        push!(result, momentum)
    end
    println(result)
end

function _4h_6h()
    result = []
    momentum_count, momentum = 0, 0
    for i in range(1, 20)
        if momentum_count > 4
            momentum += 0.02
        else
            momentum += 0.01
        end
        momentum += 0.03
        momentum_count += 1
        push!(result, momentum)
    end
    println(result)
end



function _8h()
    result = []
    momentum_count, momentum = 0, 0
    for i in range(1, 20)
        if momentum_count > 9
            momentum += 0.18
        elseif momentum_count > 4
            momentum += 0.12
        else
            momentum += 0.03
        end
        momentum += 0.01
        momentum_count += 1
        push!(result, momentum)
    end
    println(result)
end


_1h_2h_12h()

println("#######################")

_4h_6h()

println("#######################")

_8h()



function elastic(n)
    if n ≤ 5 
        return 0.0004
    end
    if n ≤ 11
        return 0.0004n
    end
    if n ≤ 25
        return 0.0022 + 0.0015n
    end
    return 0.04+0.006n
end


result = []

for i in 1:100
    push!(result, elastic(i))
end

println(result)


[0.0004, 0.0004, 0.0004, 0.0004, 0.0004, 0.0024, 0.0028, 0.0032, 0.0036, 0.004, 0.0044, 0.02, 0.0217, 0.0232, 0.0247, 0.0262, 0.0277, 0.0292, 0.0307, 0.0322, 0.0337, 0.0352, 0.0367, 0.0382, 0.0397, 0.196, 0.202, 0.208, 0.214, 0.22, 0.226, 0.232, 0.238, 0.244, 0.25, 0.256, 0.262, 0.268, 0.274, 0.28, 0.286, 0.292, 0.298, 0.304, 0.31, 0.316, 0.322, 0.328, 0.334, 0.34, 0.346, 0.352, 0.358, 0.364, 0.37, 0.376, 0.382, 0.388, 0.394, 0.4, 0.406, 0.412, 0.418, 0.424, 0.43, 0.436, 0.442, 0.448, 0.454, 0.46, 0.466, 0.472, 0.478, 0.484, 0.49, 0.496, 0.502, 0.508, 0.514, 0.52, 0.526, 0.532, 0.538, 0.544, 0.55, 0.556, 0.562, 0.568, 0.574, 0.58, 0.586, 0.592, 0.598, 0.604, 0.61, 0.616, 0.622, 0.628, 0.634, 0.64]