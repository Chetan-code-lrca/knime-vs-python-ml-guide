# Learning path: from zero to choosing the right tool

This path is designed for someone who has heard of KNIME, Python, and machine learning but is unsure how they fit together.

## Level 0 — Understand the three layers

Before opening a tool, separate these ideas:

1. **Problem:** What decision or prediction are we trying to support?
2. **Method:** What data-science or ML approach is appropriate?
3. **Tool:** Which environment helps us implement, inspect, automate, and maintain it?

A tool does not choose a sound method for you automatically. A visual workflow can be wrong, and a program can be wrong.

## Level 1 — Learn the KNIME mental model

Read [KNIME in 10 minutes](knime-in-10-minutes.md).

Be able to explain:
- A node is a task or operation.
- A port is an input or output connection point.
- A workflow is a connected sequence of operations.
- A node must be configured and executed before its output is ready.
- A visible workflow helps people inspect the sequence of transformations.

Exercise: load a CSV, inspect it, remove an irrelevant column, group or filter rows, and write the result.

## Level 2 — Learn the Python mental model

Read [Python in 10 minutes](python-in-10-minutes.md).

Be able to explain:
- Python is the language; pandas and scikit-learn are libraries.
- A DataFrame is a labelled, table-like data structure.
- A function or estimator performs a specific operation.
- A scikit-learn `Pipeline` chains preprocessing and an estimator.
- Code can be tested, versioned, reused, packaged, and integrated into software.

Exercise: load the same CSV, inspect missing values, select features, and calculate descriptive statistics.

## Level 3 — Understand the ML workflow

Read [ML workflow concepts](ml-workflow-concepts.md) before training a model. Know the difference between features and target, training and testing, regression and classification, and evaluation metrics.

Exercise: write down the target, allowed inputs, split strategy, baseline, and evaluation metric before opening the learner node or calling `.fit()`.

## Level 4 — Build the same case study twice

Follow the [inventory-demand case study](../tutorials/01-inventory-demand-case-study.md):

1. Run the Python script and inspect its output.
2. Build the KNIME flow using the instructions in [`../knime/README.md`](../knime/README.md).
3. Compare the workflow structure and the outputs.
4. Explain any differences without assuming that one result proves a tool is superior.

## Level 5 — Choose by use case

Use the [decision guide](decision-guide.md). Then try one of these extensions:

- Repeat the workflow with a linear regression model.
- Remove the recent-demand features and observe the score change.
- Use a different train/test time window.
- Add a data-quality report before training.
- Use KNIME's Python integration for one custom step.
- Build a small FastAPI service around the Python model.

## Self-check

You are ready to move on when you can answer these without looking them up:

- Why is KNIME not a programming language?
- Why is Python not itself a machine-learning algorithm?
- Why does the test set need to remain unseen during preprocessing decisions?
- Why should a model be compared with a baseline?
- Why might two correct implementations produce slightly different metrics?
- What makes a task a good fit for a visual workflow?
- What makes a task a good fit for a code-first implementation?
