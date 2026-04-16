After building in the previous phase the two feature-layer files:

- `src/features/preprocessor.py` -> python file responsible for building the fit-ready preprocessor object
- `src/features/preprocess.py` -> python file responsible for deterministic transformations and target splitting

we can now start building `src/pipeline/train_pipeline.py`.

This file should orchestrate the full flow as described below:

1. load raw data
2. apply deterministic transformations
3. split target
4. drop excluded columns
5. split train/test
6. identify numeric and categorical columns from `X_train`
7. build preprocessor
8. fit preprocessor on `X_train`
9. transform `X_train` and `X_test`
10. return or pass the result to the next modeling step

As previously established, this file functions primarily as an orchestrator.

Its role is to define the execution flow rather than implement the detailed logic itself.

To maintain a clean separation of concerns, this file coordinates calls to other modules and should not contain manual implementations such as:
- imputation logic
- encoding logic
- deterministic feature engineering logic
- model-specific training logic

In alignment with the previous workflow, the script performs automated feature inspection on `X_train`.

It extracts:
- `numeric_features`
- `categorical_features`

These two lists are required to configure and build the fit-ready preprocessor object.

To enable this orchestration, the script connects several project layers together:

- data layer
- feature engineering layer
- preprocessing layer
- modeling layer later

So the orchestrator imports:
- `train_test_split` from scikit-learn
- internal project modules such as:
  - `RANDOM_STATE`
  - raw data loader
  - deterministic feature engineering functions
  - `build_preprocessor`

For now, we only need one main function to act as the entry point:

- `run_training_pipeline()`

This function runs the full flow from raw data to clean transformed features.

At this stage, it handles everything up to preprocessing only.

Later, we can extend the flow by connecting model training after this step.

The function should return a package containing:

- transformed `X_train` and `X_test`
- `y_train` and `y_test`
- fitted preprocessor

This keeps the design modular, meaning the model can be changed later without rewriting all the preprocessing logic.

At the top of the file, we can also define simple constants such as:

- `TARGET_COLUMN = "default"`
- `COLUMNS_TO_DROP = ["id", "title", "desc", "zip_code"]`
- `RAW_DATA_FILENAME = "LC_loans_granting_model_dataset.csv"`
- `TEST_SIZE = 0.2`

**Important note:** after ColumnTransformer, transformed outputs may not remain pandas DataFrames. They can become NumPy arrays or sparse matrices depending on the transformers used.