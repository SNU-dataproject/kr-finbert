# Dataset
### 1. Raw Data Crawling 📄
* 기업명_raw_naver_finance_news.xlsx
* 기업명_raw_naver_news.xlsx
* 기업명_raw_report.xlsx

### 2. Merge & Sort & Preprocess & Combine 📚
* 기업명_cleaned_combined_dataset.xlsx


### 3. Add finbert score 😱
* 기업명_cleaned_combined_dataset_finBERT.xlsx

### 4. Add finbert score to FinanceDataReader😇
##### FinanceDataReader 정보에 kr-finBERT col 추가 및 결측치 처리
* 기업명_stock_dataset_finBERT_notnull.xlsx

---

# Model
### 1. LSTM📝
* Base Model : [model_base.ipynb](https://github.com/SNU-dataproject/kr-finbert/blob/main/model/model_base.ipynb)
* Select columns(normalization X) : [model_select_column_no_normalize.ipynb](https://github.com/SNU-dataproject/kr-finbert/blob/main/model/model_select_column_no_normalize.ipynb)
* Select columns(normalization O) : [model_select_column.ipynb](https://github.com/SNU-dataproject/kr-finbert/blob/main/model/model_select_column.ipynb)
* Add finBERT col : [model_add_bert.ipynb](https://github.com/SNU-dataproject/kr-finbert/blob/main/model/model_add_bert.ipynb)
* [model_add_all.ipynb](https://github.com/SNU-dataproject/kr-finbert/blob/main/model/model_add_all.ipynb)
