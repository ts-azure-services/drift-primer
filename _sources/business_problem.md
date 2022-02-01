# The Business Scenario
"XYZ Corporation" is a telecommunications provider that provides cellular and internet services for US
consumers. Being in a tough, competitive market, they are interested in learning how to improve customer
satisfaction and improve retention. 

As the company continues to improve its analytics and data science practices, they are interested in
understanding how to better adopt an MLOps centric approach. They have seen from companies in other
industries, and increasingly among their competitors, mature data science practices that leverage cloud scale
and repeatable and reproducible software practices. This is particularly important as they would like to
improve the rate of experimentation on new data initiatives and see more projects succeed to production.

In the pursuit of customer retention, a first step is to analyze churn. While many hypotheses exist why churn
is prevalent, as short-term and long-term mitigations evolve, the marketing team wants a model to help
identify in real-time customers who are high potentials for churn. Using this, they have a variety of
campaigns they are looking to run as short-term mitigations. As the ballpark math has shown, even an
improvement of 1-5% of customer retention would mean millions of dollars in revenue.

It is worth noting that while the model will seek to predict customers who may churn, the ultimate goal is to
improve retention by understanding the factors that lead to churn. Prediction of churn is not a business goal
in and of itself, but minimizing it at a reasonable cost is.


## Key Goals
- Consider a simple business scenario through several evolutions of the dataset to explore concepts around
  deployment, devops, model and data drift.
- Build an intuition for MLOps processes and considerations with the Azure Machine Learning platform.
- Ensure success for future ML projects by investing in the right tools, processes and roles.

## Key Assumptions
- Technologies in use:
	- For Machine Learning (training, deployment): Azure Machine Learning.
	- For CI/CD, deployment of scripts: Github Actions.
- Deployment: Real-time endpoint, using Azure Container Instances.
- Mention what ground truth is here. And how fast it comes through other data engineering efforts.
- How is churn defined?
