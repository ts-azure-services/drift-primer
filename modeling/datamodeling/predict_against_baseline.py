"""Score retrain, concept and drift data snapshots against baseline endpoint """
import os
import sys
import os.path
import pandas as pd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..')))
#from scripts.authentication.service_principal import ws
from scripts.setup.common import load_env_variables#, score_request
from scripts.setup.common import create_predictions, get_accuracy


def request_records(source=None):
    """Create request records"""

    # Pull in the CSV directly
    ds = pd.read_csv(source)

    # Drop 'Churn column'
    churn_df = ds[['Churn']]
    ds = ds.drop('Churn', axis=1)
    assert list(ds.index) == list(churn_df.index)

    list_of_records = ds.to_dict('records')
    return list_of_records, churn_df


def compare_cols(y1,y2):
    if y1 == y2:
        return "MATCH"
    else:
        return "COMPARE_ERROR"

def tf_reporting(col_name=None, series_df=None, df_len=None):
    y1 = series_df.get(key='False')
    if y1 is not None:
        print(f"'FALSE' for {col_name} is: {y1}")
    else:
        print(f"'FALSE' for {col_name} is: 0")

    y2 = series_df.get(key='True')
    if y2 is not None:
        print(f"'TRUE' for {col_name} is: {y2}")
        churn_rate = 100 * y2 / df_len
        print(f"Churn Rate for {col_name}: {churn_rate}")
    else:
        print(f"'TRUE' for {col_name} is: 0")

def compare_reporting(series_df=None, df_len=None):
    y1 = series_df.get(key='COMPARE_ERROR')
    if y1 is not None:
        print(f"'COMPARE_ERROR' is: {y1}")
        print(f"Error rate: { 100 * y1 / df_len}")
    else:
        print("'All match. No errors.")


def main():
    "Main operational workflow"

    # Load relevant authentication
    auth_dict = load_env_variables(url='BASELINE_URI', api_key='BASELINE_APIKEY')
    
    # Create request list
    list_of_records, churn_df = request_records(source=sys.argv[1])#'./datasets/baseline_revised.csv'

    # Create predictions from real-time endpoint
    prediction_list = create_predictions(auth_dict=auth_dict, list_of_records=list_of_records)

    # Get accuracy, comparing actual churn vs. predicted churn
    cdf = get_accuracy(prediction_list=prediction_list, churn_df=churn_df)#, final_output='test_concept_churn.csv')

    # Reporting of results
    cdf['Compare'] = cdf.apply(lambda x: compare_cols(x['Actual_Churn'], x['Predicted_Churn']), axis=1)
    cdf_len = len(cdf)
    print(f"Length of dataframe is: {cdf_len}")

    # Break into series, and report on results
    ac_series = cdf['Actual_Churn'].value_counts()
    pc_series = cdf['Predicted_Churn'].value_counts()
    diff_series = cdf['Compare'].value_counts()

    tf_reporting(col_name='Actual Churn', series_df=ac_series, df_len=cdf_len)
    tf_reporting(col_name='Predicted Churn', series_df=pc_series, df_len= cdf_len)
    compare_reporting(series_df=diff_series,df_len=cdf_len)


if __name__ == "__main__":
    main()
