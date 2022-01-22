import math
import pandas as pd


def get_ratios(column_name=None):
    """Get ratios for specified column from original dataset"""

    # Ensure that the sum of the values is the customer count
    df = pd.read_csv('./../datasets/original/WA_Fn-UseC_-Telco-Customer-Churn.csv')
    df = df[column_name].value_counts().to_frame()
    customer_count = df[column_name].sum()
    df['percent'] = df[column_name] / customer_count
    df['new_percent'] = 1/len(df)
    df['new_allocation'] = customer_count * df['new_percent']
    df['new_allocation'] = round(df['new_allocation']).astype(int)

    # Ensure it adds up to the total customer count
    new_customer_totals = df['new_allocation'].tolist()
    while sum(new_customer_totals) != customer_count:
        last_value = new_customer_totals[-1:][0]
        last_value = last_value - 1
        new_customer_totals[-1:] = [last_value]

    # Apply back the total to the list
    df['new_allocation'] = new_customer_totals
    df['delta'] = df['new_allocation'] - df[column_name]
    print(new_customer_totals)
    print(df)

    burndown_list = df['delta'].tolist()
    print(f'Burndown list: {burndown_list}')
    return burndown_list

burndown_list = get_ratios(column_name='OnlineSecurity')

if sum(burndown_list) == 0:

    while len(burndown_list) != 1:
        # Sort the list
        burndown_list.sort()
        print(f'Sorted list: {burndown_list}')

        # Offset the extremes
        lhs, rhs = (burndown_list[:1][0], burndown_list[-1:][0])
        print(lhs, rhs)
        result = lhs + rhs
        print(result)

        # Remove elements, add to new list
        burndown_list.remove(lhs)
        burndown_list.remove(rhs)
        burndown_list.append(result)
        print(f'New list: {burndown_list}')

