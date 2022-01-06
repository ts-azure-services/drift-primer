# Script to run a few data filtering and transformation operations
import os, datetime, random, argparse
import pandas as pd
import datetime as dt

def getArgs(argv=None):
    parser = argparse.ArgumentParser(description="filepaths")
    parser.add_argument("--input_file_path", help='Input file path')
    parser.add_argument("--output_file_path", help='Output file path')
    parser.add_argument("--filename", help='Filename')
    return parser.parse_args(argv)

def transform(source=None):
    """Load original data"""
    df = pd.read_csv(source)
    df['TotalCharges'] = df['TotalCharges'].str.replace(r' ','0').astype(float)
    df['Churn'] = df['Churn'].apply(lambda x: 0 if x == "No" else 1)
    df['SeniorCitizen'] = df['SeniorCitizen'].apply(lambda x: "No" if x == 0 else "Yes")
    return df

if __name__ == "__main__":
    args = getArgs()
    print(f'Input args: {args.input_file_path}')
    print(f'Output args: {args.output_file_path}')
    print(f'Filename: {args.filename}')
    df = transform(source=args.input_file_path)
    df.to_csv(args.output_file_path + '/' + args.filename, index=False)
