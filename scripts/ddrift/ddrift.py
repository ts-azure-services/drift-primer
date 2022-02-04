"""Data drift script that includes
uploading the dataset, registering it as a tabular dataset,
training it with AutoML, and registering the model
"""
import sys
import time
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..')))
from scripts.authentication.service_principal import ws
from scripts.setup.common import upload_and_register, model_train, register_best_model
from azureml.core import Dataset#, ScriptRunConfig, Environment
from azureml.core.compute import ComputeTarget
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')



def main():
    
    # Declare key objects
    name = 'Data Drift Dataset'
    experiment_name = 'ddrift_experiment'
    compute_target = ComputeTarget(workspace=ws, name='cpu-cluster')
    local_data_folder = './datasets/ddrift_data/'
    target_def_blob_store_path = '/blob-ddrift-dataset/'

    # Upload the dataset, and register as a tabular dataset
    upload_and_register(
            name=name,
            local_data_folder=local_data_folder,
            target_def_blob_store_path=target_def_blob_store_path
            )

    # Train the model
    ds = Dataset.get_by_name(workspace=ws, name=name)
    remote_run = model_train(
            dataset=ds, 
            compute_target= compute_target, 
            experiment_name=experiment_name
            )

    # Register the best model
    register_best_model(
            remote_run = remote_run, 
            model_name='DataDrift_Model',
            model_path='outputs/model.pkl',
            description='AutoML Data Drift Model'
            )


if __name__ == "__main__":
    main()

