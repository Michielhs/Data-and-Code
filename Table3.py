# imports
import pandas as pd
import statsmodels.api as sm
import numpy as np

# load data
data_input = 'Data results/GPT3.5/With explanation/RUN1/RUN1_cleaned.csv'
original_data = pd.read_csv(data_input)
data_df = original_data.copy()

## Regression model 1 Efficient
# Filter data for ex ante round equal to 1
df_reg_1 = original_data.copy()
df_reg_1 = data_df[data_df['ex_ante_round'] == 1]
df_reg_1 = pd.get_dummies(df_reg_1, columns=['treatment_number'], drop_first=True)

# Define independent variables and dependent variable
dependent_var = 'efficient_mech_choice'
df_reg_1.dropna(subset=['efficient_mech_choice'], inplace=True)
df_reg_1[dependent_var] = df_reg_1[dependent_var].astype(int)

# Create 'treatment_number_Left-skewed' column based on dummy variables
df_reg_1['treatment_number_Left-skewed'] = 0
df_reg_1.loc[(df_reg_1['treatment_number_Right-skewed'] == 0) &
             (df_reg_1['treatment_number_Robustness'] == 0) &
             (df_reg_1['treatment_number_symmetric'] == 0), 'treatment_number_Left-skewed'] = 1

# Convert boolean columns to integer (0 or 1)
df_reg_1['treatment_number_Right-skewed'] = df_reg_1['treatment_number_Right-skewed'].astype(int)
df_reg_1['treatment_number_Robustness'] = df_reg_1['treatment_number_Robustness'].astype(int)
df_reg_1['treatment_number_symmetric'] = df_reg_1['treatment_number_symmetric'].astype(int)

# Reorder columns to have 'treatment_number_Left-skewed' in the desired order
df_reg_1 = df_reg_1[['valuation_negative', 'treatment_number_symmetric',
                       'treatment_number_Right-skewed', 'treatment_number_Left-skewed',
                       'treatment_number_Robustness', dependent_var]]

# Define independent variables after adding 'treatment_number_Left-skewed'
independent_vars = ['valuation_negative', 'treatment_number_symmetric',
                    'treatment_number_Right-skewed', 'treatment_number_Left-skewed',
                    'treatment_number_Robustness']

# Perform logistic regression
logit_model = sm.Logit(df_reg_1[dependent_var], df_reg_1[independent_vars])
logit_result = logit_model.fit()

# Get summary of the logistic regression results
summary = logit_result.summary()

# Print summary of the logistic regression results
print(summary)

## Regression model 2 NSQ
df_reg_2 = data_df[data_df['ad_interim_round'] == 1]

# Define dependent and independent variables
dependent_var = 'chose_NSQ'

df_reg_2 = df_reg_2.dropna(subset=[dependent_var])
df_reg_2[dependent_var] = df_reg_2[dependent_var].astype(int)

# Create dummy variables for 'treatment_number'
df_reg_2 = pd.get_dummies(df_reg_2, columns=['treatment_number'], drop_first=True)

# Create 'treatment_number_Left-skewed' column based on dummy variables
df_reg_2['treatment_number_Left-skewed'] = 0
df_reg_2.loc[(df_reg_2['treatment_number_Right-skewed'] == 0) &
             (df_reg_2['treatment_number_Robustness'] == 0) &
             (df_reg_2['treatment_number_symmetric'] == 0), 'treatment_number_Left-skewed'] = 1

# Convert boolean columns to integer (0 or 1)
df_reg_2['treatment_number_Right-skewed'] = df_reg_2['treatment_number_Right-skewed'].astype(int)
df_reg_2['treatment_number_Robustness'] = df_reg_2['treatment_number_Robustness'].astype(int)
df_reg_2['treatment_number_symmetric'] = df_reg_2['treatment_number_symmetric'].astype(int)

# Reorder columns to have 'treatment_number_Left-skewed' in the desired order
df_reg_2 = df_reg_2[['valuation_negative', 'treatment_number_symmetric',
                       'treatment_number_Right-skewed', 'treatment_number_Left-skewed',
                       'treatment_number_Robustness', dependent_var]]

