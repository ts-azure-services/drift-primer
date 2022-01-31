import pandas as pd
import logging
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..')))
from modeling.datamodeling.common import get_ratios, create_adjusted_list
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


def main():

    # Get input dataset
    df = pd.read_csv('./datasets/baseline_revised.csv')

    # Get delta ratios, based on the new ratio
    column_name = 'Contract'
    temp_dict = get_ratios(df=df, column_name=column_name)

    # Pass in the list to adjust to get the adjusted list
    _, temp_column_df = create_adjusted_list(
            column_df=df[[column_name]], 
            column_name=column_name, 
            temp_dict=temp_dict
            )

    ## Check if variances have been accounted for
    #combined_df = pd.merge(column_df, temp_column_df, left_index=True, right_index=True)
    #combined_df.to_csv('COMBINED.csv', encoding='utf-8')

    # Adjust the new column on the dataframe
    df[column_name] = temp_column_df
    df.to_csv('./datasets/ddrift_data/datadrift_dataset.csv', encoding='utf-8')

if __name__ == "__main__":
    main()
