# The Business Scenario
PFS Corporation is a telecommunications provider that provides cellular and internet services for US
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

## Key Goals
- Leverage the above narrative to work through successive stages of model evaluation and improvement.
- Explore concepts around both **concept drift** and **data drift**.
- Build an intuition for MLOps processes and considerations with the Azure Machine Learning platform.
- Ensure success for future ML projects by investing in the right tools, processes and roles.

## Key Assumptions
- **Key Technologies Used.** In these examples, Azure Machine Learning is the platform used to cycle through
  the MLOps process. We have not deployed any specific CI/CD methodologies, though this is highly recommended.
  For the inference endpoints, we have used managed real-time endpoints in Azure Machine Learning.
- **Establishing ground truth.** For this business problem, establishing ground truth can be tricky due to
  two reasons: one, a delayed feedback loop (how soon you can establish whether a customer has churned or not)
  and two, customers marked as 'Churned' could come back to the service. In reality, the former is likely the
  more critical variable to account for. Certain heuristics like "a customer is churned if they have not used
  their account for 30 days" may be a helpful guide, but customers churn in shorter timeframes and sometimes,
  with better clues (e.g. support tickets, negative feedback reviews, etc.). For the ensuing
  examples, we abstract away these realities and assume that ground truth for the target variable is already
  established on the `Retrain Dataset`, the `Concept Dataset` and the `Data Drift Dataset`.
- **Survivorship Bias.** One of the training attributes in the baseline dataset relates to how long the
  customer has been with the service. While this attribute has a decent variability among the customers in the
  source data, it is assumed that this is a fairly representative population of both churned and non-churned
  customers. If this were not true, or more specifically if it biased towards an active base of customers,
  this would not reflect a good population of churned customers and their characteristics. Figuring out what
  sample to include can be challenging. One approach would be to randomly pick all customers who signed up for
  the service in a specific period of time to get a random population of those who may stay or leave (churn).
  This needs to be applied with discretion, accounting for seasonal effects as well. For the purpose of this
  exercise, we assume the datasets are adequately screened for survivorship bias.
