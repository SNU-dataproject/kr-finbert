import pandas as pd


# 날짜 중복삭제 & title 합치기
def eliminate_dup_date(d, new_d):
    for date, tit, dup in d.values:
        if not dup:
            new_d = new_d.append(pd.Series([date, tit], index=new_d.columns), ignore_index=True)
        else:
            new_d.iloc[-1, -1] = new_d.iloc[-1, -1] + ', ' + tit
    return new_d


df = pd.read_excel('./datasets/combined_dataset_cleaned.xlsx', index_col=0)
df['duplicated'] = df.duplicated(['date'])
res = eliminate_dup_date(df, pd.DataFrame(columns=['date', 'title']))
res.to_excel('./datasets/preprocessed_dup_eliminated_dataset.xlsx', encoding='cp949')