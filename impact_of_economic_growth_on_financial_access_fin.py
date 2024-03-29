# -*- coding: utf-8 -*-
"""Determining the Impact of Economic Growth on Financial Access in Kenya Using Ordinary Least Squares (OLS) Multiple Regression Model

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pdOMnvSkIHKpi4qNeqfrEuxgoE6xVd2j

**Data Import**
"""

# Import necessary libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.regression.linear_model import OLSResults

import pickle
import ipywidgets as widgets
from IPython.display import display

# Specify file paths
account_ownership_path = 'account_ownership_data.csv'
gdp_path = 'gdp_data.csv'
cpi_path = 'cpi_data.csv'

# Load CSV files
account_ownership_data = pd.read_csv(account_ownership_path)
gdp_data = pd.read_csv(gdp_path)
cpi_data = pd.read_csv(cpi_path)

# View the imported data
print("Account Ownership Data:")
print(account_ownership_data.head())

print("\nGDP Data:")
print(gdp_data.head())

print("\nCPI Data:")
print(cpi_data.head())

print("\nAccount Ownership Data Info:")
print(account_ownership_data.info())

print("\nGDP Data Info:")
print(gdp_data.info())

print("\nCPI Data Info:")
print(cpi_data.info())

"""Data Selection, Visualization and Pre-Processing"""

# Selecting data for Kenya
country = 'Kenya'

# Filter data for Kenya from 2011 to 2021
years_to_include = [str(year) for year in range(2011, 2022)]

account_ownership_country = account_ownership_data.loc[
    (account_ownership_data['Country Name'] == country),
    ['Indicator Code'] + years_to_include
]

gdp_country = gdp_data.loc[
    (gdp_data['Country Name'] == country),
    ['Indicator Code'] + years_to_include
]

cpi_country = cpi_data.loc[
    (cpi_data['Country Name'] == country),
    ['Indicator Code'] + years_to_include
]

# View filtered data for Kenya only

print("Account Ownership Kenya:")
print(account_ownership_country.head())

print("\nGDP Data Kenya:")
print(gdp_country.head())

print("\nCPI Data Kenya:")
print(cpi_country.head())

# Check for missing values for Kenya

print("Account Ownership Kenya - Missing Data:")
print(account_ownership_country.isnull().sum())

print("\nGDP Data Kenya - Missing Data:")
print(gdp_country.isnull().sum())

print("\nCPI Data Kenya - Missing Data:")
print(cpi_country.isnull().sum())

# Check data types of columns to prepare for imputing missing data

print("Account Ownership Kenya - Data Types:")
print(account_ownership_country.dtypes)

print("\nGDP Data Kenya - Data Types:")
print(gdp_country.dtypes)

print("\nCPI Data Kenya - Data Types:")
print(cpi_country.dtypes)

# Specify the columns for imputation
columns_to_impute = ['2012', '2013', '2015', '2016', '2018', '2019', '2020']

# Iterate through each row and impute missing values with the previous non-null value in the same row
for index, row in account_ownership_country.iterrows():
    for col in columns_to_impute:
        if pd.isna(row[col]):
            previous_col = row.index.get_loc(col) - 1
            while previous_col >= 0:
                if not pd.isna(row.iloc[previous_col]):
                    account_ownership_country.at[index, col] = row.iloc[previous_col]
                    break
                previous_col -= 1

# Display the imputed DataFrame
print(account_ownership_country)

# View Account Ownership Kenya Mising Data after imputing

print(account_ownership_country.isnull().sum())

# There is no missing data

# View Account Ownership Kenya Data after imputing

print(account_ownership_country.head())

"""Data Visualization"""

# Plotting Financial Inclusion over the years
plt.figure(figsize=(12, 6))
years = account_ownership_country.columns[1:].astype(int)  # Extracting years as integers
plt.plot(years, account_ownership_country.iloc[:, 1:].values.flatten(), marker='o', label='Financial Inclusion')
plt.title(f'Financial Inclusion Over the Years - {country}')
plt.xlabel('Year')
plt.ylabel('Financial Inclusion (annual %)')
plt.legend()
plt.show()

