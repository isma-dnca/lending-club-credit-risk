# This is the main.py file which is used to run the whole project. It is the entry point of the project.

#-01----------------------------------------------------------------------------

# This is the 1st entry point of the main.py file and it is used to test the data loading function.
# from src.data.load import load_raw_data

# def main(): 
#     df = load_raw_data("LC_loans_granting_model_dataset.csv")
#     print("Data loaded successfully.")
#     print("shape:", df.shape)

# if __name__ == "__main__":
#       main()

#-02-----------------------------------------------------------------------------

# This is the 2nd entry point of the main.py file and it is used to test the data loading function
# and the basic cleaning function.

# from src.data.load import load_raw_data
# from src.features.preprocess import basic_cleaning

# def main(): 
#     df = load_raw_data("LC_loans_granting_model_dataset.csv")
#     df = basic_cleaning(df)

#     print("shape after cleaning:", df.shape)

# if __name__ == "__main__":
#     main()


#-03-----------------------------------------------------------------------------

# This is the 3rd entry point of modifying the main.py file acording to the new changes in the
# preprocess.py file after creating the split_target function to check if the target_column exist
# in the DataFrame clumns or not. If it does not exist, it will raise a ValueError. if it exist, 
# it will split the DataFrame into features (X) and target (y).

# from src.data.load import load_raw_data
# from src.features.preprocess import basic_cleaning
# from src.features.preprocess import split_target

# def main():
#     df = load_raw_data("LC_loans_granting_model_dataset.csv")
#     df = basic_cleaning(df)

#     X,y = split_target(df, target_column="default")

#     print("X shape:", X.shape)
#     print("y shape:", y.shape)

#     # print ("_\nCOLUMNS_:")
#     # print(df.columns.tolist())

# if __name__ == "__main__":
#     main()


#-04-----------------------------------------------------------------------------
# This is the 4th entry point of modifying the main.py file in order to remove the
# `id` column as it meangless identifier and it does not provide any useful information for the model. It is just a unique identifier for each row in the dataset.
# also we are going to remove the `title` and `desc` columns as they are raw text (we are not doing NLP) and they are not useful for the model.

from src.data.load import load_raw_data
from src.features.preprocess import basic_cleaning
from src.features.preprocess import split_target
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


import pandas as pd


