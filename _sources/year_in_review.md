# A Year in Review
It's been nearly a year since the team first embarked upon creating an ML model for predicting churn!

Along the way, much has happened. The MLOps team has had to update for changes for new data, and respond to
changes in the distribution and relationships of the underlying data. None of this has been done in siloes,
but in active participation with the marketing organization. The team has also grown familiar with the
operations of Azure Machine Learning, and learned how to leverage the system to hit a range of goals around
performance, data lineage, governance all while extensively using AutoML to simplify the training process.
Though this was an initial step, the team is now geared up to further expand the range of possible ML
solutions to target even more use cases around customer experience.

Through this example, we attempted to model concept and data drift discretely. In reality, these are not
mutually exclusive and a combination of concept and data drift may creep into production models. In this
example, we also treated the datasets as specific batches at various points in time. This simplified the
exercise, but in reality, one will have to decide on where to start and end batches of data for training,
whether to include the old data with newer batches, etc. Another important factor is the trade-off between
choosing features that may be high in accuracy, but volatile from a drift perspective and conversely, those
that are less predictive, but more stable over time, hence reducing the need to keep retraining. All this of
course, depends on the model, the standards for accuracy and the business use case.

We hope you've enjoyed this primer!
