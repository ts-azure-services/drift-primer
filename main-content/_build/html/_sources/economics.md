# Solution Costs
Prioritizing machine learning projects is a function of impact and cost. Through this illustrative example,
you can see the projected costs based on the actual resources deployed and used as part of this exercise.
![cost_analysis](./imgs/cost-analysis.jpg)

## Key Observations
1. The estimated cost for an end-to-end solution from training to real-time inferencing is approximately $500
   per month. Rationalizing this cost involves comparing it against the impact of the customer efforts to
   minimize churn and improve retention. If the cost of acquiring a net new customer is presumably in hundreds
   of thousands as per the initial estimate in the beginning, the cost of maintaining this solution will
   likely provide an **ROI of +10x**. **However, do note that this is highly variable depending upon usage
   patterns in each organization. For example, having multiple individuals working on different parts of the
   solution may require multiple copies of the data, the resources, etc.**
2. The bulk of the cost is in keeping live VMs operational to serve the real-time endpoints. The cost of
   training and storage of datasets is trivial by comparison. However, note that this estimate assumes
   **keeping all endpoints live** for the duration of the entire month. In practice, as one model gets
   promoted to production, we will take down older endpoints. For the illustration, we required all of them to
   be live to compare back and forth between them to understand prediction accuracy.
3. The compute cluster profile (as of the time of this example) is shown below:
   ![resource-profile](./imgs/resource-profile.jpg)

