import pandas as pd
import hashlib
#import numpy as np


def load_data(source='./../datasets/WA_Fn-UseC_-Telco-Customer-Churn.csv'):
    """Load original data, and key lists"""
    df = pd.read_csv(source)
    df['TotalCharges'] = df['TotalCharges'].str.replace(r' ','0').astype(float)
    df['Churn'] = df['Churn'].apply(lambda x: 0 if x == "No" else 1)
    df['SeniorCitizen'] = df['SeniorCitizen'].apply(lambda x: "No" if x == 0 else "Yes")
    #df.info()
    total_cols = df.columns
    non_attribute_cols = ['customerID', 'MonthlyCharges', 'TotalCharges', 'Churn', 'tenure']
    attribute_cols = list( set(total_cols) - set(non_attribute_cols) )
    attribute_cols.sort()
    return df, attribute_cols


def churn_distribution(df=None, non_numeric_cols=None):
    """Showcase metrics by discrete combinations"""
    temp_df = df [ df['Churn'] == 1 ]
    temp_df = temp_df.groupby(non_numeric_cols).agg({'Churn': ['sum']})
    temp_df = temp_df.sort_values(by = ('Churn', 'sum'), ascending=False)

    # Create a distribution column
    temp_df['percent'] = temp_df[('Churn', 'sum')] / temp_df[('Churn', 'sum')].sum() 
    #temp_df.to_csv('dist.csv')
    print(temp_df.index)

    # Create a hash

#def hash_values(df):
#    """Get hash values for both columns"""
#    df['t_hash'] = df['subscription_id'] + df['server_name'] + df['create_time'].astype(str)
#    df['t_hash'] = df['t_hash'].str.encode('utf-8').apply(lambda x: (hashlib.sha3_256(x).hexdigest())) 
#    return df

def main():
    # Load and format data
    df, attribute_cols = load_data()

    # Get the numeric spread for numeric columns
    churn_distribution(df=df, non_numeric_cols=attribute_cols)

if __name__ == "__main__":
    main()
