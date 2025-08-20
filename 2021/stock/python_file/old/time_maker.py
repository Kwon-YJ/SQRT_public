import csv
import os


def Csv_init(data):
    with open(str(os.getcwd()) + "/test.csv", "a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([data])
        # writer.writerow(['1.87'])
        # writer.writerow(['1.88'])
        # writer.writerow('')
        # writer.writerow('')

        # tickers = list(binance.fetch_tickers().keys())
        # writer.writerow(tickers)
        # writer.writerow([SignalMaker(tickers[x]) for x in range(24)])
        # writer.writerow([0 for i in range(24)])


for i in range(1, 21):
    for j in range(1, 13):
        if j == 12:
            data = "%d년 12-1월" % (i)
            # print(data)
        else:
            data = "%d년 %d-%d월" % (i, j, j + 1)
            # print(data)

        Csv_init(data)
