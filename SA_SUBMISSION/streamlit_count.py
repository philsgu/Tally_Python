import streamlit as st
import pandas as pd
import gspread
#from fuzzywuzzy import fuzz
from datetime import datetime

# service account json credentials 
SERVICE_ACCOUNT_FILE = 'accesspysheet-bd152702637a.json'
# Authenticate with the Google Sheets API
gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)

# Open the Google Sheet by URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1h4HlBY1_vOAuFmWQxTgHRr3075wgfxfroIWmHZm4b98/edit?gid=0#gid=0"
sh = gc.open_by_url(SHEET_URL)

# Select the first worksheet
worksheet = sh.get_worksheet(0)

# Extract all data as a list of list
data = worksheet.get_all_values()

# Convert to a Pandas DataFrame
df = pd.DataFrame(data[1:], columns=data[0])
df = df.drop_duplicates(subset=df.columns[0])
# Convert the 'Submitted at' column to datetime
df['Submitted at'] = pd.to_datetime(df['Submitted at'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

today = datetime.today().strftime('%m-%d-%Y')
st.header("SAMC 2025 Research Day Registration")
st.subheader("As of " + today)

st.divider()
count_yes = df[df.iloc[:, 84] == "YES"].shape[0]
st.write(f"## Total Registrants: {count_yes}/{(len(df))}")
# Filter the original dataframe to only include rows where the submission for research day is "YES"

# Select the first worksheet
worksheet = sh.get_worksheet(0)

# Extract all data as a list of lists
data = worksheet.get_all_values()

# Convert to a Pandas DataFrame
df = pd.DataFrame(data[1:], columns=data[0])

# Drop duplicates based on the first column Submission ID
df = df.drop_duplicates(subset=df.columns[0])

# Ensure the 'working title' column is treated as strings
df['What is your working project title?'] = df['What is your working project title?'].astype(str)

# Convert the 'Submitted at' column to datetime
df['Submitted at'] = pd.to_datetime(df['Submitted at'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

# Merge columns from indices 11 and 14 into a new column called 'CATEGORY'
df['STUDY_TYPE'] = df.iloc[:, [11, 14]].apply(lambda x: ' '.join(x), axis=1)

# Select the specified columns by their indices
selected_columns = [3, 4, 8, 9, 84, 88]
new_df = df.iloc[:, selected_columns]
column_renames = ['Title', 'PI', 'Dept', 'Role', 'RD_Submit', 'Category']

# Rename the columns using the column_renames list
new_df.columns = column_renames
# Display the new dataframe
new_df.rename(columns=dict(zip(new_df.columns, column_renames)), inplace=True)
# Remove spaces and unnecessary strings in the 'Category' column
new_df['Category'] = new_df['Category'].str.replace(r'\s+', '', regex=True).str.replace(r'[^a-zA-Z]', '', regex=True)
new_df_yes = new_df[new_df['RD_Submit'] == 'YES']
pivot_table = new_df_yes.pivot_table(index='Dept', columns=['Category'], aggfunc='size', fill_value=0)
# Add a new column 'Total' to get the total count for each department
pivot_table['Total'] = pivot_table.sum(axis=1)

# Calculate the sum for each category column
category_totals = pivot_table.sum(axis=0)

# Append the totals as a new row to the pivot_table
pivot_table.loc['Total'] = category_totals

st.dataframe(pivot_table)