```
└── 📁src
    └── crypto_816_12h_valid.jl
    └── crypto_816_verbose_true.jl
    └── crypto_data_refac.jl
    └── crypto_data_save_module.jl
    └── main_backtest_daily.jl
    └── main_backtest.jl // data 폴더의 모든 csv 파일을 읽어 백테스트 수행 후 result 폴더에 유의미한 결과만 추려 저장
    └── main_data_save.jl // 모든 ticker의 모든 타임프레임 ohlcv 데이터를 csv로 저장 (저장 위치: data 폴더)
    └── readme.md
    └── result_post_processing_old.py
    └── time_frame_sort.py
```

### 실행순서
1. main_data_save.jl 실행하여 데이터 적재
2. main_backtest.jl 실행하여 백테스트 수행
3. main_backtest_daily.jl 실행하여 daily 백테스트 수행
4. 




