import streamlit as st
import pandas as pd
import gspread
from fuzzywuzzy import fuzz
from datetime import datetime

# service account json credentials 
SERVICE_ACCOUNT_FILE = 'accesspysheet-bd152702637a.json'
# Authenticate with the Google Sheets API
gc = gspread.service_account(filename=SERVICE_ACCOUNT_FILE)

# Open the Google Sheet by URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1dPqV9v60a_5e-c1b0__hh4GTQS0gx6aWYsCmCv8v4Qc/edit?pli=1&gid=0"
sh = gc.open_by_url(SHEET_URL)

# Select the first worksheet
worksheet = sh.get_worksheet(0)

# Extract all data as a list of lists
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
df_yes = df[df['Will you submit this project for the upcoming SAMC\'s Annual Research Poster Day?'] == 'YES']

# Group by department and the unique values in column index 11 and 14
grouped_df_yes = df_yes.groupby([df_yes.columns[8], df_yes.columns[11], df_yes.columns[14]]).size().reset_index(name='Total Count')

# Pivot the table to get a better view
pivot_df_yes = grouped_df_yes.pivot_table(index=df_yes.columns[8], columns=[df_yes.columns[11], df_yes.columns[14]], values='Total Count', fill_value=0)

# Add a new column 'Total' to get the total count for each department
pivot_df_yes['Total'] = pivot_df_yes.sum(axis=1)

pivot_df_yes = pivot_df_yes.astype(int)
st.write(pivot_df_yes)