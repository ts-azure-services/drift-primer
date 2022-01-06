# Model Deployment
- Four models of deployment exist: local, K8S, managed endpoints, ACI, and Azure ML clusters.
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

```python
import numpy as np
import pandas as pd

df = pd.read_csv('blah.csv')
```
