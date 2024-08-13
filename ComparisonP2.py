import pandas as pd
import numpy as np
from openpyxl import load_workbook, Workbook

# Load new data
input_data_path = "Data results/GPT4/RUN5/RUN5_cleaned.csv"
input_data = pd.read_csv(input_data_path)

# Load original data
experiment_data_path = "Input data/experimental_data_flip_a_coin_cleaned.csv"
experiment_data = pd.read_csv(experiment_data_path)

# Ensure 'Rational' column exists
if 'Rational' not in input_data.columns or 'Rational' not in experiment_data.columns:
    raise ValueError("The 'Rational' column does not exist in the input or experiment data.")

# Function to calculate the percentage of 1s in a specified column for a given condition
def calculate_percentage(data, condition):
    filtered_data = data.query(condition)
    count = len(filtered_data)
    sum_vals = filtered_data['Rational'].sum()
    percentage = (sum_vals / count) * 100 if count > 0 else 0
    return percentage

# Calculate the percentage of 1s for 'Rational' in 'input_data' for each condition
input_rational_percentage_overall = calculate_percentage(input_data, 'Rational >= 0')
input_rational_percentage_val_pos_0 = calculate_percentage(input_data, 'ex_ante_round == 0 & valuation_positive == 0')
input_rational_percentage_val_pos_1 = calculate_percentage(input_data, 'ex_ante_round == 0 & valuation_positive == 1')

# Calculate the percentage of 1s for 'Rational' in 'experiment_data' for each condition
exp_rational_percentage_overall = calculate_percentage(experiment_data, 'Rational >= 0')
exp_rational_percentage_val_pos_0 = calculate_percentage(experiment_data, 'ex_ante_round == 0 & valuation_positive == 0')
exp_rational_percentage_val_pos_1 = calculate_percentage(experiment_data, 'ex_ante_round == 0 & valuation_positive == 1')

# Convert 'vote' columns to string type for consistency
input_data['vote'] = input_data['vote'].astype(str).replace({'1': 'Yes', '0': 'No'})
experiment_data['vote'] = experiment_data['vote'].astype(str).replace({'1': 'Yes', '0': 'No'})

# part 2 Compare truth telling AGV

# Calculate the percentage of 1s for 'experiment_data'
exp_truth_telling_count = experiment_data['truth_telling'].count()
exp_truth_telling_sum = experiment_data['truth_telling'].sum()
exp_truth_telling_percentage = (exp_truth_telling_sum / exp_truth_telling_count) * 100 if exp_truth_telling_count > 0 else 0

exp_truth_telling_sign_count = experiment_data['truth_telling_sign'].count()
exp_truth_telling_sign_sum = experiment_data['truth_telling_sign'].sum()
exp_truth_telling_sign_percentage = (exp_truth_telling_sign_sum / exp_truth_telling_sign_count) * 100 if exp_truth_telling_sign_count > 0 else 0

# Calculate the percentage of 1s for 'input_data'
input_truth_telling_count = input_data['truth_telling'].count()
input_truth_telling_sum = input_data['truth_telling'].sum()
input_truth_telling_percentage = (input_truth_telling_sum / input_truth_telling_count) * 100 if input_truth_telling_count > 0 else 0

input_truth_telling_sign_count = input_data['truth_telling_sign'].count()
input_truth_telling_sign_sum = input_data['truth_telling_sign'].sum()
input_truth_telling_sign_percentage = (input_truth_telling_sign_sum / input_truth_telling_sign_count) * 100 if input_truth_telling_sign_count > 0 else 0

# Calculate the percentage of 1s for 'experiment_data' where valuation_positive == 1
exp_filtered_pos = experiment_data[experiment_data['valuation_positive'] == 1]
exp_truth_telling_pos_count = exp_filtered_pos['truth_telling'].count()
exp_truth_telling_pos_sum = exp_filtered_pos['truth_telling'].sum()
exp_truth_telling_pos_percentage = (exp_truth_telling_pos_sum / exp_truth_telling_pos_count) * 100 if exp_truth_telling_pos_count > 0 else 0

exp_truth_telling_sign_pos_count = exp_filtered_pos['truth_telling_sign'].count()
exp_truth_telling_sign_pos_sum = exp_filtered_pos['truth_telling_sign'].sum()
exp_truth_telling_sign_pos_percentage = (exp_truth_telling_sign_pos_sum / exp_truth_telling_sign_pos_count) * 100 if exp_truth_telling_sign_pos_count > 0 else 0

