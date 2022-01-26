# Model Training
With the increasing use of AutoML, the training phase is often the easiest to work through and operationalize.
For this purpose, we will be taking advantage of Azure ML's AutoML solution to classify this dataset and
predict churn. 

## Top Features 
As a part of AutoML's process, the final "VotingEnsemble" model will also produce an "explanations" run to
highlight a number of aspects, including which features were most predictive of the target variable, i.e.
Churn. The results are shown below.
![top_features](./imgs/top_features.jpg)

## Key Metrics

### ROC curve
![roc_curve](./imgs/ROC.jpg)


## Create a pipeline
Creating a pipeline is particularly helpful to standardize the process to repeat when new data flows in. As
we'll see with the first event (a few months in), we will leverage this same pipeline to produce a new model.

- Insist on using a pipeline that can be re-used later for training.
	- Highlight the difference between the initial script to create the pipeline.
	- And the script to run an existing pipeline.
- Specifically highlight versioning, data registration capabilities to show lineage.

https://github.com/ts-azure-services/aml-automl-pipeline

![training_process](./imgs/training_process.jpg)

- Another way to trigger a model can be using Functions.
