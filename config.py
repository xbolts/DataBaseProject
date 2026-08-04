import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")

if not URL or not KEY:
    print("Error: Variables SUPABASE_URL y SUPABASE_KEY no configuradas.")
    print("Crea un archivo .env con tus credenciales. Ver .env.example")
    exit(1)

supabase: Client = create_client(URL, KEY)
