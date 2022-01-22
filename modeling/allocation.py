import pandas as pd
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

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

def main():

    # Get original data
    #df = pd.read_csv('./../datasets/original/WA_Fn-UseC_-Telco-Customer-Churn.csv')
    df = pd.read_csv('./../datasets/baseline_revised.csv')

    # Get delta ratios, based on the new ratio
    column_name = 'Contract'
    temp_dict = get_ratios(df=df, column_name=column_name)

    # Pass in the list to adjust to get the adjusted list
    column_df, temp_column_df = create_adjusted_list(
            column_df=df[[column_name]], 
            column_name=column_name, 
            temp_dict=temp_dict
            )

    ## Check if variances have been accounted for
    #combined_df = pd.merge(column_df, temp_column_df, left_index=True, right_index=True)
    #combined_df.to_csv('COMBINED.csv', encoding='utf-8')

    # Adjust the new column on the dataframe
    df[column_name] = temp_column_df
    df.to_csv('FINAL.csv', encoding='utf-8')

if __name__ == "__main__":
    main()
