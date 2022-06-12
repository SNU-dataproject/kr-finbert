# kr-finbert PJT

# Dataset
### 1. Raw Data Crawling 📄
##### 네이버 금융의 뉴스 기사, 네이버 기사에 검색 조건 추가, 증권사 레포트 크롤링
검색 기업 : **삼성전자**, **현대자동차**, **카카오뱅크**
###### Code
* [scrape_naver_finance_news.py](https://github.com/SNU-dataproject/kr-finbert/blob/main/scrape_naver_finance_news.py)
* [scrape_naver_news.py](https://github.com/SNU-dataproject/kr-finbert/blob/main/scrape_naver_news.py)
* [scrape_report.py](https://github.com/SNU-dataproject/kr-finbert/blob/main/scrape_report.py)
###### Dataset
* [samsung_raw_naver_finance_news.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/samsung_raw_naver_finance_news.xlsx)
* [samsung_raw_naver_news.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/samsung_raw_naver_news.xlsx)
* [samsung_raw_report.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/samsung_raw_report.xlsx)
* [hyundai_raw_naver_finance_news.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/hyundai_raw_naver_finance_news.xlsx)
* [hyundai_raw_naver_news.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/hyundai_raw_naver_news.xlsx)
* [hyundai_raw_report.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/hyundai_raw_report.xlsx)

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
* [samsung_cleaned_combined_dataset.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/samsung_cleaned_combined_dataset.xlsx)
* [hyundai_cleaned_combined_dataset.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/hyundai_cleaned_combined_dataset.xlsx)


### 3. Add finbert score 😱
##### 각각 title에 대하여 kr-finBERT 모델 적용, Neg Neu Pos 수치와 대표값 표시
###### Code
* [kr_finbert_getVal_from_file.ipynb](https://github.com/SNU-dataproject/kr-finbert/blob/main/kr_finbert_getVal_from_file.ipynb)
###### Dataset
* [samsung_cleaned_combined_dataset_finBERT.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/samsung_cleaned_combined_dataset_finBERT.xlsx)
* [hyundai_cleaned_combined_dataset_finBERT.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/hyundai_cleaned_combined_dataset_finBERT.xlsx)

### 4. Add finbert score to FinanceDataReader😇
##### FinanceDataReader 정보에 kr-finBERT col 추가 및 결측치 처리
###### Code
``` python
from datetime import datetime

s["negative"] = 0.0
s["neutral"] = 0.0
s["positive"] = 0.0
s["sentiment"] = "null"

filename = "./cleaned_combined_dataset_finBERT.xlsx"
Fb_dataset = pd.read_excel(filename)
Fb_dataset["date"] = pd.to_datetime(Fb_dataset["date"], format='%Y%m%d')

for i in range(len(s)) : 
    for j in range(len(Fb_dataset)) :
        if(s.index[i] == Fb_dataset['date'][j]) :
            s["negative"][i] = Fb_dataset['negative'][j]
            s["neutral"][i] = Fb_dataset['neutral'][j]
            s["positive"][i] = Fb_dataset['positive'][j]
            s["sentiment"][i] = Fb_dataset['sentiment_to_num'][j]
            
# 결측치 처리
# 2 = avg(1, 5), 3 = avg(2, 5), 4 = avg(3, 5) 
for i in range(len(s)) : 
    prev_val = {"negVal" : 0.0, "neuVal" : 0.0, "posVal" : 0.0}
    next_val = {"negVal" : 0.0, "neuVal" : 0.0, "posVal" : 0.0}
    avg_val = {"negVal" : 0.0, "neuVal" : 0.0, "posVal" : 0.0}
    if(s['sentiment'][i] == None) :
        prev_val = {"negVal" : s['negative'][i-1], "neuVal" : s["neutral"][i-1], "posVal" : s["positive"][i-1]}
        for j in range(i, len(s)) :
            if s['sentiment'][j] != None :
                next_val = {"negVal" : s['negative'][j], "neuVal" : s["neutral"][j], "posVal" : s["positive"][j]}
                break
        avg_val['negVal'] = (prev_val['negVal']+next_val['negVal'])/2
        avg_val['neuVal'] = (prev_val['neuVal']+next_val['neuVal'])/2
        avg_val['posVal'] = (prev_val['posVal']+next_val['posVal'])/2
        s['negative'][i] = avg_val['negVal']
        s['neutral'][i] = avg_val['neuVal']
        s['positive'][i] = avg_val['posVal']
        s['sentiment'][i] = max(avg_val, key=avg_val.get)
for i in range(len(s)) :
    if(s['sentiment'][i] == "negVal") : s['sentiment'][i] = -1
    elif(s['sentiment'][i] == "neuVal") : s['sentiment'][i] = 0
    elif(s['sentiment'][i] == "posVal") : s['sentiment'][i] = 1
```
###### Dataset
* [samsung_stock_dataset_finBERT_notnull.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/samsung_stock_dataset_finBERT_notnull.xlsx)
* [hyundai_stock_dataset_finBERT_notnull.xlsx](https://github.com/SNU-dataproject/kr-finbert/blob/main/datasets/hyundai_stock_dataset_finBERT_notnull.xlsx)

---

# Model
### 1. LSTM📝
* Base Model : [model_base.ipynb](https://github.com/SNU-dataproject/kr-finbert/blob/main/model/model_base.ipynb)
* Select columns(normalization X) : [model_select_column_no_normalize.ipynb](https://github.com/SNU-dataproject/kr-finbert/blob/main/model/model_select_column_no_normalize.ipynb)
* Select columns(normalization O) : [model_select_column.ipynb](https://github.com/SNU-dataproject/kr-finbert/blob/main/model/model_select_column.ipynb)
* Add finBERT col : [model_add_bert.ipynb](https://github.com/SNU-dataproject/kr-finbert/blob/main/model/model_add_bert.ipynb)
* [model_add_all.ipynb](https://github.com/SNU-dataproject/kr-finbert/blob/main/model/model_add_all.ipynb)
