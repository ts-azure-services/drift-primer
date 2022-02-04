"""Script to consolidate some common functions"""
import sys
import time
import json
import pandas as pd
import urllib.request
import os.path
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..')))
from scripts.authentication.service_principal import ws
from scripts.setup.upload_baseline_data import upload_files_from_local, register_dataset
from azureml.core import Dataset#, ScriptRunConfig, Environment
from azureml.core.experiment import Experiment
from azureml.core.compute import ComputeTarget
from azureml.core.runconfig import RunConfiguration
from azureml.train.automl import AutoMLConfig
from azureml.train.automl.run import AutoMLRun
from azureml.core.run import Run, _OfflineRun
from azureml.core.model import Model
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def upload_and_register(
        name=None,
        local_data_folder=None,
        target_def_blob_store_path=None
        ):
    """Upload and register the specified dataset"""
    local_data_folder = local_data_folder 
    target_def_blob_store_path = target_def_blob_store_path
    def_blob_store = ws.get_default_datastore()
    datastore_paths = [(def_blob_store, str(target_def_blob_store_path))]

    # Upload files to blob store
    upload_files_from_local(
            local_data_folder=local_data_folder,
            target_def_blob_store_path=target_def_blob_store_path,
            def_blob_store=def_blob_store
            )

    # Convert to tabular, and then register as tabular
    fd = Dataset.Tabular.from_delimited_files(path=datastore_paths)
    register_dataset(dataset=fd, workspace=ws, name = name)

def model_train(dataset=None, compute_target=None, experiment_name=None):
    """Model and train with AutoML the dataset"""

    # Setup the classifier
    automl_settings = {
        "task": 'classification',
        "primary_metric":'AUC_weighted',
        "iteration_timeout_minutes": 10,
        "experiment_timeout_hours": 0.25,
        "compute_target":compute_target,
        "max_concurrent_iterations": 4,
        #"allowed_models":['XGBoostClassifier'],
        #"blocked_models":['XGBoostClassifier'],
        #"verbosity": logging.INFO,
        "training_data":dataset,#.as_named_input('retrain_dataset'),
        "label_column_name":'Churn',
        "n_cross_validations": 5,
        "enable_voting_ensemble":True,
        "enable_early_stopping": False,
        "model_explainability":True,
        #"enable_dnn":True,
            }
    automl_config = AutoMLConfig(**automl_settings)
    experiment = Experiment(ws, experiment_name)
    remote_run = experiment.submit(automl_config, show_output=True, wait_post_processing=True)
    remote_run.wait_for_completion()
    logging.info(f'Run details: {remote_run}')

    # Convert to AutoMLRun object
    remote_run = AutoMLRun(experiment, run_id=remote_run.id)
    return remote_run


def register_best_model(
        remote_run=None,
        model_name=None,
        model_path=None,
        description=None
        ):
    """Register the best model from the AutoML Run"""
    best_child = remote_run.get_best_child()
    model_name = model_name
    model_path = model_path
    description = description
    model = best_child.register_model(
            model_name = model_name,
            model_path = model_path,
            description = description,
            )
    logging.info(f"Registered {model_name}, with {description}")
    return model

def load_env_variables(url=None, api_key=None):
    """Load env variables"""
    env_var = load_dotenv('./endpoint_details.env')
    auth_dict = {
            "url": os.environ['BASELINE_URI'],
            "api_key": os.environ['BASELINE_APIKEY']}
    return auth_dict


def request_records(ws=None, dataset_name=None):
    """Create request records"""
    # Pull in the test dataset
    ds = Dataset.get_by_name(workspace=ws, name= dataset_name)
    ds = ds.to_pandas_dataframe()

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

    # In cases where Actual_Churn is 1 or 0, convert to T/F
    # Predicted_Churn always returns T/F
    if 1 or 0 in list(churn_df['Actual_Churn'].unique()):
        churn_df['Actual_Churn'].replace({0:False, 1:True}, inplace=True)

    churn_df['Actual_Churn'] = churn_df['Actual_Churn'].astype(str)
    churn_df['Predicted_Churn'] = churn_df['Predicted_Churn'].astype(str)
    churn_df.to_csv('churn_df.csv', index=False, encoding='utf-8')
    error_count = len(churn_df.loc[(churn_df['Actual_Churn'] != churn_df['Predicted_Churn'])])
    error_rate = error_count / len(churn_df) * 100
    print(f'Error count is: {error_count}')
    print(f'Error rate is: {error_rate}')

