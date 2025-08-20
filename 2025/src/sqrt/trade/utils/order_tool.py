"""주문 기능 구현"""

from datetime import datetime, timedelta
from pykrx import stock
from src.cfg.const import Const
from .time_tool import get_time


def get_qty(target: str, size: float) -> int:
    """
    유효한 주문 수량 조회
    """
    now = datetime.now()
    today_var: str = get_time()[0]
    start_time = str(now - timedelta(15))
    start_time = start_time.split(" ", maxsplit=1)[0].replace("-", "")
    df = stock.get_market_ohlcv(start_time, today_var, target)
    
    # money = kiwoom.GetLoginInfo("ACCNO")[0]
    money = Const.krx_money()
    price = df.tail(1)["종가"].values
    return int(money / price[0] * size)
