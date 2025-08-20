# CCXT를 사용한 Binance USD-M 선물 모든 심볼 레버리지 및 마진 모드 설정 예제
import ccxt

# Binance API 인증정보
api_key = ""       # 사용자의 Binance API 키
api_secret = ""     # 사용자의 Binance 시크릿 키

# Binance USD-M 선물 거래소 객체 생성
exchange = ccxt.binanceusdm({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True  # 안전한 호출을 위한 속도 제한
})

# 사용자 설정: 목표 레버리지 배율과 마진 모드
target_leverage = 5         # 원하는 레버리지 배율 (예: 5배)
margin_mode = 'ISOLATED'    # 마진 모드: 'ISOLATED' 또는 'CROSSED' (격리 또는 교차)

# 모든 선물 마켓 정보 로드
exchange.load_markets()
symbols = exchange.symbols  # 거래 가능한 모든 선물 심볼 목록

# 각 심볼에 대해 마진 모드와 레버리지 설정
for symbol in symbols:
    # try:
    #     # 1) 마진 모드 설정
    #     exchange.set_margin_mode(margin_mode, symbol)
    #     print(f"{symbol} 마진 모드를 {margin_mode}로 설정했습니다.")
    # except Exception as e:
    #     print(f"{symbol} 마진 모드 설정 실패: {e}")

    try:
        # 2) 레버리지 배율 설정
        exchange.set_leverage(target_leverage, symbol)
        print(f"{symbol} 레버리지를 {target_leverage}배로 설정했습니다.")
    except Exception as e:
        print(f"{symbol} 레버리지 설정 실패: {e}")
