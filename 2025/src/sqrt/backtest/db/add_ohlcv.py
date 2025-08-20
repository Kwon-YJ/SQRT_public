import os
import pandas as pd
from datetime import datetime
import pymssql
from tqdm import tqdm


class Use_DB():
    def __init__(self):
        self.conn = pymssql.connect(
            server="172.20.112.1",
            user="sa",
            password="asd852456!",
            port=1433
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute("use crypto")
        self.conn.commit()
        self.all_table_names = self.get_all_table_name()
        # get_all_table_name, bulk insert 시 중복 회피

    def get_all_table_name(self):
        self.cursor.execute("SELECT name FROM crypto.sys.tables")
        result = self.cursor.fetchall()
        if len(result) == 0:
            return []
        return list(result[0])
    
    def bulk_insert(self, file_dir,ticker)-> None:
        self.cursor.execute(rf"""
                                BULK INSERT dbo.{ticker}
                                FROM '{file_dir}'
                                WITH (
                                    FIELDTERMINATOR = ',',
                                    ROWTERMINATOR = '0x0a', -- linux는 back slash n
                                    FIRSTROW = 2 -- 헤더 처리
                                );
                            """)
        self.conn.commit()

    def create_table(self, ticker):
        self.cursor.execute(f"""CREATE TABLE {ticker} (
                                Timestamp DATETIME2(0) NOT NULL,
                                Open_ DECIMAL(18,8) NOT NULL,          
                                High_ DECIMAL(18,8) NOT NULL,          
                                Low_ DECIMAL(18,8) NOT NULL,           
                                Close_ DECIMAL(18,8) NOT NULL,         
                            );""")
        self.conn.commit()

    def add_all_ohlcv(self):
        os.makedirs("/mnt/c/Temp",exist_ok=True)
        os.system("rm /mnt/c/Temp/*")
        folder_name = "1m"
        file_names = os.listdir(folder_name)
        file_names.sort()
        for file_name in tqdm(file_names):
            try:
                ticker = file_name.split("_")[0]
                target = os.path.join(folder_name, file_name)
                df = pd.read_csv(target, names = ["UnixTimestamp", "Symbol", "Open", "High", "Low", "Close", "Volume"])
                df['Timestamp'] = pd.to_datetime(df['UnixTimestamp'], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')
                df = df[['Timestamp', 'Open', 'High', 'Low', 'Close']]
                df.to_csv(rf'/mnt/c/Temp/{file_name}', index=False, float_format='%.8f')  # 소수점 8자리로 고정
                if ticker not in self.all_table_names:
                    use_db.create_table(ticker) # 생각해서 바꾸기 (있으면 추가, 없으면 패스)
                use_db.bulk_insert(rf"C:\Temp\{file_name}", ticker)
                os.system("rm /mnt/c/Temp/*")
            except Exception as e:
                print(f"{ticker} err\n {e}")
                continue

use_db = Use_DB()
# use_db.add_all_ohlcv()




use_db.conn.close()


