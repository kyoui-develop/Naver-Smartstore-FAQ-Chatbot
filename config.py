import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
DATA_DIR = "./data"

# chroma
PERSIST_DIR = "./chroma_db"
COLLECTION_NAME = "faq"
os.environ["CHROMA_OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
EMBEDDING_MODEL_NAME = "text-embedding-3-small"
TOP_K = 3
# openai
MODEL_NAME = "gpt-4o-mini"
MAX_TOKENS = 8192