# Define independent variables after adding 'treatment_number_Left-skewed'
independent_vars = ['valuation_negative', 'treatment_number_symmetric',
                    'treatment_number_Right-skewed', 'treatment_number_Left-skewed',
                    'treatment_number_Robustness']

# Perform logistic regression without a constant term
logit_model = sm.Logit(df_reg_2[dependent_var], df_reg_2[independent_vars])
logit_result = logit_model.fit()

# Display summary of logistic regression results
print(logit_result.summary())

## Regression model 3 NSQ
dependent_var = 'chose_NSQ'

# Filter the data for the second part
df_reg_3 = data_df[data_df['ad_interim_round'] == 1].copy()

# Filter out rows with Valuation -7 and -2
df_reg_3 = df_reg_3[~df_reg_3['Valuation'].isin([-7, -2])]

# Reset index after removing rows
df_reg_3.reset_index(drop=True, inplace=True)

df_reg_3 = df_reg_3.dropna(subset=[dependent_var])
df_reg_3[dependent_var] = df_reg_3[dependent_var].astype(int)

# Create dummy variables for 'treatment_number' with drop_first=False
df_reg_3 = pd.get_dummies(df_reg_3, columns=['treatment_number'], drop_first=False)

# Manually select which dummy columns to keep, including the first one
columns_to_keep = ['treatment_number_Left-skewed', 'treatment_number_Right-skewed', 'treatment_number_Robustness', 'chose_NSQ', 'Valuation']

# Select the columns to keep
df_reg_3 = df_reg_3[columns_to_keep]

df_reg_3 = pd.get_dummies(df_reg_3, columns=['Valuation'], drop_first=False)

# Convert boolean columns to integer (0 or 1)
df_reg_3['treatment_number_Right-skewed'] = df_reg_3['treatment_number_Right-skewed'].astype(int)
df_reg_3['treatment_number_Robustness'] = df_reg_3['treatment_number_Robustness'].astype(int)
df_reg_3['treatment_number_Left-skewed'] = df_reg_3['treatment_number_Left-skewed'].astype(int)

df_reg_3['Valuation_-3'] = df_reg_3['Valuation_-3'].astype(int)
df_reg_3['Valuation_-1'] = df_reg_3['Valuation_-1'].astype(int)
df_reg_3['Valuation_1'] = df_reg_3['Valuation_1'].astype(int)
df_reg_3['Valuation_3'] = df_reg_3['Valuation_3'].astype(int)
df_reg_3['Valuation_7'] = df_reg_3['Valuation_7'].astype(int)

# Define independent variables
independent_vars = ['Valuation_-3', 'Valuation_-1',
                    'Valuation_1', 'Valuation_3', 'Valuation_7',
                    'treatment_number_Right-skewed', 'treatment_number_Left-skewed',
                    'treatment_number_Robustness']

# Perform logistic regression without a constant term
logit_model = sm.Logit(df_reg_3[dependent_var], df_reg_3[independent_vars])
logit_result = logit_model.fit()

# Display summary of logistic regression results
print(logit_result.summary())

## Regression Model 4 RAND
# Define dependent variable
dependent_var = 'chose_RAND'

# Filter the data for the second part and specific conditions (Rule_1 and Rule_2)
# Filter the DataFrame based on the specified combinations
df_reg_4 = data_df[
    (data_df['ad_interim_round'] == 1) &
    (
        ((data_df['Rule_1'].isin(['AGV', 'SM'])) & (data_df['Rule_2'] == 'RAND')) |
        ((data_df['Rule_1'] == 'RAND') & (data_df['Rule_2'].isin(['AGV', 'SM'])))
    )
].copy()

# Reset index after filtering
df_reg_4.reset_index(drop=True, inplace=True)

# Drop rows with missing values in the dependent variable
df_reg_4 = df_reg_4.dropna(subset=[dependent_var])
df_reg_4[dependent_var] = df_reg_4[dependent_var].astype(int)

# Create dummy variables for 'treatment_number' with drop_first=False
df_reg_4 = pd.get_dummies(df_reg_4, columns=['treatment_number'], drop_first=False)

