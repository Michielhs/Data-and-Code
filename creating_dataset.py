import pandas as pd
import openpyxl
import itertools
import numpy as np
import os
import re

# Load the CSV file into a Pandas DataFrame
data_input = 'Data results/GPT4/RUN5/RUN5.csv'
original_data = pd.read_csv(data_input)
data_df = original_data.copy()

# Ensure that the DataFrame is sorted appropriately if order within groups matters
data_df.sort_values(by=['session', 'Period', 'matching_group'], inplace=True)

# Apply a function to each group to assign the valuation values to the ValuationVector columns
def assign_valuation_vectors(group):
    valuations = group['Valuation'].tolist()  # Get all valuations in the group as a list
    for i, valuation in enumerate(valuations, start=1):
        group[f'ValuationVector{i}'] = valuation
    return group

# Clean 'reported_valuation' column: remove '=', letters, and curly braces '{}'
data_df['reported_valuation'] = data_df['reported_valuation'].astype(str)
data_df['reported_valuation'] = data_df['reported_valuation'].str.replace('=', '')
data_df['reported_valuation'] = data_df['reported_valuation'].str.replace('[a-zA-Z{}]', '', regex=True)

# Convert 'reported_valuation' to numeric, replacing non-numeric values with -10
data_df['reported_valuation'] = pd.to_numeric(data_df['reported_valuation'], errors='coerce').fillna(-10)

# Convert 'reported_valuation' to integers
data_df['reported_valuation'] = data_df['reported_valuation'].astype(int)

# Applying the function to each group
data_df = data_df.groupby(['session', 'Period', 'matching_group']).apply(assign_valuation_vectors)

# Reset the index if needed (apply can sometimes return a MultiIndex)
data_df.reset_index(drop=True, inplace=True)

# Sum the values of the three ValuationVector columns to create the SurplusGroup
data_df['SurplusGroup'] = data_df[['ValuationVector1', 'ValuationVector2', 'ValuationVector3']].sum(axis=1)

# Create 'EfficientChoice' column: 1 if SurplusGroup > 0, otherwise 0
data_df['EfficientChoice'] = (data_df['SurplusGroup'] > 0).astype(int)

# Initialize the column
data_df['efficient_mech_choice'] = 0

# Apply the conditions for efficiency using 'loc' for safer and more correct indexing
data_df.loc[(data_df['GroupDecisionVote'] == 'RAND') &
            (data_df['BinaryChoice'] == 'NSQ vs. RAND') &
            (data_df['treatment_number'].isin(['Robustness', 'Right-skewed'])),
            'efficient_mech_choice'] = 1

data_df.loc[(data_df['GroupDecisionVote'] == 'NSQ') &
            (data_df['BinaryChoice'] == "NSQ vs. RAND") &
            (data_df['treatment_number'] == 'Left-skewed'),
            'efficient_mech_choice'] = 1

data_df.loc[(data_df['GroupDecisionVote'] == 'SM') &
            (data_df['BinaryChoice'] != 'AGV vs. SM'),
            'efficient_mech_choice'] = 1

data_df.loc[(data_df['GroupDecisionVote'] == 'AGV'),
            'efficient_mech_choice'] = 1

# Apply the missing data condition using 'loc' for correct indexing
data_df.loc[(data_df['treatment_number'] == 'Symmetric') &
            (data_df['BinaryChoice'] == 'NSQ vs. RAND'),
            'efficient_mech_choice'] = np.nan

data_df['efficient'] = np.where(data_df['efficient_mech_choice'].isna(), 1, data_df['efficient_mech_choice'])


# set sum_reported_valuations
data_df['sum_reported_valuations'] = pd.NA  # Or data_df['column_name'] = None for older versions of Pandas
data_df['sum_reported_valuations'] = data_df.groupby(['session', 'Period', 'matching_group'])['reported_valuation'].transform('sum')

# Ensure the 'vote' column is of type string
data_df['vote'] = data_df['vote'].astype(str)

# Replace values in the 'vote' column
data_df['vote'] = data_df['vote'].replace({'1': 'Yes', '0': 'No'})


# set VotesInFavor
data_df['VotesInFavour'] = data_df[data_df['vote'] == 'Yes'].groupby(['session', 'Period', 'matching_group'])['vote'].transform('size')
data_df['VotesInFavour'] = data_df['VotesInFavour'].fillna(0).astype(int)

# Initialize the 'provision' column to 0 (assuming this is the default value)
data_df['provision'] = 0

data_df['sum_reported_valuations'] = pd.to_numeric(data_df['sum_reported_valuations'], errors='coerce')

