"""Script to generate records as per baseline distributions"""
import math
import uuid
import time
import random
import pandas as pd
import numpy as np
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


def bin_column(df=None, new_col_name=None, base_col=None, number_bins=None):
    """Bin data for specific columns"""
    df[new_col_name] = pd.cut(x = df[base_col],bins=number_bins,include_lowest=True)
    return df

def round_logic(val=None):
    """Rounding logic for customer assignments"""
    frac, whole = math.modf(val)
    if frac < 0.5:
        ret_val = math.floor(val)
    else:
        ret_val = np.ceil(val)
    return ret_val

def integer_alignment(
        base_list=None,
        change_list=None,
        target=None,
        ):
    """Align float values to the targeted integer total"""
    # Get the sum of the base and the list to change
    base_list_sum=sum(base_list)
    change_list_sum=sum(change_list)

    # Compare against the target, and iterate
    if base_list_sum == target:
        pass
    elif base_list_sum < target:
        # Then +1, for each list item
        i = 0
        while change_list_sum != target:
            # Keep iterating through if you come to the end of the list
            if i > len(change_list) - 1:
                i = 0
            else:
                change_list[i] = change_list[i] + 1
                change_list_sum = sum(change_list)
                i += 1
    else:
        # Then -1, for each list item
        i = 0
        while change_list_sum != target:
            if i > len(change_list) - 1:
                i = 0
            else:
                change_list[i] = change_list[i] - 1
                change_list_sum = sum(change_list)
                i += 1
    return base_list, change_list, base_list_sum, change_list_sum

def transform_original_dataset():
    """Get original dataset into transformed state"""

    # Initial transformations
    df = pd.read_csv('./datasets/original/WA_Fn-UseC_-Telco-Customer-Churn.csv')
    df['Churn'] = df['Churn'].apply(lambda x: 0 if x == "No" else 1)
    df['SeniorCitizen'] = df['SeniorCitizen'].apply(lambda x: "No" if x == 0 else "Yes")

    # Bin columns
    df = bin_column(df=df, new_col_name='tenure_bins', base_col='tenure', number_bins=10)
    df = bin_column(df=df, new_col_name='monthly_charges_bins', base_col='MonthlyCharges', number_bins=10)
    df = df.drop(['TotalCharges', 'MonthlyCharges', 'tenure'], axis=1)
    df['monthly_charges_bins'] = df['monthly_charges_bins'].astype(object)
    df['tenure_bins'] = df['tenure_bins'].astype(object)
    #df.to_csv('./../datasets/baseline_revised.csv', encoding='utf-8', index=False)

    # Groupby unique combinations
    col_list = list(df.columns)
    non_attribute_cols = ['customerID', 'MonthlyCharges', 'Churn']
    attribute_cols = list( set(col_list) - set(non_attribute_cols) )
    return df, attribute_cols

def create_lookup(
        df=None,
        attribute_cols=None,
        volume=None,
        churn_factor=None,
        dataset_name=None
        ):
    """Create lookup blueprint"""

    # Groupby to get unique combinations
    new_df = df.groupby(by=attribute_cols).agg({
        'customerID':'count',
        'Churn':['sum']
        })
    new_df.columns = ['original_customer_count', 'original_churn_sum']#, 'churn_count']

    # Convert to new df
    new_df = new_df.reset_index()
    new_df['original_customer_ratio'] = new_df['original_customer_count'] / new_df['original_customer_count'].sum()

    # Calculate churn, adjust for any factor
    new_df['original_churn_ratio'] = new_df['original_churn_sum'] / new_df['original_customer_count']
    if churn_factor is not None:
        new_df['original_churn_ratio'] = new_df['original_churn_ratio'] * churn_factor

    # Distribute customer totals
    new_df['new_customer_count_float'] = new_df['original_customer_ratio'] * volume
    new_df['new_customer_count_int'] = new_df.apply(lambda x: round_logic(x['new_customer_count_float']), axis=1)

    # Sort to get the most volume for reconciling
    new_df = new_df.sort_values(by='new_customer_count_int', ascending=False)

    # After resolving to integers and sorting, then finetune to get to the right population size
    cust_count_base_list = new_df['new_customer_count_int'].to_list()
    change_list = cust_count_base_list.copy()

    # This iterates to ensure the volume specified is adjusted
    base_list, change_list, base_list_sum, change_list_sum =\
            integer_alignment(
            base_list=cust_count_base_list,
            change_list=change_list,
            target= volume,
            )

    new_df['new_customer_optimized'] = change_list

    # Convert to int, so it can be used in range functions
    new_df['new_customer_optimized'] = new_df['new_customer_optimized'].astype(int)
    new_df['new_churn_customers'] = new_df['new_customer_optimized'] * new_df['original_churn_ratio']
    new_df['new_churn_customers'] = new_df.apply(\
            lambda x: round_logic(x['new_churn_customers']),axis=1)\
            .astype(int)
    #new_df.to_csv('newdf.csv', index=False, encoding='utf-8')

    list_of_records = new_df.to_dict('records')

    # Iterate through the dictionary to produce rows
    final_df = pd.DataFrame()
    for dictionary in list_of_records:
        # Initialize the temporary list and dataframe
        temp_customer_list = []
        temp_df = pd.DataFrame()

        # Iterate through each bluelogging.info to produce rows
        for i in range(dictionary['new_customer_optimized']):
            temp_dict = dictionary.copy()
            temp_dict.update({'customerID': str(uuid.uuid1())})
            temp_customer_list.append(temp_dict)

        temp_df = temp_df.append(temp_customer_list)
        temp_df['Churn'] = 0
        churn_temp_df = temp_df.sample(n=dictionary['new_churn_customers'])
        temp_df.loc[ churn_temp_df.index, 'Churn' ] = 1

        # Append the temp_df results to the final dataframe
        final_df = final_df.append(temp_df)

    # Assert that the final dataframe equals the volume inputted into the function
    assert len(final_df) == volume

    # Shuffle the final result, and produce output
    final_df = final_df.sample(frac=1)
    final_df = final_df.reset_index(drop=True)
    final_df = final_df.drop([
        'original_churn_ratio',
        'original_customer_ratio',
        'original_customer_count',
        'original_churn_sum',
        'new_churn_customers',
        'new_customer_count_float',
        'new_customer_count_int',
        'new_customer_optimized'
        ], axis=1)
    final_df.to_csv('./datasets/' + str(dataset_name) + '.csv', encoding='utf-8', index=False)

