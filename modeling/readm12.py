import pandas as pd
df = pd.read_pickle('./../datasets/M12.pkl')
df.to_csv('M12.csv')
