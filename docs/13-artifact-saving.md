# Artifact Saving in ML Pipeline (Model, Preprocessor, Metrics)

## Purpose of the file

`src/persistence/save_artifacts.py` is a module responsible for saving everything during training so it can be reused later.
As we all know, training is useless if we cannot reproduce the exact same behavior in production. so this file ensure us to use again what we trained again in production without redoing all computation that will may not be coherent and inconsistent.
this module save three things so far : 
    - the trained model
    - the fitted preprocessor
    - the metrics evaluation
  
## Saving artifacts
A trained model is not enough. The model is trained in transformed data, and not raw input! That transformation has performed by the preprocessor object that has learned parameters from the TRAINING DATA.

By saving **the preprocessor** we can transform new unseen data correctly which same transformation logic, then the model receives consistent input and the most important; predictions are reliable. that's why saving artifacts is critical for decision logic, transformation logic, and performance record.

## Training and production must follow the exact same transformation logic.
the module, file `src/persistence/save_artifacts.py` contains three functions so far, follows the same structure
    - Convert the path to Path object
    - Ensure the directory exits
    - And save the object
This structure helps us to avoid any path errors, missing folder issues and duplicated logic
so we save :
**- the model :** 
```python 
            def save_model(model, output_path): 
```

**- the preprocessor :** 
```python 
            def save_preprocessor(preprocessor, output_path): 
```
This is critical because the preprocessor contains learned parameters such as:
    median values for missing data
    category mappings for encoding
    feature ordering
    column transformations
The preprocessor is not just cleaning logic, but it is a fitted object that remembers how training data was transformed.
So in production, we must apply:
```python 
            preprocessor.transform(new_data) 
```
before calling:
```python 
            model.predict(...) 
```
So to reproduce the training conditions, we must save the preprocessor

**- the metrics :** 
```python 
            def save_metrics(metrics, output_path): 
```
Metrics are saved as JSON. This is different from model/preprocessor because:
    metrics are simple dictionaries
    no need for binary serialization
    JSON is human-readable
Also Metrics are not used for prediction like model and preprocessor, but we save them essentially for tracking the performance of our model, comparing experiments and for document results if needed.


## Training pipeline flow &  Production transformation logic
Typical flow for the training pipeline :
                        load data
                        ↓
                        clean / preprocess (fit on X_train)
                        ↓
                        train model
                        ↓
                        evaluate model
                        ↓
                        save artifacts
At the end of this steps we should have `model.pkl`, `preprocessor.pkl`, and `metrics.json`

This can be used and applied in production as follow :
                        raw input
                        ↓
                        load preprocessor
                        ↓
                        preprocessor.transform(raw input)
                        ↓
                        load model
                        ↓
                        model.predict(transformed input)
