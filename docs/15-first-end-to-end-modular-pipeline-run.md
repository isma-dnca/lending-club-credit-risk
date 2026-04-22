# First successful end-to-end run of the modular pipeline
At this point, after finishing the refactoring of the `main.py` file by building project modular pipeline structure instead of monolithic script, i run the project end-to-end using : 
```bash
 python -m src.main
```
This is an important step milestone, because it is the first time that the whole project as **new modular architecture** worked successfully from end-to-end as one connected system.

After this run the project architecture became a real working pipeline. 
here is the full output of the previous command : 
```bash
(lending-club-ml) PS C:\Users\Utilisateur\\..\\lending-club-credit-risk> python -m src.main
[CLEANING] shape before: (1347681, 15), shape after: (1347681, 15)
[LightGBM] [Info] Number of positive: 215399, number of negative: 862745
[LightGBM] [Info] Auto-choosing row-wise multi-threading, the overhead of testing was 0.033102 seconds.
You can set `force_row_wise=true` to remove the overhead.
And if memory is not enough, you can set `force_col_wise=true`.
[LightGBM] [Info] Total Bins 1748
[LightGBM] [Info] Number of data points in the train set: 1078144, number of used features: 79
[LightGBM] [Info] [binary:BoostFromScore]: pavg=0.199787 -> initscore=-1.387627
[LightGBM] [Info] Start training from score -1.387627
C:\Users\Utilisateur\miniconda3\envs\lending-club-ml\Lib\site-packages\sklearn\utils\validation.py:2691: UserWarning: X does not have valid feature names, but LGBMClassifier was fitted with feature names
warnings.warn(
Training pipeline executed successfully.
Model saved to:
C:\Users\Utilisateur\\...\\ML\lending-club-credit-risk\outputs\models\lightgbm_model.joblib
Preprocessor saved to:
C:\Users\Utilisateur\\...\\ML\lending-club-credit-risk\outputs\preprocessors\preprocessor.joblib
Metrics saved to:
C:\Users\Utilisateur\\...\\ML\lending-club-credit-risk\outputs\reports\metrics.json
ROC-AUC: 0.6803
Recall: 0.0194
Precision: 0.5668
```

## What was actually executed during this run
According to the order and the orchestrate of the `main.py` file. The refactored `main.py` lunches the full modular architecture flow in this order: 
    1. load raw data
    2. apply deterministic transformations
    3. split features and target
    4. split train/test
    5. identify numerical and categorical columns
    6. build and fit the preprocessor on `X_train`
    7. transform `X_train` and `X_test`
    8. train the LightGBM model
    9. evaluate the trained model
    10. save the model, fitted preprocessor and metrics
So this execution validated that all the modules can work together successfully and in correct way.

## Modules that worked together
This execution confirmed the integration of the following modules :
    - `src/main`
    - `src/pipeline/train_pipeline.py`
    - `src/features/preprocess.py`
    - `src/features/preprocessor.py`
    - `src/modeling/preprocessor.py`
    - `src/modeling/train.py`
    - `src/modeling/evaluate.py`
    - `src/persistence/save_artifacts.py`
Before the project is relying on monolithic script. Now is more operational by relying on modular structure.

## Console output recap 
The run completed successfully and printed the following key messages:
```bash
    - cleaning step executed successfully
    - LightGBM training started and completed
    - the full training pipeline executed successfully
    - model was saved
    - preprocessor was saved
    - metrics were saved
```


Saved outputs:
```bash
    - model saved to: outputs/models/lightgbm_model.joblib
    - preprocessor saved to: outputs/preprocessors/preprocessor.joblib
    - metrics saved to: outputs/reports/metrics.json
```
This confirms that the artifact-saving layer is working correctly. 

## Evaluation results from our first successful run :
```bash
ROC-AUC: 0.6803
Recall: 0.0194
Precision: 0.5668
```
First thing first f those results validate that thr project has modular processing, modular training, modular evaluation, artifact saving, and an executable entry point.
Second this is the prediction behavior; Is not yet ideal for the business objective.
``Recall = 0.0194`` is still very low at ``threshold = 0.5``, which means that our current model situation is not flagging enough risky case; defaulters clients. It is too conservative when predicting defaults.Even that ``AUC: 0.6803`` shows clearly that the model has signal.
So the pipeline works technically, but the decision threshold is not yet aligned with the real objective of credit risk detection.

## Final recap 
The first successful end-to-end run proves that the new modular pipeline architecture is now operational.

The project can now:

preprocess data safely, train a model through separated modules, evaluate model behavior, save the trained artifacts, run through a clean main.py entry point.