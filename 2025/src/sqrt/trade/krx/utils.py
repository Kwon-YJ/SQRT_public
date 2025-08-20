"""utils for time, csv, LSapi"""

import datetime
import os
import csv
import json
import requests


def get_time() -> tuple[str, str]:
    """20010101, 1107"""
    now = datetime.datetime.now()
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


def load_csv2list(csv_dir: str):
    encodings = ["utf-8", "euc-kr", "cp949"]
    for encoding in encodings:
        try:
            with open(os.path.join(csv_dir), "r", encoding=encoding) as f:
                return [x for x in csv.reader(f)][1:]
        except UnicodeDecodeError:
            continue
    raise Exception(f"Failed to read file with encodings: {encodings}")


class LSSecuritiesAPI:
    def __init__(
        self, appkey, appsecretkey, base_url="https://openapi.ls-sec.co.kr:8080"
    ):
        self.appkey = appkey
        self.appsecretkey = appsecretkey
        self.base_url = base_url
        self.access_token = None
        self.token_expires_in = None

    def authenticate(self):
        """LS 증권 OpenAPI 인증 (접근토큰 발급)을 수행합니다."""
        url = f"{self.base_url}/oauth2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "client_credentials",
            "appkey": self.appkey,
            "appsecretkey": self.appsecretkey,
            "scope": "oob",
        }

        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
            response_data = response.json()
            if response_data.get("access_token"):
                self.access_token = response_data["access_token"]
                return True
            else:
                print(f"인증 실패: {response_data.get('rsp_msg', '알 수 없는 오류')}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"인증 요청 중 오류 발생: {e}")
            return False

    def _get_auth_headers(self, tr_cd=None, tr_cont="N"):
        """API 호출을 위한 Authorization 헤더를 반환합니다."""
        if not self.access_token:
            print("접근 토큰이 없습니다. 먼저 인증을 수행해주세요.")
            return None

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
            "tr_cont": tr_cont,  # 연속구분 (N: 신규조회, Y: 연속조회)
        }

        if tr_cd:
            headers["tr_cd"] = tr_cd

        return headers

    def place_order(
        self, isu_no, ord_qty, ord_prc, bns_tp_code, ordprc_ptn_code, acnt_no, acnt_pwd
    ):
        """주식 현물 주문 (매수/매도)을 실행합니다.

        Args:
            isu_no (str): 종목번호 (예: 'A005930')
            ord_qty (int): 주문수량
            ord_prc (float): 주문가
            bns_tp_code (str): 매매구분 (1:매도, 2:매수)
            ordprc_ptn_code (str): 호가유형코드 (예: '00' for 지정가, '03' for 시장가)
            acnt_no (str): 계좌번호 (예: '12345678901')
            acnt_pwd (str): 계좌비밀번호
        """
        url = f"{self.base_url}/stock/order"
        headers = self._get_auth_headers(tr_cd="CSPAT00601")  # TR 코드 추가
        if not headers:
            return False

        # 계좌 정보 추가
        payload = {
            "CSPAT00601InBlock1": {
                "RecCnt": 1,
                "AcntNo": acnt_no,  # 계좌번호 추가
                "InptPwd": acnt_pwd,  # 계좌비밀번호 추가
                "IsuNo": isu_no,
                "OrdQty": ord_qty,
                "OrdPrc": float(ord_prc),  # float로 명시적 변환
                "BnsTpCode": bns_tp_code,
                "OrdprcPtnCode": ordprc_ptn_code,
                "PrgmOrdprcPtnCode": "00",
                "StslAbleYn": "0",
                "StslOrdprcTpCode": "0",
                "CommdaCode": "41",
                "MgntrnCode": "000",
                "LoanDt": "",
                "MbrNo": "000",
                "OrdCndiTpCode": "0",
                "StrtgCode": " ",
                "GrpId": " ",
                "OrdSeqNo": 0,
                "PtflNo": 0,
                "BskNo": 0,
                "TrchNo": 0,
                "ItemNo": 0,
                "OpDrtnNo": "0",
                "LpYn": "0",
                "CvrgTpCode": "0",
            }
        }

        try:
            # JSON을 문자열로 직렬화할 때 ensure_ascii=False 사용
            json_data = json.dumps(payload, ensure_ascii=False)

            response = requests.post(url, headers=headers, data=json_data)

            # 응답 상태와 내용 출력 (디버깅용)
            print(f"응답 코드: {response.status_code}")
            print(f"응답 내용: {response.text}")

            response.raise_for_status()
            response_data = response.json()

            if response_data.get("rsp_cd") == "00000":  # 성공 코드
                print(f"주문 성공: {response_data.get('rsp_msg')}")
                if "CSPAT00601OutBlock2" in response_data:
                    print(
                        f"주문 번호: {response_data['CSPAT00601OutBlock2'].get('OrdNo')}"
                    )
                return True
            else:
                print(f"주문 실패: {response_data.get('rsp_msg', '알 수 없는 오류')}")
                print(f"응답 코드: {response_data.get('rsp_cd')}")
                return False

        except requests.exceptions.RequestException as e:
            print(f"주문 요청 중 오류 발생: {e}")
            if hasattr(e, "response") and e.response is not None:
                print(f"응답 내용: {e.response.text}")
            return False

    def get_current_price(self, shcode, exchgubun="K"):
        """주식 현재가(시세)를 조회합니다.

        Args:
            shcode (str): 종목코드 (예: \'005930\' for 삼성전자)
            exchgubun (str): 거래소구분코드 (K: KRX, N: NXT, U:통합, 기본값: K)
        """
        url = f"{self.base_url}/stock/market-data"
        headers = self._get_auth_headers()
        if not headers:
            return None
        headers["tr_cd"] = "t1102"
        headers["tr_cont"] = "N"

        payload = {"t1102InBlock": {"shcode": shcode, "exchgubun": exchgubun}}

        try:
            response = requests.post(url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            response_data = response.json()

            if response_data.get("rsp_cd") == "00000":  # 성공 응답 코드
                current_price = response_data["t1102OutBlock"]["price"]
                # print(f"종목 {shcode}의 현재가: {current_price}원")
                return current_price
            else:
                print(
                    f"현재가 조회 실패: {response_data.get('rsp_msg', '알 수 없는 오류')}"
                )
                return None
        except requests.exceptions.RequestException as e:
            print(f"현재가 조회 요청 중 오류 발생: {e}")
            return None