# Manually select which dummy columns to keep
columns_to_keep = ['treatment_number_Left-skewed', 'treatment_number_Right-skewed',
                   'treatment_number_Robustness', 'chose_RAND', 'Valuation']

# Select the columns to keep
df_reg_4 = df_reg_4[columns_to_keep]

# Create dummy variables for 'Valuation'
df_reg_4 = pd.get_dummies(df_reg_4, columns=['Valuation'], drop_first=False)

# Convert boolean columns to integer (0 or 1)
df_reg_4['treatment_number_Right-skewed'] = df_reg_4['treatment_number_Right-skewed'].astype(int)
df_reg_4['treatment_number_Robustness'] = df_reg_4['treatment_number_Robustness'].astype(int)
df_reg_4['treatment_number_Left-skewed'] = df_reg_4['treatment_number_Left-skewed'].astype(int)

df_reg_4['Valuation_-7'] = df_reg_4['Valuation_-7'].astype(int)
df_reg_4['Valuation_-3'] = df_reg_4['Valuation_-3'].astype(int)
df_reg_4['Valuation_-2'] = df_reg_4['Valuation_-2'].astype(int)
df_reg_4['Valuation_-1'] = df_reg_4['Valuation_-1'].astype(int)
df_reg_4['Valuation_1'] = df_reg_4['Valuation_1'].astype(int)
df_reg_4['Valuation_3'] = df_reg_4['Valuation_3'].astype(int)
df_reg_4['Valuation_7'] = df_reg_4['Valuation_7'].astype(int)

# Define independent variables
independent_vars = ['Valuation_-7','Valuation_-3', 'Valuation_-2', 'Valuation_-1',
                    'Valuation_1', 'Valuation_3', 'Valuation_7',
                    'treatment_number_Right-skewed', 'treatment_number_Left-skewed',
                    'treatment_number_Robustness']

# Perform logistic regression without a constant term
logit_model = sm.Logit(df_reg_4[dependent_var], df_reg_4[independent_vars])
logit_result = logit_model.fit()

# Display summary of logistic regression results
print(logit_result.summary())

## Regression Model 5 AGV

# Define dependent variable
dependent_var = 'chose_AGV'

# Filter the DataFrame based on the specified condition
df_reg_5 = data_df[
    (data_df['BinaryChoice'] == "AGV vs. SM")
].copy()

# Reset index after filtering
df_reg_5.reset_index(drop=True, inplace=True)

# Drop rows with missing values in the dependent variable
df_reg_5 = df_reg_5.dropna(subset=[dependent_var])
df_reg_5[dependent_var] = df_reg_5[dependent_var].astype(int)
df_reg_5 = df_reg_5.dropna(subset=['GK_prefAGV'])

# Create dummy variables for 'treatment_number' with drop_first=False
df_reg_5 = pd.get_dummies(df_reg_5, columns=['treatment_number'], drop_first=False)

# Manually select which dummy columns to keep
columns_to_keep = ['treatment_number_symmetric', 'treatment_number_Right-skewed','treatment_number_Left-skewed',
                   'treatment_number_Robustness', 'chose_AGV', 'GK_prefAGV']

# Manually select which dummy columns to have as independent_vars
independent_vars = ['GK_prefAGV',
                    'treatment_number_symmetric', 'treatment_number_Right-skewed', 'treatment_number_Left-skewed',
                   'treatment_number_Robustness']

# Select the columns to keep
df_reg_5 = df_reg_5[columns_to_keep]

# Convert dummy variables to integers
df_reg_5['treatment_number_symmetric'] = df_reg_5['treatment_number_symmetric'].astype(int)
df_reg_5['treatment_number_Left-skewed'] = df_reg_5['treatment_number_Left-skewed'].astype(int)
df_reg_5['treatment_number_Right-skewed'] = df_reg_5['treatment_number_Right-skewed'].astype(int)
df_reg_5['treatment_number_Robustness'] = df_reg_5['treatment_number_Robustness'].astype(int)

# Perform logistic regression without a constant term
logit_model = sm.Logit(df_reg_5[dependent_var], df_reg_5[independent_vars])
logit_result = logit_model.fit()

# Display summary of logistic regression results
print(logit_result.summary())

