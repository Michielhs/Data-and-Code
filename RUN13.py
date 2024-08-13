# set time
import time
start_time = time.time()

# code part #: dials

# 1 for with explanation, 0 for without explanation
explanation = 1

# 1 for GPT4, 0 for GPT3.5
GPT_select = 1
if GPT_select == 1:
    print("warning GPT4 is selected")

# code part #: setting up the environment

# import the required module
import openai
import csv
import pandas as pd
import re
import json

# set your OpenAI API key
OPENAI_API_KEY = ""

# set client object using your API key
client = openai.Client(api_key=OPENAI_API_KEY)

# set environment
GPT3 = "gpt-3.5-turbo-0125"
GPT4 =  "gpt-4o-2024-05-13"

# code part #: import and load variables
# General introduction text
with open('Explanations/RUN0_introduction Ex Ante.txt', 'r') as file:
    # Read the contents
    contents = file.read()

introduction_ex_ante = contents

with open('Explanations/RUN0_introduction Ad Interim.txt', 'r') as file:
    # Read the contents
    contents = file.read()

introduction_ad_interim = contents

with open('Explanations/RUN0_end with explanation.txt', 'r') as file:
    # Read the contents
    contents = file.read()

end_with_explanation = contents

with open('Explanations/RUN0_end without explanation.txt', 'r') as file:
    # Read the contents
    contents = file.read()

end_without_explanation = contents

# General introduction text
with open('Explanations/RUN0_AGV.txt', 'r') as file:
    # Read the contents
    contents = file.read()

AGV = contents

# General introduction text
with open('Explanations/RUN0_NSQ.txt', 'r') as file:
    # Read the contents
    contents = file.read()

NSQ = contents

# General introduction text
with open('Explanations/RUN0_RAND.txt', 'r') as file:
    # Read the contents
    contents = file.read()

RAND = contents

# General introduction text
with open('Explanations/RUN0_SM.txt', 'r') as file:
    # Read the contents
    contents = file.read()

SM = contents

symmetric = "-3 euro, -1 euro, +1 eurp, +3 euro"
right_skewed = "-3 euro, -1 euro, +1 euro, +7 euro"
left_skewed = "-7 euro, -1 euro, +1 euro, +3 euro"
robustness = "-3 euro, -2 euro, -1 euro, +7 euro"

# Code part 2: loading the data

# Load the CSV file into a Pandas DataFrame
original_data = pd.read_csv('Input data/experimental_data_flip_a_coin.csv')
filtered_df = original_data.copy()

# Further filter the DataFrame based on the 'Period' column (values 1 to 12)
filtered_df = filtered_df[(filtered_df['Period'] >= 1) & (filtered_df['Period'] <= 18)]

# Define columns to clean
columns_to_clean = ['GroupDecisionVote', 'GroupDecisionRule', 'vote', 'reported_valuation']

# Clean each column
for column in columns_to_clean:
    filtered_df[column] = ""

# Code part #: Abbreviation function
def extract_abbreviation(completion):
    # Convert completion to uppercase and remove leading/trailing whitespace
    completion = completion.strip().upper()
    # Use regular expressions to extract "SM" or "NSQ" from the completion
    match = re.search(r'\b(SM|NSQ|RAND|AGV)\b', completion)
    if match:
        return match.group(0)
    else:
        return "Invalid response"

# Fix the "Invalid responses"
def search_word_in_sentence(sentence, word):
    # Create a regex pattern for the word with word boundaries
    pattern = rf'\b{re.escape(word)}\b'

    # Search for the word in the sentence
    if re.search(pattern, sentence, re.IGNORECASE):
        return 1
    else:
        return 0

def extract_number(completion):
    # Convert completion to uppercase and remove leading/trailing whitespace
    completion = completion.strip().upper()
    # Use regular expressions to extract "0" or "1" from the completion
    match = re.search(r'\b(0|1)\b', completion)
    if match:
        return match.group(0)
    else:
        return "Invalid response"

# Code part #: get responses
def get_response(text):
    if GPT_select == 0:
        model = GPT3
    else:
        model = GPT4

    response = client.chat.completions.create(model=model, messages=text, temperature=1.5)
    return response


