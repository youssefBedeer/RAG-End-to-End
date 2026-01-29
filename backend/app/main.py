from fastapi import FastAPI 
from contextlib import asynccontextmanager
from backend.app.rag.retriever import create_index 
from backend.app.api import upload, chat 

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_index() 
    yield
    

app = FastAPI(
    title="RAG API",
    version="1.0.0",
    lifespan=lifespan
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(upload.router)
app.include_router(chat.router)

@app.get("/")
def health_check():
    return {"status":"working"}