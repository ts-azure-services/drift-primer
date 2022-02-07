# Welcome
Welcome to the MLOps primer! 

This is a miniature training guide to better understand Machine Learning operations (or "MLOps") with a focus
on concept and data drift, all within Azure Machine Learning.

MLOps can often be relegated to just "better automation for machine learning". This is partly true, since
DevOps practices and automation are foundational practices in MLOps workflows. But a critical part of keeping
a model healthy or "in production" is focusing on practices around concept and data drift. To a business user,
this can feel a foreign concept. However, it essentially asks: "how is the data changing from the original
assumptions that trained your model?

In practice, there are no one size fit all best practices (at least, not yet). However, being aware is half the
battle. And this awareness can lead to processes and practices that allow models to continue to stay healthy
and serve key business outcomes.

To illustrate these concepts, we have created a fictional narrative that looks at a telecommunication company
(PFS Corporation) that is looking to predict customer churn. We then try to simulate data changes from the
original dataset to illustrate concepts around 'concept drift' and 'data drift'. Along the way, we highlight
capabilities in Azure Machine Learning that ease the transitions and implementations around these key decision
points. As in real life, there is no one way to address changes in the underlying data. More often than not,
this exposes the responsibliity of the MLOps team working in partnership with the business and their data
scientists to keep models healthy and productive. 

## Disclaimers
- Behind this Jupyter notebook sits a working deployment that can be accessed
  [here](https://github.com/ts-azure-services/mlops-primer). The goal is to ensure individuals can follow
  along and reproduce the same results. While much development is notebook-driven, this is biased towards use
  of the Python SDK, and with python scripts.
- Given the focus on Azure Machine Learning, as product capabilities mature, we will look to update this to
  reflect updates.
- This content is relevant as of Jan 2022.
