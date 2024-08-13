# code part 1: setting up the environment

# import the required module
import openai
import csv
import pandas as pd
import re

# set your OpenAI API key
OPENAI_API_KEY = "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"

# set client object using your API key
client = openai.Client(api_key=OPENAI_API_KEY)

# set environment
GPT3 = "gpt-3.5-turbo-0125"
GPT4 =  "gpt-4-0125-preview"

# General introduction text
with open('Explanations/Without explanation/SM_RAND_SYM.txt', 'r') as file:
    # Read the contents
    contents = file.read()

SM_RAND_SYM = contents

# General introduction text
with open('Explanations/Without explanation/SM_NSQ_SYM.txt', 'r') as file:
    # Read the contents
    contents = file.read()

SM_NSQ_SYM = contents

# General introduction text
with open('Explanations/Without explanation/SM_AGV_SYM.txt', 'r') as file:
    # Read the contents
    contents = file.read()

SM_AGV_SYM = contents

# General introduction text
with open('Explanations/Without explanation/RAND_NSQ_SYM.txt', 'r') as file:
    # Read the contents
    contents = file.read()

RAND_NSQ_SYM = contents

# General introduction text
with open('Explanations/Without explanation/AGV_RAND_SYM.txt', 'r') as file:
    # Read the contents
    contents = file.read()

AGV_RAND_SYM = contents

# General introduction text
with open('Explanations/Without explanation/AGV_NSQ_SYM.txt', 'r') as file:
    # Read the contents
    contents = file.read()

AGV_NSQ_SYM = contents

# Code part 2: loading the data
import pandas as pd

# Load the CSV file into a Pandas DataFrame
original_data = pd.read_csv('Input data/experimental_data_flip_a_coin.csv')
filtered_df = original_data.copy()

# Filter for symmetric distribution
filtered_df = filtered_df[filtered_df['treatment_distribution'] == 'symmetric']

# Further filter the DataFrame based on the 'Period' column (values 1 to 12)
filtered_df = filtered_df[(filtered_df['Period'] >= 1) & (filtered_df['Period'] <= 12)]

# Define columns to clean
columns_to_clean = ['GroupDecisionVote', 'GroupDecisionRule', 'vote', 'VotesInFavour']

# Clean each column
for column in columns_to_clean:
    filtered_df[column] = ""

# Code part 3: Abbreviation function
def extract_abbreviation(completion):
    # Convert completion to uppercase and remove leading/trailing whitespace
    completion = completion.strip().upper()
    # Use regular expressions to extract "SM" or "NSQ" from the completion
    match = re.search(r'\b(SM|NSQ|RAND|AGV)\b', completion)
    if match:
        return match.group(0)
    else:
        return "Invalid response"

# Code part #: get responses
def get_response(text):
    response = client.chat.completions.create(
        model= GPT4,
        messages=text)
    return response

# Store all responses in a dictionary
responses = {}

# Part x: Get choice
for index, row in filtered_df.iterrows():
    message_history = []
    if row['BinaryChoice'] == "SM vs. RAND":
        input_text = SM_RAND_SYM
    elif row['BinaryChoice'] == "SM vs. NSQ":
        input_text = SM_NSQ_SYM
    elif row['BinaryChoice'] == "AGV vs. SM":
        input_text = SM_AGV_SYM
    elif row['BinaryChoice'] == "AGV vs. NSQ":
        input_text = AGV_NSQ_SYM
    elif row['BinaryChoice'] == "AGV vs. RAND":
        input_text = AGV_RAND_SYM
    elif row['BinaryChoice'] == "NSQ vs. RAND":
        input_text = RAND_NSQ_SYM
    message_history.append({"role": "user", "content": input_text})
    reply = get_response(message_history)
    assistant_reply = reply.choices[0].message.content
    message_history.append({"role": "system", "content": assistant_reply})
    content_only = [msg["content"] for msg in message_history]  # Extracting content only
    abbreviation = extract_abbreviation(content_only[1])
    responses[index] = [content_only[0], abbreviation, []]
    filtered_df.at[index, 'GroupDecisionVote'] = abbreviation