# Calculate the percentage of 1s for 'experiment_data' where valuation_positive == 0
exp_filtered_neg = experiment_data[experiment_data['valuation_positive'] == 0]
exp_truth_telling_neg_count = exp_filtered_neg['truth_telling'].count()
exp_truth_telling_neg_sum = exp_filtered_neg['truth_telling'].sum()
exp_truth_telling_neg_percentage = (exp_truth_telling_neg_sum / exp_truth_telling_neg_count) * 100 if exp_truth_telling_neg_count > 0 else 0

exp_truth_telling_sign_neg_count = exp_filtered_neg['truth_telling_sign'].count()
exp_truth_telling_sign_neg_sum = exp_filtered_neg['truth_telling_sign'].sum()
exp_truth_telling_sign_neg_percentage = (exp_truth_telling_sign_neg_sum / exp_truth_telling_sign_neg_count) * 100 if exp_truth_telling_sign_neg_count > 0 else 0

# Calculate the percentage of 1s for 'input_data' where valuation_positive == 1
input_filtered_pos = input_data[input_data['valuation_positive'] == 1]
input_truth_telling_pos_count = input_filtered_pos['truth_telling'].count()
input_truth_telling_pos_sum = input_filtered_pos['truth_telling'].sum()
input_truth_telling_pos_percentage = (input_truth_telling_pos_sum / input_truth_telling_pos_count) * 100 if input_truth_telling_pos_count > 0 else 0

input_truth_telling_sign_pos_count = input_filtered_pos['truth_telling_sign'].count()
input_truth_telling_sign_pos_sum = input_filtered_pos['truth_telling_sign'].sum()
input_truth_telling_sign_pos_percentage = (input_truth_telling_sign_pos_sum / input_truth_telling_sign_pos_count) * 100 if input_truth_telling_sign_pos_count > 0 else 0

# Calculate the percentage of 1s for 'input_data' where valuation_positive == 0
input_filtered_neg = input_data[input_data['valuation_positive'] == 0]
input_truth_telling_neg_count = input_filtered_neg['truth_telling'].count()
input_truth_telling_neg_sum = input_filtered_neg['truth_telling'].sum()
input_truth_telling_neg_percentage = (input_truth_telling_neg_sum / input_truth_telling_neg_count) * 100 if input_truth_telling_neg_count > 0 else 0

input_truth_telling_sign_neg_count = input_filtered_neg['truth_telling_sign'].count()
input_truth_telling_sign_neg_sum = input_filtered_neg['truth_telling_sign'].sum()
input_truth_telling_sign_neg_percentage = (input_truth_telling_sign_neg_sum / input_truth_telling_sign_neg_count) * 100 if input_truth_telling_sign_neg_count > 0 else 0

# Calculate the percentage of "Yes" votes for 'experiment_data' where 'valuation_positive == 1' and 'GroupDecisionRule == SM'
exp_filtered_pos = experiment_data[(experiment_data['valuation_positive'] == 1) & (experiment_data['GroupDecisionRule'] == 'SM')]
exp_vote_yes_count = exp_filtered_pos['vote'].count()
exp_vote_yes_sum = exp_filtered_pos['vote'].str.contains("Yes", na=False).sum()
exp_vote_yes_percentage = (exp_vote_yes_sum / exp_vote_yes_count) * 100 if exp_vote_yes_count > 0 else 0

# Calculate the percentage of "Yes" votes for 'input_data' where 'valuation_positive == 1' and 'GroupDecisionRule == SM'
input_filtered_pos = input_data[(input_data['valuation_positive'] == 1) & (input_data['GroupDecisionRule'] == 'SM')]
input_vote_yes_count = input_filtered_pos['vote'].count()
input_vote_yes_sum = input_filtered_pos['vote'].str.contains("Yes", na=False).sum()
input_vote_yes_percentage = (input_vote_yes_sum / input_vote_yes_count) * 100 if input_vote_yes_count > 0 else 0

# Calculate the percentage of "No" votes for 'experiment_data' where 'valuation_positive == 0' and 'GroupDecisionRule == SM'
exp_filtered_neg = experiment_data[(experiment_data['valuation_positive'] == 0) & (experiment_data['GroupDecisionRule'] == 'SM')]
exp_vote_no_count = exp_filtered_neg['vote'].count()
exp_vote_no_sum = exp_filtered_neg['vote'].str.contains("No", na=False).sum()
exp_vote_no_percentage = (exp_vote_no_sum / exp_vote_no_count) * 100 if exp_vote_no_count > 0 else 0

