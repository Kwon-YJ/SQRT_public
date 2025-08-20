
#=
using Distributed
# 프로세스 간에 Julia 세션을 초기화합니다.
addprocs(4)  # 2개의 원격 프로세스를 추가합니다.

# 첫 번째 프로세스에서 배열을 생성하고 난수로 채웁니다.
@everywhere begin
    if myid() == 4
        arr = rand(10)
    end
end

while true
    sleep(5)
    result = remotecall_fetch(()->arr, 4)
    print(result)
    end
end
=#


using Distributed

# 프로세스 간에 Julia 세션을 초기화합니다.
addprocs(4)  # 2개의 원격 프로세스를 추가합니다.

# 로컬 프로세스에서 update_arr 함수를 정의합니다.
@everywhere function update_arr()
    global arr = rand(10)
    while true
        sleep(1)
        global arr = rand(10)
    end
end

# 원격 프로세스 4에서 update_arr 함수를 실행합니다.
remotecall(update_arr, 4)

while true
    sleep(5)
    result = remotecall_fetch(()->arr, 4)
    println(result)
end



#=

using Distributed
# 프로세스 간에 Julia 세션을 초기화합니다.
addprocs(4)
# 로컬 프로세스에서 update_arr 함수를 정의합니다.
@everywhere function update_arr()
    global arr = rand(10)
    while true
        sleep(1)
        global arr = rand(10)
    end
end
# 원격 프로세스 4에서 update_arr 함수를 실행합니다.
remotecall(update_arr, 4)
# 로컬 프로세스에서 get_arr 함수를 정의합니다.
@everywhere function get_arr()
    remotecall_fetch(()->arr, 4)
end

while true
    sleep(5)
    result = remotecall_fetch(get_arr, 2)
    println(result)
end
=#


#=
addprocs(1)
function f()
    global x = 10 * x
    println(x)
end
@everywhere x = 1
remote_do(f, 2)
=#
