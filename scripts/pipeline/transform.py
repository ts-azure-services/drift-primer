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

def getArgs(argv=None):
    parser = argparse.ArgumentParser(description="filepaths")
    parser.add_argument("--input_file_path", help='Input file path')
    parser.add_argument("--input_filename", help='Input filename')
    parser.add_argument("--output_file_path", help='Output file path')
    parser.add_argument("--output_filename", help='Filename')
    return parser.parse_args(argv)

def transform(source=None):
    """Load original data"""
    def_blob_store = ws.get_default_datastore()

    df = pd.read_csv(source)
    #df['TotalCharges'] = df['TotalCharges'].str.replace(r' ','0').astype(float)
    df['Churn'] = df['Churn'].apply(lambda x: 0 if x == "No" else 1)
    df['SeniorCitizen'] = df['SeniorCitizen'].apply(lambda x: "No" if x == 0 else "Yes")
    df['Tenure_Bucket'] = pd.cut(
            x = df['tenure'],
            bins=[0,10,30,100],
            labels=['One to 10 days', '+10 to 30 days', 'Beyond +1 month'],
            include_lowest=True
            )

    # Register the training dataset
    _ = Dataset.Tabular.register_pandas_dataframe(
            dataframe=df,
            target=def_blob_store,
            name='Transformed Training Baseline Dataset',
            description='90% of baseline dataset being used for training'
            )

    return df


if __name__ == "__main__":
    args = getArgs()
    logging.info(f'Input args: {args.input_file_path}')
    logging.info(f'Output args: {args.output_file_path}')
    logging.info(f'Filename: {args.output_filename}')
    df = transform(source=args.input_file_path + '/' + args.input_filename)
    df.to_csv(args.output_file_path + '/' + args.output_filename, index=False)
