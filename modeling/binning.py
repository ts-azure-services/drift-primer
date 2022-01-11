import pandas as pd

df = pd.read_csv('./../datasets/input-data/WA_Fn-UseC_-Telco-Customer-Churn.csv')

df = df[['customerID','tenure', 'Churn']]
df['Churn'] = df['Churn'].apply(lambda x: 0 if x == "No" else 1)

df['bucket'] = pd.cut(
        x = df['tenure'],
        bins=[0,10,30,100],
        labels=['One to 10 days', '+10 to 30 days', 'Beyond +1 month'],
        include_lowest=True
        )
df = df.sort_values(by = 'tenure', ascending=True)

df = df.groupby(['bucket']).agg({
    'customerID': 'count',
    'Churn':'sum',
    })

df['Churn %'] = df['Churn'] / df['customerID']

print(df)

