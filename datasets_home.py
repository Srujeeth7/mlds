import streamlit as st
import pandas as pd 
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions

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


st.header("Dataset Upload",divider=True)
train_df = st.file_uploader(label="Upload your train dataset",type= ['csv','json','xlsx'])
test_df = st.file_uploader(label="Upload your test dataset",type=['csv','json','xlsx'])

if train_df:
    train_df = pd.read_csv(train_df)
    # st.write(supabase.schema("personal_ml").table("datasets").select("*").execute())
    response = supabase.schema("personal_ml").table("datasets").insert({"status":"pending",
                                                  "created_by":"srujeeth"}).execute()
    if response.data:
        st.success('file uploaded successfully')
    else:
        st.error('Failed to create an entry')
    st.header('Sample Train Dataset',divider=True)
    st.dataframe(train_df.head())


@st.cache_data()
def run_query():
    return supabase.table("datasets").select("*").execute()