# Set provision based on the GroupDecisionRule: SM
data_df.loc[(data_df['GroupDecisionRule'] == 'SM') & (data_df['VotesInFavour'] > 1), 'provision'] = 1

# Set provision based on the GroupDecisionRule: AGV
data_df.loc[(data_df['GroupDecisionRule'] == 'AGV') & (data_df['sum_reported_valuations'] > 0), 'provision'] = 1

# Set provision based on the GroupDecisionRule: RAND
data_df.loc[(data_df['GroupDecisionRule'] == 'RAND') & (data_df['Draw_random_provision'] == 1), 'provision'] = 1

# set valuation variables
data_df['dummy_valuation_negative'] = pd.NA  # Or data_df['column_name'] = None for older versions of Pandas
for index, row in data_df.iterrows():
    if data_df.at[index, 'Valuation'] < 0:
        data_df.at[index, 'dummy_valuation_negative'] = 'negative'
        data_df.at[index, 'valuation_positive'] = 0
        data_df.at[index, 'valuation_negative'] = 1
    elif data_df.at[index, 'Valuation'] > 0:
        data_df.at[index, 'dummy_valuation_negative'] = 'positive'
        data_df.at[index, 'valuation_positive'] = 1
        data_df.at[index, 'valuation_negative'] = 0
        data_df.at[index, 'positive'] = 1

# Multiply the 'efficient' column by the 'ex_ante_round' column
data_df['ex_ante_efficient'] = data_df['efficient'] * data_df['ex_ante_round']


# set chose variables
# Initialize all chose_* columns with NaN (empty)
data_df['chose_AGV'] = np.nan
data_df['chose_SM'] = np.nan
data_df['chose_RAND'] = np.nan
data_df['chose_NSQ'] = np.nan

# Define conditions checking if the respective rule is in Rule_1 or Rule_2
agv_in_rules = (data_df['Rule_1'] == 'AGV') | (data_df['Rule_2'] == 'AGV')
sm_in_rules = (data_df['Rule_1'] == 'SM') | (data_df['Rule_2'] == 'SM')
rand_in_rules = (data_df['Rule_1'] == 'RAND') | (data_df['Rule_2'] == 'RAND')
nsq_in_rules = (data_df['Rule_1'] == 'NSQ') | (data_df['Rule_2'] == 'NSQ')

# Populate the chose_AGV column
data_df.loc[agv_in_rules & (data_df['GroupDecisionVote'] == 'AGV'), 'chose_AGV'] = 1
data_df.loc[agv_in_rules & (data_df['GroupDecisionVote'] != 'AGV'), 'chose_AGV'] = 0

# Populate the chose_SM column
data_df.loc[sm_in_rules & (data_df['GroupDecisionVote'] == 'SM'), 'chose_SM'] = 1
data_df.loc[sm_in_rules & (data_df['GroupDecisionVote'] != 'SM'), 'chose_SM'] = 0

# Populate the chose_RAND column
data_df.loc[rand_in_rules & (data_df['GroupDecisionVote'] == 'RAND'), 'chose_RAND'] = 1
data_df.loc[rand_in_rules & (data_df['GroupDecisionVote'] != 'RAND'), 'chose_RAND'] = 0

# Populate the chose_NSQ column
data_df.loc[nsq_in_rules & (data_df['GroupDecisionVote'] == 'NSQ'), 'chose_NSQ'] = 1
data_df.loc[nsq_in_rules & (data_df['GroupDecisionVote'] != 'NSQ'), 'chose_NSQ'] = 0

# Generate HypotheticalResult for AGV as the same as EfficientChoice
data_df['HypotheticalResultAGV'] = data_df['EfficientChoice']

# Initialize HypotheticalResult for SM with NaN, then set based on conditions
data_df['HypotheticalResultSM'] = pd.NA

# Set HypotheticalResultSM to 1 where any two ValuationVectors are > 0
conditions_positive = (
    ((data_df['ValuationVector1'] > 0) & (data_df['ValuationVector2'] > 0)) |
    ((data_df['ValuationVector1'] > 0) & (data_df['ValuationVector3'] > 0)) |
    ((data_df['ValuationVector2'] > 0) & (data_df['ValuationVector3'] > 0))
)
data_df.loc[conditions_positive, 'HypotheticalResultSM'] = 1

# Set HypotheticalResultSM to 0 where any two ValuationVectors are < 0
conditions_negative = (
    ((data_df['ValuationVector1'] < 0) & (data_df['ValuationVector2'] < 0)) |
    ((data_df['ValuationVector1'] < 0) & (data_df['ValuationVector3'] < 0)) |
    ((data_df['ValuationVector2'] < 0) & (data_df['ValuationVector3'] < 0))
)
data_df.loc[conditions_negative, 'HypotheticalResultSM'] = 0