# Plotting GDP growth over the years
plt.figure(figsize=(12, 6))
plt.plot(gdp_country.columns[1:], gdp_country.iloc[:, 1:].values.flatten(), marker='o', label='GDP Growth')
plt.title(f'GDP Growth Over the Years - {country}')
plt.xlabel('Year')
plt.ylabel('GDP Growth (annual %)')
plt.legend()
plt.show()

# Plotting CPI over the years
plt.figure(figsize=(12, 6))
plt.plot(cpi_country.columns[1:], cpi_country.iloc[:, 1:].values.flatten(), marker='o', label='CPI')
plt.title(f'Consumer Price Index (CPI) Over the Years - {country}')
plt.xlabel('Year')
plt.ylabel('Inflation, consumer prices (annual %)')
plt.legend()
plt.show()

# Transpose the dataframe - Account Ownership
account_ownership_country_T = account_ownership_country.T # Transpose the DataFrame

# View Transposed columns and rows
print("Columns in Account Ownership Kenya:")
print(account_ownership_country_T.columns)

print("\nRows in Account Ownership Kenya:")
print(account_ownership_country_T.head())

# Reset the index and set column names
account_ownership_country_T.reset_index(inplace=True)
account_ownership_country_T.columns = ['Year', 'Account Ownership']

# Filter out the row with 'Indicator Code' equal to 'FX.OWN.TOTL.ZS'
account_ownership_country_T = account_ownership_country_T[account_ownership_country_T['Account Ownership'] != 'FX.OWN.TOTL.ZS']

# Reset the index and set column names
account_ownership_country_T.reset_index(drop=True, inplace=True)

# View Modified columns and rows
print("Columns in Account Ownership Kenya:")
print(account_ownership_country_T.columns)

print("\nRows in Account Ownership Kenya:")
print(account_ownership_country_T.head())

# Transpose the dataframe - GDP

gdp_country_T = gdp_country.T # Transpose the DataFrame

# View Transposed columns and rows
print("Columns in GDP Kenya:")
print(gdp_country_T.columns)

print("\nRows in GDP Kenya:")
print(gdp_country_T.head())

# Reset the index and set column names
gdp_country_T.reset_index(inplace=True)

# Exclude the row with 'Indicator Code' and 'NY.GDP.MKTP.KD.ZG'
gdp_country_T = gdp_country_T[gdp_country_T['index'] != 'Indicator Code']

# Set column names
gdp_country_T.columns = ['Year', 'GDP']

# Inspect columns after setting column names
print("Columns after setting column names in GDP Kenya:")
print(gdp_country_T.columns)

print("\nRows in GDP Kenya:")
print(gdp_country_T.head())

# Transpose the dataframe - CPI

cpi_country_T = cpi_country.T # Transpose the DataFrame

# View Transposed columns and rows
print("Columns in CPI Kenya:")
print(cpi_country_T.columns)

print("\nRows in CPI Kenya:")
print(cpi_country_T.head())

# Reset the index and set column names
cpi_country_T.reset_index(inplace=True)

# Exclude the row with 'Indicator Code' and 'FP.CPI.TOTL.ZG'
cpi_country_T = cpi_country_T[cpi_country_T['index'] != 'Indicator Code']

# Set column names
cpi_country_T.columns = ['Year', 'CPI']

# Inspect columns after setting column names
print("Columns after setting column names in CPI Kenya:")
print(cpi_country_T.columns)

print("\nRows in CPI Kenya:")
print(cpi_country_T.head())

# Merge the DataFrames on 'Year'

merged_data = pd.merge(account_ownership_country_T, gdp_country_T, on='Year')
merged_data = pd.merge(merged_data, cpi_country_T, on='Year')

# Convert columns to numeric

merged_data[['Account Ownership', 'GDP', 'CPI']] = merged_data[['Account Ownership', 'GDP', 'CPI']].apply(pd.to_numeric)

# View Merged Data

print("\Merged Kenya Indicators Data:")
print(merged_data)

print("\nData Types of Merged Data:")
print(merged_data.info())

