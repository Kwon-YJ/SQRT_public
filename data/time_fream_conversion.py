import pandas as pd

# 데이터를 읽어옵니다.
df = pd.read_csv("E6_1h.CSV", parse_dates=[0], index_col=0)

df.columns = ["o", "h", "l", "c", "v"]


# 시간 간격을 재조정합니다.
df_resampled = df.resample("12H").agg(
    {"o": "first", "h": "max", "l": "min", "c": "last", "v": "sum"}
)


df_resampled.to_csv("resampled_12h.csv")
