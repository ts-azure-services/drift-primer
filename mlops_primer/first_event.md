# Three Months Later...
A few months into the use of the ML model, the business is pleased at both the use of the model to identify
potential churned customers, and the internal cultural and process changes that marketing is continuing to
drive to improve customer retention. Though the churn rate has not dramatically improved, the learnings from
the model coupled with the ongoing short-term and long-term investments feels a much better step in the right
direction.

The MLOps team is encouraged by the progress. But now that three months have passed, they are intersted in
ensuring the model continues to be retrained on more recent data. As a policy, and in agreement with the
business, an early goal had been not to let data grow stale beyond a few months.

As part of the ongoing monitoring, there has been no significant degradation in the model performance. Still,
they would like to retrain on a fresh batch of data, and test if the new model performs equally well, or
consistent with the old model. It's an opportunity to:
	- Test the new model on the old data
	- Test the old model on the new data

Based on the above, they can take a call on whether to keep the existing model in operation, or push a new
model into production. This is also where having the original pipeline which trained the model will come in
handy since this allows for reusability of the same workflows.

## Steps involved
- Retrain using the existing pipeline
- Show accuracy of the new model on the old data
- Show accuracy of the old model on the new data


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
