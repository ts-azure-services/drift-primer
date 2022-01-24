# Model Deployment
XYZ Corporation requires a real-time endpoint to profile new customers as they come in. This provides the
marketing/GTM team an opportunity to assess if there are ways to ensure these customers are more successful,
and retain better. They are aware of multiple methods to deploy a model (a local deployment, through Azure ML clusters,
with Azure Kubernetes Service (AKS), managed endpoints and ACI. Given the need to move fast and manage as
minimal infrastucture as possible, they are interested in leveraging ACI.

- Requirements to deploy a model:
	- A registered model
	- A software environment
	- A scoring script
	- A deployment configuration
	- RESTFUL interface
- Online vs. Batch scoring. In this case, we would like a live endpoint as part of our application roll-out
  that can immediately classify the "potential for churn" among the customers signing up to the service.
- Deploy using managed online endpoint or an AKS cluster?
- If you need the blue/green deployment, or A/B testing later, might need AKS.
- If you want to promote the managed online endpoint better, use that (given v2 focus)
- Briefly evaluate if you need to deploy through the inferencing in AML, and what other options exist
  (packaging as a Docker container, Flask app etc.)

## Specify an inference configuration 
```python
from azureml.core.model import InferenceConfig
from azureml.core.environment import Environment, CondaDependencies

env = Environment.from_pip_requirements(name="onnxruntime_env", file_path='./model_requirements.txt')
env.register(workspace=ws)

inference_config = InferenceConfig(environment=env, source_directory='./source_dir', entry_script='./score_real.py')
```

## Specify a deployment configuration
```python
from azureml.core.webservice import AciWebservice
deployment_config = AciWebservice.deploy_configuration(
    cpu_cores=1, memory_gb=1, auth_enabled=True
)
```

## Deploy the service and retrieve the REST endpoint
```python
service = Model.deploy(
    ws,
    "myservice",
    [model],
    inference_config,
    deployment_config,
    overwrite=True,
)
service.wait_for_deployment(show_output=True)
```
