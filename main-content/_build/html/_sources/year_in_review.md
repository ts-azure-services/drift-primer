# A Year in Review
It's been nearly a year since the team first embarked upon creating an ML model for predicting churn!

Along the way, much has happened. The MLOps team has had to update for changes for new data, and respond to
changes in the distribution and relationships of the underlying data. None of this has been done in siloes,
but in active participation with the marketing organization. The team has also grown familiar with the
operations of Azure Machine Learning, and learned how to leverage the system to hit a range of goals around
performance, data lineage, governance all while extensively using AutoML to simplify the training process.
Though this was an initial step, the team is now geared up to further expand the range of possible ML
solutions to target even more use cases around customer experience.

**Note:** Through this example, we attempted to focus on concept and data drift discretely. In reality, there
is likely a continuous interplay of both concept and data drift at the same time. Both the underlying data
attributes may change, as well as their relationship to the target variable. In this example, we also
treated the datasets as specific batches at various points in time. This simplified the exercise, but in
reality, one will have to manage this effort with real-time data and understand how changes are impacting the
model on a daily basis. This of course, depends on the model, the standards for accuracy and the business use
case.

We hope you've enjoyed this primer!
