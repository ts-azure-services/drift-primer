import pandas as pd
import numpy as np
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


def churn_ratio_by_attribute(df=None, col_list=None):
    """Get churn ratio by key attributes"""
    churn_prob = {}
    for i in col_list:
        temp_df = df.groupby(i).agg({'Churn': ['sum','count']})
        temp_df.columns = ['sum', 'count']
        temp_df['percent'] = temp_df['sum'] / temp_df['count']
        temp_df = temp_df.reset_index()
        #print( temp_df )
        churn_prob[i] = {'categories': temp_df[i].to_list(), 'probabilities': temp_df['percent'].to_list()}
        churn_prob_keys = list(churn_prob.keys())
    return churn_prob, churn_prob_keys


#def churn_distribution(df=None, non_numeric_cols=None):
#    temp_df = df [ df['Churn'] == 1 ]
#    temp_df = temp_df.drop(['customerID','MonthlyCharges', 'TotalCharges', 'tenure'], axis=1)
#    temp_df = temp_df.groupby(non_numeric_cols).sum()
#    temp_df = temp_df.sort_values(by = 'Churn', ascending=False)
#
#    # Create a distribution column
#    temp_df['percent'] = temp_df['Churn'] / temp_df['Churn'].sum() 
#
#    # Create a hash on the unique string of attribute combinations
#    temp_df = temp_df.reset_index()
#    temp_df['combined'] = temp_df[non_numeric_cols].agg('|'.join, axis=1).astype(str)
#    temp_df['t_hash'] = temp_df['combined'].str.encode('utf-8').apply(lambda x: (hashlib.sha3_256(x).hexdigest()))
#    temp_df.to_csv('dist.csv')
#
#    new_dict = dict( zip( temp_df['t_hash'], temp_df['percent'] ) )
#
#    return new_dict




def main():
    # Load and format data
    df, attribute_cols = load_data()

    ## Get the numeric spread for numeric columns
    #cd = churn_distribution(df=df, non_numeric_cols=attribute_cols)
    churn_prob, churn_prob_keys = churn_ratio_by_attribute(df=df, col_list=attribute_cols)
    print( churn_prob )

    # Alternative approach
    df1 = pd.read_pickle('./../datasets/M12.pkl')
    print( df1.head() )

    for i,v in enumerate(churn_prob_keys):
        for iterator, val in enumerate(churn_prob[v]['categories']):
            sample_slice = df1 [ df1[ churn_prob_keys[i] ] == val ]
            c_prob_value = churn_prob[v]['probabilities'][iterator]
            sample_slice['Churn'] = np.random.choice(
                    [0,1], 
                    size=len(sample_slice),
                    p=(c_prob_value, 1 - c_prob_value )
                    )
            print( sample_slice )





if __name__ == "__main__":
    main()
