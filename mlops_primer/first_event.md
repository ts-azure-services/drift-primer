# The First Train (t+3...)
A few months into the use of the ML model, the business is pleased at how the predictive capabilities of the
pipeline are now saving time, and producing results that demonstrate accuracy.  The model is accurate (show
this with a comparison of residuals vs. predictions - new dataset to create...), and the business is getting
comfortable with the use of ML in their activities. A great win!

As a policy, the MLOps team has decided to never let the model 'get stale' beyond 3 months. Three months have
passed and the team is ready to re-train the model, and re-deploy it.

A couple of things to note:
- Since they had a pipeline trained and ready, this is re-usable and just needs to account for the full
  dataset.
- Show how data was collected at the endpoint.
- The data drift monitor has been operational every day since it started, and highlighted that there are no
  major changes in the distributions, or the categories of the data feeding the model.
- There are 2 new attributes that the business onboarded.
- They anticipate little to no changes to the algorithm being used.

https://github.com/ts-azure-services/aml-datadrift

## Requirements
- Show how the re-training works with snapshots.
- Show how the re-deployment works, including the lineage aspects.
