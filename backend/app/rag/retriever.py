from langchain_community.document_loaders import PyPDFLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone
from ..config import * 

def load_and_split_pdf(file_path:str):
    # load pdf 
    try:
        ## load text
        loader = PyPDFLoader(file_path=file_path)
        documents = loader.load()
        
        ## split into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        
        return text_splitter.split_documents(documents)
    
    except Exception as e:
        raise ValueError(f"Failed to load or split documents: {e}")
    
    
    
def create_index():
    """create pinecone index if not exist""" 
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    existing_indexes = pc.list_indexes().names()
    
    if PINECONE_INDEX not in existing_indexes:
        pc.create_index(
            name= PINECONE_INDEX,
            dimension=INDEX_DIMENSION,
            metric=INDEX_METRIC,
            spec={
                "serverless":{
                    "cloud":"aws",
                    "region": "us-east-1"
                }
            }
        )
        
        
def get_vectorstore():
    return PineconeVectorStore.from_existing_index(
        index_name=PINECONE_INDEX,
        embedding=HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL)
    )
    
if __name__ == "__main__":
    docs = load_and_split_pdf(r"D:\Programming\ML\End-to-End\GenAi\RAG-End-to-End\backend\app\data\cv.pdf")
    print(f"Number of chunks {len(docs)}")