import random, uuid
from collections import defaultdict
import pandas as pd
import numpy as np

# Load choice list for 16 attributes
# Tenure, customer_id, monthly charges, total charges and churn ignored
choice_list = {
        "gender":['Female', 'Male'],
        "SeniorCitizen":['No','Yes'],
        "Partner":['No', 'Yes'],
        "Dependents":['No', 'Yes'],
        "PhoneService":['No', 'Yes'],
        "MultipleLines":['No', 'No phone service', 'Yes'],
        "InternetService":['DSL', 'Fiber optic', 'No'],
        "OnlineSecurity": ['No', 'No internet service', 'Yes'],
        "OnlineBackup": ['No', 'No internet service', 'Yes'],
        "DeviceProtection": ['No', 'No internet service', 'Yes'],
        "TechSupport": ['No', 'No internet service', 'Yes'],
        "StreamingTV": ['No', 'No internet service', 'Yes'],
        "StreamingMovies": ['No', 'No internet service', 'Yes'],
        "Contract": ['One year', 'Two year', 'Month-to-month'],
        "PaperlessBilling": ['No', 'Yes'],
        "PaymentMethod": ['Bank transfer (automatic)',\
                'Electronic check', 'Credit card (automatic)',\
                'Mailed check'],
        }

def load_original_data(source='./../datasets/WA_Fn-UseC_-Telco-Customer-Churn.csv'):
    """Load original data"""
    df = pd.read_csv(source)
    df['TotalCharges'] = df['TotalCharges'].str.replace(r' ','0').astype(float)
    df['Churn'] = df['Churn'].apply(lambda x: 0 if x == "No" else 1)
    df['SeniorCitizen'] = df['SeniorCitizen'].apply(lambda x: "No" if x == 0 else "Yes")
    df['Period'] = 'M0'
    #df.info()
    df.to_pickle('./../datasets/M0.pkl')


def generate_monthly_pull(
        prior_period = None,
        current_period = None,
        prior_source = None,
        min_vol=None,
        max_vol=None
        ):
    """Generate the monthly output"""

    # Create the new customers
    new_customers = generate_new_customers(period=current_period, min_vol=min_vol, max_vol=max_vol)

    # Take the prior base, and filter out churned customers
    prior_customers = pd.read_pickle(prior_source)
    prior_customers = prior_customers.loc[ prior_customers['Churn'] == 0 ]

    # Identify the balance of customers that will churn, capped at x%
    prior_customers['Churn'] = np.random.choice([0,1], size=len(prior_customers), replace=True, p=(0.74,0.26))

    # Increment their tenure by 1
    prior_customers['tenure'] = prior_customers['tenure'] + 1

    # Distribute monthly charges, and aggregate total charges
    prior_customers['MonthlyCharges'] = 65.22
    prior_customers['TotalCharges'] = prior_customers['MonthlyCharges'] + prior_customers['TotalCharges']

    # Add the current period to the install base
    prior_customers['Period'] = current_period

    # Add the prior base to the new customer base
    combined_df = pd.concat([prior_customers, new_customers])

    # Pickle the latest file
    combined_df.to_pickle('./../datasets/' + str(current_period) + '.pkl')

    return combined_df



def generate_new_customers(
        period=None,
        min_vol=None, 
        max_vol=None, 
        keys=list(choice_list.keys())
        ):
    """Generate new customer records for a specific period."""

    def random_attribute_generator(keys):
        """Generate records based upon prior attributes"""
        for i in keys:
            customer_records[i].append( random.choice(choice_list[i]))
        customer_records['customer_id'].append(str(uuid.uuid1()))
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


def main():
    """Main operational flow"""

    # Load the original dataset, mark as M0
    load_original_data()

    # M1 operations
    prior_period='M0'
    current_period='M1'
    df = generate_monthly_pull(
            prior_period= prior_period, 
            current_period= current_period,
            prior_source='./../datasets/' + str(prior_period) +'.pkl',
            min_vol=1000,
            max_vol=2000
            )
    print(df)


if __name__ == "__main__":
    main()



