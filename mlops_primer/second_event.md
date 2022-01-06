# Model Degradation (t+6...)

- Deliberately degrade the model's accuracy over time. Why? Shift in attributes, and predictions.
- Introduce data drift, and concept drift as concepts.
- This is where alerting can be showcased through App Insights, and Power BI.
- Use of data drift monitor.

- Change the underlying assumptions on the model side.
- In our case, this is likely going to be changes on the 'data drift'. " To detect data drift, we can trigger
  data factory pipelines weekly that analyze the dataset profiles, with data validation tests."

- How do we handle these situations?
	- Establish a new pipeline, with data after xyz date and train a new model
	- In practice, are the changes this dramatic?

