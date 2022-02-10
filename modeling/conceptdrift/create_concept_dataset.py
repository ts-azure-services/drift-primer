"""Script to generate records as per baseline distributions"""
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..')))
from modeling.datamodeling.common import transform_original_dataset, create_lookup
import time
import random
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


def main():
    start_time = time.time()

    # Load, and transform original dataset
    df, attribute_cols = transform_original_dataset()
    #df.to_csv('./datasets/baseline_revised.csv', encoding='utf-8', index=False)

    # Use original dataset to create a bluelogging.info for simulating data
    min_vol = 6900
    max_vol = 7200
    churn_factor = 0.5
    create_lookup(
            df = df,
            attribute_cols= attribute_cols,
            volume = random.randint(min_vol, max_vol),
            churn_factor= churn_factor,
            dataset_name= 'cdrift_data/concept_dataset'
            )

    logging.info('Entire script took %s seconds', (time.time() - start_time))

if __name__ == "__main__":
    main()
