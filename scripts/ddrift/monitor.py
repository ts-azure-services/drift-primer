"""Data drift monitor script"""
import sys
import time
import os.path
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..')))
from scripts.authentication.service_principal import ws
from scripts.setup.common import upload_and_register, model_train, register_best_model
from azureml.core import Dataset#, ScriptRunConfig, Environment
from azureml.core.compute import ComputeTarget
from azureml.datadrift import DataDriftDetector, AlertConfiguration
import pandas as pd
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


# Reference datasets and add timestamp column
def create_monitor_datasets(
        ws=None,
        base_dataset=None,
        target_dataset=None
        ):
    def_blob_store = ws.get_default_datastore()

    # BASELINE DATA
    baseline_data = Dataset.get_by_name(workspace=ws, name=base_dataset)
    baseline_data = baseline_data.to_pandas_dataframe()
    baseline_data['Period'] = pd.to_datetime('2021-01-01')

    # Register baseline data with timestamp
    name = 'Data Monitor Baseline (pre-timestamp)'
    bd_tabular = Dataset.Tabular.register_pandas_dataframe(
            dataframe = baseline_data,
            target = def_blob_store,
            name = name
            )

    name = 'Data Monitor Baseline'
    bd_tabular = bd_tabular.with_timestamp_columns('Period')
    _ = bd_tabular.register(ws, name = name,
            create_new_version=True, description='Data Drift Monitor Baseline Dataset')

    # TARGET COMPARISON
    target_data = Dataset.get_by_name(workspace=ws, name=target_dataset)
    target_data = target_data.to_pandas_dataframe()
    target_data['Period'] = pd.to_datetime('2021-03-01')

    # Register target data with timestamp
    name = 'Data Monitor Target (pre-timestamp)'
    td_tabular = Dataset.Tabular.register_pandas_dataframe(
            dataframe = target_data,
            target = def_blob_store,
            name = name
            )

    name = 'Data Monitor Target'
    td_tabular = td_tabular.with_timestamp_columns('Period')
    _ = td_tabular.register(
            workspace=ws, 
            name = name,
            create_new_version=True, 
            description='Data Drift Monitor Target Dataset'
            )
    return bd_tabular, td_tabular


# Select features
def select_features(tabular_dataset=None):
    columns  = list(tabular_dataset.take(1).to_pandas_dataframe())
    exclude  = ['__index_level_0__']
    features = [col for col in columns if col not in exclude]
    return features

# Get dataset monitor
def get_dataset_monitor(
        ws=None, 
        dset_monitor_name=None, 
        baseline=None, 
        target=None, 
        compute_target=None, 
        features=None
        ):
    try:
        monitor = DataDriftDetector.get_by_name(ws, dset_monitor_name)
        print(f'Found the dataset monitor called: {dset_monitor_name}')
    except:
        # replace with your email to recieve alerts from the scheduled pipeline after enabling
        alert_config = AlertConfiguration(['thomassantosh@gmail.com']) 
        monitor = DataDriftDetector.create_from_datasets(
            ws, dset_monitor_name, baseline, target,
            compute_target=compute_target, 
          frequency='Week',# how often to analyze target data
          feature_list=features,                
          drift_threshold=None,# threshold from 0 to 1 for email alerting
          latency=0,# SLA in hours for target data to arrive in the dataset
          alert_config=alert_config)
        print(f'Created the dataset monitor called {dset_monitor_name}')
    return monitor 


def trigger_run(monitor=None):
    """Trigger the data drift run"""
    ## update the feature list
    #monitor  = monitor.update(feature_list=features)

    # Trigger run for backfill for one month
    start_date = datetime(2021, 1, 1)
    end_date = datetime(2021, 3, 31)
    backfill = monitor.backfill(start_date, end_date)
    backfill.wait_for_completion(wait_post_processing=True)


def main():
    bd_tabular, td_tabular = create_monitor_datasets(
            ws=ws, base_dataset='Transformed Training Baseline Dataset',
            target_dataset='Data Drift Dataset')

    features = select_features(td_tabular)

    monitor = get_dataset_monitor(
            ws=ws,
            dset_monitor_name='churn-data-drift',
            baseline=bd_tabular,
            target=td_tabular,
            compute_target = ComputeTarget(workspace=ws, name='cpu-cluster'),
            features=features
            )

    trigger_run(monitor=monitor)

if __name__ == "__main__":
    main()