# Generate HypotheticalResult for SQ, which is always 0
data_df['HypotheticalResultSQ'] = 0

# Generate HypotheticalResult for RAND, which is always 0.5
data_df['HypotheticalResultRAND'] = 0.5

# Define a function to map GroupDecisionRule to the corresponding HypotheticalResult
def map_choice_result(row):
    if row['GroupDecisionVote'] == 'AGV':
        return row['HypotheticalResultAGV']
    elif row['GroupDecisionVote'] == 'SM':
        return row['HypotheticalResultSM']
    elif row['GroupDecisionVote'] == 'RAND':
        return row['HypotheticalResultRAND']
    elif row['GroupDecisionVote'] == 'NSQ':
        return row['HypotheticalResultSQ']
    else:
        return np.nan  # handle unexpected cases or errors

# Apply the function across the DataFrame
data_df['ChoiceResultSubject'] = data_df.apply(map_choice_result, axis=1)

# Initialize 'truth_telling' as NaN to denote emptiness
data_df['truth_telling'] = np.nan

# Filtering the DataFrame where GroupDecisionRule is 'AGV'
mask = data_df['GroupDecisionRule'] == 'AGV'

# Apply the np.where condition only within this filtered set
data_df.loc[mask, 'truth_telling'] = np.where(
    data_df.loc[mask, 'Valuation'] == data_df.loc[mask, 'reported_valuation'],
    1,
    0
)

# Initialize 'truth_telling_sign' as NaN to denote emptiness
data_df['truth_telling_sign'] = np.nan

# Filtering DataFrame first to ensure matching lengths
agv_rows = data_df['GroupDecisionRule'] == 'AGV'
filtered_df = data_df[agv_rows]

# Now applying the np.where() only to this filtered DataFrame
data_df.loc[agv_rows, 'truth_telling_sign'] = np.where(
    np.sign(filtered_df['Valuation']) == np.sign(filtered_df['reported_valuation']),
    1,
    0
)

# Initialize GK_prefAGV column as NaN
data_df['GK_prefAGV'] = np.nan

# Filter to affect only rows where BinaryChoice is "AGV vs. SM"
binary_filter = data_df['BinaryChoice'] == "AGV vs. SM"

# Symmetric treatment preferences
data_df.loc[binary_filter & (data_df['treatment_number'] == 'symmetric') & (data_df['ad_interim_round'] == 1), 'GK_prefAGV'] = 0
data_df.loc[binary_filter & (data_df['treatment_number'] == 'symmetric') &
            (data_df['Valuation'].isin([-3, 3])) &
            (data_df['ad_interim_round'] == 1), 'GK_prefAGV'] = 1

# Skewed treatments preferences
# Right-skewed: Subjects with -3 or -1 prefer SM over AGV (Set to 0)
data_df.loc[binary_filter & (data_df['treatment_number'] == 'Right-skewed') &
            (data_df['Valuation'].isin([-3, -1])) &
            (data_df['ad_interim_round'] == 1), 'GK_prefAGV'] = 0

data_df.loc[binary_filter & (data_df['treatment_number'] == 'Right-skewed') &
            (data_df['Valuation'].isin([1, 7])) &
            (data_df['ad_interim_round'] == 1), 'GK_prefAGV'] = 1

# Left-skewed: Subjects with 3 or 1 prefer SM over AGV (Set to 0)
data_df.loc[binary_filter & (data_df['treatment_number'] == 'Left-skewed') &
            (data_df['Valuation'].isin([3, 1])) &
            (data_df['ad_interim_round'] == 1), 'GK_prefAGV'] = 0

data_df.loc[binary_filter & (data_df['treatment_number'] == 'Left-skewed') &
            (data_df['Valuation'].isin([-1, -7])) &
            (data_df['ad_interim_round'] == 1), 'GK_prefAGV'] = 1

# Robustness treatment preferences
# Generally prefer SM, except types -1 and 7 prefer AGV
data_df.loc[binary_filter & (data_df['treatment_number'] == 'Robustness') &
            (data_df['ad_interim_round'] == 1), 'GK_prefAGV'] = 0
data_df.loc[binary_filter & (data_df['treatment_number'] == 'Robustness') &
            (data_df['Valuation'].isin([-1, 7])) &
            (data_df['ad_interim_round'] == 1), 'GK_prefAGV'] = 1

# Explicitly setting GK_prefAGV to NaN for rows where BinaryChoice is not "AGV vs. SM"
data_df.loc[data_df['BinaryChoice'] != "AGV vs. SM", 'GK_prefAGV'] = np.nan


