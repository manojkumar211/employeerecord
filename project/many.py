import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from agent_llm import agent_executor
from database import collection
from data_cleaning import clean_text
import time
from datetime import datetime
import json
import re




def extract_multiple_employees(llm_output: str):
    """
    Converts LLM output into a list of employee dictionaries.
    Handles:
    - Single employee
    - Multiple employees
    """

    try:
        # Try direct JSON parsing
        data = json.loads(llm_output)

        # If single dict → wrap in list
        if isinstance(data, dict):
            return [data]

        # If already list
        if isinstance(data, list):
            return data

    except Exception:
        pass

    # 🔹 Fallback: regex-based splitting (LLM text output)
    employees = []
    blocks = re.split(r"\n\s*\n", llm_output.strip())

    for block in blocks:
        emp = {}
        lines = block.split("\n")
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                emp[key.strip().lower()] = value.strip()
        if emp:
            employees.append(emp)

    return employees


# -------------------------------
# CONFIG
# -------------------------------
PDF_FILE = "C:/braneenterprises/employees_brane.pdf"

st.set_page_config(page_title="Employee Agent", layout="centered")
st.title("🤖 Employee Management Assistant")

# -------------------------------
# SESSION STATE (STOP FLAG)
# -------------------------------
if "stop_execution" not in st.session_state:
    st.session_state.stop_execution = False

# -------------------------------
# CONTROL BUTTONS
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Submit"):
        st.session_state.stop_execution = False
        run_agent = True
    else:
        run_agent = False

with col2:
    if st.button("⛔ Stop"):
        st.session_state.stop_execution = True
        st.warning("Execution stopped by user.")

# -------------------------------
# USER INPUT
# -------------------------------
user_input = st.text_area(
    "Enter the Employee Details",
    placeholder="Create employee sno 1 name Manoj age 28 department AI ..."
)

# -------------------------------
# PROCESS INPUT
# -------------------------------
if run_agent:

    if user_input.strip() == "":
        st.warning("Please enter employee details.")

    elif st.session_state.stop_execution:
        st.warning("Execution cancelled.")

    else:
        with st.spinner("Processing..."):

            # 🔹 Clean input
            cleaned_user_input = clean_text(user_input)

            # 🔹 STOP CHECK BEFORE LLM CALL
            if st.session_state.stop_execution:
                st.warning("Stopped before agent execution.")
                st.stop()

            response = agent_executor.invoke({
                "input": cleaned_user_input
            })

        # 🔹 STOP CHECK AFTER LLM CALL
        if st.session_state.stop_execution:
            st.warning("Stopped after agent execution.")
            st.stop()

        output = response.get("output", "No response generated")

        # Display response
        st.success("Agent Response")
        st.write(output)

        # Save to MongoDB
        # 🔹 Extract multiple employees
        employees = extract_multiple_employees(output)

        if not employees:
            st.warning("No employee records found to save.")
        else:
            for emp in employees:
                emp["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            collection.insert_many(employees)

            st.success(f"Saved {len(employees)} employee records to MongoDB")

        st.info("Saved response to MongoDB")

# -------------------------------
# PDF EXPORT FUNCTION
# -------------------------------
def export_mongodb_to_pdf():
    data = list(collection.find({}, {"_id": 0}))
    if not data:
        return False

    pdf = SimpleDocTemplate(
        PDF_FILE,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    story = []

    for idx, emp in enumerate(data, start=1):

        # 🔴 STOP CHECK DURING PDF LOOP
        if st.session_state.stop_execution:
            st.warning("PDF generation stopped.")
            return False

        story.append(Paragraph(f"<b>Record {idx}</b>", styles["Heading3"]))
        story.append(Spacer(1, 0.2 * inch))

        for key, value in emp.items():
            story.append(Paragraph(f"<b>{key}</b>: {value}", styles["Normal"]))
            story.append(Spacer(1, 0.1 * inch))

        story.append(Spacer(1, 0.3 * inch))
        story.append(Paragraph("-" * 80, styles["Normal"]))
        story.append(Spacer(1, 0.3 * inch))

        time.sleep(0.05)  # allows stop button to respond

    pdf.build(story)
    return True

# -------------------------------
# PDF EXPORT BUTTON
# -------------------------------
st.divider()

if st.button("📄 Export MongoDB to PDF"):
    st.session_state.stop_execution = False

    with st.spinner("Generating PDF..."):
        success = export_mongodb_to_pdf()

    if success:
        st.success(f"PDF exported successfully to:\n{PDF_FILE}")
    else:
        st.error("PDF generation stopped or no data found.")
