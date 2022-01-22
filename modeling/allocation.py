import math
import pandas as pd

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
    print(new_customer_totals)
    print(df)

    delta_dict = dict(zip(df[column_name], df['delta']))
    print(f'Delta dict: {delta_dict}')
    return delta_dict

def create_adjusted_list(
        column_df=None, 
        column_name= None, 
        temp_dict=None
        ):
    """Create the adjusted list for the specified column"""
    original_column_df = column_df

    if sum(temp_dict.values()) == 0:

        while len(temp_dict) != 1:
            # Sort the dictionary
            marklist=sorted(temp_dict.items(), key=lambda x:x[1])

            # Test if marklist has elements
            if not marklist:
                print('No elements in dictionary')
                break

            # Sort the dictionary
            sortdict = dict(marklist)
            print(f'Sorted dictionary: {sortdict}')

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
                temporary_slice = column_df[ column_df[column_name] == keys[0] ].copy()
                temporary_slice = temporary_slice.sample(n=abs(result))
                column_df.loc[temporary_slice.index, column_name] == keys[ len(keys) - 1 ]

            elif result < 0:
                rem_key = {n_key:n_val for n_key, n_val in sortdict.items() if n_val != lhs}
                rem_key = {n_key:n_val for n_key, n_val in rem_key.items() if n_val != rhs}
                temp_dict = rem_key
                temp_dict[keys[0]] = result

                # Augment the dataframe for the LHS, for the exact number on RHS
                temporary_slice = column_df[ column_df[column_name] == keys[0] ].copy()
                temporary_slice = temporary_slice.sample(n=abs(result))
                column_df.loc[temporary_slice.index, column_name] == keys[ len(keys) - 1 ]

            #else:
            #    rem_key = {n_key:n_val for n_key, n_val in sortdict.items() if n_val != lhs}
            #    rem_key = {n_key:n_val for n_key, n_val in rem_key.items() if n_val != rhs}
            #    temp_dict = rem_key
            #    temp_dict[keys[len(values)-1]] = result

            #    # Augment the dataframe for the LHS, for the exact number on RHS
            #    temporary_slice = column_df[ column_df[column_name] == key[0] ].copy()
            #    temporary_slice = temporary_slice.sample(n=abs(result))
            #    column_df.loc[temporary_slice.index, column_name] == key[ len(keys) - 1 ]

            #print(result)
            print(f'New list: {temp_dict}')

    return original_column_df, column_df

def main():

    # Get original data
    df = pd.read_csv('./../datasets/original/WA_Fn-UseC_-Telco-Customer-Churn.csv')

    # Get delta ratios
    column_name = 'PaymentMethod'
    temp_dict = get_ratios(df=df, column_name=column_name)

    # Pass in the list to adjust to get the adjusted list
    original_df, column_df = create_adjusted_list(
            column_df=df[[column_name]], 
            column_name=column_name, 
            temp_dict=temp_dict
            )

    original_df.to_csv('originaldf.csv', encoding='utf-8')
    column_df.to_csv('columndf.csv', encoding='utf-8')
    print(column_df)

if __name__ == "__main__":
    main()
