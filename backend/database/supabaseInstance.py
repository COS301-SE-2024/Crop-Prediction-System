from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Singleton class
class supabaseInstance:
    __instance = None # private instance variable

    def __init__(self):
        # Load environment variables
        load_dotenv()

        # Get Supabase URL and Key
        self.url = os.environ.get("SUPABASE_URL")
        self.key = os.environ.get("SUPABASE_KEY")

        # Create Supabase client
        self.sbClient: Client = create_client(self.url, self.key)

    def get_client(self):
        if not supabaseInstance.__instance:
            supabaseInstance.__instance = supabaseInstance()

        return supabaseInstance.__instance.sbClient