import os
import pandas as pd
from datetime import datetime

def convert_csv_data():
    raw_dir = 'csv_raw_file'
    result_dir = 'convert_result'

    # 디렉토리가 없으면 생성
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(result_dir, exist_ok=True)

    # csv_raw_file 폴더 내 모든 csv 파일 불러오기
    csv_files = [f for f in os.listdir(raw_dir) if f.endswith('.csv')]

    for file_name in csv_files:
        file_path = os.path.join(raw_dir, file_name)
        stock_name = os.path.splitext(file_name)[0] # 파일명에서 종목명 추출

        try:
            df = pd.read_csv(file_path)

            # '날짜' 컬럼을 타임스탬프로 변환 (밀리초 단위)
            df['날짜'] = df['날짜'].apply(lambda x: int(datetime.strptime(x, '%Y-%m-%d').timestamp() * 1000))

            # 컬럼명 변경 및 순서 조정
            # 원본: 날짜,시가,고가,저가,종가,거래량,등락률
            # 대상: 타임스탬프,종목명,시가,고가,저가,종가,거래량
            df = df[['날짜', '시가', '고가', '저가', '종가', '거래량']]
            df.insert(1, '종목명', stock_name)
            df.columns = ['timestamp', 'symbol', 'open', 'high', 'low', 'close', 'volume']

            # 등락률 컬럼은 제외

            output_path = os.path.join(result_dir, file_name)
            df.to_csv(output_path, index=False, header=False)
            print(f"'{file_name}' 파일 변환 완료 및 '{result_dir}'에 저장.")

        except Exception as e:
            print(f"'{file_name}' 파일 변환 중 오류 발생: {e}")

if __name__ == '__main__':
    convert_csv_data()