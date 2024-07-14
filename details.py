import streamlit as st
import pandas as pd

# Mock data
data = {
    'ID': [1, 2, 3, 4, 5],
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Age': [24, 27, 22, 32, 29],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Detail page
query_params = st.query_params
if 'id' in query_params:
    row_id = int(query_params['id'][0])
    details = df[df['ID'] == row_id]
    st.write("## User Details")
    st.write(details)
else:
    st.write("No details available.")
