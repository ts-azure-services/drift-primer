# Concept Drift
Six months after the initial deployment of the model, there are early signs that the model is starting to
degrade. On the bright side, this seems to be largely because the churn rate is starting to decline in
response to some of the initiatives taken by the marketing and customer success teams. Given the MLOps team is
being held to a +80% accuracy on the churn prediction metric, an early alert has shown continual decline in
the model's ability to predict accurately.

In response, the MLOps team will retrain the model, and evaluate the new model on the fresh batch of data. It
it outperforms the existing model, it will be promoted as the new model to the production system.

- This is where alerting can be showcased through App Insights, and Power BI.

- Change the underlying assumptions on the model side.
- In our case, this is likely going to be changes on the 'data drift'. " To detect data drift, we can trigger
  data factory pipelines weekly that analyze the dataset profiles, with data validation tests."

- How do we handle these situations?
	- Establish a new pipeline, with data after xyz date and train a new model
	- In practice, are the changes this dramatic?
