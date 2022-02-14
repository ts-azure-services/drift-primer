import os
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..')))
from scripts.authentication.service_principal import ws
from scripts.setup.common import load_env_variables, request_records#, score_request
from scripts.setup.common import create_predictions, get_accuracy


def main():
    "Main operational workflow"

    # Load relevant authentication
    auth_dict = load_env_variables(url='BASELINE_URI', api_key='BASELINE_APIKEY')
    
    # Create request list
    list_of_records, churn_df = request_records(ws=ws, dataset_name='Data Drift Dataset')

    # Create predictions from real-time endpoint
    prediction_list = create_predictions(auth_dict=auth_dict, list_of_records=list_of_records)

    # Get accuracy, comparing actual churn vs. predicted churn
    get_accuracy(prediction_list=prediction_list, churn_df=churn_df)


if __name__ == "__main__":
    main()
