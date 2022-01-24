import pandas as pd
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def bin_column(df=None, new_col_name=None, base_col=None, number_bins=None):
    """Bin data for specific columns"""
    df[new_col_name] = pd.cut(x = df[base_col],bins=number_bins,include_lowest=True)
    return df

def load_data(source=None):
    """Load original data, and key lists"""
    if 'parquet' in source:
        df = pd.read_parquet(source)
    else:
        df = pd.read_csv(source)
        df['TotalCharges'] = df['TotalCharges'].str.replace(r' ','0').astype(float)
        df['Churn'] = df['Churn'].apply(lambda x: 0 if x == "No" else 1)
        df['SeniorCitizen'] = df['SeniorCitizen'].apply(lambda x: "No" if x == 0 else "Yes")
        #df.info()

    # Bin columns
    df = bin_column(df=df, new_col_name='tenure_bins', base_col='tenure', number_bins=10)
    df = bin_column(df=df, new_col_name='monthly_charges_bins', base_col='MonthlyCharges', number_bins=10)

    total_cols = df.columns
    non_attribute_cols = ['customerID', 'MonthlyCharges', 'TotalCharges', 'Churn', 'tenure']
    attribute_cols = list( set(total_cols) - set(non_attribute_cols) )
    attribute_cols.sort()
    return df, attribute_cols


def attribute_col_ratio(df=None, col_list=None):
    """Show percent of customers represented by non-numeric attributes"""
    for i in col_list:
        temp_df = df['customerID'].groupby(df[i]).count().to_frame()
        temp_df['percent'] = temp_df['customerID'] / temp_df['customerID'].sum()
        logging.info(f'Customer count by {i}:\n{temp_df}\n')


def churn_ratio_by_attribute(df=None, col_list=None):
    """Get churn ratio by key attributes"""
    col_list.append('tenure')
    for i in col_list:
        temp_df = df.groupby(i).agg({'Churn': ['sum','count']})
        temp_df.columns = ['sum', 'count']
        temp_df['percent'] = temp_df['sum'] / temp_df['count']
        logging.info(f'For {i}, the dataframe is:\n {temp_df}\n')


def numeric_col_spreads(df=None, non_numeric_cols=None):
    """Showcase metrics by discrete combinations"""
    #non_numeric_cols.append('Churn')
    logging.info(non_numeric_cols)
    temp_df = df.groupby(non_numeric_cols).\
        agg({'Churn': ['min','mean', 'median', 'max', 'sum', 'count']})
    temp_df.columns = ['min', 'mean', 'median', 'max', 'sum', 'count']
    logging.info(temp_df.head())
    logging.info(temp_df.columns)
    logging.info(temp_df.index)


def main():
    # Load and format data
    source = './../datasets/M1.parquet'
    df, attribute_cols = load_data(source=source)

    #df = df [ df['tenure'] <= 3 ]

    # Get customer count by major attribute
    #attribute_col_ratio(df=df, col_list=attribute_cols)

    # Get churn ratio by key attribute
    churn_ratio_by_attribute(df=df, col_list=attribute_cols)

    ## Get the numeric spread for numeric columns
    #numeric_col_spreads(df=df, non_numeric_cols=attribute_cols)

if __name__ == "__main__":
    main()
