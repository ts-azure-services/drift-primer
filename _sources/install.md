# Next Steps
If you'd like to get started with reproducing some of these insights where getting versed with Azure Machine
Learning, do follow the installation steps below, and learn more at the <repo>.

## Installation Steps
**Pre-requisites:** You need to have the Azure CLI installed, with the `ml` extension installed.

1. Create a virtualized environment and activate it.
![create_virtual_env](./imgs/install_gifs/create_virtual_env.gif)

2. Install the required python dependencies into this environment. With the included Makefile, once you are in
   the virtualized environment, you can run `make install`.
![make_install](./imgs/install_gifs/make_install.gif)

- **Note:** While you can install the python dependencies as per the `requirements.txt file`, a more
  step-by-step approach is to install progressively as the scripts are run. Generally, that workflow is shown
  below:
	- `pip install python-dotenv` (for environment variables)
	- `pip install azureml-core` (for installing the base SDK of Azure ML)
	- `pip install azureml-dataset-runtime` (particularly needed before running the upload of datasets)
	- `pip install pandas` (needed before creating the simulated datasets)
	- `pip install azureml.pipeline` (needed before triggering the `ml_pipeline.py` script)
	- `pip install azureml.datadrift` (before triggering the data drift monitor)

3. Ensure you have an environment variable file called `sub.env` in your root, with the Azure subscription you
   are using listed in the file as `SUB_ID=<your subscription>`.
![sub_env](./imgs/install_gifs/sub_env_file.png)

4. Run `make setup_run`. This will trigger the creation of the basic Azure Machine Learning setup, followed by
   creation of the cluster, and uploading of the original raw dataset.
![make_setup_run](./imgs/install_gifs/make_setup_run.gif)

5. Create the initial training pipeline run with `make create_pipeline`.

6. To train any of the retrain, data drift or concept drift scenarios, use the following commands:
	- For re-training, `make trigger_retrain`.
	- For data drift, `make trigger_ddrift`.
	- For concept drift, `make trigger_cdrift`.