# Generate all possible combinations of values for the specified columns
combinations = list(itertools.product(
    data_df['treatment_distribution'].unique(),
    data_df['BinaryChoice'].unique(),
    data_df['valuation_positive'].unique(),
    data_df['ad_interim_round'].unique()
))

# Create a DataFrame with the combinations
comparison_ad_interim = pd.DataFrame(combinations, columns=['treatment_distribution', 'BinaryChoice', 'valuation_positive', 'ad_interim_round'])

# Group data_df by the specified columns and count occurrences of chose_AGV, chose_SM, chose_RAND, and chose_NSQ being 1
counts = data_df.groupby(['treatment_distribution', 'BinaryChoice', 'valuation_positive', 'ad_interim_round']).agg({
    'chose_AGV': 'sum',
    'chose_SM': 'sum',
    'chose_RAND': 'sum',
    'chose_NSQ': 'sum'
}).reset_index()

# Merge the counts DataFrame with the comparison DataFrame
comparison_ad_interim = comparison_ad_interim.merge(counts, on=['treatment_distribution', 'BinaryChoice', 'valuation_positive', 'ad_interim_round'], how='left')

# Fill NaN values with 0 (occurs when there were no occurrences of a specific choice being 1)
columns_to_fill = ['chose_AGV', 'chose_SM', 'chose_RAND', 'chose_NSQ']
comparison_ad_interim[columns_to_fill] = comparison_ad_interim[columns_to_fill].fillna(0)

# Define the columns to sum
columns_to_sum = ['chose_AGV', 'chose_SM', 'chose_RAND', 'chose_NSQ']

# Recalculate the total for each row in the comparison DataFrame
comparison_ad_interim['total'] = comparison_ad_interim[columns_to_sum].sum(axis=1)

# Display the updated comparison DataFrame
original_data_file_name = data_input
output_csv_file_name = f"{original_data_file_name}_comparison_ad_interim.csv"
comparison_ad_interim.to_csv(output_csv_file_name, index=False)

# Generate all possible combinations of values for the specified columns
combinations = list(itertools.product(
    data_df['treatment_distribution'].unique(),
    data_df['BinaryChoice'].unique(),
    data_df['ad_interim_round'].unique()
))

# Create a DataFrame with the combinations
comparison_ex_ante = pd.DataFrame(combinations, columns=['treatment_distribution', 'BinaryChoice', 'ad_interim_round'])

# Group data_df by the specified columns and count occurrences of chose_AGV, chose_SM, chose_RAND, and chose_NSQ being 1
counts = data_df.groupby(['treatment_distribution', 'BinaryChoice', 'ad_interim_round']).agg({
    'chose_AGV': 'sum',
    'chose_SM': 'sum',
    'chose_RAND': 'sum',
    'chose_NSQ': 'sum'
}).reset_index()

# Merge the counts DataFrame with the comparison DataFrame
comparison_ex_ante = comparison_ex_ante.merge(counts, on=['treatment_distribution', 'BinaryChoice', 'ad_interim_round'], how='left')

# Fill NaN values with 0 (occurs when there were no occurrences of a specific choice being 1)
columns_to_fill = ['chose_AGV', 'chose_SM', 'chose_RAND', 'chose_NSQ']
comparison_ex_ante[columns_to_fill] = comparison_ex_ante[columns_to_fill].fillna(0)

# Define the columns to sum
columns_to_sum = ['chose_AGV', 'chose_SM', 'chose_RAND', 'chose_NSQ']

# Recalculate the total for each row in the comparison DataFrame
comparison_ex_ante['total'] = comparison_ex_ante[columns_to_sum].sum(axis=1)

# Display the updated comparison DataFrame
original_data_file_name = data_input
output_csv_file_name = f"{original_data_file_name}_comparison_ex_ante.csv"
comparison_ex_ante.to_csv(output_csv_file_name, index=False)

data_df["Rational"] = 0

