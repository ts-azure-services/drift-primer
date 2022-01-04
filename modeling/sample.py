import random, uuid
from collections import defaultdict
import pandas as pd
import numpy as np

# Load choice list for 16 attributes
# Tenure, customerID, monthly charges, total charges and churn ignored
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
    print(choice_list)

    # Include periods
    df['Period'] = 'M0'
    df.to_pickle('./../datasets/M0.pkl')


load_original_data()
