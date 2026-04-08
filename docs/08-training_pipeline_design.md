# Convert current script into reproducible training pipeline that saves fitted model, fitted preprocessor, and evaluation metrics

The goal for this Milestone is to move from a script that trains a model in one block into a clean and reproducible training pipeline.

So far, the logical stages that my script already contains are:
    - load raw data
    - basic cleaning
    - deterministic feature engineering
    - split features and target
    - split train / test
    - fit preprocessing on train only
    - transform train / test
    - train model
    - evaluate model
    - save artifacts
    - save metadata

Current state: my `src/main.py` mixes all of this together, and there is no explicit separation of each responsibility.

Target structure: make each logical stage become its own clear function or module, so that the training flow becomes easier to read, easier to maintain, and more professional.
So far, the most important methodological issue I’m facing here is leakage-safe preprocessing.
My first step here is to define the pipeline responsibilities.
The main goal of this step is to clarify the training flow that the repo should have.
------------------------

# Step 1 : Training flow

## Scope of Milestone 1
To avoid confusion and feature creep, this milestone is intentionally limited to:
    - one dataset: `data/raw/LC_loans_granting_model_dataset.csv`
    - one target: `default`
    - one model: LightGBM
    - one train/test split
    - no model comparison
    - no hyperparameter search
    - no text modeling (`title`, `desc` are excluded)
    - no experimental features during refactoring

The goal is not performance optimization.
The goal is to build a **reproducible, leakage-safe training pipeline**.
-----------------

## 1. `Load raw data`

    - Question: What file enters the pipeline?
The real question is: which file is accepted as the official input to the pipeline?
It is the original input file that the pipeline consumes before any transformation.
In this project:
    `data/raw/LC_loans_granting_model_dataset.csv`
This file is the starting point of the entire pipeline.
---------

## 2. `Apply deterministic feature engineering`

    - Question: What transformations do not need to learn from the dataset?
At this stage, I apply only transformations that do not compute or learn anything from the data.
These transformations:
    - do not require a fit step
    - do not compute statistics such as mean, median, or category levels
    - can be applied directly row by row

Examples in this project:
    - parsing `issue_d` into `issue_year` and `issue_month`
    - mapping `emp_length` into numeric form
    - creating ratio features from existing columns

These are deterministic transformations.
They are safe to apply before the train/test split.
------------

## 3. `Split features and target`
    - Question: Where do `X` and `y` get created?
At this stage, the dataset is separated into:
    - `y` -> target (`default`)
    - `X` -> input features

Then I explicitly define the modeling feature set.
From `X`, I remove:
    - `id` (identifier)
    - `title`, `desc` (text, excluded in this milestone)
    - `zip_code` (excluded for simplicity in this milestone)

This step ensures:
    - the target is isolated early
    - only relevant features are passed to the pipeline

This happens after deterministic transformations and before any learning step.
---------

## 4. `Train/test split`

    - Question: At what exact point does the split happen?
The split happens immediately after creating `X` and `y`, and before any transformation that learns from data.
Pipeline order:
    1. Load data  
    2. Deterministic transformations  
    3. Split into `X` and `y`  
    4. **Train/test split**

This acts as a **firewall**.
Before this point:
      - safe zone, because no learning has happened yet
After this point:
    - learning begins

---------

## 5. `Fit preprocessing on train only`

    - Question: Which transformations must be learned only from `X_train`?
All transformations that need to compute something from data must be fitted on `X_train` only.
These include:
    - missing value imputation
    - categorical encoding
    - any transformation based on data distribution
    - any preprocessing step that learns categories, statistics, or structure

These transformations require a fit step.
They must never use `X_test`.
This is the core rule that prevents data leakage.
-----------

## 6. `Transform train and test`

    - Question: How do you guarantee the same feature space?
Same feature space means:
    - same columns
    - same order
    - same encoding
    - same preprocessing logic

This is guaranteed by:
    - fitting one preprocessor on `X_train`
    - reusing the same fitted object on both `X_train` and `X_test`

Critical rule:
> `X_test` must never define new preprocessing structure.

The train set defines the transformation logic.  
The test set only follows it.
That is what makes the transformation reproducible and safe.
---------

## 7. `Train model`

    - Question: Which single model is trained?
The model trained for this milestone is:
**LightGBM**
This choice is based on previous experiments where it performed better than Logistic Regression.
The goal here is not comparison.
The goal is to build one clean and reproducible pipeline around one model.
-------

## 8. `Evaluate`

    - Question: Which metrics are computed and kept?

The model is evaluated using metrics adapted to classification and class imbalance.
Main metrics:
    - `ROC-AUC` -> primary metric for ranking performance
    - `Precision` -> quality of predicted defaults
    - `Recall` -> ability to detect defaults
    - `F1-score` -> balance between precision and recall

