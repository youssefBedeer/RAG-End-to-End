from fastapi import APIRouter 
from fastapi.responses import StreamingResponse 
from ..rag.pipeline import build_rag_graph 
from ..memory.chat_history import add_message, maybe_summarize, build_prompt
from ..rag.generator import get_llm

router = APIRouter() 
graph = build_rag_graph() 
llm = get_llm()

@router.post("/chat/stream")
def chat_stream(question: str, session_id: str):
    # store user prompt
    add_message(session_id, "user", question)

    # update long-term memory if needed 
    maybe_summarize(session_id, llm)

    # build prompt (summary + recent messages)
    messages = build_prompt(session_id, question)

    # Invoke graph before streaming
    result = graph.invoke({"messages": messages, "session_id": session_id})
    answer = result["answer"]
    
    # Extract text from AIMessage
    text = answer.content if hasattr(answer, 'content') else str(answer)
    
    # Store message immediately
    add_message(session_id, "assistant", text)

    def event_generator():
        yield text

    return StreamingResponse(event_generator(), media_type="text/plain")