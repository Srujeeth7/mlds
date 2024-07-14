import streamlit as st
import pandas as pd
from supabase import create_client, Client
import os
from supabase.lib.client_options import ClientOptions


st.set_page_config(page_title="Datasets", page_icon="📊")

# Initialize connection.
# Uses st.cache_resource to only run once.

SUPABASE_URL = "https://txlyjbcyrijkkjnpkfqq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR4bHlqYmN5cmlqa2tqbnBrZnFxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjA4OTY0NzIsImV4cCI6MjAzNjQ3MjQ3Mn0.fc6_Hc9RV42-_wTornUfs6Am_fNQZXcb0dQlP9A-IIo"


@st.cache_resource
def init_connection():
    url = SUPABASE_URL
    key = SUPABASE_KEY
    opts = ClientOptions().replace(schema="personal_ml")
    return create_client(url, key,options = opts)

supabase = init_connection()

# Function to generate the detail URL
def generate_url(row_id):
    return f"http://localhost:8501/Dataset_Details?id={row_id}"

def highlight_rows(row):
    if row['status'] == 'SUCCESS':
        return ['background-color: lightgreen'] * len(row)
    elif row['status'] == 'Pending':
        return ['background-color: lightyellow'] * len(row)
    elif row['status'] == 'Error':
        return ['background-color: lightred'] * len(row)
    else:
        return [''] * len(row)



st.title("Datasets")

# Create Dataset button
if st.button("Create Dataset"):
    st.switch_page("pages/2_Create_Dataset.py")

# Fetch datasets from Supabase
response = supabase.table("datasets").select("*").execute()
datasets = response.data


if datasets:
    # Convert to DataFrame
    df = pd.DataFrame(datasets)

    # Add the "View Details" column
    df["View Details"] =  df['id'].apply(lambda x: f"<a target='_blank' href='{generate_url(x)}'>View Details</a>")
    
    # Display the dataframe

    styled_page_df = df.style.apply(highlight_rows, axis=1).set_properties(subset=['View Details'], **{'text-align': 'left'})

    st.write(styled_page_df.to_html(escape=False), unsafe_allow_html=True)

    # # Check if a dataset was selected
    # if selected_rows:
    #     selected_id = selected_rows["id"].values[0]
    #     st.session_state.selected_dataset_id = int(selected_id)
    #     st.switch_page("pages/3_Dataset_Details.py")

else:
    st.info("No datasets available. Create a new dataset to get started!")