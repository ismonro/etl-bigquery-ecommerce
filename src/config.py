import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID")
CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

DATA_RAW_DIR = "data/raw"
DATA_PROCESSED_DIR = "data/processed"

