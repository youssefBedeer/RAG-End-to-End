from typing import TypedDict, List, Any
from langgraph.graph import StateGraph
from .retriever import get_vectorstore
from .generator import get_llm

class RAGState(TypedDict):
    session_id: str
    messages: List[Any]
    docs: List[Any]
    answer: Any



def build_rag_graph():

    llm = get_llm()
    
    def extract_content(message):
    # LangChain message (AIMessage / HumanMessage)
        if hasattr(message, "content"):
            return message.content

        # Dict message {"role": ..., "content": ...}
        if isinstance(message, dict):
            return message.get("content", "")

        # Fallback
        return str(message)

    

    # -----------------------------
    # Retriever Node
    # -----------------------------
    def retriever(state: RAGState):
        last_user_msg = state["messages"][-1]
        query = extract_content(last_user_msg)

        vectorstore = get_vectorstore(namespace=state["session_id"])
        
        docs = vectorstore.similarity_search(
            query,
            k=4
        )

        return {
            **state,
            "docs": docs
        }

    # -----------------------------
    # Generator Node
    # -----------------------------
    def generate(state: RAGState):
        context = "\n\n".join(
            d.page_content for d in state["docs"]
        )

        system_prompt = f"""
        You are a helpful assistant.
        Use the context below to answer.
        If the answer is not in the context, say you don't know.

        Context:
        {context}
        """

        messages = [
            {"role": "system", "content": system_prompt},
            *state["messages"]
        ]

        answer = llm.invoke(messages)

        return {
            **state,
            "answer": answer
        }

    # -----------------------------
    # Graph
    # -----------------------------
    graph = StateGraph(RAGState)

    graph.add_node("retriever", retriever)
    graph.add_node("generate", generate)

    graph.set_entry_point("retriever")
    graph.add_edge("retriever", "generate")
    graph.set_finish_point("generate")

    return graph.compile()
