# Data Drift
As a few more months pass, the MLOps team starts to notice the retrained model's accuracy regress. 

On further inspection, they notice that some of the key attributes (including `Contract`, `tenure_bins`, etc.)
are starting to have different distributions. For example, in the `Contract` attribute, 'Month-to-Month'
contracts were almost ~55% of the customer contract preference. However, this is becoming more of an even
spread across month-to-month, 1-year and 2-year contracts. Given the recent pandemic with more people working
from home, the business speculates that more customers are willing to commit to a longer-term plan to lock in
more predictable rates. Telecomm providers are also focusing more efforts on expanding services through
internet services, and are making available better deals on longer-term contracts, with fewer switching
incentives.

As the business continues to learn more, the MLOps team has a more immediate concern. The existing model needs
to reflect this new reality and be retrained on the new batch of data. Attributes like the `Contract`
attribute were also one of the primary features in the baseline/retrained model hence sharper deviations on
this attribute may likely cause changes in the current model's assumptions. 

This is an example of **data drift** - when the original distributions of the attributes used to build the
model start to change. In response, the model needs to change, and hence be retrained.

In reality, there are a whole host of approaches a business may take. There may be an acceptable level of
degradation implicit in the model that the business is willing to assume before retraining. Establishing
degradation is also a factor of how soon the business can establish 'ground truth'. In the prior section, we
outlined that establishing churn can often be delayed target variable. 

From an MLOps perspective, the business may also require a more manual, human-judgement process to trigger the
retrain, or the need for a new production model. In other cases, a retrain may automatically be automated if model
performance falls below a certain threshold. When other variables are reasonably consistent (e.g. same
algorithm, same objective/use case), this is a reasonable and recommended approach. In other cases, there may
be a need to have more manual intervention, and take a judgement call before pushing a new model to
production.

## Necessary Steps
1. **Artifact the new batch of data.** The new batch of data (the `Data Drift Dataset`) needs to be registered
   in the workspace. This helps with data lineage and reproducability of results. This dataset contains the
   same attributes, and relative relationship of churn as the `Transformed Training Baseline Dataset`.
   However, as noted above,  a number of attributes are starting to show changes in their spread. More context
   on how this was created is in the *Background Context* section below.
2. **Train the model.** Off the `Data Drift Dataset`, a new training run with AutoML can be triggered to find
   the best model. The AutoML configuration is similar to the retraining step the few months before.
	- Results of the training process yield the following results:
	  ![datadrift_models](./imgs/ddrift_models.jpg)
	- After re-training, a number of other features and their importance have rejiggered from their
	  original baseline positions. ![ddrift_exp_features](./imgs/ddrift_exp_features.jpg)
	- Test accuracy is slightly better at ~84% vs. ~82%...
	  ![ddrift_test_accuracy](./imgs/ddrift_test_accuracy.jpg)

## Data Drift Monitor
One of the ways to keep track of some of these shifts is to periodically run a **dataset monitor** which
specifically cmpares datasets over time and between different time periods. Setting this up requires some
configuration on the datasets to compare. In this case, both the baseline and the new batch of the `Data
Drift Dataset` are discretely added for comparison, with appropriate timestamps. ![data_drift_datasets](./imgs/data_drift_datasets.jpg)

### Viewing Data Drift Results
The studio experience allows an overview of a composite metric for data drift, some level of exploration
of which attributes are driving the data drift, and how they contribute. More customization is possible given
the tight integration with App Insights and Azure Monitor to define reporting and thresholds at even granular
levels. 

For a quick overview of the out-of-box view, see the video below:
![data_drift_monitor](./gifs/data_drift_monitor.gif)

### Alerting
One of the benefits of setting up a data drift monitor is its tight integration with Azure Monitor, along with
its alerting capabilities to identify when drift has exceeded a certain threshold.

For example, this is the email notification one receives when a data drift alert is detected.
![data_drift_alert](./imgs/data_drift_alert.jpg)

And this is the email notification which can help define the specific users/group to be part of to be notified
when there is drift detected.
![data_drift_action_group](./imgs/data_drift_action_group.jpg)

Such alerting mechanisms enable the MLOps team to be proactive with how their data is changing and respond
accordingly. Note that not all data drifts are inherently data relationships changing. Often, there can be
some quality gaps in the attributes coming through the system, and this can be a early signal to mitigate
system issues.

## Comparing the Baseline Model
To see how much the new dataset has degraded on the baseline model, we can compare the `Data Drift Dataset` on
the original `baseline-model-endpoint`. This yields an error rate of +23.6%, compared to the baseline test
accuracy rate of ~19-20%. Hence, the inherent drift in the data distributions is leading to this increased
inaccuracy for predictions.

![data_drift_comparison](./gifs/compare_data_drift.gif)

## Background Context
To simulate this scenario, a simulated dataset was created adjusting for a more consistent spread across the
`Contract`, `PaymentMethod`, `Dependents`, `OnlineSecurity`, `TechSupport` and `tenure_bins` attribute in the
baseline dataset. All else was maintained in terms of attribute distributions and overall churn rate compared
to the baseline dataset.
