# Three Months Later...
A few months into the use of the ML model, the business is pleased at both the use of the model to identify
potential churned customers, and the internal cultural and process changes that marketing is continuing to
drive to improve customer retention. Though the churn rate has not dramatically improved, the learnings from
the model coupled with the ongoing short-term and long-term investments is a better step in the right
direction.

The MLOps team is encouraged by the progress. But now that three months have passed, they are interested in
ensuring the model continues to be retrained on more recent data. As a policy, and in agreement with the
business, an early goal had been not to let data grow stale beyond a few months.


As part of the ongoing monitoring, there has been no significant degradation in the model performance. Still,
they would like to retrain on a fresh batch of data and see if the new model is any different to the old
model.
![dataset](./imgs/retrain_dataset.png)

To do this, the MLOps team would like to:
1. Score the new data (`Retrain Dataset`) on the old model endpoint (`baseline-model-endpoint`).
2. Score the old data (`Transformed Training Baseline Dataset`) on the new model endpoint (`retrain-endpoint`).

Based on the above, they can take a call on whether to keep the existing model in operation, or push a new
model into production. In most scenarios, re-using the original pipeline would be the best practice since that
would keep consistent the data transformations and the reproducibility of the process. For expediency, we have
pre-created the datasets, and the models that are trained on them. Hence, the new model (`retrain-endpoint`) has been trained on
the new dataset (`Retrain Dataset`). Note that by pursuing this approach, the `Run Types` in Azure Machine
Learning are different; the former is a `Pipeline` run, while the current method is an `Automated ML` run.
![run_types](./imgs/run_types.jpg)

Another difference in the pipeline approach is that while we explicitly had a step to break out the train and
test split, this can also be configured in the AutoML configuration as well. As a part of the training run,
there will also be a test run immediately run, taking the best model.
![retrain_test_data](./imgs/retrain_test_data.jpg)


## Considerations
- For simulating this scenario, a simulated dataset has been created which mimics similar distributions and
  input/output relationships from the original dataset. The retraining process should yield a model that is
  fairly close in accuracy to the original model. As mentioned in the 'The Business Scenario', establishing
  ground truth for a customer that has actually churned is a function of both time lag since recent
  transactions and part of the marketing team labelling customers who have decided to leave the service.


A couple of things to note:
- Show how data was collected at the endpoint.
- The data drift monitor has been operational every day since it started, and highlighted that there are no
  major changes in the distributions, or the categories of the data feeding the model.
- There are 2 new attributes that the business onboarded.
- They anticipate little to no changes to the algorithm being used.

https://github.com/ts-azure-services/aml-datadrift

## Requirements
- Show how the re-training works with snapshots.
- Show how the re-deployment works, including the lineage aspects.
