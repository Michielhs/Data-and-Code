import pandas as pd

# Load the CSV file into a Pandas DataFrame
original_data = pd.read_csv('Input data/experimental_data_flip_a_coin.csv')

# Filter the DataFrame based on the 'BinaryChoice' column
filtered_df = original_data[original_data['BinaryChoice'] == 'SM vs. RAND']

# Further filter the DataFrame based on the 'Period' column (values 1 to 12)
filtered_df = filtered_df[(filtered_df['Period'] >= 1) & (filtered_df['Period'] <= 12)]

# Define columns to clean
columns_to_clean = ['GroupDecisionVote', 'GroupDecisionRule', 'vote', 'VotesInFavour']

# Clean each column
for column in columns_to_clean:
    filtered_df[column] = ""
