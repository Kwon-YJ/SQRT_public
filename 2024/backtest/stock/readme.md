```
└── 📁src
    └── daily_backtest.py // 일별 백테스트 수행
    └── get_perform_daily.py // 일별 백테스트 결과 시각화
    └── stock_816_postprocess.jl // 백테스트 결과 후처리 적용 (post_result 폴더에 저장)
    └── stock_816.jl // 백테스트 실행 및 결과 csv 파일 저장 (result 폴더에 저장)
    └── utils.py // 국내 주식 데이터 csv 저장 파일 (csv_raw_file 폴더에 저장)
```

### 실행 순서
0. runfile.py 실행, 끝.

1. utils.py로 데이터 적재
2. stock_816.jl로 백테스트 실행
3. stock_816_postprocess.jl 로 후처리 작업 적용
4. daily_backtest.py로 일별 거래 내역 생성
5. get_perform_daily.py로 일별 자산 증감 측정
- param 계산을 위한 과정에선 슬리피지 없이, daily 백테스트에선 슬리피지 적용

