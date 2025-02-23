import streamlit as st
import pandas as pd
from datetime import datetime

# URL and data loading code remains the same
url = 'https://docs.google.com/spreadsheets/d/1h4HlBY1_vOAuFmWQxTgHRr3075wgfxfroIWmHZm4b98/edit?usp=sharing'
file_id = url.split('/')[-2]
url = f'https://docs.google.com/spreadsheets/d/{file_id}/gviz/tq?tqx=out:csv'
df = pd.read_csv(url)

# Basic data cleaning
df = df.drop_duplicates(subset=df.columns[0])
df['Submitted at'] = pd.to_datetime(df['Submitted at'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

# Display header and counts
today = datetime.today().strftime('%m-%d-%Y')
st.header("SAMC 2025 Research Day Registration")
st.subheader("As of " + today)
st.divider()
count_yes = df[df.iloc[:, 84] == "YES"].shape[0]
st.write(f"## Total Registrants: {count_yes}/{(len(df))}")

# Create the working dataframe
df['What is your working project title?'] = df['What is your working project title?'].astype(str)

# Create STUDY_TYPE column - modified to handle NaN values
df['STUDY_TYPE'] = df.iloc[:, [11, 14]].fillna('').apply(lambda x: ' '.join(x.astype(str)), axis=1)

# Select and rename columns
selected_columns = [3, 4, 8, 9, 84, 88]
new_df = df.iloc[:, selected_columns]
column_renames = ['Title', 'PI', 'Dept', 'Role', 'RD_Submit', 'Category']
new_df.columns = column_renames

# Clean up Category column - modified to preserve meaningful categories
new_df['Category'] = new_df['Category'].fillna('')
new_df['Category'] = new_df['Category'].str.strip()
new_df['Category'] = new_df['Category'].replace('', 'Uncategorized')

# Filter for YES submissions
new_df_yes = new_df[new_df['RD_Submit'] == 'YES']

# Create pivot table with modified categories
pivot_table = pd.pivot_table(
    new_df_yes,
    index='Dept',
    columns='Category',
    aggfunc='size',
    fill_value=0
)

# Add total column
pivot_table['Total'] = pivot_table.sum(axis=1)

# Calculate and add totals row
category_totals = pivot_table.sum(axis=0)
pivot_table.loc['Total'] = category_totals

# Display the pivot table
st.dataframe(pivot_table)