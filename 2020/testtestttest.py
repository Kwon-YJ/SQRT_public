# -*- coding: utf-8 -*-

import multiprocessing
import csv
import math
import ccxt
import time
import datetime
import numpy as np
from pprint import pprint
import parmap


exchange_class = getattr(ccxt, "binance")
binance = exchange_class(
    {
        "urls": {
            "api": {
                "public": "https://fapi.binance.com/fapi/v1",
                "private": "https://fapi.binance.com/fapi/v1",
            },
        }
    }
)

binance.enableRateLimit = True
binance.RateLimit = 10000
binance.load_markets()
is_entering = {}


a = list(binance.fetch_tickers().keys())


print(a[24])
