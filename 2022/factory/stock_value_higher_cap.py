import datetime
import pickle
import Utils
import parmap
import time
from pykrx import stock

from tabulate import tabulate


def sub_df_col(df):
    return df["시가총액"] - df["거래대금"]


if __name__ == "__main__":
    Today = Utils.get_time()[0]
    df = stock.get_market_cap("20220406")
    df["cap-value"] = df.apply(sub_df_col, axis=1)
    result = df.loc[df["cap-value"] < 0, :]
    print(result)
