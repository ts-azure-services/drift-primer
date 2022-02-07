# Concept Drift
Six months after the initial deployment of the model, there are signs that the model is degrading in
performance (again). On the bright side, this seems to be largely because the churn rate is starting to decline in
response to some of the marketing initiatives. Given the MLOps team is being held to a +80% accuracy on the
churn prediction metric, an early alert has shown continual decline in the model's ability to predict
accurately. This is an example of **concept drift** - where the fundamental relationship between the input(s),
or the attributes and the predicted target variable (i.e. churn) is undergoing change.

As before, the MLOps team will retrain the model, and evaluate the new model on the fresh batch of
data. If it outperforms the existing model, it will be promoted as the new model to the production system.

- This is where alerting can be showcased through App Insights, and Power BI.

## Necessary Steps
1. The new batch of data (the `Concept Dataset`) needs to be registered in the workspace. This dataset
   contains the same attributes though the relationship between the input(s) and the target variable has
   changed. (For example, in the original dataset, the churn was ~26% of the entire population while in the
   new batch of data, it is ~x%.) ![dataset](./imgs/concept_dataset.png)
2. Off the `Concept Dataset`, a new training run with AutoML can be triggered to find the best model. The
   AutoML configuration is similar to the retraining step the few months before.
	- Post-training, the feature attribution is shown below:  ![ddrift_exp_features](./imgs/ddrift_exp_features.jpg)
	- Test accuracy is validated with ...
3. **Data Drift Monitor.** One of the ways to keep track of some of these shifts is to periodically run a
   **dataset monitor** which specifically compares datasets between different time periods. It then reports
   back on where differences between distributions are crossing an all-up threshold which can trigger email
   alerts and notifications like below: ![data_drift_alert](./imgs/data_drift_alert.jpg)
	- A few examples of some of the available views include: <pic1>
4. **Model inaccuracy.** To see how much the new dataset has degraded on the baseline model, we can compare
   the `Concept Dataset` on the older `retrain-endpoint`. This yields a prediction accuracy of xx, compared
   to the 'ground truth'.


## Background Context
To illustrate this scenario, a simulated dataset was created adjusting a factor on the churn allocation across
the customer base. Attribute distributions were kept consistent, while the overall volume of customers stayed
in a similar range as before. 
