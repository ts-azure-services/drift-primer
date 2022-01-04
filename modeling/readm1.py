import pandas as pd
df = pd.read_pickle('./../datasets/M1.pkl')
df.to_csv('M1.csv')
