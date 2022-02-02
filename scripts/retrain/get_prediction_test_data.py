import urllib.request
import json
import time
import os
import ssl
from azureml.core import Workspace
from azureml.core import Dataset
import pandas as pd
from dotenv import load_dotenv

def load_env_variables():
    """Load env variables"""
    env_var = load_dotenv('./baseline_endpoint.env')
    auth_dict = {"url": os.environ['URL'],"api_key": os.environ['API_KEY']}
    ws = Workspace.from_config()
    return ws, auth_dict

def request_records(ws=None):
    """Create request records"""
    # Pull in the test dataset
    ds = Dataset.get_by_name(workspace=ws, name='Test Baseline Dataset')
    ds = ds.to_pandas_dataframe()
    ds['TotalCharges'] = ds['TotalCharges'].fillna(0)
    #print(ds.info())

    # Get the original dataset
    # Will not be needed if you reconfigure the pipeline
    df = pd.read_csv('../../datasets/original/WA_Fn-UseC_-Telco-Customer-Churn.csv')
    df['Tenure_Bucket'] = pd.cut(x = df['tenure'],bins=10,include_lowest=True).astype(str)
    df = df[['customerID', 'Tenure_Bucket']]

    # Merge on the index to get the tenure bucket attribute
    ds = ds.merge(df, how='inner',on='customerID')
    ds = ds.reset_index() # keeping index, since part of data request

    # Drop 'Churn column'
    churn_df = ds[['Churn']]
    ds = ds.drop('Churn', axis=1)
    assert list(ds.index) == list(churn_df.index)

    list_of_records = ds.to_dict('records')
    return list_of_records, churn_df

def score_request(
        record_list=None,
        url=None,
        api_key=None
        ):
    """Score request"""
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

def create_predictions(
        auth_dict=None,
        list_of_records=None
        ):
    """Create predictions"""
    # Create batch size
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
    return result_list

def get_accuracy(prediction_list=None, churn_df=None):
    """Compare accuracy"""
    final_list = []
    for item in prediction_list:
        for val in item:
            final_list.append(val)

    new_df = pd.DataFrame(final_list)
    assert list(new_df.index) == list(churn_df.index)

    # Compare model accuracy against test dataset prediction
    churn_df = churn_df.merge(new_df, how='inner', left_index=True, right_index=True)
    churn_df.columns = ['Actual_Churn', 'Predicted_Churn']
    churn_df['Actual_Churn'] = churn_df['Actual_Churn'].astype(str)
    churn_df['Predicted_Churn'] = churn_df['Predicted_Churn'].astype(str)
    #churn_df.to_csv('churn_df.csv', index=False, encoding='utf-8')
    error_count = len(churn_df.loc[(churn_df['Actual_Churn'] != churn_df['Predicted_Churn'])])
    error_rate = error_count / len(churn_df) * 100
    print(f'Error count is: {error_count}')
    print(f'Error rate is: {error_rate}')


def main():
    "Main operational workflow"

    # Load relevant authentication
    ws, auth_dict = load_env_variables()
    
    # Create request list
    list_of_records, churn_df = request_records(ws=ws)

    # Create predictions from real-time endpoint
    prediction_list = create_predictions(auth_dict=auth_dict, list_of_records=list_of_records)

    # Get accuracy, comparing actual churn vs. predicted churn
    get_accuracy(prediction_list=prediction_list, churn_df=churn_df)


if __name__ == "__main__":
    main()