`Accuracy` may still be computed, but it is not treated as a reliable metric because of class imbalance.

Additional diagnostics:
    - confusion matrix
    - classification threshold used for prediction

For this milestone, the threshold can remain fixed at `0.5` in order to keep the pipeline simple and stable during the refactoring.
Threshold optimization belongs to a later milestone.
All metrics are computed on the test set.
---------

## 9. `Save artifacts`

    - Question: What is saved after training?

The pipeline saves all elements required to reuse the model without retraining.
Artifacts:
    - fitted preprocessing pipeline
    - trained LightGBM model
    - evaluation metrics file

Artifacts are stored in a dedicated output location, separate from raw data.
Without the preprocessor, the model is unusable.
So both the preprocessor and the model must always be saved together.
--------

## 10. `Save run metadata`

    - Question: What additional information is recorded?
Metadata describes how the model was trained.

It includes:

    - data information  
      (dataset path, number of samples, target)
    - train/test split configuration  
      (test size, random seed)
    - model configuration  
      (LightGBM parameters)
    - preprocessing configuration  
      (feature lists, strategies used)
    - evaluation setup  
      (metrics used, threshold)
    - run information  
      (timestamp, run ID)
    - code version  
      (git commit hash or project version)

Artifacts = what was produced  
Metadata = how it was produced

Both are required for reproducibility.
--------------------

## Final understanding of Step 1

The central rule of this pipeline is:
Deterministic transformations can happen before the split because they do not learn from data.
Any transformation that computes statistics, categories, or parameters must be fitted only on `X_train`.

This is what makes the pipeline:
    - leakage-safe
    - reproducible
    - reusable
    - maintainable

The purpose of this milestone is not just cleaner code.
It is to define a **professional training flow** where:
    - each step has one responsibility
    - the process is traceable
    - the outputs can be reused reliably
---------

## Next step
The next step is to classify all current transformations into:
    - deterministic feature engineering
    - train-fitted preprocessing

This will prepare the implementation of the full reproducible training pipeline.


# Step 2 - Classify current transformations into deterministic vs train-fitted preprocessing

After defining the pipeline responsibilities above, in Step 1, the next step is to classify the current transformations that already exist in `src/features/preprocess.py`.

The reason for doing this is simple:
before refactoring anything, I need to know clearly which transformations are safe to apply before the train/test split, and which ones must wait until after the split because they learn something from the data.

This step is important because not all preprocessing is the same.

Some transformations are just direct transformations.
They do not need to observe the full dataset to work.

Other transformations first need to compute something from the data, such as:
    - a median
    - a mean
    - a category list
    - an encoding structure
These transformations are different because they contain a learning step.

And once a transformation learns from data, it must be fitted only on `X_train`, never on the full dataset.

That is exactly the foundation of leakage-safe preprocessing.

---

## Current transformations found in `src/features/preprocess.py`

So far, the functions I have in this file are:
    - `basic_cleaning`
    - `split_target`
    - `engineer_issue_date_features`
    - `engineer_emp_length`
    - `handle_missing_values`
    - `engineer_ratio_features`
Now I classify them one by one.
------

## 1. `basic_cleaning`

This function does:
    - remove duplicate rows
    - strip whitespace from column names
    - convert column names to lowercase

This is a **deterministic transformation**.
Why?
Because it does not learn anything from the dataset.
It does not compute a statistic, does not discover categories, and does not depend on the train set to define how it should behave.
It just applies fixed rules.
So this transformation is safe to apply before the train/test split.
------
## 2. `engineer_issue_date_features`

This function transforms `issue_d` into:
    - `issue_year`
    - `issue_month`
and then removes the original `issue_d` column.
This is also a **deterministic transformation**.
Why?
Because each row is transformed directly from its own value.
The function does not need to look at other rows.
It does not learn any parameter from the dataset.
So this step is safe before the split.
--------

## 3. `engineer_emp_length`

This function maps values like:
    - `< 1 year`
    - `1 year`
    - `2 years`
    - ...
    - `10+ years`
into numeric values.
This is also a **deterministic transformation**.
Why?
Because the transformation uses a fixed mapping already defined in the code.
It does not compute anything from the dataset itself.
It just applies the same rule to each row.
So it is safe before the split.
---------------

## 4. `engineer_ratio_features`

This function creates new columns like:
    - `loan_to_revenue`
    - `loan_to_fico`
    - `revenue_to_fico`
