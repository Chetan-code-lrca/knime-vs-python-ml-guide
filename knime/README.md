# Build the KNIME workflow: inventory-demand regression

This guide builds a visual workflow using the CSV and split labels shared with the Python example. It is a **build-along specification**, not a ready-to-import `.knwf` file yet. The workflow should be recreated, tested, and exported from the KNIME version used by a contributor before a serialized workflow is added here.

## Prerequisites

1. Install [KNIME Analytics Platform](https://www.knime.com/downloads).
2. Download or clone this repository.
3. Check that your installation includes the current KNIME Base Nodes and KNIME Ensemble Learning Wrappers nodes. Install the extension family if the regression learner/predictor is unavailable.
4. Keep `data/inventory_demand.csv` in a known location.

Node names and extension packaging can vary across versions. Prefer the non-deprecated/current node variant shown in the Node Repository and verify the node description in your installation.

## What you are building

```mermaid
flowchart TD
    A[CSV Reader] --> B[Row Filter: split = train]
    A --> C[Row Filter: split = test]
    B --> D[Column Filter: exclude IDs and split metadata]
    D --> E[Missing Value: learn replacements on train]
    E --> F[Random Forest Learner: Regression]
    E -. transformation PMML .-> G[Missing Value (Apply)]
    C --> H[Column Filter: exclude IDs and split metadata]
    H --> G
    F --> I[Random Forest Predictor: Regression]
    G --> I
    I --> J[Numeric Scorer]
```

The target `demand_next_week` must be retained in the training data for the learner and in the test data for scoring. It must not be treated as an input feature.

## Step 1 — Read the CSV

1. Create a new workflow.
2. Add **CSV Reader**.
3. Browse to `data/inventory_demand.csv`.
4. Configure the delimiter and header row if they are not detected automatically.
5. Execute the node and inspect the output table.

Expected data size: **3,120 rows**. Your output should contain a column named `split` with values `train` and `test`.

## Step 2 — Separate the pre-defined train and test periods

Create two branches from the reader:

- **Training branch:** use **Row Filter** to keep rows where `split` equals `train`.
- **Test branch:** use another **Row Filter** to keep rows where `split` equals `test`.

Expected row counts: 2,490 training rows and 630 test rows.

Do not make a new random split in KNIME. The provided chronological split is intentional and is also used by the Python code.

## Step 3 — Remove columns that are not model inputs

On both branches, remove these columns from the learner/predictor input:

- `week_start`
- `week_index`
- `store_id`
- `split`

Keep `demand_next_week` in both branches. The learner needs it as the target; the scorer needs it as the observed reference value.

The model input features should be:

- `region`
- `store_format`
- `product_category`
- `price_next_week`
- `discount_pct_next_week`
- `promotion_next_week`
- `holiday_next_week`
- `forecast_month`
- `previous_week_units`
- `avg_4_week_units`

## Step 4 — Learn missing-value replacements on training data

1. Add the current **Missing Value** node to the training branch.
2. Choose appropriate handling for numeric and nominal columns. For example, use a central-value strategy for numeric features and a most-frequent strategy for nominal features.
3. Do not remove rows just because a feature is missing. The target is complete in this dataset.
4. Execute the node.
5. Inspect its output ports. The current PMML-capable node provides transformed data and a PMML transformation describing the replacement rules.

Connect the transformed training table to the learner in the next step.

## Step 5 — Apply the same replacements to test data

1. Add **Missing Value (Apply)**.
2. Connect the PMML transformation output from the training **Missing Value** node to the PMML input of **Missing Value (Apply)**.
3. Connect the test table to its data input.
4. Execute it and inspect the resulting test table.

This is important: do not calculate a new median or most-frequent category from the test rows. The test set must not influence fitted preprocessing values.

## Step 6 — Train a Random Forest regressor

1. Add **Random Forest Learner (Regression)** (the modern/current variant).
2. Connect the transformed training table.
3. Set `demand_next_week` as the target column.
4. Select the ten model input features listed above as training attributes.
5. Use a static seed if the node offers one, and record the value.
6. Start with a modest number of trees (for example, 250) if your installed node exposes this setting. Record the parameters actually available in your version.
7. Execute the learner and inspect the output model port.

Random Forest regression can work with nominal and numeric columns in the current KNIME tree-ensemble implementation. This differs from the Python example, which explicitly one-hot encodes categories before calling scikit-learn.

## Step 7 — Predict on the test data

1. Add **Random Forest Predictor (Regression)**.
2. Connect the model output from the learner to the predictor's model input.
3. Connect the transformed test data to the predictor's data input.
4. Execute the node.
5. Inspect the prediction column appended to the test data.

## Step 8 — Evaluate

1. Add **Numeric Scorer**.
2. Select `demand_next_week` as the reference column.
3. Select the prediction column created by the predictor as the predicted column.
4. Execute and inspect MAE, RMSE, and R².

Write down the metrics and model settings so the result can be compared with `python python/train_model.py`.

## What should be similar, and what may differ?

**Should be the same:** CSV, target, train/test rows, intended input columns, task type, and metric definitions.

**May differ:** internal category representation, implementation details, hyperparameter defaults, supported parameter ranges, random-number implementation, and software versions. Therefore, exact metric equality is not expected.

## Optional visual extensions

After you reproduce the baseline:

- Add a view comparing observed and predicted demand.
- Inspect residuals (`actual - predicted`).
- Build a branch that excludes recent-demand features.
- Try a second learner and score both models on the same test rows.
- Package a reusable part of the flow as a component.
- Explore calling a Python script from a workflow for a custom operation.

## Useful references

- [KNIME nodes and workflows](https://docs.knime.com/build/nodes-workflows/)
- [KNIME Python integration](https://docs.knime.com/ap/latest/python_installation_guide/)
- [Missing Value node](https://nodepit.com/node/org.knime.base.node.preproc.pmml.missingval.compute.MissingValueHandlerNodeFactory)
- [Missing Value (Apply) node](https://nodepit.com/node/org.knime.base.node.preproc.pmml.missingval.apply.MissingValueApplyNodeFactory)
- [Random Forest Learner (Regression)](https://nodepit.com/node/org.knime.base.node.mine.treeensemble2.node.randomforest.learner.regression.RandomForestRegressionLearnerNodeFactory)
- [Random Forest Predictor (Regression)](https://nodepit.com/node/org.knime.base.node.mine.treeensemble2.node.randomforest.predictor.regression.RandomForestRegressionPredictorNodeFactory)
- [Numeric Scorer](https://nodepit.com/node/org.knime.base.node.mine.scorer.numeric2.NumericScorer2NodeFactory)