# Visualize the relationship between variables in the merged dataframe before OLS
plt.figure(figsize=(12, 6))

# Plot Financial Inclusion vs. GDP
plt.subplot(1, 2, 1)
plt.scatter(merged_data['Account Ownership'], merged_data['GDP'])
plt.title('Financial Inclusion vs. GDP')
plt.xlabel('Financial Inclusion (annual %)')
plt.ylabel('GDP Growth (annual %)')

# Plot Financial Inclusion vs. CPI
plt.subplot(1, 2, 2)
plt.scatter(merged_data['Account Ownership'], merged_data['CPI'])
plt.title('Financial Inclusion vs. CPI')
plt.xlabel('Financial Inclusion (annual %)')
plt.ylabel('CPI (annual %)')

plt.tight_layout()
plt.show()

# Visualize the relationship before OLS using line graphs
plt.figure(figsize=(12, 6))

# Plot Financial Inclusion over the years
plt.subplot(1, 3, 1)
plt.plot(merged_data['Year'], merged_data['Account Ownership'], marker='o')
plt.title('Financial Inclusion Over the Years')
plt.xlabel('Year')
plt.ylabel('Financial Inclusion (annual %)')

# Plot GDP growth over the years
plt.subplot(1, 3, 2)
plt.plot(merged_data['Year'], merged_data['GDP'], marker='o')
plt.title('GDP Growth Over the Years')
plt.xlabel('Year')
plt.ylabel('GDP Growth (annual %)')

# Plot CPI over the years
plt.subplot(1, 3, 3)
plt.plot(merged_data['Year'], merged_data['CPI'], marker='o')
plt.title('Consumer Price Index (CPI) Over the Years')
plt.xlabel('Year')
plt.ylabel('Inflation, consumer prices (annual %)')

plt.tight_layout()
plt.show()

# Visualize the relationship before OLS using combined line graph
plt.figure(figsize=(12, 6))

# Plot Financial Inclusion, GDP, and CPI over the years
plt.plot(merged_data['Year'], merged_data['Account Ownership'], marker='o', label='Financial Inclusion')
plt.plot(merged_data['Year'], merged_data['GDP'], marker='o', label='GDP Growth')
plt.plot(merged_data['Year'], merged_data['CPI'], marker='o', label='CPI')

# Set labels and title
plt.title('Relationship Over the Years')
plt.xlabel('Year')
plt.ylabel('Percentage')
plt.legend()

plt.show()

"""OLS Regression to determine Relationship between Financial Inclusion and Economic Growth (GDP and CPI)"""

# OLS Regression for Financial Inclusion and GDP
X_gdp = sm.add_constant(merged_data['Account Ownership'])
y_gdp = merged_data['GDP']
model_gdp = sm.OLS(y_gdp, X_gdp).fit()

# OLS Regression for Financial Inclusion and CPI
X_cpi = sm.add_constant(merged_data['Account Ownership'])
y_cpi = merged_data['CPI']
model_cpi = sm.OLS(y_cpi, X_cpi).fit()

# Display regression results
print("OLS Regression Results for Financial Inclusion and GDP:")
print(model_gdp.summary())

print("\nOLS Regression Results for Financial Inclusion and CPI:")
print(model_cpi.summary())

# Visualize the relationship after OLS
plt.figure(figsize=(12, 6))

# Plot Financial Inclusion vs. GDP
plt.subplot(1, 2, 1)
plt.scatter(merged_data['Account Ownership'], merged_data['GDP'])
plt.plot(merged_data['Account Ownership'], model_gdp.predict(), color='red', linewidth=2, label='OLS')
plt.title('Financial Inclusion vs. GDP (After OLS)')
plt.xlabel('Financial Inclusion (annual %)')
plt.ylabel('GDP Growth (annual %)')
plt.legend()

# Plot Financial Inclusion vs. CPI
plt.subplot(1, 2, 2)
plt.scatter(merged_data['Account Ownership'], merged_data['CPI'])
plt.plot(merged_data['Account Ownership'], model_cpi.predict(), color='red', linewidth=2, label='OLS')
plt.title('Financial Inclusion vs. CPI (After OLS)')
plt.xlabel('Financial Inclusion (annual %)')
plt.ylabel('CPI (annual %)')
plt.legend()

