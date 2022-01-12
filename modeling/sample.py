import pandas as pd

df = pd.read_csv('./../datasets/input-data/WA_Fn-UseC_-Telco-Customer-Churn.csv')
df = df [ df['tenure'] ==1 ]
df.to_csv('one_month.csv', index=False)
