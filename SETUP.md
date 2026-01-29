# RAG End-to-End Project Setup

This project consists of a FastAPI backend and a Streamlit frontend for a Retrieval-Augmented Generation (RAG) chatbot.

## Prerequisites
- Python 3.8+
- pip or conda

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up Environment Variables
Create a `.env` file in the project root with your API keys:
```env
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=your_pinecone_environment
BACKEND_URL=http://localhost:8000
```

## Running the Application

### Terminal 1: Start the Backend
```bash
python -m uvicorn backend.app.main:app --reload
```
The backend will run on `http://localhost:8000`

### Terminal 2: Start the Frontend
```bash
streamlit run frontend.py
```
The frontend will open in your browser at `http://localhost:8501`

## Usage

1. **Upload Documents**: Use the sidebar to upload PDF files
2. **Ask Questions**: Type questions about the uploaded documents
3. **Get Answers**: The RAG system retrieves relevant content and generates responses
4. **Manage Sessions**: Each session maintains its own chat history

## Project Structure
```
├── backend/
│   └── app/
│       ├── main.py                 # FastAPI app entry point
│       ├── config.py               # Configuration
│       ├── api/
│       │   ├── chat.py            # Chat endpoint
│       │   └── upload.py          # File upload endpoint
│       ├── rag/
│       │   ├── pipeline.py        # RAG pipeline
│       │   ├── retriever.py       # Vector retrieval
│       │   └── generator.py       # LLM generation
│       └── memory/
│           └── chat_history.py    # Session management
├── frontend.py                     # Streamlit UI
├── requirements.txt               # Dependencies
└── SETUP.md                       # This file
```

## Features

### Backend
- **FastAPI**: Modern async REST API
- **RAG Pipeline**: LangGraph-based retrieval and generation
- **Vector Storage**: Pinecone for document embeddings
- **Chat Memory**: Session-based conversation history
- **Streaming**: Server-sent events for real-time responses

### Frontend
- **Streamlit**: Interactive web interface
- **File Upload**: PDF document processing
- **Chat UI**: Real-time conversation interface
- **Session Management**: Independent chat sessions
- **Backend Status**: Health check indicator

## API Endpoints

- `GET /` - Health check
- `POST /upload` - Upload and process PDF documents
- `POST /chat/stream` - Stream chat responses with RAG

## Troubleshooting

### Backend not responding
- Ensure backend is running: `python -m uvicorn backend.app.main:app --reload`
- Check if it's accessible at `http://localhost:8000`

### Upload fails
- Verify file is a valid PDF
- Check backend logs for errors
- Ensure temp directory has write permissions

### No responses from chat
- Verify documents are uploaded (check console logs)
- Check API keys in `.env` file
- Review backend logs for LLM errors

## Notes
- Each chat session is identified by a unique session ID
- Chat history is maintained in memory during the session
- Uploaded documents are processed into vector embeddings
- Sessions can be reset from the sidebar
