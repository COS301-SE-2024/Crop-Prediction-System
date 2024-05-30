import os
from supabase import create_client, Client
import json

url: str = "https://iimtpbzfrdcuuklwnprq.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlpbXRwYnpmcmRjdXVrbHducHJxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTU4MTQ1MDMsImV4cCI6MjAzMTM5MDUwM30.o2gbIkgZaTQlFRLabs-abzkim462xatVumMJXo06m6w"
supabase: Client = create_client(url, key)

def sbGetFieldInfo():
    return supabase.table("fieldInfo").select("*").execute().data