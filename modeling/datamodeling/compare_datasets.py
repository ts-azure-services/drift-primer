import pandas as pd
import numpy as np
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


def main():
    # Load and format data
    baseline = pd.read_parquet('./../datasets/M0.parquet')
    comparison = pd.read_parquet('./../datasets/M1.parquet')

    # Combine both baselines
    combined = pd.concat([baseline, comparison])
    combined = combined.reset_index(drop=True)

    # Mix difference by period
    col_list = list(combined.columns)
    non_attribute_cols = ['customerID', 'MonthlyCharges', 'TotalCharges', 'Churn', 'Period']
    attribute_cols = list( set(col_list) - set(non_attribute_cols) )

    # Compare distributions of attributes
    for i in attribute_cols:
        temp_df = combined.groupby(by=[i, 'Period']).agg({'customerID':'count'})
        temp_df.columns = ['customer_count']
        temp_df = temp_df.pivot_table(index=i, columns='Period', values='customer_count')
        temp_df['M0%'] = temp_df['M0'] / temp_df['M0'].sum()
        temp_df['M1%'] = temp_df['M1'] / temp_df['M1'].sum()
        logging.info(f'For {i}, the dataframe is:\n {temp_df}\n')

    # Compare churn ratios
    for i in attribute_cols:
        temp_df = combined.groupby(by=[i, 'Period']).agg({'Churn': ['sum','count']})
        temp_df.columns = ['sum', 'count']
        temp_df = temp_df.pivot_table(index=i, columns='Period', values=['sum', 'count'])
        temp_df.columns = ['M0_count', 'M1_count', 'M0_sum', 'M1_sum']
        temp_df['M0-Churn'] = temp_df['M0_sum'] / temp_df['M0_count']
        temp_df['M1-Churn'] = temp_df['M1_sum'] / temp_df['M1_count']
        logging.info(f'For {i}, the dataframe is:\n {temp_df}\n')


if __name__ == "__main__":
    main()
