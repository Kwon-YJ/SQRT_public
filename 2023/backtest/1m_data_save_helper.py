from datetime import datetime


def get_timestamp(date: str) -> int:
    year, month = map(int, date.split("-"))
    year += 2000
    dt = datetime(year, month, 1)
    timestamp = int(dt.timestamp() * 1000)
    return timestamp


# date = input('날짜를 입력하세요 (예: 22-2): ')
# print(get_timestamp(date))


calendar = [
    "23-6",
    "23-5",
    "23-4",
    "23-3",
    "23-2",
    "23-1",
    "22-1",
    "22-1",
    "22-1",
    "22-9",
    "22-8",
    "22-7",
    "22-6",
    "22-5",
    "22-4",
    "22-3",
    "22-2",
    "22-1",
    "21-12",
    "21-11",
    "21-10",
    "21-9",
    "21-8",
    "21-7",
    "21-6",
    "21-5",
    "21-4",
    "21-3",
    "21-2",
    "21-1",
    "20-12",
    "20-11",
    "20-10",
    "20-9",
    "20-8",
    "20-7",
    "20-6",
    "20-5",
    "20-4",
    "20-3",
    "20-2",
    "20-1",
]


for i in range(len(calendar) - 1):
    y = calendar[i + 1].split("-")[0]
    m = calendar[i + 1].split("-")[1]
    print(f"# {y}년 {m}월 ")
    print('start_time = "' + str(get_timestamp(calendar[i + 1])) + '"')
    print('end_time = "' + str(get_timestamp(calendar[i])) + '"')
    file_name = f"./{y}_{m}.pkl"
    print(f'@time make_pickle(start_time, end_time, "{file_name}")')

    print("")
