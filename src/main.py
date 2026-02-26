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
from src.data.load import load_raw_data
from src.features.preprocess import basic_cleaning
from src.features.preprocess import split_target

def main():
    df = load_raw_data("LC_loans_granting_model_dataset.csv")
    df = basic_cleaning(df)

    X,y = split_target(df, target_column="loan_status")

    print("X shape:", X.shape)
    print("y shape:", y.shape)

if __name__ == "__main__":
    main()