# Store all responses in a dictionary
responses = {}

# Part x: Get choice mechanism
for index, row in filtered_df.iterrows():
    message_history = []
    valuation = row["Valuation"]

    if row['ex_ante_round'] == 0:
        if row['treatment_number'] == 'symmetric':
            if row['Rule_1'] == "SM":
                if row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {AGV} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "AGV":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "RAND":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {AGV} {end_with_explanation}"

            if row['Rule_1'] == "NSQ":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_with_explanation}"

        elif row['treatment_number'] == "Right-skewed":
            if row['Rule_1'] == "SM":
                if row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {AGV} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "AGV":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "RAND":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {AGV} {end_with_explanation}"

            if row['Rule_1'] == "NSQ":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_with_explanation}"

        elif row['treatment_number'] == "Left-skewed":
            if row['Rule_1'] == "SM":
                if row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {AGV} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "AGV":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "RAND":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {AGV} {end_with_explanation}"

            if row['Rule_1'] == "NSQ":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation}\n Rule 1 = {NSQ} Rule 2 = {RAND} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_with_explanation}"

        elif row['treatment_number'] == 'Robustness':
            if row['Rule_1'] == "SM":
                if row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {AGV} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "AGV":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "RAND":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                        if explanation == 0:
                            input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {AGV} {end_without_explanation}"
                        elif explanation == 1:
                            input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {AGV} {end_with_explanation}"

            if row['Rule_1'] == "NSQ":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_with_explanation}"

    elif row['ex_ante_round'] == 1:
        if row['treatment_number'] == 'symmetric':
            valuation = row['Valuation']
            if row['Rule_1'] == "SM":
                if row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely. \n Rule 1 = {SM} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {AGV} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "AGV":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "RAND":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {AGV} {end_with_explanation}"

            if row['Rule_1'] == "NSQ":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_with_explanation}"

        elif row['treatment_number'] == "Right-skewed":
            if row['Rule_1'] == "SM":
                if row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {AGV} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "AGV":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "RAND":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {AGV} {end_with_explanation}"

            if row['Rule_1'] == "NSQ":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_with_explanation}"

        elif row['treatment_number'] == "Left-skewed":
            if row['Rule_1'] == "SM":
                if row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {AGV} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "AGV":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "RAND":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {AGV} {end_with_explanation}"

            if row['Rule_1'] == "NSQ":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_with_explanation}"

        elif row['treatment_number'] == 'Robustness':
            if row['Rule_1'] == "SM":
                if row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {AGV} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "AGV":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "RAND":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {AGV} {end_with_explanation}"

            if row['Rule_1'] == "NSQ":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_with_explanation}"

    # save the message history
    message_history.append({"role": "user", "content": input_text})

    # get reply from OPENAI API
    reply = get_response(message_history)

    # format reply into abbreviation and explanation
    assistant_reply = reply.choices[0].message.content
    message_history.append({"role": "system", "content": assistant_reply})
    content_only = [msg["content"] for msg in message_history]  # Extracting content only
    abbreviation = extract_abbreviation(content_only[1])
    responses[index] = [content_only[0], abbreviation, []]
    filtered_df.at[index, 'GroupDecisionVote'] = abbreviation
    filtered_df.at[index, "input_text"] = json.dumps(message_history)
    if explanation == 1:
        filtered_df.at[index, 'explanation_mechanism'] = content_only[1]
    else:
        filtered_df.at[index, 'explanation_mechanism'] = "no explanation requested"

    print(f'loop 1: {index}')

