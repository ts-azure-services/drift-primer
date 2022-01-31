import pandas as pd
# make a single prediction with the model
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_blobs
# create the inputs and outputs
X, y = make_blobs(n_samples=10000, centers=2, n_features=2, random_state=2)

df = pd.DataFrame(X)
df['target'] = y
df.columns = ['att1', 'att2', 'target']
df.to_csv('train_baseline.csv', encoding='utf-8', index=False)
# define model
model = LogisticRegression(solver='lbfgs')
# fit model
model.fit(X, y)
# make predictions on the entire training dataset
yhat = model.predict(X)
# connect predictions with outputs
for i in range(10):
	print(X[i], yhat[i])
