"""Retrain script that includes
uploading the dataset, registering it as a tabular dataset,
training it with AutoML, and registering the model
"""
import sys
import time
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..')))
from scripts.authentication.service_principal import ws
from scripts.setup.upload_baseline_data import upload_files_from_local, register_dataset
from azureml.core import Dataset#, ScriptRunConfig, Environment
from azureml.core.experiment import Experiment
from azureml.core.compute import ComputeTarget
from azureml.core.runconfig import RunConfiguration
from azureml.train.automl import AutoMLConfig
from azureml.core.run import Run, _OfflineRun
from azureml.core.model import Model
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


def upload_and_register(name=None):
    """Upload and register the specified dataset"""
    local_data_folder = './datasets/retrain_data/'
    target_def_blob_store_path = '/blob-retrain-dataset/'
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
        "allowed_models":['XGBoostClassifier'],
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
    run = experiment.submit(automl_config, show_output=True, wait_post_processing=True)
    run.wait_for_completion()
    run_context = run.get_context()
    logging.info(f'Run details: {run}')
    logging.info(f'Run details: {run_context}')
    return run


def register_best_model(run=None):
    """Register the best model from the AutoML run"""
    best_run = run.get_best_child()
    model_name = best_run.properties['model_name']
    description = 'AutoML retrain model'
    tags = str(time.strftime('%d/%m/%Y %H:%M:%S'))
    model = best_run.register_model(
            model_name = model_name,
            description = description,
            tags = tags
            )
    logging.info(f"Registered {model_name}, with {description} and {tags}")


def main():

    name = 'Retrain Dataset'
    experiment_name = 'retrain_experiment'
    compute_target = ComputeTarget(workspace=ws, name='cpu-cluster')
    ## Upload the dataset, and register as a tabular dataset
    #upload_and_register(name=name)

    # Train the model
    ds = Dataset.get_by_name(workspace=ws, name=name)
    run = model_train(dataset=ds, compute_target= compute_target, experiment_name=experiment_name)

    # Register the best model
    register_best_model(run = run)


if __name__ == "__main__":
    main()