This is also a **deterministic transformation**.
Why?
Because it creates new features directly from existing columns in the same row.
It does not need to observe the rest of the dataset, neither to learn a parameter from data or compute a global statistic.
This point is important for my own understanding:
creating a new feature does **not automatically mean** the transformation is learning from data.
A transformation becomes train-fitted only when it needs to compute something from the dataset first.
Here, ratio features are created row by row from already available values, so this remains deterministic.
So this step is safe before the split.
-----------------

## 5. `handle_missing_values`

This function does two things:
    - fills numeric missing values using the median
    - fills categorical missing values using `"missing"`
This function is **not fully deterministic**.
It belongs to **train-fitted preprocessing**.
Why?
Because the numeric imputation step computes the median from the data.
That means the function first needs to observe the dataset in order to learn the value it will use.
And once a transformation computes something from the data, it is no longer just a direct transformation. It becomes a learned preprocessing step.

This means:
    - it must not be fitted on the full dataset
    - it must be fitted on `X_train` only
    - then the same learned values must be reused to transform `X_test`

This is exactly why missing value handling is part of leakage-safe preprocessing.
Important note for myself:
even if a function looks simple, if it computes statistics like median, mean, or category levels, then it is already a learning transformation.
So `handle_missing_values` must happen **after** splitting.
More precisely:
it must be **fitted after the split on `X_train`**, then applied to both `X_train` and `X_test`.
--------

## 6. `split_target`

`split_target` is a special case.

It is **not really a transformation** in the same sense as the others.
It does not engineer features.
It does not clean data.
It does not learn from data.

Its role is simply to separate:
    - `X` = input features
    - `y` = target

So I should not force it into either category.
It is neither:
    - deterministic feature engineering
    - nor train-fitted preprocessing
It is better understood as a **structural pipeline step**.
Its role is to define the boundary between features and target before the train/test split.
----------

# Final classification

## Deterministic transformations

These can happen before the split because they do not learn anything from the dataset:
    - `basic_cleaning`
    - `engineer_issue_date_features`
    - `engineer_emp_length`
    - `engineer_ratio_features`

## Train-fitted preprocessing
These must be fitted on `X_train` only because they compute something from data:
    - `handle_missing_values`

## Structural pipeline step
This is not a transformation, but a separation step in the pipeline:
    - `split_target`
--------

## Final understanding of Step 2

At this point, the most important thing I understand is this:
not every preprocessing step is the same.
Some preprocessing steps are just fixed transformations.
These are safe before the split.
Other preprocessing steps first need to learn something from data.
These must be fitted only on `X_train`.
This is the exact reason why I cannot treat all preprocessing as one single block.

I now clearly see that in my current file:
    - most feature engineering steps are deterministic
    - `handle_missing_values` is already a learned preprocessing step
    - `split_target` is not a transformation, but a structural step in the pipeline

This classification gives me the foundation I need before refactoring the training pipeline.
It also helps me understand where the leakage risk really begins.
Before the split:
    - deterministic zone
After the split:
    - learning zone

That distinction is one of the most important foundations of a professional ML pipeline.

## Next step
The next step is to define what the fitted preprocessor must contain in the current project.

Now that I have classified the current transformations, I need to identify exactly which preprocessing steps belong inside the fitted preprocessor, because these are the steps that must be learned from `X_train` only and then reused on `X_test` without change.

This step will prepare the implementation of the full reproducible training pipeline.

----------------------------



## Step 3 - Define what the fitted preprocessor must contain

The goal of this step is to define what the fitted preprocessor object must contain.
In my understanding so far, it must contain all the transformations that learn from `X_train` only.
Deterministic transformations, as I identified in the previous steps, are not concerned with fitting because they do not learn anything from the dataset while transforming it.

So deterministic transformations stay outside the fitted preprocessor object:
        - `basic_cleaning`
        - `engineer_issue_date_features`
        - `engineer_emp_length`
        - `engineer_ratio_features`

While these belong inside the fitted preprocessor:
    - missing value handling
    - categorical encoding

because they learn something from data, or require a learned structure before transforming.
So this step is all about defining what goes inside the fitted preprocessor.
-----------------

### 3.1

As I already know, deterministic feature transformations stay outside the fitted preprocessor object.
But after those deterministic transformations, the structure of the columns changes.

Some original categorical columns may become numeric after transformation.
For example:
    - `issue_d` is transformed into `issue_year` and `issue_month`
    - `emp_length` is transformed into `emp_length_num`

So when I think about preprocessing, I should not think only about the raw columns.
I should think about the final columns that remain **after** deterministic transformations are applied.

At the end of this stage, I will always end up with two broad families of features:
    - numerical features
    - categorical features