# fill decision of group

# Group by 'session', 'Period', and 'matching_group' and find the row with the maximum 'rand' value within each group
grouped_df = filtered_df.groupby(['session', 'Period', 'matching_group'])
max_rand_indexes = grouped_df['rand'].idxmax()
max_rand_rows = filtered_df.loc[max_rand_indexes]

# Group by 'session', 'Period', 'matching_group', 'treatment_number', and 'BinaryChoice'
grouped_df = filtered_df.groupby(['session', 'Period', 'matching_group', 'treatment_number', 'BinaryChoice'])

# Find the row with the maximum 'rand' value within each group
max_rand_indexes = grouped_df['rand'].idxmax()
max_rand_rows = filtered_df.loc[max_rand_indexes]

# Merge the maximum 'rand' rows back into the original DataFrame
filtered_df = pd.merge(filtered_df, max_rand_rows[['session', 'Period', 'matching_group', 'treatment_number', 'BinaryChoice', 'GroupDecisionVote']],
                        on=['session', 'Period', 'matching_group', 'treatment_number', 'BinaryChoice'], how='left', suffixes=('', '_max'))

# Fill 'GroupDecisionRule' based on the 'GroupDecisionVote' value of the row with the maximum 'rand' value
filtered_df['GroupDecisionRule'] = filtered_df['GroupDecisionVote_max']

# Forward fill missing values in 'GroupDecisionRule'
filtered_df['GroupDecisionRule'] = filtered_df.groupby(['session', 'Period', 'matching_group', 'treatment_number', 'BinaryChoice'])['GroupDecisionRule'].ffill()

# Drop unnecessary columns
filtered_df.drop(['GroupDecisionVote_max'], axis=1, inplace=True)

for index, row in filtered_df.iterrows():
    message_history = []
    if row['BinaryChoice'] == "SM vs. RAND":
        input_text = SM_RAND_SYM
    elif row['BinaryChoice'] == "SM vs. NSQ":
        input_text = SM_NSQ_SYM
    elif row['BinaryChoice'] == "AGV vs. SM":
        input_text = SM_AGV_SYM
    elif row['BinaryChoice'] == "AGV vs. NSQ":
        input_text = AGV_NSQ_SYM
    elif row['BinaryChoice'] == "AGV vs. RAND":
        input_text = AGV_RAND_SYM
    elif row['BinaryChoice'] == "NSQ vs. Rand":
        input_text = RAND_NSQ_SYM
    message_history.append({"role": "user", "content": input_text})
    message_history.append({"role": "system", "content": row['GroupDecisionVote']})
    group_mechanism = row['GroupDecisionRule']
    valuation = row['Valuation']
    if group_mechanism == "SM":
        message_history.append(
            {"role": "user", "content": f"your reward if the project is implemented is {valuation} euro and the final"
                                        "decision rule is SM, do you vote in favor or against? Answer "
                                        "1 for in favor and 0 for against"})
        reply = get_response(message_history)
        assistant_reply = reply.choices[0].message.content
        # Update the 'vote' column in the DataFrame
        filtered_df.at[index, 'vote'] = assistant_reply
    elif group_mechanism == "AGV":
        message_history.append(
            {"role": "user", "content": f"your reward if the project is implemented is {valuation} euro and the final"
                                        "decision rule is AGV, what valuation do you state? Answer only with 1 number"})
        reply = get_response(message_history)
        assistant_reply = reply.choices[0].message.content
        # Update the 'vote' column in the DataFrame
        filtered_df.at[index, 'reported_valuation'] = assistant_reply
    else:
        filtered_df.at[index, 'vote'] = "-1"  # Fill -1 if group_mechanism is not "SM"
        filtered_df.at[index, 'reported_valuation'] = "-10"  # Fill with -10  if group_mechanism is not "AGV"
    print(index)


filtered_df.to_csv('responses.csv', index=False)
