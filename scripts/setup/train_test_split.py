import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..')))
from scripts.authentication.service_principal import ws
from azureml.core import Dataset
#from azureml.data.dataset_factory import DataType
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


def register_train_test_split(fd=None, def_blob_store=None):
    # Create dataframe out of registered dataset
    df = fd.to_pandas_dataframe()
    df = df.reset_index()

    # Create train, test splits
    train = df.sample(frac=0.9, random_state=200)
    test = df.drop(train.index)

    # Prep for loading into a Tabular Dataset
    logging.info(f"Length of dataframe is: {len(df)}")
    logging.info(f"Length of 'train' dataframe is: {len(train)}")
    logging.info(f"Length of 'test' dataframe is: {len(test)}")

    # Register the training dataset
    _ = Dataset.Tabular.register_pandas_dataframe(
            dataframe=train,
            target=def_blob_store,
            name='Training Baseline Dataset',
            description='90% of baseline dataset being used for training'
            )

    # Register the test dataset
    _ = Dataset.Tabular.register_pandas_dataframe(
            dataframe=test,
            target=def_blob_store,
            name='Test Baseline Dataset',
            description='90% of baseline dataset reserved for testing'
            )


def main():
    """Main operational flow"""
    # Set target locations, retrieve default blob store and upload files
    #target_def_blob_store_path = '/blob-input-data/'
    def_blob_store = ws.get_default_datastore()

    # Get the registered baseline dataset
    #datastore_paths = [(def_blob_store, str(target_def_blob_store_path))]
    fd = Dataset.get_by_name(name='Baseline Dataset', workspace=ws)

    # Create test, train set
    register_train_test_split(
            fd = fd, 
            def_blob_store = def_blob_store
            )

if __name__ == "__main__":
    main() 
