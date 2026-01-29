from langchain_openai import ChatOpenAI
from backend.app.config import OPENROUTER_API_KEY, LLM_MODEL


def get_llm():
    return ChatOpenAI(
        model=LLM_MODEL,
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )
