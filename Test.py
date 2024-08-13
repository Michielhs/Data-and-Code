import pandas as pd

# Load the CSV file into a Pandas DataFrame
data_input = 'Data results/GPT4/RUN0/RUN0.csv'
original_data = pd.read_csv(data_input)
data_df = original_data.copy()

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

# Save the updated DataFrame to a new CSV file
data_df.to_csv('updated_dataset.csv', index=False)
