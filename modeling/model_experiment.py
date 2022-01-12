"""Script to test training against simulated data"""
import sys
sys.path.append('./../scripts/')
import os
from authentication import ws
import pandas as pd
from azureml.data.dataset_factory import TabularDatasetFactory
from azureml.core.compute import ComputeTarget
from azureml.core.experiment import Experiment
from azureml.train.automl import AutoMLConfig

def main():

    datastore = ws.get_default_datastore()
    compute_target = ComputeTarget(workspace=ws, name='cpu-cluster')
    experiment = Experiment(ws, name='baseline_scenario')

    training_data = TabularDatasetFactory.register_pandas_dataframe(
            pd.read_parquet('./../datasets/M9.parquet'),
            target=(datastore, "M9_data"),
            name='M9_adfas'
            )
    label_column_name = 'Churn'

    automl_settings = {
        #"n_cross_validations": 3,
        "primary_metric": 'AUC_weighted',
        "enable_early_stopping": False,
        "max_concurrent_iterations": 4,
        #"experiment_timeout_hours": 0.25,
        #"verbosity": logging.INFO,
        "enable_dnn": True,
        "enable_voting_ensemble": False,
        "enable_stack_ensemble": False
    }

    automl_config = AutoMLConfig(
            task = 'classification',
            #debug_log = 'automl_errors.log',
            compute_target = compute_target,
            training_data = training_data,
            label_column_name = label_column_name,
            **automl_settings
            )

    remote_run = experiment.submit(automl_config, show_output = False)

if __name__ == "__main__":
    main()
