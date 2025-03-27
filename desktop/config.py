import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')

if not API_KEY:
    raise ValueError("Please set OPENAI_API_KEY in your .env file")