plt.tight_layout()
plt.show()

"""Model Saving for Deployment"""

# Save OLS regression models
with open('model_gdp.pkl', 'wb') as file:
    pickle.dump(model_gdp, file)

with open('model_cpi.pkl', 'wb') as file:
    pickle.dump(model_cpi, file)

"""Model Deployment"""

# Load models
with open('model_gdp.pkl', 'rb') as file:
    model_gdp = pickle.load(file)

with open('model_cpi.pkl', 'rb') as file:
    model_cpi = pickle.load(file)

# User input widgets with longer sliders
account_ownership_input = widgets.FloatSlider(min=0.0, max=100.0, step=0.1, description='Account Ownership:')
gdp_input = widgets.FloatSlider(min=-10.0, max=20.0, step=0.1, description='GDP Growth:')
cpi_input = widgets.FloatSlider(min=0.0, max=20.0, step=0.1, description='CPI:')

# Adjust the length of the sliders
slider_layout = widgets.Layout(width='40%')
account_ownership_input.layout = slider_layout
gdp_input.layout = slider_layout
cpi_input.layout = slider_layout

# Display input widgets
display(account_ownership_input, gdp_input, cpi_input)

# Define Prediction Function

def predict_and_visualize(account_ownership, gdp, cpi):
    # Predict with the models
    predicted_access_gdp = model_gdp.predict([[account_ownership, gdp]])[0]
    predicted_access_cpi = model_cpi.predict([[account_ownership, cpi]])[0]

    # Display predictions
    print(f"Predicted Impact on Financial Access (GDP Model): {predicted_access_gdp:.2f}")
    print(f"Predicted Impact on Financial Access (CPI Model): {predicted_access_cpi:.2f}")

    # Visualize the relationship
    plt.figure(figsize=(12, 6))

    # Plot Financial Inclusion vs. GDP
    plt.subplot(1, 2, 1)
    plt.scatter(merged_data['Account Ownership'], merged_data['GDP'])
    plt.plot(merged_data['Account Ownership'], model_gdp.predict(), color='red', linewidth=2, label='OLS')
    plt.title('Financial Inclusion vs. GDP (After OLS)')
    plt.xlabel('Financial Inclusion (annual %)')
    plt.ylabel('GDP Growth (annual %)')
    plt.legend()

    # Plot Financial Inclusion vs. CPI
    plt.subplot(1, 2, 2)
    plt.scatter(merged_data['Account Ownership'], merged_data['CPI'])
    plt.plot(merged_data['Account Ownership'], model_cpi.predict(), color='red', linewidth=2, label='OLS')
    plt.title('Financial Inclusion vs. CPI (After OLS)')
    plt.xlabel('Financial Inclusion (annual %)')
    plt.ylabel('CPI (annual %)')
    plt.legend()

    plt.tight_layout()
    plt.show()

# Call the prediction function with widget values
predict_and_visualize(account_ownership_input.value, gdp_input.value, cpi_input.value)

# User input widgets - GDP

account_ownership_input = widgets.FloatSlider(min=0.0, max=100.0, step=0.1, description='Account Ownership:')
gdp_input = widgets.FloatSlider(min=-10.0, max=10.0, step=0.1, description='GDP Growth:')

# Display input widgets
display(account_ownership_input, gdp_input)

# Link the sliders
def update_gdp_slider(change):
    gdp_input.value = account_ownership_input.value

account_ownership_input.observe(update_gdp_slider, 'value')

# User input widgets - CPI

account_ownership_input = widgets.FloatSlider(min=0.0, max=100.0, step=0.1, description='Account Ownership:')
cpi_input = widgets.FloatSlider(min=-10.0, max=10.0, step=0.1, description='CPI Growth:')

# Display input widgets
display(account_ownership_input, cpi_input)

# Link the sliders
def update_cpi_slider(change):
    cpi_input.value = account_ownership_input.value

account_ownership_input.observe(update_cpi_slider, 'value')