# Calculate the percentage of "No" votes for 'input_data' where 'valuation_positive == 0' and 'GroupDecisionRule == SM'
input_filtered_neg = input_data[(input_data['valuation_positive'] == 0) & (input_data['GroupDecisionRule'] == 'SM')]
input_vote_no_count = input_filtered_neg['vote'].count()
input_vote_no_sum = input_filtered_neg['vote'].str.contains("No", na=False).sum()
input_vote_no_percentage = (input_vote_no_sum / input_vote_no_count) * 100 if input_vote_no_count > 0 else 0

# Calculate the percentage of 1s for 'efficient' in 'experiment_data'
exp_efficient_count = experiment_data['efficient'].count()
exp_efficient_sum = experiment_data['efficient'].sum()
exp_efficient_percentage = (exp_efficient_sum / exp_efficient_count) * 100 if exp_efficient_count > 0 else 0

# Calculate the percentage of 1s for 'efficient' in 'input_data'
input_efficient_count = input_data['efficient'].count()
input_efficient_sum = input_data['efficient'].sum()
input_efficient_percentage = (input_efficient_sum / input_efficient_count) * 100 if input_efficient_count > 0 else 0

# Calculate the percentage of 1s for 'efficient_mech_choice' in 'experiment_data'
exp_efficient_mech_choice_count = experiment_data['efficient_mech_choice'].count()
exp_efficient_mech_choice_sum = experiment_data['efficient_mech_choice'].sum()
exp_efficient_mech_choice_percentage = (exp_efficient_mech_choice_sum / exp_efficient_mech_choice_count) * 100 if exp_efficient_mech_choice_count > 0 else 0

# Calculate the percentage of 1s for 'efficient_mech_choice' in 'input_data'
input_efficient_mech_choice_count = input_data['efficient_mech_choice'].count()
input_efficient_mech_choice_sum = input_data['efficient_mech_choice'].sum()
input_efficient_mech_choice_percentage = (input_efficient_mech_choice_sum / input_efficient_mech_choice_count) * 100 if input_efficient_mech_choice_count > 0 else 0

# Calculate the percentage of 1s for 'EfficientChoice' in 'experiment_data'
exp_efficient_choice_count = experiment_data['EfficientChoice'].count()
exp_efficient_choice_sum = experiment_data['EfficientChoice'].sum()
exp_efficient_choice_percentage = (exp_efficient_choice_sum / exp_efficient_choice_count) * 100 if exp_efficient_choice_count > 0 else 0

# Calculate the percentage of 1s for 'EfficientChoice' in 'input_data'
input_efficient_choice_count = input_data['EfficientChoice'].count()
input_efficient_choice_sum = input_data['EfficientChoice'].sum()
input_efficient_choice_percentage = (input_efficient_choice_sum / input_efficient_choice_count) * 100 if input_efficient_choice_count > 0 else 0

# Function to calculate efficient_mech_choice and EfficientChoice for a given condition
def calculate_metrics(filtered_input, filtered_experiment):
    input_efficient_mech_choice = filtered_input['efficient_mech_choice'].mean() * 100 if len(filtered_input) > 0 else 0
    exp_efficient_mech_choice = filtered_experiment['efficient_mech_choice'].mean() * 100 if len(filtered_experiment) > 0 else 0

    input_efficient_choice = filtered_input['EfficientChoice'].mean() * 100 if len(filtered_input) > 0 else 0
    exp_efficient_choice = filtered_experiment['EfficientChoice'].mean() * 100 if len(filtered_experiment) > 0 else 0

    return input_efficient_mech_choice, exp_efficient_mech_choice, input_efficient_choice, exp_efficient_choice

# Metrics for the entire dataset
efficient_mech_choice_total = (input_data['efficient_mech_choice'].mean() * 100, experiment_data['efficient_mech_choice'].mean() * 100)
EfficientChoice_total = (input_data['EfficientChoice'].mean() * 100, experiment_data['EfficientChoice'].mean() * 100)

# Metrics for the specified conditions
conditions = [
    'ex_ante_round == 1',
    '(ex_ante_round == 0) & (valuation_positive == 1)',
    '(ex_ante_round == 0) & (valuation_positive == 0)'
]

results = []
for condition in conditions:
    filtered_input = input_data.query(condition)
    filtered_experiment = experiment_data.query(condition)
    metrics = calculate_metrics(filtered_input, filtered_experiment)
    results.append(metrics)

