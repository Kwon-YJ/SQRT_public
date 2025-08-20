macro catch_errors(expr)
    quote
        try
            $expr
        catch e
            println("Error: ", e)
        end
    end
end

function my_function(x, y)
# function my_function(x, y)
    z = x / y
    println("z = $z")
    print(c)
end

@catch_errors my_function(1,0)