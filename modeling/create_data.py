import random, uuid
from collections import defaultdict
import pandas as pd
import numpy as np

# Load original data source, create choice list
def load_original_data(source='./../datasets/WA_Fn-UseC_-Telco-Customer-Churn.csv'):
    """Load original data"""
    df = pd.read_csv(source)
    df['TotalCharges'] = df['TotalCharges'].str.replace(r' ','0').astype(float)
    df['Churn'] = df['Churn'].apply(lambda x: 0 if x == "No" else 1)
    df['SeniorCitizen'] = df['SeniorCitizen'].apply(lambda x: "No" if x == 0 else "Yes")

    # Get the core attributes in the dataset
    def key_columns(df=None):
        total_cols = df.columns
        non_attribute_cols = ['customerID', 'MonthlyCharges', 'TotalCharges', 'Churn', 'tenure']
        attribute_cols = list( set(total_cols) - set(non_attribute_cols) )
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
    df.to_pickle('./../datasets/M0.pkl')
    return choice_list, min_mc, max_mc


def random_monthly_charge(min_mc=None, max_mc=None):
    """Generate a random monthly charge"""
    rn = min_mc + (max_mc - min_mc) * random.random()
    return rn


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
        customer_records['tenure'] = 1
        #customer_records['MonthlyCharges'] = 45.22
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
        prior_source = None,
        min_vol=None,
        max_vol=None,
        choice_list=None,
        min_mc = None,
        max_mc = None
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

    # Take the prior base, and filter out churned customers
    prior_customers = pd.read_pickle(prior_source)
    prior_customers = prior_customers.loc[ prior_customers['Churn'] == 0 ]

    # Increment their tenure by 1
    prior_customers['tenure'] = prior_customers['tenure'] + 1

    # Distribute monthly charges, and aggregate total charges
    #prior_customers['MonthlyCharges'] = 65.22
    prior_customers['MonthlyCharges'] = prior_customers['MonthlyCharges'].apply(\
            lambda x : min_mc + (max_mc - min_mc)*random.random() 
            ) 
    prior_customers['TotalCharges'] = prior_customers['MonthlyCharges'] + prior_customers['TotalCharges']

    # Add the current period to the install base
    prior_customers['Period'] = current_period

    # Add the prior base to the new customer base
    combined_df = pd.concat([prior_customers, new_customers])

    # Churn based on the combined dataset
    combined_df['Churn'] = np.random.choice(
            [0,1], 
            size=len(combined_df), 
            p=(0.74,0.26)
            )

    # Pickle the latest file
    combined_df.to_pickle('./../datasets/' + str(current_period) + '.pkl')
    print(f'Current period: {current_period}')
    print(f'Length of prior customers: {len(prior_customers)}')
    print(f'Length of new customers: {len(new_customers)}')
    print(f'Length of combined dataframe: {len(combined_df)}')

    #return combined_df




def main():
    """Main operational flow"""

    # Load the original dataset, mark as M0
    choice_list, min_mc, max_mc = load_original_data()

    # M1 operations
    period_list = ['M'+str(i) for i in range(13)]
    for j,_ in enumerate(period_list):
        if period_list[j] != 'M12':
            prior_period=period_list[j]
            current_period=period_list[j+1]
            generate_monthly_pull(
                #prior_period = prior_period, 
                current_period = current_period,
                prior_source='./../datasets/' + str(prior_period) +'.pkl',
                min_vol=1500,
                max_vol=2000,
                choice_list=choice_list,
                min_mc = min_mc,
                max_mc = max_mc
                )


if __name__ == "__main__":
    main()
