# pip install tabulate 해야함 !!
import pandas as pd
from tabulate import tabulate
import re


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


df = pd.read_excel('combined_dataset.xlsx', index_col=0)
# df에 중복 여부 컬럼 추가
df['duplicated'] = df.duplicated(['date'])
print_df(df.head(10))
print_df(df.tail(10))

res = eliminate_dup_date(df, pd.DataFrame(columns=['date', 'title']))
print_df(res.tail(10))

# date 열 datetime 형식으로 변경하고 인덱스 지정
res['date'] = pd.to_datetime(res['date'], format='%Y%m%d').dt.normalize()
res = res.set_index('date')
print_df(res.tail(10))

# 중복 제거 전후 데이터셋의 크기 비교
print(f'중복 데이터셋의 크기: {len(df)}, 중복 제거한 데이터셋의 크기: {len(res)}')
print(df.date.unique())

res.to_excel('dup_eliminated_dataset.xlsx', encoding='cp949')