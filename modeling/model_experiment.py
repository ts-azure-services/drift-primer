import sys
sys.path.append('./../scripts/')
import os
from authentication import ws
import pandas as pd
from azureml.data.dataset_factory import TabularDatasetFactory

datastore = ws.get_default_datastore()

_ = TabularDatasetFactory.register_pandas_dataframe(
        pd.read_parquet('./../datasets/M9.parquet'),
        target=(datastore, "M9_data"),
        name='M9_adfas'
        )