# Fix the invalid responses
for index, row in filtered_df.iterrows():
    if row['GroupDecisionVote'] == "Invalid response":
        sentence = row['explanation_mechanism']
        if search_word_in_sentence(sentence, 'Rule 1') == 1:
            filtered_df.at[index, 'GroupDecisionVote'] = row["Rule_1"]
        elif search_word_in_sentence(sentence, "Rule 2") == 1:
            filtered_df.at[index, 'GroupDecisionVote'] = row["Rule_2"]

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
    valuation = row["Valuation"]

    if row['ex_ante_round'] == 0:
        if row['treatment_number'] == 'symmetric':
            if row['Rule_1'] == "SM":
                if row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {AGV} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "AGV":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "RAND":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {AGV} {end_with_explanation}"

            if row['Rule_1'] == "NSQ":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {symmetric}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_with_explanation}"

        elif row['treatment_number'] == "Right-skewed":
            if row['Rule_1'] == "SM":
                if row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {AGV} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "AGV":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "RAND":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {AGV} {end_with_explanation}"

            if row['Rule_1'] == "NSQ":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {right_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_with_explanation}"

        elif row['treatment_number'] == "Left-skewed":
            if row['Rule_1'] == "SM":
                if row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {AGV} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "AGV":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "RAND":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {AGV} {end_with_explanation}"

            if row['Rule_1'] == "NSQ":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation}\n Rule 1 = {NSQ} Rule 2 = {RAND} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {left_skewed}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_with_explanation}"

        elif row['treatment_number'] == 'Robustness':
            if row['Rule_1'] == "SM":
                if row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {AGV} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {SM} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "AGV":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {AGV} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "RAND":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                        if explanation == 0:
                            input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {AGV} {end_without_explanation}"
                        elif explanation == 1:
                            input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {RAND} Rule 2 = {AGV} {end_with_explanation}"

            if row['Rule_1'] == "NSQ":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ad_interim} the valuation of each group member can be {robustness}. All values are equally likely. Your private valuation is {valuation} \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_with_explanation}"

    elif row['ex_ante_round'] == 1:
        if row['treatment_number'] == 'symmetric':
            valuation = row['Valuation']
            if row['Rule_1'] == "SM":
                if row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely. \n Rule 1 = {SM} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {AGV} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "AGV":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "RAND":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {AGV} {end_with_explanation}"

            if row['Rule_1'] == "NSQ":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {symmetric}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_with_explanation}"

        elif row['treatment_number'] == "Right-skewed":
            if row['Rule_1'] == "SM":
                if row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {AGV} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "AGV":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "RAND":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {AGV} {end_with_explanation}"

            if row['Rule_1'] == "NSQ":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {right_skewed}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_with_explanation}"

        elif row['treatment_number'] == "Left-skewed":
            if row['Rule_1'] == "SM":
                if row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {AGV} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "AGV":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "RAND":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {AGV} {end_with_explanation}"

            if row['Rule_1'] == "NSQ":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {left_skewed}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_with_explanation}"

        elif row['treatment_number'] == 'Robustness':
            if row['Rule_1'] == "SM":
                if row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {AGV} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {SM} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "AGV":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {AGV} Rule 2 = {RAND} {end_with_explanation}"

            if row['Rule_1'] == "RAND":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "NSQ":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {NSQ} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {RAND} Rule 2 = {AGV} {end_with_explanation}"

            if row['Rule_1'] == "NSQ":
                if row["Rule_2"] == "SM":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {SM} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {SM} {end_with_explanation}"
                elif row["Rule_2"] == "RAND":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {RAND} {end_with_explanation}"
                elif row["Rule_2"] == "AGV":
                    if explanation == 0:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_without_explanation}"
                    elif explanation == 1:
                        input_text = f"{introduction_ex_ante} the valuation of each group member can be {robustness}. All values are equally likely \n Rule 1 = {NSQ} Rule 2 = {AGV} {end_with_explanation}"


    message_history.append({"role": "user", "content": input_text})
    message_history.append({"role": "system", "content": row['GroupDecisionVote']})
    group_mechanism = row['GroupDecisionRule']

    if group_mechanism == "SM":
        if explanation == 1:
            if valuation > 0:
                message_history.append(
                    {"role": "user", "content": f"your private valuation is positive and is +{valuation} euro. "
                                                "The final decision rule is SM, do you vote in favor or against? Answer "
                                                "1 for in favor and 0 for against, also explain your decision in 1 sentence"})
            elif valuation < 0:
                message_history.append(
                    {"role": "user", "content": f"your private valuation is negative and is {valuation} euro. "
                                                "The final decision rule is SM, do you vote in favor or against? Answer "
                                                "1 for in favor and 0 for against, also explain your decision in 1 sentence"})
        elif explanation == 0:
            if valuation > 0:
                message_history.append(
                    {"role": "user", "content": f"your private valuation is positive and is +{valuation} euro. "
                                                "The final decision rule is SM, do you vote in favor or against? Answer "
                                                "1 for in favor and 0 for against"})
            elif valuation < 0:
                message_history.append(
                    {"role": "user", "content": f"your private valuation is negative and is {valuation} euro. "
                                                "The final decision rule is SM, do you vote in favor or against? Answer "
                                                "1 for in favor and 0 for against"})

        reply = get_response(message_history)
        assistant_reply = reply.choices[0].message.content

        # Splitting the assistant_reply by newline characters to check its structure
        assistant_reply_parts = assistant_reply.split('\n')

        vote = extract_number(assistant_reply)
        if explanation == 1:
            explanation_phase_2 = assistant_reply.strip()
        else:
            explanation_phase_2 = "no explanation requested"


        # Update the 'vote' column in the DataFrame
        filtered_df.at[index, 'vote'] = vote

        # Update the 'explanation2' column in the DataFrame
        filtered_df.at[index, 'explanation_phase_2'] = explanation_phase_2
        filtered_df.at[index, "reported_valuation"] = -10

    elif group_mechanism == "AGV":
        if explanation == 1:
            if valuation > 0:
                message_history.append(
                    {"role": "user", "content": f"your private valuation is +{valuation} euro. "
                                                "The final decision rule is AGV. What is your stated valuation, and why?"
                                                "Note that the sum of stated valuations determines whether to implement the project "
                                                "but your payoff is based on your private valuation "})
            elif valuation < 0:
                message_history.append(
                    {"role": "user", "content": f"your private valuation is {valuation} euro. "
                                                "The final decision rule is AGV. What is your stated valuation, and why?"
                                                "Note that the sum of stated valuations determines whether to implement the project "
                                                "but your payoff is based on your private valuation "})

        elif explanation == 0:
            if valuation > 0:
                message_history.append(
                    {"role": "user", "content": f"your private valuation is +{valuation} euro. "
                                                "The final decision rule is AGV. What is your stated valuation, answer only with a number"
                                                "Note that the sum of stated valuations determines whether to implement the project "
                                                "but your payoff is based on your private valuation "})
            elif valuation < 0:
                message_history.append(
                    {"role": "user", "content": f"your private valuation is {valuation} euro. "
                                                "The final decision rule is AGV. What is your stated valuation, answer only with a number"
                                                "Note that the sum of stated valuations determines whether to implement the project "
                                                "but your payoff is based on your private valuation "})

        reply = get_response(message_history)
        assistant_reply = reply.choices[0].message.content

        # Check if a match is found before extracting the reported valuation
        match = re.search(r'[-+]?\d+', assistant_reply)
        if match:
            reported_valuation = int(match.group(0))
            # Update the 'reported_valuation' column in the DataFrame
            filtered_df.at[index, 'reported_valuation'] = reported_valuation
        else:
            # Handle the case where no match is found
            filtered_df.at[index, 'reported_valuation'] = "error"
            print("No reported valuation found in the assistant's reply.")

        # Update the 'explanation2' column with the entire sentence
        if explanation ==1:
            filtered_df.at[index, 'explanation_phase_2'] = assistant_reply
        else:
            filtered_df.at[index, 'explanation_phase_2'] = "no explanation requested"

        filtered_df.at[index, "vote"] = -1

    else:
        filtered_df.at[index, 'vote'] = -1  # Fill -1 if group_mechanism is not "SM"
        filtered_df.at[index, 'reported_valuation'] = -10  # Fill with -10  if group_mechanism is not "AGV"
    print(f" loop 2 {index}")

filtered_df.to_csv('RUN13.csv', index=False)

# End timer
end_time = time.time()

# Calculate elapsed time in seconds
elapsed_time_seconds = end_time - start_time

# Convert elapsed time to minutes
elapsed_time_minutes = elapsed_time_seconds / 60

print("Elapsed time in seconds: ", elapsed_time_seconds)
print("Elapsed time in minutes: ", elapsed_time_minutes)