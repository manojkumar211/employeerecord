from database import collection
from langchain.tools import tool
from datetime import datetime
from data_cleaning import clean_text

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

    name = clean_text(name)
    department = clean_text(department)
    role = clean_text(role)
    email = clean_text(email)
    skills = clean_text(skills)
    job_description = clean_text(job_description)

    
    collection.insert_many({
        "sno": sno,
        "name": name,
        "age": age,
        "department": department,
        "role": role,
        "email": email,
        "skills": skills,
        "job_description": job_description,
        "created_at": datetime.now()
    })

    return f"Employee {name} created successfully."