from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from tool_llm import employee_created_tool
from llm_ollama import ollama_llm
from prompt_llm import prompt_bane

agent = create_tool_calling_agent(
    llm=ollama_llm,
    tools=[employee_created_tool],
    prompt=prompt_bane
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=[employee_created_tool],
    verbose=True
)