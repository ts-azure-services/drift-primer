import pandas as pd
import numpy as np

def customer_distribution(df=None):
    """Show percent of customers by various attribuites"""
    for i in col_list:
        temp_df = df['customerID'].groupby(df[i]).count().to_frame()
        temp_df['percent'] = temp_df['customerID'] / temp_df['customerID'].sum()
        print(f'Customer count by {i}:\n{temp_df}\n')


def churn_ratio_by_attribute(df=None, col_list=None):
    """Get churn ratio by various attributes"""
    col_list.append('tenure')
    for i in col_list:
        temp_df = df.groupby(i).agg({'Churn': ['sum','count']})
        temp_df.columns = ['sum', 'count']
        temp_df['percent'] = temp_df['sum'] / temp_df['count']
        print(f'For {i}, the dataframe is:\n {temp_df}\n')


def main():
    # Load and format data
    baseline = pd.read_parquet('./../datasets/M0.parquet')
    comparison = pd.read_parquet('./../datasets/M1.parquet')

    # Combine both baselines
    combined = pd.concat([baseline, comparison])
    combined = combined.reset_index(drop=True)

    # Mix difference by period
    col_list = list(combined.columns)
    col_list.remove('Period')
    col_list.remove('Churn')
    col_list.remove('MonthlyCharges')
    col_list.remove('TotalCharges')

    for i in col_list:
        temp_df = combined.groupby(by=[i, 'Period']).agg({'customerID':['count']}).\
                rename(columns={'count':'customer_count'})
        temp_df = temp_df.pivot_table(index=i, columns='Period', values='customer_count')
        print(temp_df)


if __name__ == "__main__":
    main()
