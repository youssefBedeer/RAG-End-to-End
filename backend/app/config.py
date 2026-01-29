import os 
from dotenv import load_dotenv 
load_dotenv() 

# Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = "rag-index"
INDEX_DIMENSION = 384  # all-MiniLM-L6-v2 output size
INDEX_METRIC = "cosine"

# Embeddings  
EMBEDDINGS_MODEL = "BAAI/bge-small-en-v1.5"

# LLM 
LLM_MODEL = "meta-llama/llama-3.1-8b-instruct"
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")