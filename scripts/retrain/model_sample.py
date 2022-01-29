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
from azureml.core.model import InferenceConfig
from azureml.core.webservice import AciWebservice
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
from azureml.core import Environment
from azureml.core.conda_dependencies import CondaDependencies



def register_best_model(remote_run=None):
    """Register the best model from the AutoML run"""
    best_child = remote_run.get_best_child()
    model_name = 'Retrain_New_Model_new'
    model_path = 'outputs/model.pkl'
    description = 'AutoML Retrain Model'
    model = best_child.register_model(
            model_name = model_name,
            model_path = model_path,
            description = description,
            )
    logging.info(f"Registered {model_name}, with {description}")
    return model


def main():

    name = 'Retrain Dataset'
    experiment_name = 'retrain_experiment'
    compute_target = ComputeTarget(workspace=ws, name='cpu-cluster')
    experiment = Experiment(ws, name = experiment_name)

    remote_run = AutoMLRun(experiment, run_id='AutoML_66423fac-93b5-4188-88bc-70d1d1102929')
    print(remote_run)
    print(f'type: {type(remote_run)}')

    # Register the best model
    model = register_best_model(remote_run = remote_run)

   # # Deploy the model to ACI
   # environment = Environment('my-sklearn-environment')
   # environment.python.conda_dependencies = CondaDependencies.create(pip_packages=[
   #     'azureml-defaults',
   #     #'inference-schema[numpy-support]',
   #     'joblib',
   #     'numpy',
   #     'scikit-learn'
   # ])

   # inference_config= InferenceConfig(entry_script='score.py', environment=environment)
   # aci_config = AciWebservice.deploy_configuration(cpu_cores=1, memory_gb=1)
   # service_name='sample-service'

   # service = Model.deploy(workspace=ws,
   #                    name=service_name,
   #                    models=[model],
   #                    inference_config=inference_config,
   #                    deployment_config=aci_config,
   #                    overwrite=True)
   # service.wait_for_deployment(show_output=True)


if __name__ == "__main__":
    main()