def main():
    df = load_raw_data("LC_loans_granting_model_dataset.csv")
    ## STEP 1: Basic cleaning and Sampling to reduce the size to control the environment
    df = basic_cleaning(df)
    df = df.sample(n=200000, random_state=42)

    ## STEP 2: Split features and target : Never touch columns before splitting the features
    ##  and target because if we drop any column before splitting the features and target, 
    ## we may drop the target column by mistake and it will cause an error in the split_target function
    ##  as it will not find the target column in the DataFrame columns.
    ##  So we need to split the features and target first and then we can drop any column from the
    ##  features (X) without affecting the target (y). X= features only, y=target only.
    X,y = split_target(df, target_column="default")

    ## STEP 3: Drop unuseful columns. We are going to drop the `id` column as it is a meaningless
    ##  identifier and it does not provide any useful information for the model. It is just a unique
    ##  identifier for each row in the dataset so it is pure noise. We are also going to drop the `title` and `desc` columns
    ##  as they are raw text (we are not doing NLP) and high cardinality text explodes memory and also `zip_code`
    ##  as it is a categorical feature with high cardinality (a lot of unique values) and it is not useful
    ##  for my situation due to memory constraints of my machine. In a real-world scenario,
    ##  we can use techniques like target encoding or frequency encoding to encode the `zip_code` column
    ##  instead of dropping it, but for this project, we are going to drop it to control the environment
    ##  and avoid memory issues.
    columns_to_drop = ["id", "title", "desc","zip_code"]
    X = X.drop(columns=columns_to_drop)

    ## STEP 4: **EDA and Preprocessing.** Before we start preporocessing the data, we need to do some EDA 
    ## to understand the data and the features. We are going to check the number of categorical features 
    ## and the cardinality of the categorical  features to understand the data and choose the appropriate 
    ## encoding technique for the categorical features. We are also going to check the shape of the features 
    ## (X) and the target (y) to understand the data and choose the appropriate preprocessing technique 
    ## for the features and the target. This an important step to anwer the question: "if I encode this, 
    # how many columns will I have after encoding?" and "will I have memory issues if I encode this 
    # feature? This is important to control the environment and avoid memory issues in my machine as the
    # dataset is quite large relative to the RAM of my machine.
    print("\nCategorical cardinality:")
    for col in X.select_dtypes(include=["object"]).columns:
        print(col, ":", X[col].nunique())
    
    print ("Raw X shape:", X.shape)

    cat_cols = X.select_dtypes(include=["object"]).columns
    print("Number of categoorical (fetures) columns:", len(cat_cols))

    print("\nCategorical cardinality:")
    for col in cat_cols:
        print(col, ":" , X[col].unique())
        

    ## STEP 5: **Split the data into train and test sets**. We are going to split the data into train and
    ## test sets using the `train_test_split` function from scikit-learn. We are going to use 20% of the 
    ## data for testing and 80% of the data for training. We are also going to use stratified sampling to 
    ## ensure that the distribution of the target variable is the same in the train and test sets. This is 
    ## important to ensure that the model is trained on a representative sample of the data and it can 
    ## generalize well to unseen data. So we split before encoding to avoid data leakage and ensure that 
    ## the encoding is done only on the training data and then applied to the test data. 
    ## If we encode before splitting, we may have data leakage as the encoding will be done on the whole 
    ## dataset and it may leak information from the test set to the training set, which can lead to 
    ## overfitting and poor generalization of the model.
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    ## STEP 6: **Encoding and Alignment**. After splitting the data into train and test sets, we are going 
    ## to encode the categorical features using one-hot encoding as it is a simple and effective 
    ## encoding technique. We are going to use the `drop_first=True` parameter to avoid the dummy variable 
    ## trap. Alo align the columns of the train and test sets after encoding to ensure that they have 
    ## the same columns and the same order of columns. This is important to ensure that the model can be 
    ## trained on the training data and then applied to the test data without any issues. 
    ## If the columns of the train and test sets are not aligned, we may have issues when applying the 
    ## model to the test data as the model will expect the same columns in the test data as in the training 
    ## data, and if they are not aligned, it may cause errors or unexpected results when applying the model 
    ## to the test data.

    ### 1) **Encode**. We are going to encode teh categorical features using one-hot
    ###  encoding as it is a simple and effective encoding technique for categorical 
    ### features. We are going to use the `drop_first=True` parameter t avoid the dummy
    ### variable trap, which is a situation where the dummy variables are highly correlated
    ### and it can cause multicollinearity issues in the model. By dropping the first 
    ### category dummy variable, we can avoid the dummy variable trap and reduce the 
    ### multicollinearity issues in the model.
    X_train = pd.get_dummies(X_train, drop_first=True)
    X_test = pd.get_dummies(X_test, drop_first=True)

    ### 2) **Align**. This is important beacuse after encoding the number of columns
    ### in the train dataset and the test dataset may be different due to the
    ### presence of different categories in the categorical features in the train
    ### dataset and the test dataset. So we need to align the columns of the train
    ### dataset and the test dataset and fill the missing columns with 0.
    X_train, X_test = X_train.align(X_test, join="left", axis=1, fill_value=0)

    print("Encoded shape:", X_train.shape)

    print("Remaining object columns:",
      X_train.select_dtypes(include=["object"]).shape[1])
   
    ## STEP 7: **Convert data types & Memory Management Control**. Due to memory issues,
    ## I'm converting the data type of the features to float32 instead of float64. 
    ## This will reduce the memory usage of the features by half, which is important for my
    ## machine as it has limited memory,and the dataset is quite large relative to the RAM of my machine.

    ### 3) **Convert data types**. Due to memory issues, I'm converting the data type
    ### of the features to float32 instead of float64. This will reduce
    ### the memory usage of the features by half, which is important for my machine
    ### as it has limited memory, and the dataset is quite large relative to the ram of my machine.
    X_train = X_train.astype("float32")
    X_test = X_test.astype("float32")


    ## STEP 8: **Choose the right solver**. I'm going to use the `solver='saga'` parameter in the 
    ## Logistic Regression model. The 'saga' solver is suitable for large datasets and can handle
    ## both L1 and L2 regularization. It is also faster than other solvers for large datasets. 
    model = LogisticRegression(
        max_iter=1000, # Increase the maximum number of iterations to ensure convergence, especially for large datasets.
        solver='saga', # saga is a good choice for large datasets and it can handle both L1 and L2 regularization. It is also faster than other solvers for large datasets.
        n_jobs=-1 # n_jobs=-1 mean to use all the avilable CPU cores to speed up the training process.
        )
    # model.fit(X_train, y_train)


    print("X shape:", X.shape)
    print("y shape:", y.shape)

    # print(X_train.dtypes)


if __name__ == "__main__":
    main()
