import os
from dotenv import load_dotenv, dotenv_values 

load_dotenv() 

TG_TOKEN = os.getenv("TG_TOKEN")
