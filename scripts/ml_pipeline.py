# Import in data, do some processing and break up the file
#import logging
from authentication import ws
from azureml.core import Dataset, ScriptRunConfig, Environment
from azureml.core.experiment import Experiment
from azureml.core.compute import ComputeTarget
from azureml.core.runconfig import RunConfiguration, DEFAULT_CPU_IMAGE, DockerConfiguration
from azureml.core.conda_dependencies import CondaDependencies
from azureml.pipeline.core import Pipeline, PipelineData, TrainingOutput
from azureml.pipeline.core.graph import PipelineParameter
from azureml.pipeline.steps import PythonScriptStep
from azureml.data import OutputFileDatasetConfig, DataType#, OutputTabularDatasetConfig
from azureml.data.output_dataset_config import OutputTabularDatasetConfig
from azureml.data.data_reference import DataReference
from azureml.train.automl import AutoMLConfig
from azureml.train.automl.run import AutoMLRun
from azureml.automl.core.forecasting_parameters import ForecastingParameters
from azureml.automl.core.featurization.featurizationconfig import FeaturizationConfig
from azureml.pipeline.steps import AutoMLStep

## Set up resources and run configuration
compute_target = ComputeTarget(workspace=ws, name='cpu-cluster')
docker_config = DockerConfiguration(use_docker=True)
run_config = RunConfiguration()
run_config.environment.docker.base_image = DEFAULT_CPU_IMAGE
run_config.docker = docker_config
run_config.environment.python.user_managed_dependencies = False
run_config.environment.python.conda_dependencies = CondaDependencies.create(conda_packages=['pandas', 'pip','python-dotenv'])
#run_config.environment.python.conda_dependencies = CondaDependencies.add_pip_package(['dotenv'])

# Pipeline step 1: Transform dataset
def_blob_store = ws.get_default_datastore()
ds = Dataset.get_by_name(workspace=ws, name='Telco_Baseline')
intermediate_source = OutputFileDatasetConfig(destination=(def_blob_store,'/prep1/')).as_mount()
#intermediate_source = OutputTabularDatasetConfig(destination=(def_blob_store,'/prep1/')).as_mount()
intermediate_filename = 'step1output'
cleanup_step = PythonScriptStep(
    name="Transform data",
    source_directory=".",
    script_name="transform.py",
    compute_target=compute_target,
    arguments=[
        "--input_file_path", ds.as_named_input('starting_input').as_mount(),
        "--output_file_path", intermediate_source,
        "--filename", intermediate_filename
        ],
    runconfig=run_config,
    allow_reuse=False
    )

# Pipeline step 2: Register the transformed dataset
prepped_data = OutputFileDatasetConfig(destination=(def_blob_store,'/prep2/')).as_mount()
prepped_filename = 'step2output'
processed_step = PythonScriptStep(
    name="register_dataset",
    source_directory=".",
    script_name="register_dataset.py",
    compute_target=compute_target,
    arguments=[
        "--input_file_path", intermediate_source.as_input(),
        "--filename", intermediate_filename,
        "--output_file_path", prepped_data,
        "--output_filename", prepped_filename
        ],
    runconfig=run_config,
    allow_reuse=False
)

# Ensure that when you run the read_delimited_files it does not absorb more files than needed
prepped_data = prepped_data.read_delimited_files()
#prepped_data = prepped_data.read_delimited_files(set_column_types={"Place": DataType.to_float()})

metrics_data = PipelineData(
        name='metrics_data',
        datastore=def_blob_store,
        pipeline_output_name='metrics_output',
        training_output=TrainingOutput(type='Metrics')
        )

model_data = PipelineData(
        name='best_model_data',
        datastore=def_blob_store,
        pipeline_output_name='model_output',
        training_output=TrainingOutput(type='Model')
        )

# Setup the classifier
automl_settings = {
    "task": 'classification',
    "primary_metric":'AUC_weighted',
    "iteration_timeout_minutes": 10,
    "experiment_timeout_hours": 0.5,
    "compute_target":compute_target,
    "max_concurrent_iterations": 4,
    #"verbosity": logging.INFO,
    "training_data":prepped_data.as_input(),
    "label_column_name":'Churn',
    "n_cross_validations": 5,
    "enable_voting_ensemble":True,
    "enable_early_stopping": True,
    "model_explainability":True,
    #"enable_dnn":True,
        }

automl_config = AutoMLConfig(**automl_settings)

train_step = AutoMLStep(
        name='Churn Classification',
        automl_config=automl_config,
        passthru_automl_config=False,
        outputs=[metrics_data,model_data],
        enable_default_model_output=True,
        enable_default_metrics_output=True,
        allow_reuse=False
    )

# Register the model
model_name = PipelineParameter("model_name", default_value="bestModel")
register_model_step = PythonScriptStep(
        script_name="register_model.py",
        name="register_model",
        arguments=[
            "--model_name", model_name,
            "--model_path", model_data
            ],
        inputs=[model_data],
        compute_target=compute_target,
        runconfig=run_config,
        allow_reuse=False
        )

# Setup experiment and trigger run
experiment = Experiment(ws, name='baseline_scenario')
pipeline = Pipeline(ws, [cleanup_step, processed_step, train_step, register_model_step])
remote_run = experiment.submit(pipeline, show_output=True, wait_post_processing=True)
remote_run.wait_for_completion()

## Retrieve model and metrics
#metrics_output_port = remote_run.get_pipeline_output('metrics_output')
#model_output_port = remote_run.get_pipeline_output('model_output')
#metrics_output_port.download('.', show_progress=True)
#model_output_port.download('.', show_progress=True)
