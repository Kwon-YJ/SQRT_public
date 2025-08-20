import time


result = []


def doubler(input_list):
    start_ = time.time()
    for i in range(len(input_list)):
        time.sleep(0.1)
        result.append(input_list[i] * input_list[i])
    end_ = time.time()
    print("소요시간 :", end_ - start_)


data = range(0, 100)

doubler(data)


print(result)
