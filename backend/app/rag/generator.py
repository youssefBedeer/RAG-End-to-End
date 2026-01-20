from langchain_openai import ChatOpenAI

def get_llm():
    return ChatOpenAI(
        model="meta-llama/llama-3.1-8b-instruct",
        api_key="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",
        base_url="https://openrouter.ai/api/v1"
    )
