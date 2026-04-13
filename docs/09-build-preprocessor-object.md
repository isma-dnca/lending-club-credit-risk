So what I am doing right now is building `src/features/preprocessor.py`.

This python file has one mission only: build the fitted preprocessor object.


So in order to create it, the step-by-step questioning approach is the one I will use here.

What is happening logically to create the foundation of this object?

The first thing I ask is:

What kind of columns will enter this preprocessor?

The answer is:
- numeric columns
- categorical columns
    ```python
        (numeric_features, categorical features)
    ```
     : Those Two LISTS another part of the pipeline will create them and pass them in for the preprocessor object I am building right now. I will create soon another python file train_pipeline.py in which will figure out which are numeric and categorical features and then `train_pipeline.py` will call `build_preprocessor`
 
So immediately I know that this python file needs two branches.
The second question must be logically related to the previous answer:
What should happen to numeric columns?

In my project, numeric columns may contain missing values, so numeric preprocessing must be able to handle missing values when they are present.

There are many strategies for this, so the real question becomes:
which strategy should I choose here?

The answer is:
- `median`

That means the numeric branch will contain:
- a numeric pipeline
- an imputer with median strategy
```python
  numeric_pipeline = Pipeline(
      steps = [
          ("impute",SimpleImputer(strategy = "median")),
      ]
  )
```


Then I move to the next logical step after the numeric branch, which is the categorical branch.
The question here is:
What should happen to categorical columns?

The answer is that categorical columns need:
- missing value handling
- encoding

But this is not only because the model cannot read raw category strings.

The more complete understanding is this:

- categorical columns may contain missing values
- categorical values must be converted into numeric representation
- the category structure must be learned from training data

That is exactly why encoding belongs inside the fitted preprocessor.

So the categorical branch needs two things:
- fill missing categories
- encode categories
```python
  categorical_pipeline = Pieline(
      steps = [
          ("impute",SimpleImputer(strategy = "constant", fill_value = "missing")),
          ("encode",OneHotEncoder(uknown_value = "ignore")),
      ]
  )
```

Same road of logical steps again:
after defining the two branches, another question comes naturally:

How do I combine those two branches?

Because I am building ONE object that must say:
- these columns follow the numeric path
- those columns follow the categorical path

In other words, the whole logic of the python file I am creating is to build this structure:

- numeric pipeline
- categorical pipeline
- both combined into one global preprocessor

So now the structure is clear: 
```python
  preprocessor = ColumnTransformer (
      transformers [
          ("num", numeric_pipeline, numeric_features),
          ("cat", categorical_pipeline, categorical_features),
      ]
  )
```


After that, I can decide the function design.

I need ONE function that:
- receives `numeric_features`
- receives `categorical_features`
- returns ONE preprocessing object
  ```python
    def build_preprocessor (numeric_features, categorical_features):
        ...
        ...
        return preprpcessor
  ```

This is a good and professional design because:
- the file stays reusable
- the training pipeline decides which columns are numeric and which are categorical
- this module only builds preprocessing structure

That is clean separation.

After designing the function, the next logical step is to choose the tools inside the python file.

For this case, the building blocks are:

- `Pipeline`
- `ColumnTransformer`
- `SimpleImputer`
- `OneHotEncoder`

That is the toolbox: 
```python
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.preprocesing import OneHotEncoder
    from sklearn.compose import ColumnTransformer
```


Till now, everything sounds clear theoretically, but the real world is never perfectly aligned with theory.
So if test data or future unseen data contains unexpected categories, I need the encoder to behave safely.
That means the encoding choice must be made in a way that avoids fragile behavior that could crash the pipeline.

    ```python
        ("encode",OneHotEncoder(unknown_value = "ignore"))
    ```
This is an important detail that must always stay in mind while building this kind of object.

So finally, the file must have this shape:

1. imports
2. function definition
3. numeric pipeline
4. categorical pipeline
5. combined preprocessor
6. return the full object

## Small notices before coding

### 1. Numeric columns do not “need missing value” by definition

A more accurate way to say it is:

- numeric columns may contain missing values
- therefore numeric preprocessing must handle missing values when they exist

This sounds like a small correction, but it matters because not every numeric column is missing by default.

The real point is that the numeric branch must be ready to handle missing numeric values if they are present.

### 2. The categorical branch is not only because the model cannot read strings

That is true, but it is not the full story.

A more complete understanding is this:

- categorical columns may contain missing values
- categorical values must be converted into numeric representation
- the category structure must be learned from training data

That last point is very important.

Before encoding categories, the encoder first needs to learn what categories exist in `X_train`.

That is exactly why encoding belongs inside the fitted preprocessor.

So categorical preprocessing is not only about converting text into numbers.

It is also about learning the category structure from training data and then reusing that same structure later on test data and future unseen data.

### 3. The preprocessor builder does not create a fitted object yet

Another important correction:

this file does **not** create a fitted preprocessor.

What it does is:

- build a **fit-ready** preprocessor object

The object becomes **fitted later**, when the training pipeline applies `fit` on `X_train`.

This distinction is very important, because it helps me separate responsibilities clearly:

- `preprocessor.py` builds the object
- `train_pipeline.py` fits the object

So the role of this file is only to define the preprocessing structure, not to learn from data yet.

That learning step comes later in the training pipeline.

## Building

### Step A: Imports

For this step, first things first: import the tools already available that are needed only to build the preprocessing object.

So I need:
- pipeline building
- column transformer
- imputer
- encoder

### Step B: Function definition

One function that does the job:
- accept numeric and categorical column lists
- create the two branches
- combine them
- return the full object

### Step C: Numeric branch

This branch is for handling missing values in numeric columns using the median strategy.

No fitting here.
Just define the numeric pipeline.

### Step D: Categorical branch

This branch is for:
- filling missing values
- encoding categories

That is all.

No fitting, no saving.
Just defining the categorical pipeline.

### Step E: Combine those two branches

In order to make the file reusable and build one fit-ready preprocessor object, I need to create one object that combines:

- numeric pipeline
- categorical pipeline

This is the step where both branches become one global preprocessing object.

### Step F: Return the object

At the end, I need to return the preprocessor object definition, ready to be fit later.

So for the whole previous steps:
- no fitting
- no mixing with model training
- only building the preprocessing object
- numeric and categorical logic clearly separated

So while building, I am always asking:

- am I building the object or accidentally fitting it?
- am I keeping this python file focused only on preprocessing?
- am I separating numeric and categorical logic clearly?

The file must follow this order:

- imports
- function `build_preprocessor`
- numeric pipeline
- categorical pipeline
- full preprocessor
- return preprocessor

for full code for this step : `src/features/preprocessor.py`