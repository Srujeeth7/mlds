import streamlit as st
import pandas as pd
import numpy as np

# Mock data
data = {
    'ID': np.arange(1, 1001),
    'Name': np.random.choice(['Alice', 'Bob', 'Charlie', 'David', 'Eve'], 1000),
    'Age': np.random.randint(20, 40, size=1000),
    'City': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'], 1000)
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Function to generate the detail URL
def generate_url(row_id):
    return f"http://localhost:8501/details?id={row_id}"

# Add URL to the DataFrame
df['Details'] = df['ID'].apply(lambda x: f"<a target='_blank' href='{generate_url(x)}'>View Details</a>")

# Function to style the rows
def highlight_rows(row):
    if row['Age'] > 30:
        return ['background-color: yellow'] * len(row)
    elif row['Age'] < 25:
        return ['background-color: lightgreen'] * len(row)
    else:
        return [''] * len(row)

# Pagination
rows_per_page = 100
total_rows = len(df)
total_pages = total_rows // rows_per_page + (1 if total_rows % rows_per_page else 0)

st.write("## User Table")

page = st.number_input('Page', min_value=1, max_value=total_pages, step=1, format='%d')

start_idx = (page - 1) * rows_per_page
end_idx = start_idx + rows_per_page

page_df = df.iloc[start_idx:end_idx]

# Apply the styling function
styled_page_df = page_df.style.apply(highlight_rows, axis=1).set_properties(subset=['Details'], **{'text-align': 'left'})

# Display the table
st.write(styled_page_df.to_html(escape=False), unsafe_allow_html=True)

# Detail page
query_params = st.query_params
if 'id' in query_params:
    row_id = int(query_params['id'][0])
    details = df[df['ID'] == row_id]
    st.write("## User Details")
    st.write(details)

