from langchain_core.prompts import ChatPromptTemplate

prompt_bane = ChatPromptTemplate.from_messages([
    ("system", "You are an employee management assistant. You need to save input details and please generate more text for job_description based on skills."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])