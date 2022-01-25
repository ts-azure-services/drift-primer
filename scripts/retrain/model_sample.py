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
from azureml.train.automl.run import AutoMLRun
from azureml.core.run import Run, _OfflineRun
from azureml.core.model import Model
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


def register_best_model(remote_run=None):
    """Register the best model from the AutoML run"""
    #best_run = run.get_best_child()
    best_run, fitted_model = remote_run.get_output()
    print(f'best run properties: {best_run.properties}')
    #print(type(best_run))
    #print(type(fitted_model))
    model_name = best_run.properties['model_name']
    model_path = best_run.properties['model_output_path']
    print(f'Model name : {model_name}')
    description = 'AutoML retrain model'
    model = Model.register(
            workspace = ws,
            #model_path='outputs/model.pkl',
            model_path=model_path,#'outputs/model.pkl',
            model_name = model_name, 
            description = description,
            )
    logging.info(f"Registered {model_name}, with {description}")


def main():

    name = 'Retrain Dataset'
    experiment_name = 'retrain_experiment'
    compute_target = ComputeTarget(workspace=ws, name='cpu-cluster')
    experiment = Experiment(ws, name = experiment_name)

    remote_run = AutoMLRun(experiment, run_id='AutoML_66423fac-93b5-4188-88bc-70d1d1102929')
    print(remote_run)
    print(f'type: {type(remote_run)}')

    # Register the best model
    register_best_model(remote_run = remote_run)


if __name__ == "__main__":
    main()

