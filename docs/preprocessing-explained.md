# Data preprocessing, explained

Preprocessing converts raw data into a form that is suitable for analysis or model training. It is not a fixed checklist: the right operations depend on the dataset, task, and algorithm.

## Common operations

| Operation | What it does | When it may be useful | Common mistake |
|---|---|---|---|
| Type correction | Converts values to the intended type | Dates stored as strings, numbers stored as text | Treating an identifier as a continuous number |
| Missing-value handling | Replaces or removes missing observations | Incomplete measurements or records | Imputing with test-set statistics |
| Duplicate checks | Finds repeated rows or entities | Data imported from several sources | Removing legitimate repeated events |
| Filtering | Keeps rows matching a condition | Excluding invalid records or selecting a cohort | Filtering based on information unavailable at prediction time |
| Encoding | Converts categorical values into model-compatible values | Categories such as region or product class | Treating arbitrary category IDs as meaningful numeric order |
| Scaling | Adjusts numeric feature ranges | Distance-based and many linear/gradient-based methods | Scaling when not needed, or fitting the scaler on all rows |
| Outlier review | Identifies unusual values | Data-entry errors or extreme observations | Automatically deleting rare but valid events |
| Feature engineering | Creates useful inputs from existing information | Ratios, lags, date parts, aggregates | Using future information or target-derived values |
| Feature selection | Removes inputs that add little or cause problems | Simplifying models and reducing noise | Selecting features after repeatedly checking the test score |

## The same ideas in both tools

- **KNIME:** nodes expose operations as configurable steps connected in a workflow.
- **Python:** libraries expose operations as functions, transformers, and estimators assembled in code.

The user must still make the same conceptual choices in either environment.

## How to handle missing values

Common approaches include:
- Remove rows or columns when justified by the data and task.
- Replace numeric values with a training-set median or another defensible statistic.
- Replace categorical values with the training-set most frequent category or an explicit unknown category.
- Use domain-specific methods when missingness has a meaningful interpretation.

A missing value may itself carry information. Before imputing, ask why the value is missing and whether the absence is random or systematic.

## When scaling matters

Scaling can materially affect models based on distances, dot products, or optimization across feature magnitudes. Examples include k-nearest neighbours, support vector machines, and many linear or neural-network training setups.

Tree-based models such as decision trees and random forests generally do not require standard scaling because split decisions are based on feature thresholds. Avoid preprocessing steps that are not needed for the selected method.

## The safe order

1. Define which records are eligible for the task.
2. Create the train/test or train/validation/test split using a strategy that matches the real use case.
3. Fit preprocessing choices on training data only.
4. Apply the fitted transformations to validation and test data.
5. Tune using training/validation data, then use the held-out test set for final evaluation.

See [data leakage](data-leakage.md) for examples.
