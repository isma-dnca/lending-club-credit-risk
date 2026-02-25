from src.data.load import load_raw_data

def main(): 
    df = load_raw_data("LC_loans_granting_model_dataset.csv")
    print("Data loaded successfully.")
    print("shape:", df.shape)

if __name__ == "__main__":
      main()