import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..')))
import os
from datetime import datetime
import pandas as pd
from scripts.authentication.service_principal import ws
from azureml.core import Dataset
from azureml.data.dataset_factory import DataType
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def register_dataset(dataset=None, workspace=None, name=None, desc=None,tags=None):
    """Register datasets"""
    try:
        dataset = dataset.register(
                workspace=workspace, 
                name=name, 
                description=desc, 
                tags=tags,
                create_new_version=True
                )
        logging.info(f" Dataset registration successful for {name}")
    except Exception as e:
        logging.info(f" Exception in registering dataset. Error is {e}")


def create_test_train_set(fd=None, def_blob_store=None):
    # Create NYC dataset, in 5min intervals
    df = fd.to_pandas_dataframe()
    df = df [ df['Name'] == 'N.Y.C.']
    df = df.set_index('Time Stamp')

    # Remove any duplicate indexes
    df = df[~df.index.duplicated(keep='first')]

    # Resample to get 5 min intervals for this dataset
    df_final = df.resample('T').ffill().reindex(pd.date_range(df.index[0],df.index[-1],freq='5T'))
    logging.info(f'Index frequency is: {df_final.index.freq}')

    # Prep for loading into a Tabular Dataset
    df_final = df_final.reset_index()
    df_final.columns = ['Date','TZ','Place','Code','Load']
    logging.info(f'Length of dataframe is: {len(df_final)}')
    logging.info(f'Dataframe head is:\n {df_final.head()}')
    logging.info(f'Dataframe tail is:\n {df_final.tail()}')

    # Register the total NYC dataset
    curated_dataset = Dataset.Tabular.register_pandas_dataframe(
            dataframe=df_final,
            #target=(def_blob_store, '/curated-data'),
            target=def_blob_store,
            name='NYC energy dataset for 2020',
            description='NYC energy dataset in 5 min intervals'
            )

    # Create the test and train set, from tabular datasets
    curated_dataset = curated_dataset.with_timestamp_columns('Date')

    # Create the training set
    train = curated_dataset.time_between(
            start_time=datetime(2020,12,1,0),
            end_time=datetime(2020,12,24,23,59,0),
            include_boundary=True)
    train_df = train.to_pandas_dataframe().reset_index(drop=True)
    logging.info(train_df.head())
    logging.info(train_df.tail())
    register_dataset(dataset=train, workspace=ws, name='NYC-trainingset-Dec2020')

    # Create the test set
    test = curated_dataset.time_between(
            start_time=datetime(2020,12,25,0),
            end_time=datetime(2020,12,31,23,59,0),
            include_boundary=True)
    test_df = test.to_pandas_dataframe().reset_index(drop=True)
    logging.info(test_df.head())
    logging.info(test_df.tail())
    register_dataset(dataset=test, workspace=ws, name='NYC-testset-Dec2020')


def main():
    """Main operational flow"""
    # Set target locations, retrieve default blob store and upload files
    target_def_blob_store_path = '/blob-input-data/'
    def_blob_store = ws.get_default_datastore()

    # Create the tabular dataset for all files, and register 
    datastore_paths = [(def_blob_store, str(target_def_blob_store_path))]
    fd = Dataset.Tabular.from_delimited_files(
            path=datastore_paths, set_column_types={
                'Time Stamp':DataType.to_datetime(formats='%m/%d/%Y %H:%M:%S'),
                'Time Zone':DataType.to_string(),
                'Name':DataType.to_string(),
                'PTID':DataType.to_string(),
                'Load':DataType.to_float()
                })
    fd = fd.with_timestamp_columns(timestamp='Time Stamp')

    # Register the full dataset
    register_dataset(dataset=fd, workspace=ws, name='Energy Data for 2020')

    # Create test, train set
    create_test_train_set(fd = fd, def_blob_store = def_blob_store)

if __name__ == "__main__":
    main() 
