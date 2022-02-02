# The Business Scenario
"XYZ Corporation" is a telecommunications provider that provides cellular and internet services for US
consumers. Being in a tough, competitive market, they are interested in learning how to improve customer
satisfaction and improve retention. 

As the company continues to improve its analytics and data science practices, they are interested in
understanding how to better adopt an MLOps centric approach. They have seen from companies in other
industries, and increasingly among their competitors, mature data science practices that leverage cloud scale
and repeatable and reproducible software practices. This is particularly important as they look to improve the
rate of experimentation on new data initiatives and see more projects succeed through to production.

To address customer retention, a first step is to analyze churn. While many internal hypotheses exist why
churn is prevalent, as short-term and long-term mitigations evolve, the marketing team wants a model to help
identify in real-time customers who are high potentials for churn. Using this, they have a variety of
campaigns they are looking to run as short-term mitigations. As the ballpark math has shown, even an
improvement of 1-5% of customer retention suggests millions of dollars in terms of customer lifetime value.

The business also recognizes that while the model will seek to predict customers who may churn, the ultimate
goal is to improve retention. As a first step, they would like through this effort to understand the most
predictive factors of churn, and build up the marketing muscle and culture to respond, and as appropriate
mitigate at a reasonable cost.

## Key Goals of this exercise
- Leverage the above narrative to work through successive stages of model evaluation and improvement.
- Explore concepts around both **concept drift** and **data drift**.
- Build an intuition for MLOps processes and considerations with the Azure Machine Learning platform.
- Ensure success for future ML projects by investing in the right tools, processes and roles.

## Key Assumptions
- Technologies in use:
	- For Machine Learning (training, deployment): Azure Machine Learning.
	- For CI/CD, deployment of scripts: Github Actions.
- Deployment: Managed real-time endpoints, through Azure Machine Learning.
- 'Churn' can be a tricky target variable because it is at a point in time (for example, some customers
  identified as churned may come back), and it is a delayed classification exercise (establishing the 'ground
  truth' requires a certain period of evaluation to pass, or a definition to be in place, e.g. if the customer
  does not use the services for more than 30 days, they are churned). For the purpose of the ensuing examples,
  we will assume that churn is definitively defined, and marked on the datasets being used. In reality,
  establishing the 'ground truth' will come down to working with the business and taking a call on how best to
  define this.
