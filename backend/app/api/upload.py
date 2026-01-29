from fastapi import APIRouter, UploadFile, File 
import tempfile 
from backend.app.rag.retriever import get_vectorstore, load_and_split_pdf

router = APIRouter() 

@router.post("/upload")
async def upload_pdf(session_id:str ,file: UploadFile=File(...)):
    # save temp file 
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        path = tmp.name
        
    docs = load_and_split_pdf(path)
    
    vectorstore = get_vectorstore(namespace=session_id) 
    vectorstore.add_documents(docs)
    
    return {"status":"uploaded", "chunks":len(docs)}