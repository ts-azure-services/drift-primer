import pandas as pd

customer='6713-OKOMC'
#customer='3668-QPYBK'
#customer='1089-HDMKP'
period_list = ['M' + str(i) for i in range(13)]
customer_records = pd.DataFrame()

for i,v in enumerate(period_list):
    temp_df = pd.read_parquet('./../datasets/' + str(period_list[i]) + '.parquet')
    customer_check = temp_df [ temp_df['customerID']==customer]
    if customer_check.empty == True:
        print(f'No record for {period_list[i]}')
    else:
        customer_records = customer_records.append(customer_check)
        print(f'Records for {period_list[i]}')

print(customer_records)

