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
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import itertools

def split_data(df=None, frac=None):
    """Split data into train/test"""
    test_data = df.sample(frac=frac, axis=0)
    train_data = df.drop(index=test_data.index)
    return train_data, test_data

def run_automl_classification(
        df=None,
        datastore=None,
        datastore_folder_name=None,
        dataset_name=None,
        compute_target=None,
        experiment=None
        ):
    """Execute AutoML training run"""

    training_data = TabularDatasetFactory.register_pandas_dataframe(
            #pd.read_parquet('./../datasets/M9.parquet'),
            df,
            target=(datastore, datastore_folder_name),
            name=dataset_name
            )
    label_column_name = 'Churn'

    automl_settings = {
        #"n_cross_validations": 3,
        "primary_metric": 'AUC_weighted',
        "enable_early_stopping": False,
        "max_concurrent_iterations": 4,
        #"experiment_timeout_hours": 0.25,
        "enable_dnn": True,
        "enable_voting_ensemble": False,
        "enable_stack_ensemble": False
    }

    automl_config = AutoMLConfig(
            task = 'classification',
            compute_target = compute_target,
            training_data = training_data,
            label_column_name = label_column_name,
            **automl_settings
            )

    # Execute run
    remote_run = experiment.submit(automl_config, show_output = False)
    remote_run.wait_for_completion(show_output=True)
    return remote_run

def plot_confusion_matrix(
        y_test_df = None,
        y_pred = None
        ):
    cf =confusion_matrix(y_test_df.values,y_pred)
    plt.imshow(cf,cmap=plt.cm.Blues,interpolation='nearest')
    plt.colorbar()
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    class_labels = ['False','True']
    tick_marks = np.arange(len(class_labels))
    plt.xticks(tick_marks,class_labels)
    plt.yticks([-0.5,0,1,1.5],['','False','True',''])
    # plotting text value inside cells
    thresh = cf.max() / 2.
    for i,j in itertools.product(range(cf.shape[0]),range(cf.shape[1])):
        plt.text(j,i,format(cf[i,j],'d'),horizontalalignment='center',color='white' if cf[i,j] >thresh else 'black')
    plt.show()
    plt.savefig('./image.png')

def main():

    # Load initial dataframe
    df = pd.read_parquet('./../datasets/M0.parquet')
    train, test = split_data(df=df, frac=0.2)

    # Set key objects
    experiment_name = 'baseline_scenario'
    datastore = ws.get_default_datastore()
    compute_target = ComputeTarget(workspace=ws, name='cpu-cluster')
    experiment = Experiment(ws, name=experiment_name)

    # Train model
    run = run_automl_classification(
            df = train,
            datastore = datastore,
            datastore_folder_name='base',
            dataset_name='base_boo',
            compute_target = compute_target,
            experiment = experiment,
            )

    # Retrieve results
    best_run, fitted_model = run.get_output()
    print(fitted_model)

    # Convert test dataframe in features/target
    # Predict with model
    x_test = test.drop('Churn', axis=1)
    y_test = test['Churn'].to_frame()
    y_pred = fitted_model.predict( x_test )
    print(y_pred)
    

    # Plot confusion matrix
    plot_confusion_matrix(
            y_test_df= y_test,
            y_pred= y_pred,
            )

    # Calculate metrics

    # Build an inference


if __name__ == "__main__":
    main()
