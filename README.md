# kr-finbert PJT

# 발표자료
[발표자료](https://github.com/SNU-dataproject/kr-finbert/blob/main/%EB%B9%85%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%B0%9C%ED%91%9C_1%EC%A1%B0.pdf)

# Dataset
### 1. Raw Data Crawling 📄
##### 네이버 금융의 뉴스 기사, 네이버 기사에 검색 조건 추가, 증권사 레포트 크롤링
검색 기업 : **삼성전자**, **현대자동차**, **카카오뱅크**
###### Code
* [scrape_naver_finance_news.py](https://github.com/SNU-dataproject/kr-finbert/blob/main/scrape_naver_finance_news.py)
* [scrape_naver_news.py](https://github.com/SNU-dataproject/kr-finbert/blob/main/scrape_naver_news.py)
* [scrape_report.py](https://github.com/SNU-dataproject/kr-finbert/blob/main/scrape_report.py)
###### Dataset
* [samsung_raw_naver_finance_news.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/samsung/samsung_raw_naver_finance_news.xlsx)
* [samsung_raw_naver_news.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/samsung/samsung_raw_naver_news.xlsx)
* [samsung_raw_report.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/samsung/samsung_raw_report.xlsx)
* [hyundai_raw_naver_finance_news.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/hyundai/hyundai_raw_naver_finance_news.xlsx)
* [hyundai_raw_naver_news.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/hyundai/hyundai_raw_naver_news.xlsx)
* [hyundai_raw_report.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/hyundai/hyundai_raw_report.xlsx)
* [kakaobank_raw_naver_finance_news.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/hyundai/hyundai_raw_naver_finance_news.xlsx)
* [kakaobank_raw_naver_news.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/kakaobank/kakaobank_raw_naver_news.xlsx)
* [kakaobank_raw_report.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/kakaobank/kakaobank_raw_report.xlsx)
### 2. Merge & Sort & Preprocess & Combine 📚
##### 크롤링으로 생성된 파일들을 1개로 병합하고 날짜 기준으로 정렬하여 전처리, 한 날짜에 데이터가 여러 row인 경우 title을 한 문장으로 combine
###### * 전처리 조건
```
YoY or yoy or YOY      -> 전년 대비 증감율
QoQ or qoq or QOQ      -> 전분기 대비 증감율
MoM or mom or MOM      -> 전월 대비 증감율
YTD                    -> 연초 누계
MTD                    -> 월초 누계
분기 표현 1Q21F        -> 21년도 1분기 예측값
분기 표현 1Q21         -> 21년도 1분기
반기 표현 1H21         -> 21년도 상반기
[내용] 제거
문장 시작의 "삼성전자-" 삭제
다중 띄어쓰기 제거
앞뒤 공백 제거
```

###### Code
* [combine_dataset.py](https://github.com/SNU-dataproject/kr-finbert/blob/main/combine_dataset.py)
###### Dataset
* [samsung_cleaned_combined_dataset.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/samsung/samsung_cleaned_combined_dataset.xlsx)
* [hyundai_cleaned_combined_dataset.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/hyundai/hyundai_cleaned_combined_dataset.xlsx)
* [kakaobank_cleaned_combined_dataset.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/kakaobank/kakaobank_cleaned_combined_dataset.xlsx)


### 3. Add finbert score 🤔
##### 각각 title에 대하여 kr-finBERT 모델 적용, Neg Neu Pos 수치와 대표값 표시
###### Code
* [kr_finbert_getVal_from_file.ipynb](https://github.com/SNU-dataproject/kr-finbert/blob/main/kr_finbert_getVal_from_file.ipynb)
###### Dataset
* [samsung_cleaned_combined_dataset_finBERT.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/samsung/samsung_cleaned_combined_dataset_finBERT.xlsx)
* [hyundai_cleaned_combined_dataset_finBERT.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/hyundai/hyundai_cleaned_combined_dataset_finBERT.xlsx)
* [kakaobank_cleaned_combined_dataset_finBERT.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/kakaobank/kakaobank_cleaned_combined_dataset_finBERT.xlsx)


### 4. Add finbert score to FinanceDataReader 🤑
##### FinanceDataReader 정보에 kr-finBERT col 추가 및 결측치 처리
###### Code
* [load_stock_by_FDR_with_TA.ipynb](https://github.com/SNU-dataproject/kr-finbert/blob/main/load_stock_by_FDR_with_TA.ipynb)
###### Dataset
* [samsung_stock_dataset_finBERT_notnull.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/samsung/samsung_stock_dataset_finBERT_notnull.xlsx)
* [hyundai_stock_dataset_finBERT_notnull.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/hyundai/hyundai_stock_dataset_finBERT_notnull.xlsx)
* [kakaobank_stock_dataset_finBERT_notnull.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/kakaobank/kakaobank_stock_dataset_finBERT_notnull.xlsx) 

---

# Model
### 1. LSTM📝
* LSTM : [model_LSTM.ipynb](https://github.com/SNU-dataproject/kr-finbert/blob/main/model/model_LSTM.ipynb)
* RNN : [model_RNN.ipynb](https://github.com/SNU-dataproject/kr-finbert/blob/main/model/model_RNN.ipynb)
* Neural Prophet : [model_NeuralProphet.ipynb](https://github.com/SNU-dataproject/kr-finbert/blob/main/model/model_NeuralProphet.ipynb)
* ARIMA : [model_ARIMA.ipynb](https://github.com/SNU-dataproject/kr-finbert/blob/main/model/model_ARIMA.ipynb)
