#=
mutable struct my_struct
    var_1
    var_2
end

function other_space(data)
    println("here is other_space before square : $(data)")
    data.var_1 = data.var_1^2
    data.var_2 = data.var_2^2
    println("here is other_space after square : $(data)")

end

function my_space()
    temp_struct = my_struct(123, 456)
    println(temp_struct)
    println("here is my_space before square : $(temp_struct)")
    other_space(temp_struct)
    println("here is my_space after square : $(temp_struct)")

end

my_space()


ticker_list = get_tickers()


=#

# using Async
using Distributed

# define an asynchronous function
function async_function()
    
    for i in range(1,1000)
        # perform some long-running task
        sleep(2)
        println("Async function completed")
    end
end

# execute the asynchronous function
task = @async async_function()

# do some other work while the async function is running
println("Doing some other work")
sleep(1)
println("Done doing other work")

# wait for the async function to complete


sleep(999999)

# wait(task)



function test_main()
    test_list = []

    for i in range(1,1000)
        sleep(5)
        if i==10
            @async remove_list_item(test_list)
        end
        push!(test_list, i)
        println(test_list)
    end
end


function remove_list_item(target_list)
    while true
        sleep(4.5)
        deleteat!(target_list, findall(x->x==target_list[1],target_list))
    end
end


test_main()