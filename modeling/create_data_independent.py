"""Simulate data independent of prior data pulls"""
import random
import uuid
import math
from collections import defaultdict
import pandas as pd
import numpy as np

# Load original data source, create choice list
def load_original_data(source='./../datasets/input-data/WA_Fn-UseC_-Telco-Customer-Churn.csv'):
    """Load original data"""
    df = pd.read_csv(source)
    df['TotalCharges'] = df['TotalCharges'].str.replace(r' ','0').astype(float)
    df['Churn'] = df['Churn'].apply(lambda x: 0 if x == "No" else 1)
    df['SeniorCitizen'] = df['SeniorCitizen'].apply(lambda x: "No" if x == 0 else "Yes")
    df = df.drop('TotalCharges', axis=1)

    # Get the core attributes in the dataset
    def key_columns(df=None):
        total_cols = df.columns
        #non_attribute_cols = ['customerID', 'MonthlyCharges', 'TotalCharges', 'Churn', 'tenure']
        #non_attribute_cols = ['customerID', 'MonthlyCharges', 'TotalCharges', 'Churn']
        non_attribute_cols = ['customerID', 'MonthlyCharges', 'Churn']
        attribute_cols = list( set(total_cols) - set(non_attribute_cols) )
        attribute_cols.sort()
        return attribute_cols

    attribute_cols = key_columns(df=df)

    # For each column, you need to define the categories, and their probabilities
    choice_list = {}
    for i in attribute_cols:
        temp_df = df['customerID'].groupby(df[i]).count().to_frame()
        temp_df['percent'] = temp_df['customerID'] / temp_df['customerID'].sum()
        categories = list(temp_df.index)
        probabilities = temp_df['percent'].tolist()
        choice_list[i] = {
                'categories': categories,
                'probabilities':probabilities
            }

    # Get monthly charges ranges
    def monthly_charge_generator(df=None):
        mc_list = df['MonthlyCharges'].tolist()
        min_mc = min(mc_list)
        max_mc = max(mc_list)
        return min_mc, max_mc

    min_mc, max_mc = monthly_charge_generator(df=df)

    # Include periods
    df['Period'] = 'M0'
    df.to_parquet('./../datasets/M0.parquet', index=False)
    return df, attribute_cols, choice_list, min_mc, max_mc


def random_monthly_charge(min_mc=None, max_mc=None):
    """Generate a random monthly charge"""
    rn = min_mc + (max_mc - min_mc) * random.random()
    return rn


def churn_ratio_by_attribute(df=None, col_list=None):
    """Get churn ratio by key attributes off the original data"""
    col_list.append('tenure')
    churn_prob = {}
    for i in col_list:
        temp_df = df.groupby(i).agg({'Churn': ['sum','count']})
        temp_df.columns = ['sum', 'count']
        temp_df['percent'] = temp_df['sum'] / temp_df['count']
        temp_df = temp_df.reset_index()
        churn_prob[i] = {'categories': temp_df[i].to_list(), 'probabilities': temp_df['percent'].to_list()}
    return churn_prob


def apply_churn(churn_prob=None, df=None, churn_percentage=None):
    """Apply churn on dataframe"""
    churn_prob_keys = list(churn_prob.keys())

    for i,v in enumerate(churn_prob_keys):
        for iterator, val in enumerate(churn_prob[v]['categories']):
            sample_slice = df [ df[ churn_prob_keys[i] ] == val ]
            c_prob_value = churn_prob[v]['probabilities'][iterator]
            churn_values = np.random.choice([1,0],size=len(sample_slice),p=(c_prob_value, 1 - c_prob_value ))
            df.loc[sample_slice.index, 'Churn'] += churn_values

    df = df.sort_values(by = 'Churn', ascending=False)
    rows_to_churn = math.floor(churn_percentage * len(df))

    # Preserve the order of the rows to rank with 'churn' and assign churn values
    df = df.reset_index(drop=True) 
    #print(f'Rows to churn: {rows_to_churn}')
    df.loc[:rows_to_churn, 'Churn'] = 1
    df.loc[rows_to_churn:, 'Churn'] = 0

    # Reshuffle the entire dataframe
    df = df.sample(frac=1)
    return df


