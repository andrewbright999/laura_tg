import os
from dotenv import load_dotenv, dotenv_values 

load_dotenv() 

TG_TOKEN = os.getenv("TG_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
YA_TOKEN = os.getenv("YA_TOKEN")