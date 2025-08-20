"""시간 관련 기능"""

from datetime import datetime


def get_time() -> tuple[str, str]:
    """
    현재 시간과 일자를 보내는 함수
    """
    now = datetime.now()
    yyyy = str(now.year)
    month = str(now.month)
    day = str(now.day)
    hh = str(now.hour)
    mm = str(now.minute)
    if len(month) != 2:
        month = "0" + month
    if len(day) != 2:
        day = "0" + day
    if len(hh) != 2:
        hh = "0" + hh
    if len(mm) != 2:
        mm = "0" + mm
    return yyyy + month + day, hh + mm


def is_weekday() -> bool:
    today = datetime.today()
    is_weekday = today.weekday() < 5
    return is_weekday
