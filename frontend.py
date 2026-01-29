import streamlit as st
import requests
import uuid
from datetime import datetime
import os
import hashlib


# Configure Streamlit page
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-container {
        max-width: 900px;
        margin: 0 auto;
    }
    .chat-message {
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 8px;
        word-wrap: break-word;
    }
    .user-message {
        background-color: #e8f4f8;
        text-align: right;
        margin-left: 20%;
    }
    .assistant-message {
        background-color: #f0f0f0;
        margin-right: 20%;
    }
    .upload-container {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 8px;
        border: 2px dashed #ccc;
    }
</style>
""", unsafe_allow_html=True)

# Backend configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# Header
st.title("🤖 RAG Chatbot")
st.markdown("Ask questions about your uploaded documents")


if "uploaded_file_hashes" not in st.session_state:
    st.session_state.uploaded_file_hashes = set()

# Sidebar for file upload and settings
with st.sidebar:
    st.header("📁 Document Management")
    
    uploaded_file = st.file_uploader(
        "Upload PDF documents",
        type=["pdf"],
        key=f"pdf_uploader_{st.session_state.session_id}"
    )
    
    if uploaded_file is not None:
        file_bytes = uploaded_file.getvalue()
        file_hash = hashlib.md5(file_bytes).hexdigest()
        
        if file_hash not in st.session_state.uploaded_file_hashes:

            with st.spinner("Uploading and processing document..."):
                try:
                    # Prepare file for upload
                    files = {"file": (uploaded_file.name, file_bytes, "application/pdf")}

                    
                    # Send to backend
                    response = requests.post(
                        f"{BACKEND_URL}/upload",
                        params={"session_id": st.session_state.session_id},
                        files=files,
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.session_state.uploaded_file_hashes.add(file_hash)

                        st.session_state.uploaded_files.append({
                            "name": uploaded_file.name,
                            "chunks": result.get("chunks", 0),
                            "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        st.success(f"✅ Document processed! ({result.get('chunks', 0)} chunks)")
                    else:
                        st.error(f"❌ Upload failed: {response.status_code}")
                except Exception as e:
                    st.error(f"❌ Error uploading file: {str(e)}")
                    
        else:
            st.info("✅ Document already uploaded (skipped)")
    
    # Display uploaded files
    if st.session_state.uploaded_files:
        st.subheader("Uploaded Documents")
        for file_info in st.session_state.uploaded_files:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"📄 {file_info['name']}")
                st.caption(f"Chunks: {file_info['chunks']} | {file_info['uploaded_at']}")
            with col2:
                pass  # Could add delete button here
    
    # Session info
    st.divider()
    st.subheader("Session Info")
    st.caption(f"Session ID: `{st.session_state.session_id[:8]}...`")
    
    if st.button("🔄 Start New Session"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.chat_history = []
        st.session_state.uploaded_files = []
        st.session_state.uploaded_file_hashes = set()
        st.rerun()


# Main chat interface
st.subheader("💬 Chat")

# Display chat history
chat_container = st.container(height=400)
with chat_container:
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(
                f'<div class="chat-message user-message"><b>You:</b> {message["content"]}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="chat-message assistant-message"><b>Assistant:</b> {message["content"]}</div>',
                unsafe_allow_html=True
            )

# Input area
col1, col2 = st.columns([0.85, 0.15])
with col1:
    user_input = st.text_input(
        "Ask a question about your documents...",
        key="chat_input",
        placeholder="Type your question here..."
    )

with col2:
    send_button = st.button("Send", use_container_width=True, type="primary")

# Handle message submission
if send_button and user_input.strip():
    # Add user message to history
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })
    
    with st.spinner("🤔 Thinking..."):
        try:
            # Send to backend
            response = requests.post(
                f"{BACKEND_URL}/chat/stream",
                params={
                    "question": user_input,
                    "session_id": st.session_state.session_id
                },
                timeout=60
            )
            
            if response.status_code == 200:
                assistant_response = response.text
                
                # Add assistant message to history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": assistant_response
                })
                st.rerun()
            else:
                st.error(f"❌ Error getting response: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error(f"❌ Cannot connect to backend at {BACKEND_URL}")
            st.info("Make sure the backend is running: `python -m uvicorn backend.app.main:app --reload`")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

# Footer with instructions
st.divider()
st.markdown("""
### 📖 How to use:
1. **Upload Documents** - Use the sidebar to upload PDF files
2. **Ask Questions** - Type your question about the documents in the chat box
3. **Get Answers** - The RAG system will find relevant content and generate answers
4. **New Session** - Click "Start New Session" to clear chat history

### 🔧 Backend Status:
""")

try:
    health = requests.get(f"{BACKEND_URL}/", timeout=5)
    if health.status_code == 200:
        st.success("✅ Backend is running")
    else:
        st.warning("⚠️ Backend returned unexpected status")
except:
    st.error("❌ Backend is not running")
