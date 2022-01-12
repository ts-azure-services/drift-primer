import pandas as pd

def load_data(source='./../datasets/input-data/WA_Fn-UseC_-Telco-Customer-Churn.csv'):
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


def attribute_col_ratio(df=None, col_list=None):
    """Show percent of customers represented by non-numeric attributes"""
    for i in col_list:
        temp_df = df['customerID'].groupby(df[i]).count().to_frame()
        temp_df['percent'] = temp_df['customerID'] / temp_df['customerID'].sum()
        print(f'Customer count by {i}:\n{temp_df}\n')


def binning_tenure(df=None):
    df['bucket'] = pd.cut(x = df['tenure'],bins=[0,10,30,100],
            labels=['One to 10 days', '+10 to 30 days', 'Beyond +1 month'],
            include_lowest=True
            )
    df = df.sort_values(by = 'tenure', ascending=True)
    df = df.groupby(['bucket']).agg({'customerID': 'count','Churn':'sum'})
    df['Churn %'] = df['Churn'] / df['customerID']


def churn_ratio_by_attribute(df=None, col_list=None):
    """Get churn ratio by key attributes"""
    for i in col_list:
        temp_df = df.groupby(i).agg({'Churn': ['sum','count']})
        temp_df.columns = ['sum', 'count']
        temp_df['percent'] = temp_df['sum'] / temp_df['count']
        print( temp_df )


def numeric_col_spreads(df=None, non_numeric_cols=None):
    """Showcase metrics by discrete combinations"""
    #non_numeric_cols.append('Churn')
    print(non_numeric_cols)
    temp_df = df.groupby(non_numeric_cols).\
        agg({'Churn': ['min','mean', 'median', 'max', 'sum', 'count']})
    print(temp_df.head())
    print(temp_df.columns)
    print(temp_df.index)


def main():
    # Load and format data
    df, attribute_cols = load_data()

    # Get customer count by major attribute
    #attribute_col_ratio(df=df, col_list=attribute_cols)

    # Get churn ratio by key attribute
    churn_ratio_by_attribute(df=df, col_list=attribute_cols)

    ## Get the numeric spread for numeric columns
    #numeric_col_spreads(df=df, non_numeric_cols=attribute_cols)

if __name__ == "__main__":
    main()


#df_temp = df.groupby(['gender', 'SeniorCitizen', 'Contract']).\
#        agg({'MonthlyCharges': ['min','mean', 'median', 'max']})

