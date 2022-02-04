import argparse
import sys
import os.path
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..')))
from scripts.authentication.service_principal import ws
from azureml.core import Dataset
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def getArgs(argv=None):
    parser = argparse.ArgumentParser(description="filepaths")
    parser.add_argument("--input_file_path", help='Input file path')
    parser.add_argument("--input_filename", help='Input filename')
    parser.add_argument("--output_file_path", help='Output file path')
    parser.add_argument("--output_filename", help='Output filename')
    return parser.parse_args(argv)


def register_train_test_split(source=None):

    # Define blob store
    def_blob_store = ws.get_default_datastore()

    # Create dataframe out of intermediate dataset
    df = pd.read_csv(source)

    # Register the full dataset
    _ = Dataset.Tabular.register_pandas_dataframe(
            dataframe=df,
            target=def_blob_store,
            name='Transformed Training Baseline Dataset',
            description='100% of baseline dataset with some transformed features'
            )

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
            description='10% of baseline dataset reserved for testing'
            )

    # Reset index
    train = train.reset_index(drop=True)
    return train


def main():
    """Main operational flow"""
    args = getArgs()
    logging.info(f'Input file path: {args.input_file_path}')
    logging.info(f'Input filename: {args.input_filename}')
    logging.info(f'Output args: {args.output_file_path}')
    logging.info(f'Filename: {args.output_filename}')
    train_df = register_train_test_split(source=args.input_file_path + '/' + args.input_filename)
    train_df.to_csv(args.output_file_path + '/' + args.output_filename, index=False)


if __name__ == "__main__":
    main() 
