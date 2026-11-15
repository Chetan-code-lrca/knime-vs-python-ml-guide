# KNIME-to-Python mapping

The table maps common *tasks*, not identical APIs. A visual node and a Python function may differ in configuration, defaults, data representation, and execution semantics.

| Data-science task | KNIME approach | Python approach |
|---|---|---|
| Read CSV | CSV Reader | `pandas.read_csv()` |
| Inspect data | Table view, Statistics nodes, visualizations | `DataFrame.head()`, `.info()`, `.describe()` |
| Select columns | Column Filter | `frame[columns]` |
| Filter rows | Row Filter / Rule-based Row Filter | Boolean indexing or `.query()` |
| Handle missing values | Missing Value node; use its transformation output when applying learned replacements consistently | `SimpleImputer` in a scikit-learn pipeline |
| Encode categories | One to Many / category-aware learners | `OneHotEncoder`, `OrdinalEncoder` |
| Scale numeric data | Normalizer and related preprocessing nodes | `StandardScaler`, `MinMaxScaler` |
| Split data | Partitioning or filter on a pre-defined split column | `train_test_split()` or explicit filtering |
| Train a regression model | Random Forest Learner (Regression) | `RandomForestRegressor` |
| Generate predictions | Random Forest Predictor (Regression) | `pipeline.predict()` |
| Evaluate regression | Numeric Scorer | `mean_absolute_error`, `root_mean_squared_error` / `sqrt(mean_squared_error)`, `r2_score` |
| Reuse a sequence | Component / wrapped workflow | Function, class, module, package, or pipeline |
| Add custom logic | Components and supported scripting integrations | Python functions and libraries |

## Important differences

- KNIME is a workflow platform; Python is a language used through libraries and frameworks. The comparison is between ways of constructing a data workflow, not between equivalent products.
- A KNIME learner and scikit-learn estimator may implement the same model family but use different defaults and internal details.
- The Python example uses one-hot encoding for categorical values. The current KNIME Random Forest regression learner can work with nominal and numeric columns; the representations are therefore not identical.
- Use the same source data, target, split, and intended features for a meaningful learning comparison, but do not assume the metrics must match exactly.
- Node names, extension packaging, and interfaces can vary by KNIME release. Verify the node description in your installed version.

## A note about scaling

Do not add a scaling step just because a preprocessing checklist contains one. A random forest does not generally need standardization because tree splits depend on feature order/thresholds rather than comparable numeric magnitudes. Scaling can matter for algorithms such as k-nearest neighbours, support vector machines, and many linear or gradient-based methods.
