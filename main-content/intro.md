# Welcome
Welcome to the MLOps primer! 

This is a miniature training guide to better understand Machine Learning operations (or "MLOps") with a focus
on concept and data drift, all within Azure Machine Learning.

MLOps can often be relegated to "better automation for machine learning". This is somewhat true, since
DevOps practices and automation are foundational for MLOps workflows. But a critical part of keeping
a model healthy or "in production" is focusing on processes around concept and data drift. 

To a business user, this can feel a foreign concept. However, it essentially asks: "*how is the data changing from the original
assumptions that trained the model""*?

In practice, there are no "one size fit all" best practices (at least, not yet). However, being responsive to
changes is half the battle. And this iterative learning approach can lead to processes and practices that
sustain ML models in production and continue to serve key business outcomes.

## The Structure
To illustrate these concepts, we have spun a fictional narrative that looks at a telecommunication company
(PFS Corporation) looking to predict customer churn. We then try to simulate different batches of data from
the original dataset to illustrate concepts around **concept drift** and **data drift**. Along the way, we
highlight capabilities in Azure Machine Learning that support these ideas and practices. As in real life,
there is no one way to address changes in the underlying data. More often than not, this exposes the
joint responsibility of the MLOps team working in partnership with the business and their data scientists to keep
models healthy and productive. 

## Disclaimers
- Behind this Jupyter notebook sits a working deployment that can be accessed
  [here](https://github.com/ts-azure-services/mlops-primer). The goal is to ensure individuals can follow
  along and reproduce similar results. While much development nowadays is notebook-driven, this is biased towards use
  of the Python SDK through scripts.
- Given the focus on Azure Machine Learning, as product capabilities mature, we will look to update this to
  reflect updates. **This content is relevant as of Feb 2022.**
