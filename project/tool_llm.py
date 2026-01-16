from database import collection
from langchain.tools import tool
from datetime import datetime

@tool
def employee_created_tool(
    sno: int,
    name: str,
    age: int,
    department: str,
    role: str,
    email: str,
    skills: str,
    job_description: str
) -> str:
    """
    Store employee details into MongoDB.
    """
    collection.insert_one({
        "sno": sno,
        "name": name,
        "age": age,
        "department": department,
        "role": role,
        "email": email,
        "skills": skills,
        "job_description": job_description,
        "created_at": datetime.utcnow()
    })

    return f"Employee {name} created successfully."