def generate_new_customers(
        period=None,
        min_vol=None, 
        max_vol=None,
        choice_list=None,
        min_mc = None,
        max_mc = None
        ):
    """Generate new customer records for a specific period."""

    keys = list( choice_list.keys() )

    def random_attribute_generator(keys):
        """Generate records based upon prior attributes"""
        for i in keys:
            #customer_records[i].append( random.choice(choice_list[i]))
            customer_records[i].append( np.random.choice(
                choice_list[i]['categories'],
                size=1,
                p=choice_list[i]['probabilities'])[0]
                )
        customer_records['customerID'].append(str(uuid.uuid1()))
        #customer_records['tenure'] = 1
        customer_records['MonthlyCharges'].append(random_monthly_charge(min_mc, max_mc))
        customer_records['TotalCharges'] = customer_records['MonthlyCharges']
        customer_records['Churn'] = 0
        customer_records['Period'] = period

    # Generate new customer records
    customer_records = defaultdict(list)
    month_volume = random.randint(min_vol,max_vol)
    for _ in range(month_volume):
        random_attribute_generator(keys)
    return pd.DataFrame(customer_records)


def generate_monthly_pull(
        #prior_period = None,
        current_period = None,
        #prior_source = None,
        min_vol=None,
        max_vol=None,
        choice_list=None,
        min_mc = None,
        max_mc = None,
        churn_prob=None
        ):
    """Generate the monthly output"""

    # Create the new customers
    new_customers = generate_new_customers(
            period=current_period, 
            min_vol=min_vol, 
            max_vol=max_vol,
            choice_list=choice_list, 
            min_mc = min_mc,
            max_mc = max_mc
            )

    ## Take the prior base, and filter out churned customers
    #prior_customers = pd.read_parquet(prior_source)
    #prior_customers = prior_customers.loc[ prior_customers['Churn'] == 0 ]

    ## Increment their tenure by 1
    #prior_customers['tenure'] = prior_customers['tenure'] + 1

    ## Distribute monthly charges, and aggregate total charges
    #prior_customers['MonthlyCharges'] = prior_customers['MonthlyCharges'].apply(\
    #        lambda x : min_mc + (max_mc - min_mc)*random.random() 
    #        ) 
    #prior_customers['TotalCharges'] = prior_customers['MonthlyCharges'] + prior_customers['TotalCharges']

    ## Add the current period to the install base
    #prior_customers['Period'] = current_period

    # Add the prior base to the new customer base
    #combined_df = pd.concat([prior_customers, new_customers])
    combined_df = pd.concat([new_customers])

    # Reset the index, so that when you apply churn values, there are unique indexes
    combined_df = combined_df.reset_index(drop=True)

    ## Churn based on the combined dataset
    #combined_df['Churn'] = np.random.choice([0,1], size=len(combined_df), p=(0.74,0.26))
    churn_percentage = 0.26
    combined_df = apply_churn(
            churn_prob=churn_prob, 
            df=combined_df, 
            churn_percentage=churn_percentage
            )

    # Convert to a parquet file
    combined_df.to_parquet('./../datasets/' + str(current_period) + '.parquet', index=False)
    print(f'Current period: {current_period}')
    #print(f'Length of prior customers: {len(prior_customers)}')
    print(f'Length of new customers: {len(new_customers)}')
    print(f'Length of combined dataframe: {len(combined_df)}')


def main():
    """Main operational flow"""

    # Load the original dataset, mark as M0
    original_df, attribute_cols, choice_list, min_mc, max_mc = load_original_data()

    # Get the churn ratios and probabilities from the original data
    churn_prob = churn_ratio_by_attribute(
            df=original_df, 
            col_list=attribute_cols
            )

    ## M1 operations
    #period_list = ['M' + str(i) for i in range(13)]
    #for j,_ in enumerate(period_list):
    #    if period_list[j] != 'M12':
    #        prior_period=period_list[j]
    #        current_period=period_list[j+1]

    #        # Generate the monthly pull
    #        generate_monthly_pull(
    #            current_period = current_period,
    #            #prior_source='./../datasets/' + str(prior_period) +'.parquet',
    #            min_vol=6800,
    #            max_vol=7200,
    #            choice_list=choice_list,
    #            min_mc = min_mc,
    #            max_mc = max_mc,
    #            churn_prob = churn_prob
    #            )

    ## M1 operations
    #period_list = ['M' + str(i) for i in range(13)]
    #for j,_ in enumerate(period_list):
    #    # Generate the monthly pull
    generate_monthly_pull(
        current_period = 'M1',#period_list[j],
        #prior_source='./../datasets/' + str(prior_period) +'.parquet',
        min_vol=6800,
        max_vol=7200,
        choice_list=choice_list,
        min_mc = min_mc,
        max_mc = max_mc,
        churn_prob = churn_prob
        )

if __name__ == "__main__":
    main()
