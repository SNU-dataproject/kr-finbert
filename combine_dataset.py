import pandas as pd
import re
from tabulate import tabulate


# tabulate 라이브러리 사용해서 로컬에서 print 대신 print_df 함수 사용해서 Jupyter notebook 처럼 보기
def print_df(d):
    print(tabulate(d, headers='keys', tablefmt='psql'))


def date_preprocess(d):
    d['date'] = d['date'].apply(lambda x: re.sub('[./]', '', x))
    return d


finance_news = pd.read_excel('naver_finance_news.xlsx', usecols=[2, 0])
finance_news = date_preprocess(finance_news)

naver_news = pd.read_excel('naver_news.xlsx')
naver_news = date_preprocess(naver_news)

report = pd.read_excel('report.xlsx')
report = date_preprocess(report)

df = naver_news.append(finance_news, ignore_index=True)
df = df.append(report, ignore_index=True)
df = df.sort_values('date', ignore_index=True)

print(df.shape)
# df['duplicated'] = df.duplicated(['date'])
# print_df(df.head(10))
# print_df(df.tail(10))
df.to_excel('combined_dataset.xlsx', encoding='cp949')