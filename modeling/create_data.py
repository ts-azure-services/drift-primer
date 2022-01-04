import random, uuid
from collections import defaultdict
import pandas as pd
import numpy as np

# Load choice list for 16 attributes
# Tenure, customerID, monthly charges, total charges and churn ignored

def load_original_data(source='./../datasets/WA_Fn-UseC_-Telco-Customer-Churn.csv'):
    """Load original data"""
    df = pd.read_csv(source)
    df['TotalCharges'] = df['TotalCharges'].str.replace(r' ','0').astype(float)
    df['Churn'] = df['Churn'].apply(lambda x: 0 if x == "No" else 1)
    df['SeniorCitizen'] = df['SeniorCitizen'].apply(lambda x: "No" if x == 0 else "Yes")

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

    # Include periods
    df['Period'] = 'M0'
    df.to_pickle('./../datasets/M0.pkl')
    return choice_list


def generate_new_customers(
        period=None,
        min_vol=None, 
        max_vol=None,
        choice_list=None,
        #keys=None,#list(choice_list.keys())
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
                p=choice_list[i]['probabilities'])
                )
        customer_records['customerID'].append(str(uuid.uuid1()))
        customer_records['tenure'] = 1
        customer_records['MonthlyCharges'] = 45.22
        customer_records['TotalCharges']= customer_records['MonthlyCharges']
        customer_records['Churn'] = 0
        customer_records['Period'] = period

    # Generate new customer records
    customer_records = defaultdict(list)
    month_volume = random.randint(min_vol,max_vol)
    for j in range(month_volume):
        random_attribute_generator(keys)
    return pd.DataFrame(customer_records)


def generate_monthly_pull(
        prior_period = None,
        current_period = None,
        prior_source = None,
        min_vol=None,
        max_vol=None,
        choice_list=None
        ):
    """Generate the monthly output"""

    # Create the new customers
    new_customers = generate_new_customers(
            period=current_period, 
            min_vol=min_vol, 
            max_vol=max_vol,
            choice_list=choice_list
            #keys=list(choice_list.keys())
            )

    # Take the prior base, and filter out churned customers
    prior_customers = pd.read_pickle(prior_source)
    prior_customers = prior_customers.loc[ prior_customers['Churn'] == 0 ]

    # Increment their tenure by 1
    prior_customers['tenure'] = prior_customers['tenure'] + 1

    # Distribute monthly charges, and aggregate total charges
    prior_customers['MonthlyCharges'] = 65.22
    prior_customers['TotalCharges'] = prior_customers['MonthlyCharges'] + prior_customers['TotalCharges']

    # Add the current period to the install base
    prior_customers['Period'] = current_period

    # Add the prior base to the new customer base
    combined_df = pd.concat([prior_customers, new_customers])

    # Churn based on the combined dataset
    combined_df['Churn'] = np.random.choice(
            [0,1], 
            size=len(combined_df), 
            replace=True, p=(0.74,0.26)
            )

    # Pickle the latest file
    combined_df.to_pickle('./../datasets/' + str(current_period) + '.pkl')
    print(f'Current period: {current_period}')
    print(f'Length of prior customers: {len(prior_customers)}')
    print(f'Length of new customers: {len(new_customers)}')
    print(f'Length of combined dataframe: {len(combined_df)}')

    return combined_df




def main():
    """Main operational flow"""

    # Load the original dataset, mark as M0
    choice_list = load_original_data()

    # M1 operations
    period_list = ['M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'M8', 'M9', 'M10', 'M11', 'M12']
    for j,k in enumerate(period_list):
        if period_list[j] != 'M12':
            prior_period=period_list[j]
            current_period=period_list[j+1]
            df = generate_monthly_pull(
                    prior_period= prior_period, 
                    current_period= current_period,
                    prior_source='./../datasets/' + str(prior_period) +'.pkl',
                    min_vol=500,
                    max_vol=1200,
                    choice_list=choice_list
                    )


if __name__ == "__main__":
    main()
