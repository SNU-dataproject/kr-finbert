# kr-finbert PJT

# Dataset
### 1. raw data 📄
##### 네이버 금융의 뉴스 기사, 네이버 기사에 검색 조건 추가, 증권사 레포트 크롤링
검색 기업 : **삼성전자**
* [scrape_naver_finance_news.py](https://github.com/SNU-dataproject/kr-finbert/blob/main/scrape_naver_finance_news.py)
* [scrape_naver_news.py](https://github.com/SNU-dataproject/kr-finbert/blob/main/scrape_naver_news.py)
* [scrape_report.py](https://github.com/SNU-dataproject/kr-finbert/blob/main/scrape_report.py)
* [naver_finance_news.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/naver_finance_news.xlsx)
* [naver_news.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/naver_news.xlsx)
* [report.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/report.xlsx)

### 2. merge into one file & sort by date 📚
##### 1번에서 크롤링해서 생성된 3 파일을 1개로 병합하고 날짜 기준으로 정렬
* [combine_dataset.py](https://github.com/SNU-dataproject/kr-finbert/blob/main/combine_dataset.py)
* [combined_dataset.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/combined_dataset.xlsx)

### 3. preprocess 📝
##### 전체 데이터에 대하여 전처리
전처리 조건
```
YoY or yoy or YOY      -> 전년 대비 증감율
QoQ or qoq or QOQ      -> 전분기 대비 증감율
MoM or mom or MOM      -> 전월 대비 증감율
YTD                    -> 연초 누계
MTD                    -> 월초 누계
분기 표현 1Q21F        -> 21년도 1분기 예측값
분기 표현 1Q21         -> 21년도 1분기
반기 표현 1Q21         -> 21년도 
[내용] 제거
문장 시작의 "삼성전자-" 삭제
다중 띄어쓰기 제거
앞뒤 공백 제거
```
* [preprocessing.ipynb](https://github.com/SNU-dataproject/kr-finbert/blob/main/preprocessing.ipynb)
* [combined_dataset_cleaned.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/combined_dataset_cleaned.xlsx)

### 4. combine data from one date into one row 📔
##### 한 날짜에 데이터가 여러 row인 경우, title을 한 문장으로 combine
* [make_dataset_to_time_series.py](https://github.com/SNU-dataproject/kr-finbert/blob/main/make_dataset_to_time_series.py)
* [preprocessed_dup_eliminated_dataset.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/preprocessed_dup_eliminated_dataset.xlsx)

### 5. add finbert score 😱
##### 각각 title에 대하여 kr-finBERT 모델 적용, Neg Neu Pos 수치와 대표값 표시
* [kr_finbert_getVal_from_file.ipynb](https://github.com/SNU-dataproject/kr-finbert/blob/main/kr_finbert_getVal_from_file.ipynb)
* [preprocessed_dup_eliminated_dataset_finBERT.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/preprocessed_dup_eliminated_dataset_finBERT.xlsx)

### 6. add finbert score to FinanceDataReader
##### FinanceDataReader의 삼성전자 정보에 kr-finBERT 대표값 col 추가
``` python
for i in range(len(s)) : 
    for j in range(len(Fb_dataset)) :
        if(s.index[i] == Fb_dataset['date'][j]) :
            s["sentiment"][i] = Fb_dataset['sentiment'][j]
```

---

# Model
### 1. LSTM
* [LSTM_model.ipynb](https://github.com/SNU-dataproject/kr-finbert/blob/main/model/lstm_0609_v2.ipynb)
