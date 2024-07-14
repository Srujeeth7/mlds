import streamlit as st
import pandas as pd
import os
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions
from df_functions import get_file_details
import time 

st.set_page_config(page_title="Create Dataset", page_icon="➕")

# Load environment variables

# Initialize Supabase client
SUPABASE_URL = "https://txlyjbcyrijkkjnpkfqq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR4bHlqYmN5cmlqa2tqbnBrZnFxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjA4OTY0NzIsImV4cCI6MjAzNjQ3MjQ3Mn0.fc6_Hc9RV42-_wTornUfs6Am_fNQZXcb0dQlP9A-IIo"

@st.cache_resource
def init_connection():
    url = SUPABASE_URL
    key = SUPABASE_KEY
    opts = ClientOptions().replace(schema="personal_ml")
    return create_client(url, key,options = opts)

supabase = init_connection()

st.title("Create Dataset")

# File upload widget
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
df = None
if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    
    # Display the first few rows of the CSV
    st.write("Preview of the uploaded CSV:")
    st.write(df.head())

    columns = df.columns.tolist()
    data_types = df.dtypes.astype(str).tolist()
    
    # Create a dropdown for column selection
    target_col = st.selectbox("Select the Target column", columns)
 
if st.button(label = "get details"):
    if df is None:
        st.error('Please upload the df first')
    else:
        st.write("Columns and Data Types:")
        basic_details,column_info = get_file_details(df,target_col)
        st.write("Number of Rows:", basic_details['Rows'],"Number of Columns:", basic_details['Columns'])
        st.write(column_info)

if st.button(label="submit"):
    # Save the file to a fixed path

    # Create an entry in the Supabase dataset table
    table_name = "datasets"
    data = {
        "created_by": "Srujeeth",
        "status": "Pending"
    }
    
    response = supabase.table("datasets").insert(data).execute()
    max_id = supabase.table("datasets").select("id").order('id', desc=True).limit(1).execute().data[0]['id']

    save_path = f"uploads/{max_id}.csv"
    if not os.path.exists('uploads/'):
        os.makedirs('uploads/')
    
    file_path = os.path.join(save_path)
    df.to_csv(file_path, index=False)
    
    # # Get file details
    # file_size = os.path.getsize(file_path)
    # file_name = uploaded_file.name

    # https://github.com/rq/rq -- For queueing the jobs 

    time.sleep(5)
    # Create an entry in the Supabase dataset table
    # table_name = "datasets"
    # data = {
    #     "created_by": "Srujeeth",
    #     "status": "Pending"
    # }
    
    # response = supabase.table(table_name).insert(data).execute()
    
    # if response.data:
    #     st.success(f"File '{file_name}' uploaded successfully and entry created in the database.")
    # else:
    #     st.error("Failed to create entry in the database.")

# Back to Datasets button
if st.button("Back to Datasets"):
    st.switch_page("pages/1_Datasets.py")