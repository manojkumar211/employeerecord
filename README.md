# MongoDB & Environment Setup
## What this does
```
pymongo.MongoClient → allows Python to connect to MongoDB.

dotenv → loads sensitive values (like DB passwords) from a .env file.

load_dotenv() → reads .env.

os.getenv("MONGO_URI") → fetches MongoDB connection string securely.
```

## ✅ Why important
```
Keeps credentials out of source code and makes deployment safer.
```

# Import Shared MongoDB Collection
## What this does
```
Imports an already-created MongoDB collection object.

Prevents duplicate database connection logic everywhere.

📌 Typically inside database.py:
```

# LangChain Tool Definition (Core Logic)
## Why this matters
```
@tool allows LLM agents to call Python functions automatically.

This turns your function into an LLM-callable action.
```

# Employee Creation Tool
## What happens here
```
This function receives structured employee data.

The LLM extracts these values from user text automatically.
```

# Insert into MongoDB
## Key points
```
Inserts employee details into MongoDB

Adds created_at timestamp for auditing
```

# Return Response to LLM
```
return f"Employee {name} created successfully."
✔️ This message is shown to the user in Streamlit.
```

# Ollama LLM Configuration
## Explanation
```
Uses local LLM (Mistral) via Ollama

temperature=0 → deterministic, consistent outputs
```

# Prompt Template (LLM Brain)
## What this means
```
System message → sets role & behavior

Human message → user’s natural language input

Agent scratchpad → internal reasoning + tool calls
```
## 🧠 LLM understands:
```
“Extract employee fields → enhance job description → call MongoDB tool”
```

# Agent Creation (LLM + Tools)
## What happens
```
Creates an AI agent

Agent can:

Read text

Extract values

Call employee_created_tool
```

# Agent Executor
## Why this exists
```
Runs the agent

verbose=True → shows internal reasoning in terminal (debugging)
```

# Streamlit UI Setup
```
Creates a clean web interface.
```
## User Input Box
```
User types natural language, not forms.
```
## Submit Button Logic
### Flow
```
Validate input

Call LLM agent

Display result

Save response to MongoDB
```

## Invoke Agent
### 🧠 What LLM does internally:
```
Parses text

Generates job description

Calls employee_created_tool

Returns confirmation message
```

## Display Output
```
output
```

## Save LLM Output
```
✔️ Stores conversation result for auditing/logs
```

## PDF Export Logic (MongoDB → PDF)
### Why ReportLab
```
Converts structured data into professional PDFs
```

## Fetch MongoDB Data
```
Fetches all records

Removes MongoDB _id
```

## Build PDF
### Each record:
```
Heading

Key-value pairs

Divider
```

## Generate File
```
pdf.build(story)
```
## 📄 PDF saved to:
```
C:/baneenterprises/employees_bane.pdf
```
## Export Button in UI
```
Fetches MongoDB data

Generates PDF

Shows success/failure message
```

## Final MongoDB Connection (Redundant)
```
client = MongoClient(MONGO_URI)
db = client["baneenterprices"]
collection = db["employees"]

⚠️ Note
This is redundant because collection was already imported earlier.
You can safely remove this block.
```

# 🧠 What You’ve Built
```
✔️ AI-powered employee entry
✔️ Natural language → structured data
✔️ MongoDB persistence
✔️ Streamlit UI
✔️ PDF report generator
```
