import pandas as pd
import numpy as np
import re
from tabulate import tabulate


# tabulate 라이브러리 사용해서 로컬에서 print 대신 print_df 함수 사용해서 Jupyter notebook 처럼 보기
def print_df(d):
    print(tabulate(d, headers='keys', tablefmt='psql'))


# 날짜 중복삭제 & title 합치기
def eliminate_dup_date(d, new_d):
    for date, tit, dup in d.values:
        if not dup:
            new_d = new_d.append(pd.Series([date, tit], index=new_d.columns), ignore_index=True)
        else:
            new_d.iloc[-1, -1] = new_d.iloc[-1, -1] + ', ' + tit
    return new_d


def preprocess(row):
    row = re.sub('ㅁ', "", row)
    row = re.sub(r"\n", ",", row)

    # 용어
    row = re.sub("YoY|yoy|YOY", "전년 대비 증감율", row)
    row = re.sub("QoQ|qoq|QOQ", "전분기 대비 증감율", row)
    row = re.sub("MoM|mom|MOM", "전월 대비 증감율", row)
    row = re.sub("YTD", "연초 누계", row)
    row = re.sub("MTD", "월초 누계", row)

    # 분기 표현 1Q21F->21년도 1분기 예측값
    quarter_rule2 = re.compile(r'([1-4]Q[\d]{2}F)')
    quarter_text2 = quarter_rule2.finditer(row)

    startIdxList2 = []
    for text in quarter_text2:
        startIdxList2.append(text.start())
    for i in range(len(startIdxList2) - 1, -1, -1):
        idx = startIdxList2[i]
        quar = row[idx:idx + 5]
        new_quar_text = row[idx + 2:idx + 4] + "년도 " + row[idx] + "분기 예측값"
        row = row.replace(quar, new_quar_text)

    # 분기 표현 1Q21->21년도 1분기
    quarter_rule1 = re.compile(r'([1-4]Q[\d]{2})')
    quarter_text1 = quarter_rule1.finditer(row)

    startIdxList1 = []
    for text in quarter_text1:
        startIdxList1.append(text.start())
    for i in range(len(startIdxList1) - 1, -1, -1):
        idx = startIdxList1[i]
        quar = row[idx:idx + 4]
        new_quar_text = row[idx + 2:idx + 4] + "년도 " + row[idx] + "분기 "
        row = row.replace(quar, new_quar_text)

    # 분기 표현 1H21->21년도 상반기
    half_rule = re.compile(r'([12]H[\d]{2})')
    half_text = half_rule.finditer(row)
    startIdxList3 = []
    for text in half_text:
        startIdxList3.append(text.start())
    for i in range(len(startIdxList3) - 1, -1, -1):
        idx = startIdxList3[i]
        half = row[idx:idx + 4]
        if (row[idx] == 1):
            new_half_text = row[idx + 2:idx + 4] + "년도 상반기 "
        else:
            new_half_text = row[idx + 2:idx + 4] + "년도 하반기 "

        row = row.replace(half, new_half_text)

    # [내용] 제거
    row = re.sub(r'\[[^)]*\]', '', row)
    # 문장시작이 "삼성전자-"인 경우 삭제
    if (row[:5] == "삼성전자-"): row = row[5:]
    # 다중 띄어쓰기
    row = re.sub(' +', ' ', row)
    # 앞뒤 공백
    row = re.sub(r"^\s+", "", row, flags=re.UNICODE)
    row = re.sub(r"\s+$", "", row, flags=re.UNICODE)

    return row


def date_preprocess(d):
    d['date'] = d['date'].apply(lambda x: re.sub('[./]', '', x))
    return d


def combine_dataset(n, f, r):
    n = date_preprocess(n)
    f = date_preprocess(f)
    r = date_preprocess(r)

    df = n.append(f, ignore_index=True).append(r, ignore_index=True)
    df = df.sort_values('date', ignore_index=True)
    return df


def get_preprocessed_dataset():
    combined_dataset = combine_dataset(pd.read_excel('./datasets/raw_naver_news.xlsx'), \
                    pd.read_excel('./datasets/raw_naver_finance_news.xlsx', usecols="A,C"), \
                    pd.read_excel('./datasets/raw_report.xlsx'))

    logCnt = 1000
    plusCnt = 1000
    for i in range(len(combined_dataset)):
        if (i == logCnt):
            print(i)
            logCnt += plusCnt

        # 영어로만 구성된 row는 drop
        if (len(re.findall(u'[가-힣]+', combined_dataset['title'][i])) > 0):
            combined_dataset['title'][i] = preprocess(combined_dataset['title'][i])
        else:
            combined_dataset = combined_dataset.drop(i)


    combined_dataset['title'].replace('', np.nan, inplace=True)
    combined_dataset = combined_dataset.dropna(subset=['title'])
    combined_dataset = combined_dataset.reset_index(drop=True)
    print("Done!")
    print_df(combined_dataset.tail())

    combined_dataset['duplicated'] = combined_dataset.duplicated(['date'])
    res = eliminate_dup_date(combined_dataset, pd.DataFrame(columns=['date', 'title']))

    print("===========combined_dataset=============")
    print_df(combined_dataset.tail(10))
    print("===========핀버트 적용만 안 한 데이터 셋=============")
    print_df(res.tail(10))

    res.to_excel('./datasets/cleaned_combined_dataset.xlsx', encoding='cp949', index=False)


get_preprocessed_dataset()