def get_ratios(df = None, column_name=None):
    """Get ratios for specified column from original dataset"""
    # Ensure that the sum of the values is the customer count
    df = df[column_name].value_counts().to_frame()
    df = df.reset_index()
    df.columns = [column_name, 'customer_count']
    customer_count = df['customer_count'].sum()
    df['percent'] = df['customer_count'] / customer_count
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
    df['delta'] = df['new_allocation'] - df['customer_count']
    logging.info(new_customer_totals)
    logging.info(df)

    delta_dict = dict(zip(df[column_name], df['delta']))
    logging.info(f'Delta dict: {delta_dict}')
    return delta_dict


def create_adjusted_list(
        column_df=None, 
        column_name= None, 
        temp_dict=None
        ):
    """Create the adjusted list for the specified column"""
    temp_column_df = column_df.copy()

    if sum(temp_dict.values()) == 0:

        while len(temp_dict) != 1:
            # Sort the dictionary
            marklist=sorted(temp_dict.items(), key=lambda x:x[1])

            # Test if marklist has elements
            if not marklist:
                logging.info('No elements left in dictionary')
                break

            # Sort the dictionary
            sortdict = dict(marklist)
            logging.info(f'Sorted dictionary: {sortdict}')

            keys = list ( sortdict.keys() )
            values = list ( sortdict.values() )

            # Offset the extremes
            lhs, rhs = (values[0], values[len(values)-1])
            result = lhs + rhs

            # Iterate through next steps
            if result == 0:
                rem_key = {n_key:n_val for n_key, n_val in sortdict.items() if n_val != lhs}
                rem_key = {n_key:n_val for n_key, n_val in rem_key.items() if n_val != rhs}
                temp_dict = rem_key

                # Augment the dataframe for the LHS, for the exact number on RHS
                t_slice = temp_column_df[ temp_column_df[column_name] == keys[0] ]
                t_slice = t_slice.sample(n=abs(rhs))
                replacement_list = [ [ keys[len(keys)-1] ] * len(t_slice.index)][0]
                temp_column_df.loc[t_slice.index, column_name] = replacement_list

            elif result < 0:
                rem_key = {n_key:n_val for n_key, n_val in sortdict.items() if n_val != lhs}
                rem_key = {n_key:n_val for n_key, n_val in rem_key.items() if n_val != rhs}
                temp_dict = rem_key
                temp_dict[keys[0]] = result

                # Augment the dataframe for the LHS, for the exact number on RHS
                t_slice = temp_column_df[ temp_column_df[column_name] == keys[0] ]
                t_slice = t_slice.sample(n=abs(rhs))
                replacement_list = [ [ keys[len(keys)-1] ] * len(t_slice.index)][0]
                temp_column_df.loc[t_slice.index, column_name] = replacement_list

            logging.info(f'New list: {temp_dict}')

    return column_df, temp_column_df
