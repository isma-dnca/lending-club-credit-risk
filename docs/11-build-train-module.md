The next step after building the orchestrator in the previous stage is to create the training module.

In the previous step, we created a file whose role was to connect the different pieces in the correct order.  
The document `10-build-train_pipeline-script.md` contains the details of that stage.

Now, in this step, I am going to create the file `src/modeling/train.py`.

Its responsibility should stay very focused:
- receive processed `X_train`
- receive `y_train`
- build a LightGBM model
- fit the model on the training data
- return the trained model

So the role of this file is simple: create the LightGBM model, train it on preprocessed training data, and return the trained model object.

By following the pipeline flow, the sequence now becomes:

<ol type="1">
    <li>preprocessing pipeline done</li>
    <li><strong>now build training model</strong></li>
    <li>then evaluation module</li>
    <li>then saving module</li>
    <li>then wire everything together in <code>main.py</code></li>
</ol>

The core of this training file is a function that assumes the input data is already clean and preprocessed, which is true because that step has already been completed earlier in the pipeline.

```python
def train_lightgbm_model(X_train, y_train):
```
Inside this function, we instantiate an ``LGBMClassifier``, fit it on the training data, and finally return the trained model.


So what `model.fit()` changes inside the object after training?

before `.fit()` the model is just a configured object or in simple word an empty object with some parameters like : `n_estimators` and `learning_rate`. But it has NO knowledge of data. a little brain with rules and without any knowledge or experience.

After `.fit()` the object is ***MUTATED***; the same object nut it contains learned information.
So after fit(), new attributes appears inside `model`. 
running
 ```python
         print(dir(model))
 ``` 
shows a lot of stuff like
- `model.booster_` : contains all trees, splits, decisions.
- `model.feature_importances_` : mportance of each feature that tells us what the model relied on
- `model.n_features_in_` : number of features seen during training
  For more inspection and details : `02-exp_lightgbm_model_state_before_after_fit.ipynb` file 

