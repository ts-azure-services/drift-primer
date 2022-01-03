import random, uuid
from collections import defaultdict
import pandas as pd

def load_original_data(source='./../datasets/WA_Fn-UseC_-Telco-Customer-Churn.csv'):
    """Load original data"""
    df = pd.read_csv(source)
    df['TotalCharges'] = df['TotalCharges'].str.replace(r' ','0').astype(float)
    df['Churn'] = df['Churn'].apply(lambda x: 0 if x == "No" else 1)
    df['SeniorCitizen'] = df['SeniorCitizen'].apply(lambda x: "No" if x == 0 else "Yes")
    df.to_p
    return df

relevant_cols = ['gender', 'SeniorCitizen', 'Partner', 'Dependents',
       'tenure', 'PhoneService', 'MultipleLines', 'InternetService',
       'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
       'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling',
       'PaymentMethod']

"""
ORDER OF OPERATIONS:
    - NEW CUSTOMERS:
        - Randomly choose attributes, based upon populations
        - Tenure: 1
        - MonthlyCharges: (hardcode, but base on observed data)
        - TotalCharges: Equals monthly charges
        - Churn: 0, for all first-time customers
    - FOR EXISTING CUSTOMERS:
        - Increment tenure by 1 month
        - Tenure +1
        - Monthly charges: as above
        - Total charges: aggregate, by prior month
        - How should I apply churn on this base? (Cap at a 26%, and randomly assign)
        - Drop the old churn values
"""

# Load choice list
choice_list = {
        "gender":['Female', 'Male'],
        "senior_citizen":[0,1],
        "partner":['No', 'Yes'],
        "dependent":['No', 'Yes'],
        "phone_service":['No', 'Yes'],
        "multiple_lines":['No', 'No phone service', 'Yes'],
        "internet_services":['DSL', 'Fiber optic', 'No'],
        "online_security": ['No', 'No internet service', 'Yes'],
        "online_backup": ['No', 'No internet service', 'Yes'],
        "device_protection": ['No', 'No internet service', 'Yes'],
        "tech_support": ['No', 'No internet service', 'Yes'],
        "streaming_tv": ['No', 'No internet service', 'Yes'],
        "streaming_movies": ['No', 'No internet service', 'Yes'],
        "contract": ['One year', 'Two year', 'Month-to-month'],
        "paperless_billing": ['No', 'Yes'],
        "payment_method": ['Bank transfer (automatic)',\
                'Electronic check', 'Credit card (automatic)',\
                'Mailed check'],
        }


def generate_random_records():
    """Generate customer records for a specific period"""
    customer_records = defaultdict(list)
    month_volume = random.randint(100,1000)
    for i in range(month_volume):
        customer_records['customer_id'].append(str(uuid.uuid1()))
        customer_records['gender'].append( random.choice(choice_list['gender']))
        customer_records['senior_citizen'].append( random.choice(choice_list['senior_citizen']))
        customer_records['partner'].append( random.choice(choice_list['partner']))
        customer_records['dependent'].append( random.choice(choice_list['dependent']))
        customer_records['online_backup'].append(random.choice( choice_list['online_backup'] ))
    return pd.DataFrame(customer_records)

def main():
    """Main operational flow"""
    cr = generate_random_records()
    print(cr)

    # Load the original dataset, mark as M0
    m0 = load_original_data()
    # M1 operations


if __name__ == "__main__":
    main()