This distinction matters a lot because preprocessing is usually different for each family.
From my project, the original columns are:

    - `id`
    - `issue_d`
    - `revenue`
    - `dti_n`
    - `loan_amnt`
    - `fico_n`
    - `experience_c`
    - `emp_length`
    - `purpose`
    - `home_ownership_n`
    - `addr_state`
    - `zip_code`
    - `default`
    - `title`
    - `desc`

Some columns are excluded from modeling:
        - `id`
        - `title`
        - `desc`
        - `zip_code`
The target column `default` is kept separate as `y`, so it is not part of the preprocessing input `X`.

After deterministic transformations:
    - `issue_d` becomes `issue_year` and `issue_month`
    - `emp_length` becomes `emp_length_num`
    - ratio features may also be added

So the fitted preprocessor must work on the final feature set after those transformations, and then split those features into:
    - numeric columns
    - categorical columns

At this stage, the important thing is not to memorize every final column perfectly, but to clearly understand that the preprocessor will have one branch for numeric features and one branch for categorical features.
--------------------------

### 3.2

For numeric columns, the fitted preprocessor must solve one main problem:
    - missing numeric values

If some numeric values are missing, the model cannot use them directly.
So the preprocessor must learn how to fill them.

In this project, the strategy is:
    - fill missing numeric values using the median learned from `X_train`

This is a learned transformation because the median must be computed from the training data first.
That means numeric imputation belongs inside the fitted preprocessor.
For this milestone, that is enough for numeric preprocessing.

I do not need to add scaling now, especially because the chosen model is LightGBM and the current goal is to keep the pipeline simple, correct, and reusable.
----------

### 3.3

My categorical columns have two problems that need to be solved before the model can use them.
The first problem is missing values.
Some rows have no category written in them, so I need a strategy to fill those gaps.

The second problem is that the model cannot read words.
It only understands numbers.
So I need to convert categories into numbers.
That operation is called encoding.

Now the important question is:
do these operations need to learn something from the data?
Yes, especially encoding.

Because before I can convert categories into numbers, I first need to know what categories exist.
And I can only know that by looking at the training data.
So encoding learns the category structure from `X_train`.
That means categorical preprocessing must be fitted on `X_train` only, and then the same learned rules are applied to `X_test` and future data.

So my fitted preprocessor, for categorical columns, must contain two things:
    - how to handle missing categories
    - how to convert categories into numbers

That is what categorical preprocessing means inside the fitted preprocessor.
------------

### 3.4
These transformations should stay outside the fitted preprocessor:
        - `basic_cleaning`
        - `engineer_issue_date_features`
        - `engineer_emp_length`
        - `engineer_ratio_features`

Because they are deterministic.
No learning is required for these transformations.
They do not compute statistics from the dataset.
They do not discover categories.

They just apply fixed transformation rules.
That is exactly why they stay outside the preprocessor object.
Inside the preprocessor, I only put what needs fitting or learned structure.
------------------------

### 3.5
The preprocessor is like a rulebook that was written by observing `X_train`, and that exact same rulebook must be used on every new piece of data after that.
This is a simple way to understand its role.

It learns the preprocessing rules once from the training data, then reuses them consistently everywhere else.
--------------

### 3.6

My fitted preprocessor in this project contains two branches.

The first branch handles numeric columns.
The only thing it needs to do here, for now, is fill missing numeric values using the median learned from `X_train`.

The second branch handles categorical columns.
It needs to do two things:
        - fill missing categories
        - convert those categories into numbers using the structure learned from `X_train`

That is all I need for now.
I am not trying to make it perfect or advanced
I just want it to be correct, leakage-safe, and reusable.
--------------------------

### 3.7

There are many things that must stay outside the preprocessor.

The preprocessor has one job only:
take `X`, learn how to prepare it from `X_train`, and apply those same learned rules everywhere else.
So things like these do not belong inside the preprocessor:
    - splitting the target
    - deterministic feature engineering
    - training the model
    - tuning thresholds
    - comparing models
    - saving artifacts
    - saving metadata
    - evaluation logic

Those are separate responsibilities that belong to other parts of the pipeline.
----------------------

## Final understanding of Step 3
The fitted preprocessor is responsible for these things:
        - learning how to fill missing numeric values
        - learning how to handle missing categorical values
        - learning how to encode categorical variables into numbers
        - applying all of that consistently to train, test, and future data

Everything else stays outside it:
        - cleaning
        - deterministic feature engineering
        - separating the target
        - training the model
        - evaluating the model
        - saving artifacts and metadata

Each of these steps has its own place in the pipeline.
So the main thing I understand now is this:
the fitted preprocessor is not “all preprocessing”.
It is only the part of preprocessing that must be learned from training data and then reused exactly the same way later.
That is what makes the pipeline professional, reusable, and leakage-safe.

