## Section 1 — Exact Inference Contract

Inference is the moment when a trained machine learning model stops learning and starts using what it has already learned to make predictions on new unseen data.

In this project, the inference contract defines:
- what input data inference accepts
- which artifacts inference requires
- what processing steps inference applies
- what outputs inference returns
- what inference is not allowed to do

The first version of inference will consume a raw CSV file path containing new observations to score.

Inference will require:
- a saved trained model artifact
- a saved fitted preprocessor artifact

The inference workflow will follow this order:
1. load raw input data
2. apply deterministic preprocessing
3. transform the processed data with the saved fitted preprocessor
4. generate predicted probabilities
5. convert probabilities into predicted classes using a threshold

The deterministic preprocessing layer must remain consistent with training. That means inference must reuse the same deterministic preprocessing functions that were applied before fitting the training preprocessor.

The first version of inference should return prediction outputs containing at least:
- `default_probability`
- `predicted_default`

If an `id` column exists in the input, it should be preserved in the output.

Threshold behavior should remain configurable. If no threshold is passed explicitly, inference should use the project default threshold.

This first version of inference is local and package-level. It is not yet an API or deployment layer.

Inference must not:
- retrain the model
- refit the preprocessor
- split train/test
- require the target column
- call the full training pipeline
