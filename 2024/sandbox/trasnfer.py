import ccxt
import os

# 바이낸스 객체 생성 및 인증 정보 설정
exchange = ccxt.binance(
    {
    }
)

# 출금 정보 설정
code = "USDT"  # 출금할 암호화폐
amount = 10  # 출금 금액
params = {"network": "TRX"}  # 필요한 추가 파라미터

# 출금 요청
response = exchange.withdraw(code, amount, address, params=params)

# 응답 출력
print(response)
