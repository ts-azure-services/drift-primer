# Three Months Later...
A few months into the use of the churn model, the business is pleased at some of the early progress. Though
the churn rate has not dramatically improved, this was largely expected in the short-term. On the positive side, the
marketing team is aggressively using the model to prioritize outreach and learn customer pain points that
may lead to churn. This is exactly the short-term cultural push the business is looking to make, as they
modernize other processes and systems to enhance the customer experience.

The MLOps team is encouraged by this progress. However, three months have passed since the initial model was
put in operation. No significant degradation has been noticed in model performance. However, by design, the
MLOps team would like to ensure the model in operation is not based on data that is older by three months. As
before, this requires taking the most recent snapshot of customer activity and labeling the 'ground truth' for
which customers have churned (at that point in time, as per the established definition).

## Necessary Steps
1. The new batch of data (the `Retrain Dataset`) needs to be registered in the workspace. This helps with data
   lineage and reproducability of results. This dataset contains the same attributes, and relative
   relationship of churn as the `Transformed Training Baseline Dataset`. More context on how this was created is in the *Background
   Context* section below.
2. Off the `Retrain Dataset`, a new training run with AutoML can be triggered to find the best model.
	- **To pipeline or not to pipeline.** In most scenarios, re-using the original pipeline would be the
	  best practice for training a new model. This would preserve the data transformations and the
	  reproducibility of the process. However, one can also train with consistent use of scripts without a
	  pipeline, but preserving data lineage, tracking, and experiment recreation. To show this
	  flexibility, the new model is triggered through scripts that call the AutoML configuration to derive
	  the best model.
	- **Configuring a test run.** In the prior section, when we created a pipeline, we also had a discrete
	  step to breakout training and test datasets, based on a 90/10 ratio. In this approach, that can be
	  specified as part of the AutoML configuration. Once the training is done, an automatic testing run
	  is triggered using the best model. Results are shown below.
	  ![retrain_test_data](./imgs/retrain_test_data.jpg)
	- **Creating an endpoint.** The best model out of this run can be used to create the
	  `retrain-endpoint`. This will provide a real-time endpoint to test predictions against the new
	  model. ![retrain_endpoint](./imgs/retrain_endpoint.png)

## Validating Training
Given that model performance has not degraded significantly and the real driver for a retrain was to avoid a model derived off stale data, the retrained model should be relatively consistent with
the baseline model. To test this, we can run two operations:
1. Score the new data (`Retrain Dataset`) on the old model endpoint (`baseline-model-endpoint`). If this is
   relatively consistent (i.e. no major drifts), this should be relatively close in accuracy. As per the
   operation below, the accuracy is close, and we see this holds true.
2. Score the old data (`Transformed Training Baseline Dataset`) on the new model endpoint
   (`retrain-endpoint`). By checking through this approach, we find this to also hold true.

Based on the above, both models are close in predictive accuracy largely because they are based on
fundamentally *similar data*. With this, the new retrained model can be promoted to be the production model
using by the marketing team.

## Background Context
- To simulate this scenario, the `Retrain Dataset` was a simulated version of the original data. A script
  (<name of script>) was run to maintain the overall churn relationship and the data distributions inherent in
  the baseline dataset, while allowing for some variability in the total customer count.
- As mentioned in the *The Business Scenario*, it should be noted that establishing ground truth for a customer that has actually
  churned is not always straightforward. One can be deterministic in the definition (for example, saying a
  customer has churned if they have not used the service for greater than 30 days), but in some cases, you may
  know a customer has churned sooner (support calls, bad customer experience), or one may find customers
  previously classified as churned end up returning to the service. For the purposes of the above
  illustration, we are ignoring these realities.
