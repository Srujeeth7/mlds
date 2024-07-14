import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client('aws-0-ap-south-1.pooler.supabase.com', key)
dataset_path = 'datasets/'
tune_path = 'tuning_jobs/'
dataset_info = 'datasets/describe/'

