import random, uuid
from collections import defaultdict
import pandas as pd

df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')

relevant_cols = ['gender', 'SeniorCitizen', 'Partner', 'Dependents',
       'tenure', 'PhoneService', 'MultipleLines', 'InternetService',
       'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
       'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling',
       'PaymentMethod']

#for i,v in enumerate(relevant_cols):
#    df_temp = df.groupby(['Churn', v]).size().reset_index(name='Count')
#    print( df_temp )

# For any month, I want to create a list of customers and specific attributes
# For the month they come on new, their bill can vary, but it should never regress below that?
# The totals have to reflect the growing bill
# You need to account for the install base changes as well
# The churn calculation is done on the install base


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

# tenure - needs to accrue
# monthly account charges
# total charges


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
    return customer_records

def main():
    """Main operational flow"""
    cr = generate_random_records()
    print(pd.DataFrame(cr))

if __name__ == "__main__":
    main()




