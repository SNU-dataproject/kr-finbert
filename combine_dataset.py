import pandas as pd
import re
from tabulate import tabulate


# tabulate 라이브러리 사용해서 로컬에서 print 대신 print_df 함수 사용해서 Jupyter notebook 처럼 보기
# def print_df(d):
#     print(tabulate(d, headers='keys', tablefmt='psql'))


def date_preprocess(d):
    d['date'] = d['date'].apply(lambda x: re.sub('[./]', '', x))
    return d


def combine_dataset(n, f, r):
    n = date_preprocess(n)
    f = date_preprocess(f)
    r = date_preprocess(r)

    df = n.append(f, ignore_index=True).append(r, ignore_index=True)
    df = df.sort_values('date', ignore_index=True)
    print(df.shape)
    df.to_excel('./datasets/combined_dataset.xlsx', encoding='cp949')


combine_dataset(pd.read_excel('./datasets/naver_news.xlsx'), \
                pd.read_excel('./datasets/naver_finance_news.xlsx'), \
                pd.read_excel('./datasets/report.xlsx'))