[![deploy-book](https://github.com/ts-azure-services/mlops-primer/actions/workflows/book.yml/badge.svg)](https://github.com/ts-azure-services/mlops-primer/actions/workflows/book.yml)

# mlops-primer
- Goal: Educate on MLOps workflows/processes in Azure Machine Learning.
- Live Jupyter book link: [here](https://ts-azure-services.github.io/mlops-primer/intro.html)
- Leverages 'customer churn' as the general theme to illustrate the MLOps process in AML. This is not intended
  to be the best practice recommendation for how to predict customer churn using Microsoft products and
  services.


## Installation Instructions
- The general workflow to run the scripts is captured in the Makefile. Need to have the Azure CLI installed,
  with the `ml` extension. For more details, refer <xx>.
- In the `mlops-primer` root, create a `sub.env` file with `SUB_ID=<your subscription id>`.
- Create a virtualized environment, e.g. `conda create --name mlops-primer python=3.7`.
- While you can install the python dependencies as per the `requirements.txt file`, a more step-by-step
  approach is to install progressively as the scripts are run. Generally, that workflow is shown below:
	- `pip install python-dotenv` (for environment variables)
	- `pip install azureml-core` (for installing the base SDK of Azure ML)
	- `pip install azureml-dataset-runtime` (particularly needed before running the upload of datasets)
	- `pip install pandas` (needed before creating the simulated datasets)
	- `pip install azureml.pipeline` (needed before triggering the `ml_pipeline.py` script)
	- `pip install azureml.datadrift` (before triggering the data drift monitor)

