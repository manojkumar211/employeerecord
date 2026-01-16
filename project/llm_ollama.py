from langchain_ollama import ChatOllama


ollama_llm = ChatOllama(
    model="mistral",
    temperature=0
)