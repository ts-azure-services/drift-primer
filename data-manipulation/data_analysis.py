import pandas as pd
import numpy as np

df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')

#relevant_cols = ['gender', 'SeniorCitizen', 'Partner', 'Dependents',
#       'tenure', 'PhoneService', 'MultipleLines', 'InternetService',
#       'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
#       'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling',
#       'PaymentMethod']

#for i,v in enumerate(relevant_cols):
#    df_temp = df.groupby(['Churn', v]).size().reset_index(name='Count')
#    print( df_temp )

df_temp = df.groupby(['gender', 'SeniorCitizen', 'Contract']).\
        agg({'MonthlyCharges': ['min','mean', 'median', 'max']})

#df_temp = df.groupby(['gender', 'SeniorCitizen']).describe('MonthlyCharges')
print( df_temp )

# 0   customerID        7043 non-null   object 
# 1   gender            7043 non-null   object 
# 2   SeniorCitizen     7043 non-null   int64  
# 3   Partner           7043 non-null   object 
# 4   Dependents        7043 non-null   object 
# 5   tenure            7043 non-null   int64  
# 6   PhoneService      7043 non-null   object 
# 7   MultipleLines     7043 non-null   object 
# 8   InternetService   7043 non-null   object 
# 9   OnlineSecurity    7043 non-null   object 
# 10  OnlineBackup      7043 non-null   object 
# 11  DeviceProtection  7043 non-null   object 
# 12  TechSupport       7043 non-null   object 
# 13  StreamingTV       7043 non-null   object 
# 14  StreamingMovies   7043 non-null   object 
# 15  Contract          7043 non-null   object 
# 16  PaperlessBilling  7043 non-null   object 
# 17  PaymentMethod     7043 non-null   object 
# 18  MonthlyCharges    7043 non-null   float64
# 19  TotalCharges      7043 non-null   object 
# 20  Churn             7043 non-null   object