# Combine results into a DataFrame for the efficient_mech_choice and EfficientChoice metrics
results_df = pd.DataFrame({
    'Condition': [
        'Overall',
        'ex_ante_round == 1',
        'ex_ante_round == 0 & valuation_positive == 1',
        'ex_ante_round == 0 & valuation_positive == 0'
    ],
    'Input Data - Efficient Mech Choice': [
        efficient_mech_choice_total[0],
        results[0][0],
        results[1][0],
        results[2][0]
    ],
    'Experiment Data - Efficient Mech Choice': [
        efficient_mech_choice_total[1],
        results[0][1],
        results[1][1],
        results[2][1]
    ],
    'Input Data - Efficient Choice': [
        EfficientChoice_total[0],
        results[0][2],
        results[1][2],
        results[2][2]
    ],
    'Experiment Data - Efficient Choice': [
        EfficientChoice_total[1],
        results[0][3],
        results[1][3],
        results[2][3]
    ]
})

# Combine with the initial metrics
initial_results = pd.DataFrame({
    'Metric': [
        'Percentage of truth_telling = 1 (excluding NaNs)',
        'Percentage of truth_telling_sign = 1 (excluding NaNs)',
        'Percentage of truth_telling with valuation_positive = 1',
        'Percentage of truth_telling with valuation_positive = 0',
        'Percentage of truth_telling_sign with valuation_positive = 1',
        'Percentage of truth_telling_sign with valuation_positive = 0',
        'Percentage of Yes votes with valuation_positive = 1 and GroupDecisionRule = SM',
        'Percentage of No votes with valuation_positive = 0 and GroupDecisionRule = SM',
        'Percentage of efficient = 1 (excluding NaNs)',
        'Percentage of efficient_mech_choice = 1 (excluding NaNs)',
        'Percentage of EfficientChoice = 1 (excluding NaNs)',
        'Percentage of Rational = 1 (excluding NaNs)'
    ],
    'Input Data': [
        input_truth_telling_percentage,
        input_truth_telling_sign_percentage,
        input_truth_telling_pos_percentage,
        input_truth_telling_neg_percentage,
        input_truth_telling_sign_pos_percentage,
        input_truth_telling_sign_neg_percentage,
        input_vote_yes_percentage,
        input_vote_no_percentage,
        input_efficient_percentage,
        input_efficient_mech_choice_percentage,
        input_efficient_choice_percentage,
        input_rational_percentage_overall
    ],
    'Experiment Data': [
        exp_truth_telling_percentage,
        exp_truth_telling_sign_percentage,
        exp_truth_telling_pos_percentage,
        exp_truth_telling_neg_percentage,
        exp_truth_telling_sign_pos_percentage,
        exp_truth_telling_sign_neg_percentage,
        exp_vote_yes_percentage,
        exp_vote_no_percentage,
        exp_efficient_percentage,
        exp_efficient_mech_choice_percentage,
        exp_efficient_choice_percentage,
        exp_rational_percentage_overall
    ]
})

# Calculate Rational metrics for specified conditions
rational_metrics_conditions = {
    'ex_ante_round == 0 & valuation_positive == 1': {
        'Input Data': input_rational_percentage_val_pos_1,
        'Experiment Data': exp_rational_percentage_val_pos_1
    },
    'ex_ante_round == 0 & valuation_positive == 0': {
        'Input Data': input_rational_percentage_val_pos_0,
        'Experiment Data': exp_rational_percentage_val_pos_0
    }
}

# Add Rational metrics to the results_df DataFrame
rational_df = pd.DataFrame({
    'Condition': [
        'Overall',
        'ex_ante_round == 0 & valuation_positive == 1',
        'ex_ante_round == 0 & valuation_positive == 0'
    ],
    'Input Data - Rational': [
        input_rational_percentage_overall,
        rational_metrics_conditions['ex_ante_round == 0 & valuation_positive == 1']['Input Data'],
        rational_metrics_conditions['ex_ante_round == 0 & valuation_positive == 0']['Input Data']
    ],
    'Experiment Data - Rational': [
        exp_rational_percentage_overall,
        rational_metrics_conditions['ex_ante_round == 0 & valuation_positive == 1']['Experiment Data'],
        rational_metrics_conditions['ex_ante_round == 0 & valuation_positive == 0']['Experiment Data']
    ]
})

# Save both results to the same Excel file but in different sheets
with pd.ExcelWriter('ResultsP2.xlsx') as writer:
    initial_results.to_excel(writer, sheet_name='Initial Metrics', index=False)
    results_df.to_excel(writer, sheet_name='Condition Metrics', index=False)
    rational_df.to_excel(writer, sheet_name='Rational Metrics', index=False)

print("Results have been saved to 'ResultsP2.xlsx'")
