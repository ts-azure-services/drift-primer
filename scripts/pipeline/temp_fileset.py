# Script to run a few data filtering and transformation operations
import os, datetime, random, argparse
import pandas as pd
import datetime as dt
import sys
import os.path
import pandas as pd
from azureml.core import Dataset
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..')))
from scripts.authentication.service_principal import ws
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def transform(source=None):
    """Load original data"""
    def_blob_store = ws.get_default_datastore()

    df = pd.read_csv(source)
    df['Tenure_Bucket'] = pd.cut(x = df['tenure'],bins=10,include_lowest=True)

    ## Register the training dataset
    #_ = Dataset.Tabular.register_pandas_dataframe(
    #        dataframe=df,
    #        target=def_blob_store,
    #        name='Transformed Training Baseline Dataset',
    #        description='90% of baseline dataset being used for training'
    #        )
    return df


if __name__ == "__main__":
    source = './../../datasets/original/WA_Fn-UseC_-Telco-Customer-Churn.csv'
    df = transform(source = source)
    df.to_csv('./../../datasets/temp_baseline_filedataset.csv')
