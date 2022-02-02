import urllib.request
import json
import time
import os
import ssl
from azureml.core import Workspace
from azureml.core import Dataset
import pandas as pd
from dotenv import load_dotenv

env_var = load_dotenv('./baseline_endpoint.env')
auth_dict = {"url": os.environ['URL'],"api_key": os.environ['API_KEY']}
ws = Workspace.from_config()

# Pull in the test dataset
ds = Dataset.get_by_name(workspace=ws, name='Test Baseline Dataset')
ds = ds.to_pandas_dataframe()
ds['TotalCharges'] = ds['TotalCharges'].fillna(0)
print(ds.info())

# Get the original dataset
# Will not be needed if you reconfigure the pipeline
df = pd.read_csv('../../datasets/original/WA_Fn-UseC_-Telco-Customer-Churn.csv')
df['Tenure_Bucket'] = pd.cut(x = df['tenure'],bins=10,include_lowest=True).astype(str)
df = df[['Tenure_Bucket']]

# Merge on the index to get the tenure bucket attribute
ds = ds.merge(df, how='inner', left_index=True, right_index=True)

# Drop 'Churn column'
churn_truth = ds[['Churn']]
ds = ds.drop('Churn', axis=1)
ds = ds.reset_index()

list_of_records = ds.to_dict('records')

def score_request(
        record_list=None,
        url=None,
        api_key=None
        ):

    data = {
        "Inputs": {
            "data": record_list,
        },
        "GlobalParameters": {
            'method': "predict",
        }
    }

    body = str.encode(json.dumps(data))
    url = url
    api_key = api_key

    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read().decode("utf8", "ignore")
        print(result)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        print(error.info())
        result = 'No result'
    return result

print(f'length of records: {len(list_of_records)}')
n = 1000
master_list = [ list_of_records[i:i+n] for i in range(0, len(list_of_records), n) ]
result_list = []
for sublist in master_list:
    time.sleep(2)
    results = score_request(
            record_list=sublist, 
            url=auth_dict['url'], 
            api_key=auth_dict['api_key']
            )
    if results != 'No result':
        results = json.loads(results)
        result_list.append(results['Results'])
        print(f'length of result list: {len(result_list)}')

final_list = []
for item in result_list:
    for val in item:
        final_list.append(val)

new_df = pd.DataFrame(final_list)
print(len(new_df))
#print(new_df.head())

# Compare model accuracy against test dataset prediction
churn_truth = churn_truth.merge(new_df, how='inner', left_index=True, right_index=True)
churn_truth.columns = ['Actual_Churn', 'Predicted_Churn']
churn_truth.to_csv('churn_truth.csv', encoding='utf-8')
