# Data Drift

A couple of things to note:
- Show how data was collected at the endpoint.
- The data drift monitor has been operational every day since it started, and highlighted that there are no
  major changes in the distributions, or the categories of the data feeding the model.
- There are 2 new attributes that the business onboarded.
- They anticipate little to no changes to the algorithm being used.
![dataset](./imgs/data_drift_dataset.png)

https://github.com/ts-azure-services/aml-datadrift

## Requirements
- Show how the re-training works with snapshots.
- Show how the re-deployment works, including the lineage aspects.
