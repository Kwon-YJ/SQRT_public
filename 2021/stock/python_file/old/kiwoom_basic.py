from pykiwoom.kiwoom import *
from pprint import pprint


def get_balance():  # opw00001
    df = kiwoom.block_request(
        "opw00001",
        계좌번호=stock_account,
        비밀번호="",
        비밀번호입력매체구분="00",
        조회구분=2,
        output="예수금상세현황",
        next=0,
    )

    balance = int(df["100%종목주문가능금액"][0])
    return balance


kiwoom = Kiwoom()
kiwoom.CommConnect(block=True)
accounts = kiwoom.GetLoginInfo("ACCNO")
stock_account = accounts[0]


# 삼성전자, 10주, 시장가주문 매수
# kiwoom.SendOrder("시장가매수", "0101", stock_account, 1, "005930", 10, 0, "03", "") # 시장가는 0, "03"


# kiwoom.SendOrder("지정가매수", "0101", stock_account, 1, "005930", 5, 84200, "00", "") # 지정가는 희망가격, "00"


print(get_balance())


"""
account_num = kiwoom.GetLoginInfo("ACCOUNT_CNT")        # 전체 계좌수
accounts = kiwoom.GetLoginInfo("ACCNO")                 # 전체 계좌 리스트
user_id = kiwoom.GetLoginInfo("USER_ID")                # 사용자 ID
user_name = kiwoom.GetLoginInfo("USER_NAME")            # 사용자명
keyboard = kiwoom.GetLoginInfo("KEY_BSECGB")            # 키보드보안 해지여부
firewall = kiwoom.GetLoginInfo("FIREW_SECGB")           # 방화벽 설정 여부

print(account_num)
print(accounts)
print(user_id)
print(user_name)
print(keyboard)
print(firewall)

state = kiwoom.GetConnectState()
if state == 0:
    print("미연결")
elif state == 1:
    print("연결완료")
"""
