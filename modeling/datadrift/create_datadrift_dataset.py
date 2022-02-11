import pandas as pd
import logging
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..')))
from modeling.datamodeling.common import get_ratios
from modeling.datamodeling.common import create_adjusted_list
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


def column_change(df=None, column_name=None):
    """Adjust column to be evenly distributed by its attributes"""
    # Get delta ratios, based on the new ratio
    temp_dict = get_ratios(df=df, column_name=column_name)

    # Pass in the list to adjust to get the adjusted list
    _, temp_column_df = create_adjusted_list(
            column_df=df[[column_name]], 
            column_name=column_name, 
            temp_dict=temp_dict
            )
    # Adjust the new column on the dataframe
    df[column_name] = temp_column_df
    return df


def main():

    # Get input dataset
    #df = pd.read_csv('./datasets/baseline_revised.csv')
    df = pd.read_csv('./datasets/retrain_data/retrain_dataset.csv')

    # Columns to make an even mix
    #df = column_change(df=df, column_name='Contract')
    #df = column_change(df=df, column_name='PaymentMethod')
    #df = column_change(df=df, column_name='Dependents')
    #df = column_change(df=df, column_name='OnlineSecurity')
    #df = column_change(df=df, column_name='TechSupport')
    df = column_change(df=df, column_name='tenure_bins')

    df.to_csv('./datasets/ddrift_data/datadrift_dataset.csv', encoding='utf-8', index=False)

if __name__ == "__main__":
    main()