for index, row in data_df.iterrows():
    if data_df.at[index, 'Valuation'] < 0:
        if data_df.at[index, 'BinaryChoice'] == "AGV vs. NSQ":
            if data_df.at[index, 'GroupDecisionVote'] == "NSQ":
                data_df.at[index, 'Rational'] = 1

        elif data_df.at[index, 'BinaryChoice'] == "AGV vs. RAND":
            if data_df.at[index, 'GroupDecisionVote'] == "AGV":
                data_df.at[index, 'Rational'] = 1

        elif data_df.at[index, 'BinaryChoice'] == "AGV vs. SM":
            if data_df.at[index, 'treatment_number'] == "symmetric":
                if data_df.at[index, 'Valuation'] == -1:
                    data_df.at[index, 'Rational'] = 1
                elif data_df.at[index, 'Valuation'] == -3:
                    if data_df.at[index, 'GroupDecisionVote'] == "AGV":
                        data_df.at[index, 'Rational'] = 1
            elif data_df.at[index, 'treatment_number'] == "Right-skewed":
                if data_df.at[index, 'GroupDecisionVote'] == "SM":
                    data_df.at[index, 'Rational'] = 1
            elif data_df.at[index, 'treatment_number'] == "Left-skewed":
                if data_df.at[index,'GroupDecisionVote'] == "AGV":
                    data_df.at[index, 'Rational'] = 1
            elif data_df.at[index, 'treatment_number'] == "Robustness":
                if data_df.at[index, 'Valuation'] == -1:
                    if data_df.at[index, 'GroupDecisionVote'] == "AGV":
                        data_df.at[index, 'Rational'] = 1
                else:
                    if data_df.at[index, "GroupDecisionVote"] == "SM":
                        data_df.at[index, 'Rational'] = 1

        elif data_df.at[index, 'BinaryChoice'] == "NSQ vs. RAND":
            if data_df.at[index, "GroupDecisionVote"] == "NSQ":
                data_df.at[index, 'Rational'] = 1

        elif data_df.at[index, 'BinaryChoice'] == "SM vs. NSQ":
            if data_df.at[index, "GroupDecisionVote"] == "NSQ":
                data_df.at[index, 'Rational'] = 1

        elif data_df.at[index, 'BinaryChoice'] == "SM vs. RAND":
            if data_df.at[index, "GroupDecisionVote"] == "SM":
                data_df.at[index, 'Rational'] = 1

    if data_df.at[index, 'Valuation'] > 0:
        if data_df.at[index, 'BinaryChoice'] == "AGV vs. NSQ":
            if data_df.at[index, 'GroupDecisionVote'] == "AGV":
                data_df.at[index, 'Rational'] = 1

        elif data_df.at[index, 'BinaryChoice'] == "AGV vs. RAND":
            if data_df.at[index, 'GroupDecisionVote'] == "AGV":
                data_df.at[index, 'Rational'] = 1

        elif data_df.at[index, 'BinaryChoice'] == "AGV vs. SM":
            if data_df.at[index, 'treatment_number'] == "symmetric":
                if data_df.at[index, 'Valuation'] == 1:
                    data_df.at[index, 'Rational'] = 1
                else:
                    if data_df.at[index, 'GroupDecisionVote'] == "AGV":
                        data_df.at[index, 'Rational'] = 1
            elif data_df.at[index, 'treatment_number'] == "Right-skewed":
                if data_df.at[index, 'GroupDecisionVote'] == "AGV":
                    data_df.at[index, 'Rational'] = 1

            elif data_df.at[index, 'treatment_number'] == "Left-skewed":
                if data_df.at[index, 'GroupDecisionVote'] == "SM":
                    data_df.at[index, 'Rational'] = 1

            elif data_df.at[index, 'treatment_number'] == "Robustness":
                if data_df.at[index, 'GroupDecisionVote'] == "AGV":
                    data_df.at[index, 'Rational'] = 1


        elif data_df.at[index, 'BinaryChoice'] == "NSQ vs. RAND":
            if data_df.at[index, "GroupDecisionVote"] == "RAND":
                data_df.at[index, 'Rational'] = 1

        elif data_df.at[index, 'BinaryChoice'] == "SM vs. NSQ":
            if data_df.at[index, "GroupDecisionVote"] == "SM":
                data_df.at[index, 'Rational'] = 1

        elif data_df.at[index, 'BinaryChoice'] == "SM vs. RAND":
            if data_df.at[index, "treatment_number"] == "Robustness":
                if data_df.at[index, "GroupDecisionVote"] == "RAND":
                    data_df.at[index, 'Rational'] = 1
            else:
                if data_df.at[index, "GroupDecisionVote"] == "SM":
                    data_df.at[index, 'Rational'] = 1


# Save the DataFrame with a modified filename in the same directory as the input file
directory = os.path.dirname(data_input)  # Extract directory path
filename = data_input.split('/')[-1]  # Extract filename
filename_without_extension = filename.split('.')[0]  # Remove extension
new_filename = f"{filename_without_extension}_cleaned.csv"  # Append "cleaned" to the filename
output_path = os.path.join(directory, new_filename)  # Create full output path

# Save the DataFrame to CSV
data_df.to_csv(output_path, index=False)  # Save the DataFrame with the new filename in the same directory


