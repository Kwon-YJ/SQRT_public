# Systematic Quantitative Research Trading

### This repository has been edited for resume submission, so its content differs from the original and execution is not guaranteed.
### This repository aims to identify opportunities for generating alpha through technical analysis (TA) in the Korean Exchange (KRX) and cryptocurrency markets.
### 이 리포지토리는 제출용으로 수정된 것으로 원본과 내용이 달라 실행을 보장하지 않습니다.
### 이 리포지토리는 한국 증권거래소와 암호화폐 시장에서 Technical Analysis를 활용해 알파를 창출할 수 있는 기회를 탐색하는 것을 목표로 합니다.

![pnl](img/pnl.jpg)

```
# linux

TZ=UTC
0 9 * * * /usr/bin/env bash -c 'nohup /usr/local/bin/julia /mnt/c/Users/kyj1435/Documents/BTC_daytrade/2024/trade/PQ_binance.jl > /mnt/c/Users/kyj1435/Documents/BTC_daytrade/2024/trade/$(date +\%Y-\%m-\%d)_0900.log 2>&1 &'

0 21 * * * /usr/bin/env bash -c 'nohup /usr/local/bin/julia /mnt/c/Users/kyj1435/Documents/BTC_daytrade/2024/trade/PQ_binance.jl > /mnt/c/Users/kyj1435/Documents/BTC_daytrade/2024/trade/$(date +\%Y-\%m-\%d)_2100.log 2>&1 &'

0 9 * * * /usr/bin/env bash -c 'nohup /usr/bin/python3 /root/BTC_daytrade/2024/trade/PQ_bybit.py > /root/BTC_daytrade/2024/backtest/stock/$(date +\%Y-\%m-\%d)_0900_bybit.log 2>&1 &'

0 21 * * * /usr/bin/env bash -c 'nohup /usr/bin/python3 /root/BTC_daytrade/2024/trade/PQ_bybit.py > /root/BTC_daytrade/2024/backtest/stock/$(date +\%Y-\%m-\%d)_0900_bybit.log 2>&1 &'

```

```
# mac

TZ=UTC

0 9 * * * /usr/bin/env bash -c 'nohup /usr/local/bin/julia /mnt/c/Users/kyj1435/Documents/BTC_daytrade/2024/trade/PQ_binance.jl > /mnt/c/Users/kyj1435/Documents/BTC_daytrade/2024/trade/$(date +\%Y-\%m-\%d)_0900.log 2>&1 &'

0 21 * * * /usr/bin/env bash -c 'nohup /usr/local/bin/julia /mnt/c/Users/kyj1435/Documents/BTC_daytrade/2024/trade/PQ_binance.jl > /mnt/c/Users/kyj1435/Documents/BTC_daytrade/2024/trade/$(date +\%Y-\%m-\%d)_2100.log 2>&1 &'

```
