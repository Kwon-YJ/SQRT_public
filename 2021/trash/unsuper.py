import ccxt
import matplotlib.pyplot as plt
import numpy as np


from sklearn.cluster import KMeans


def timestamp_to_datetime(timestamp):
    datetimeobj = datetime.datetime.fromtimestamp(timestamp / 1000)
    original_time_data = str(datetimeobj)
    entry_time_data = str(datetimeobj)[11:-3]
    exit_time_data = str(datetimeobj)[5:-3]
    return entry_time_data, exit_time_data, original_time_data


def log_maker(name_, ohlcv_temp, rsi_entry, rsi_exit):
    price = 0
    entry_time_buffer = []

    for i in range(len(rsi_entry) - 1):
        if (
            str(rsi_entry[i]) == "nan"
            or str(rsi_exit[i]) == "nan"
            or rsi_exit[i] == None
        ):
            continue

        if price == 0:
            if rsi_entry[i] < 19:
                price = ohlcv_temp[i + 1][1]
                entry_time_buffer.append(timestamp_to_datetime(ohlcv_temp[i + 1][0])[1])
        else:
            if rsi_exit[i] > 38:
                earning = 100 * (ohlcv_temp[i + 1][1] / price * Slippage - 1)
                buy_sell_log.append(earning)
                exit_time = timestamp_to_datetime(ohlcv_temp[i + 1][0])[0]
                name_save.append("0")
                entry_exit_gap = ohlcv_temp[-1][4] - price
                print(
                    name_
                    + "  "
                    + entry_time_buffer[0][:5]
                    + "  buy : "
                    + entry_time_buffer[0][6:]
                    + "  // sell : "
                    + exit_time
                    + "  "
                    + str(earning)
                    + "  "
                    + str(entry_exit_gap)
                )
                entry_time_buffer.clear()
                price = 0

    if price != 0:
        earning = 100 * (ohlcv_temp[-1][4] / price * Slippage - 1)
        buy_sell_log.append(earning)
        exit_time = timestamp_to_datetime(ohlcv_temp[i + 1][0])[0]
        name_save.append("0")
        entry_exit_gap = ohlcv_temp[-1][4] - price
        print(
            name_
            + "  "
            + entry_time_buffer[0][:5]
            + "  buy : "
            + entry_time_buffer[0][6:]
            + "  // sell : "
            + exit_time
            + "  "
            + str(earning)
            + "  "
            + str(entry_exit_gap)
        )
        entry_time_buffer.clear()
        price = 0
        return None


binance = ccxt.binance()


ohlcv_ = binance.fetch_ohlcv("BTC/USDT", "1d")


x_value = []

y_value = []

for i in range(len(ohlcv_)):
    if i == 0 or i == len(ohlcv_):
        continue
    x_value.append(ohlcv_[i][4] - ohlcv_[i - 1][4])
    y_value.append(ohlcv_[i][5])

print(x_value)

print(y_value)


plt.scatter(x_value, y_value)


plt.show()


"""
Z = [x_value, y_value]
n = 2

from sklearn.cluster import KMeans
#클러스터의 개수 지정(n개)
num_clusters = n
#알맞은 매트릭스 Z 삽입
km = KMeans(n_clusters=num_clusters)
km.fit(Z)

from scipy.spatial.distance import cdist
distortions = []
K = range(1,10)
for k in K:
    kmeanModel = KMeans(n_clusters=k).fit(Z)
    kmeanModel.fit(Z)
    distortions.append(sum(np.min(cdist(Z, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / Z.shape[0])
# Plot the elbow
plt.plot(K, distortions, 'bx-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Elbow Method showing the optimal k')
plt.show()


plt.scatter(y_value, x_value)
plt.show()


"""
