# Common machine-learning task types

The first question is not “Which algorithm should I click?” It is “What kind of output or pattern does the problem require?”

| Task | What it does | Example question | Typical output |
|---|---|---|---|
| Regression | Predicts a numeric quantity | How many units may be demanded next week? | A number, such as 125 units |
| Classification | Predicts a category or class | Will a transaction be fraudulent? | A class label, sometimes with probabilities |
| Clustering | Groups observations by similarity without a supplied target label | Which customer groups have similar behavior? | Cluster assignments or group descriptions |
| Anomaly detection | Identifies observations that differ substantially from expected patterns | Which sensor readings look unusual? | Anomaly scores or flags |
| Association analysis | Finds items or events that frequently occur together | Which products tend to be purchased together? | Rules or co-occurrence patterns |
| Forecasting | Predicts future values using time-ordered information | What will weekly demand be next month? | Future values or ranges over time |

Forecasting can be treated as a regression problem in some setups, but the time ordering changes how data should be split and which features are valid.

## What changes between KNIME and Python?

Both environments can support many of these task types. The algorithms, nodes, library integrations, and available extensions differ. Before selecting a specific KNIME node or Python estimator, check that it supports the task and the data types you have.

## Quick examples

- **KNIME:** use visual workflows to prepare a table, apply a learner, generate predictions, and inspect evaluation outputs.
- **Python:** use pandas for data preparation and appropriate scikit-learn estimators for classical ML; use specialized libraries for deep learning and other advanced tasks.

A task label does not automatically determine the best tool. Data size, constraints, maintainability, deployment, and team experience still matter.
