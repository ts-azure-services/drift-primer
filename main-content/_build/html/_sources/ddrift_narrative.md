# Data Drift
As a few more months pass, the MLOps team starts to see the retrained model's accuracy regress. On further
inspection, they notice that one of the key attributes (`Contract`) is starting to change in its distribution.

Though 'Month-to-Month' contracts were almost ~55% of the customer preferences, this is becoming more even
across one year and two year contracts as well. The business speculates that given more people are working
from home during the pandemic, the normal hesitation to commit to longer-term plans is cooling off somewhat.
As the business learns more, the MLOps recognizes that this distribution may have a potentially negative
impact on the efficacy of the model to predict churn customers accurately. Of note, `Contract` was one of the
primary features in the baseline/retrained model. Hence, sharper deviations on this attribute likely may cause
changes in the current model's assumptions. This is an example of **data drift**: a circumstance when the
original distributions of the underlying attributes start to shift from the original distributions that
trained the base model.

The remedy is to retrain for the new dataset (if that is the new reality moving forward). At a baseline level, an
organization could take this philosophy further by automating any model performance loss to initiate a retrain
of the entire model. This new model could then be elevated to be the new baseline in production. When other
variables are reasonably consistent (e.g. same algorithm, same objective and use case), this is a reasonable,
and a recommended course of action, i.e. enforce higher levels of automation. In other cases, there may be a
need to have more manual intervention, and take a judgement call before pushing a new model to production.

## Training Results
1. The new dataset is the `Data Drift Dataset`.
2. A single script triggers an AutoML training off this dataset, with similar configuration as the retraining
   exercise a few months before.
3. After re-training, a number of other features now out-rank `Contract`.
![ddrift_exp_features](./imgs/ddrift_exp_features.jpg)
4. Retraining produces models ... with accuracy.
5. The test accuracy is ...

## Data Drift Monitor
One of the ways to keep track of some of these shifts is to periodically run a **dataset monitor** which
specifically compares datasets between different time periods. It then reports back on where differences
between distributions are crossing an all-up threshold which can trigger email alerts and notifications like
below:
![data_drift_alert](./imgs/data_drift_alert.jpg)

A few examples of some of the available views include:
<pic1>
<pic2>


## Validating Training
To see how much the new dataset has degraded on the baseline model, we can compare the `Data Drift Dataset` on
the older `retrain-endpoint`. This yields a prediction accuracy of xx, compared to the 'ground truth'.


## Background Context
To simulate this scenario, a simulated dataset was created adjusting for a more consistent spread across the
`Contract` attribute in the baseline dataset. All else was maintained in terms of attribute distributions and
overall churn rate with the baseline dataset. 
