import argparse
import pandas as pd
from authentication import ws
from azureml.core import Dataset
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def getArgs(argv=None):
    parser = argparse.ArgumentParser(description="filepaths")
    parser.add_argument("--input_file_path", help='Input file path')
    parser.add_argument("--filename", help='Input filename')
    parser.add_argument("--output_file_path", help='Output file path')
    parser.add_argument("--output_filename", help='Output filename')
    return parser.parse_args(argv)

def main():
    """Main operational flow"""
    args = getArgs()
    filepath = args.input_file_path + '/' + args.filename
    logging.info(f'Filepath is: {filepath}')

    df = pd.read_csv(filepath)
    logging.info(f' Pandas dataset:\n {df.head()}')
    logging.info(f' Pandas dataset info:\n {df.info()}')

    ## Create Tabular Dataset
    def_blob_store = ws.get_default_datastore()
    dp = (def_blob_store, '/inter')

    # Experimental method that both creates a Tabular Dataset, and register it as a Dataset
    fd = Dataset.Tabular.register_pandas_dataframe(df, target=dp, name='Telco_Baseline_Formatted')
    fd = fd.to_pandas_dataframe()
    logging.info(f' Tabular dataset:\n {fd.head()}')
    logging.info(f' Tabular dataset info:\n {fd.info()}')

    df.to_csv(args.output_file_path + '/' + args.output_filename, index=False)

if __name__ == "__main__":
    main()
