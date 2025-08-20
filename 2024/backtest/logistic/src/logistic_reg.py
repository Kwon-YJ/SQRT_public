import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score

import random


def data_preprocessing(data):
    result = pd.DataFrame(
        [],
        columns=[
            "D-2_Open",
            "D-2_High",
            "D-2_Low",
            "D-2_Close",
            "D-1_Open",
            "D-1_High",
            "D-1_Low",
            "D-1_Close",
            "target",
        ],
    )
    for i in range(0, len(data), 3):
        if i == len(data) - 2:
            break
        d_2_data = data.iloc[i]
        d_1_data = data.iloc[i + 1]
        d_day_data = data.iloc[i + 2]

        target = -1
        if d_day_data["High"] > d_day_data["Open"] * 1.01:
            target = 1
        else:
            target = 0

        result.loc[int(i / 3)] = [
            d_2_data["Open"],
            d_2_data["High"],
            d_2_data["Low"],
            d_2_data["Close"],
            d_1_data["Open"],
            d_1_data["High"],
            d_1_data["Low"],
            d_1_data["Close"],
            target,
        ]
    return result


def test_data_preprocessing(data):
    """
         D-2_Open  D-2_High   D-2_Low  ...   D-1_Low  D-1_Close  target
    0    10316.62  10475.54  10077.22  ...   9940.87   10102.02     1.0
    1    10163.06  10450.13  10042.12  ...  10153.51   10341.34     0.0
    2    10333.47  10359.20  10024.81  ...  10080.70   10249.27     0.0
    3    10183.87  10256.65  10097.92  ...   9530.02   10245.30     0.0
    4    10166.56  10175.30   9912.63  ...   9857.00   10023.04     0.0
    ..        ...       ...       ...  ...       ...        ...     ...
    494  26890.90  27085.00  26870.40  ...  26939.00   27981.40     1.0
    495  27477.70  27665.00  27123.00  ...  27163.90   27759.80     1.0
    496  27398.30  28450.00  27156.00  ...  27822.10   27943.00     0.0
    497  27901.20  27977.00  27250.00  ...  27281.00   27381.20     0.0
    498  26864.50  26939.00  26534.80  ...  26670.10   26849.80     0.0
    """

    result = pd.DataFrame(
        [],
        columns=[
            "D-2_Open",
            "D-2_High",
            "D-2_Low",
            "D-2_Close",
            "D-1_Open",
            "D-1_High",
            "D-1_Low",
            "D-1_Close",
            "target",
        ],
    )
    for i in range(0, len(data), 3):
        if i == len(data) - 2:
            break
        d_2_data = data.iloc[i]
        d_1_data = data.iloc[i + 1]
        d_day_data = data.iloc[i + 2]

        target = -1
        if d_day_data["High"] > d_day_data["Open"] * 1.01:
            target = 1
        else:
            target = 0

        result.loc[int(i / 3)] = [
            d_2_data["Open"],
            d_2_data["High"],
            d_2_data["Low"],
            d_2_data["Close"],
            d_1_data["Open"],
            d_1_data["High"],
            d_1_data["Low"],
            d_1_data["Close"],
            target,
        ]

    rand_num = random.randint(1, len(result) - 1)
    label = result["target"].iloc[rand_num]
    result = result[
        [
            "D-2_Open",
            "D-2_High",
            "D-2_Low",
            "D-2_Close",
            "D-1_Open",
            "D-1_High",
            "D-1_Low",
            "D-1_Close",
        ]
    ].iloc[rand_num]

    return result, label


global_seed = 2017
# global_seed = 2018


# 데이터 불러오기
# data = pd.read_csv('BTCUSDT_1d_train.csv')  # 주가 데이터 파일
data = pd.read_csv("ETHUSDT_1d.csv")  # 주가 데이터 파일


preprocessed_data = data_preprocessing(data)


features = preprocessed_data[
    [
        "D-2_Open",
        "D-2_High",
        "D-2_Low",
        "D-2_Close",
        "D-1_Open",
        "D-1_High",
        "D-1_Low",
        "D-1_Close",
    ]
]
targets = preprocessed_data["target"]


train_features, test_features, train_labels, test_labels = train_test_split(
    features, targets, test_size=0.1, random_state=global_seed
)


scaler = StandardScaler()


train_features = scaler.fit_transform(train_features)
test_features = scaler.transform(test_features)
# 평균 0, 표준 편차 1로 정규화


model = LogisticRegression(random_state=global_seed)
model.fit(train_features, train_labels)


# 훈련 데이터에 대한 모델의 정확도 출력
print("훈련 데이터 정확도:", model.score(train_features, train_labels))

# 테스트 데이터에 대한 모델의 정확도 출력
print("테스트 데이터 정확도:", model.score(test_features, test_labels))

# 모델의 계수(특성 중요도) 출력
print("모델 계수:", model.coef_)

# 테스트 데이터에 대한 예측 수행
btc_test, label = test_data_preprocessing(data=pd.read_csv("BTCUSDT_1d_test.csv"))
sample_passengers = np.array([btc_test])
sample_passengers = scaler.transform(sample_passengers)
# 테스트 데이터에 대한 예측 결과 출력 (0 또는 1)
print("예측 결과:", model.predict(sample_passengers))

# 테스트 데이터에 대한 예측 확률 출력 ([0일 확률, 1일 확률])
print("예측 확률:", model.predict_proba(sample_passengers))

# 실제 테스트 데이터의 레이블 출력
print("실제 레이블:", label)
