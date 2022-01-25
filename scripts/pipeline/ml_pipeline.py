"""Main pipeline script"""
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../..')))
from scripts.authentication.service_principal import ws
from azureml.core import Dataset#, ScriptRunConfig, Environment
from azureml.core.experiment import Experiment
from azureml.core.compute import ComputeTarget
from azureml.core.runconfig import RunConfiguration, DEFAULT_CPU_IMAGE, DockerConfiguration
from azureml.core.conda_dependencies import CondaDependencies
from azureml.pipeline.core import Pipeline, PipelineData, TrainingOutput
from azureml.pipeline.core.graph import PipelineParameter
from azureml.pipeline.steps import PythonScriptStep
from azureml.data import OutputFileDatasetConfig
from azureml.train.automl import AutoMLConfig
from azureml.pipeline.steps import AutoMLStep

def file_in_place(filename=None, parent_file=None):
    """Check for existence of a file and retain it"""
    if os.path.isfile(filename) is False:
        return_value = os.system("cp " + str(parent_file) + " " + str(filename))
    else:
        return_value = 0
    
    # Output value
    if return_value == 0:
        print("Operation completed successfully.")
    else:
        print("Operation failed.")


def file_delete(filename=None):
    """Check for existence of a file and delete it"""
    if os.path.isfile(filename) is True:
        return_value = os.system("rm " + str(filename))
    else:
        return_value = 0
    
    # Output value
    if return_value == 0:
        print("Operation completed successfully.")
    else:
        print("Operation failed.")

def setup_environment():
    """Setup environment for pipeline"""
    ## Set up resources and run configuration
    compute_target = ComputeTarget(workspace=ws, name='cpu-cluster')
    docker_config = DockerConfiguration(use_docker=True)
    run_config = RunConfiguration()
    run_config.environment.docker.base_image = DEFAULT_CPU_IMAGE
    run_config.docker = docker_config
    run_config.environment.python.user_managed_dependencies = False
    run_config.environment.python.conda_dependencies = CondaDependencies.create(conda_packages=['pandas', 'pip','python-dotenv'])
    return run_config, compute_target
    #run_config.environment.python.conda_dependencies = CondaDependencies.add_pip_package(['dotenv'])

def main():

    # Create the sample credentials in the root (for pipeline operation)
    # First time, will create it
    file_in_place(filename='sample.env', parent_file='variables.env')
    def_blob_store = ws.get_default_datastore()

    # Setup environment
    run_config, compute_target = setup_environment()

    # Pipeline step 1: Create a train/test split
    #def_blob_store = ws.get_default_datastore()
    ds = Dataset.get_by_name(workspace=ws, name='Baseline Dataset')
    train_df_source = OutputFileDatasetConfig(destination=(def_blob_store,'/prep1/')).as_mount()
    train_df_filename = 'step1output'
    train_test_step = PythonScriptStep(
        name="Create a train/test split",
        source_directory=".",
        script_name="./scripts/pipeline/train_test_split.py",
        compute_target=compute_target,
        arguments=[
            #"--input_file_path", ds.as_named_input('starting_input').as_mount(), #file
            "--input_file_path", ds.as_named_input('baseline_raw_input'), #tabular, will pass the Tabular ID
            "--output_file_path", train_df_source,
            "--output_filename", train_df_filename
            ],
        runconfig=run_config,
        allow_reuse=False
        )


    # Pipeline step 2: Transform and register dataset
    train_df_transformed_source = OutputFileDatasetConfig(destination=(def_blob_store,'/prep2/')).as_mount()
    train_df_transformed_filename = 'step2output'
    transform_step = PythonScriptStep(
        name="Transform Data",
        source_directory=".",
        script_name="./scripts/pipeline/transform.py",
        compute_target=compute_target,
        arguments=[
            "--input_file_path", train_df_source.as_input(),
            "--input_filename", train_df_filename,
            "--output_file_path", train_df_transformed_source,
            "--output_filename", train_df_transformed_filename
            ],
        runconfig=run_config,
        allow_reuse=False
        )

    ## Pipeline step 3: Train the model
    # Ensure that when you run the read_delimited_files it does not absorb more files than needed
    prepped_data = train_df_transformed_source.read_delimited_files()

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
        "experiment_timeout_hours": 1,
        "compute_target":compute_target,
        "max_concurrent_iterations": 4,
        #"verbosity": logging.INFO,
        "training_data":prepped_data.as_input(),
        "label_column_name":'Churn',
        "n_cross_validations": 5,
        "enable_voting_ensemble":True,
        "enable_early_stopping": False,
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
            allow_reuse=True
        )

    # Pipeline step # 4: Register the model
    model_name = PipelineParameter("model_name", default_value="bestModel")
    register_model_step = PythonScriptStep(
        name="Register the Best Model",
        source_directory=".",
        script_name="./scripts/pipeline/register_model.py",
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
    pipeline = Pipeline(ws, [
        train_test_step, 
        transform_step, 
        train_step, 
        register_model_step
        ])
    remote_run = experiment.submit(pipeline, show_output=True, wait_post_processing=True)
    remote_run.wait_for_completion()

    file_delete(filename='sample.env')

    ## Retrieve model and metrics
    #metrics_output_port = remote_run.get_pipeline_output('metrics_output')
    #model_output_port = remote_run.get_pipeline_output('model_output')
    #metrics_output_port.download('.', show_progress=True)
    #model_output_port.download('.', show_progress=True)

if __name__ == "__main__":
    main()
