import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from agent_llm import agent_executor
from database import collection

# -------------------------------
# CONFIG
# -------------------------------
PDF_FILE = "C:/baneenterprises/employees_bane.pdf"

st.set_page_config(page_title="Employee Agent", layout="centered")

st.title("🤖 Employee Management Assistant")

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
if st.button("🚀 Submit"):
    if user_input.strip() == "":
        st.warning("Please enter employee details.")
    else:
        with st.spinner("Processing..."):
            response = agent_executor.invoke({
                "input": user_input
            })

        output = response.get("output", "No response generated")

        # Display response
        st.success("Agent Response")
        st.write(output)

        # Save to MongoDB
        collection.insert_one({"LLM_response": output})
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
        story.append(Paragraph(f"<b>Record {idx}</b>", styles["Heading3"]))
        story.append(Spacer(1, 0.2 * inch))

        for key, value in emp.items():
            story.append(Paragraph(f"<b>{key}</b>: {value}", styles["Normal"]))
            story.append(Spacer(1, 0.1 * inch))

        story.append(Spacer(1, 0.3 * inch))
        story.append(Paragraph("-" * 80, styles["Normal"]))
        story.append(Spacer(1, 0.3 * inch))

    pdf.build(story)
    return True

# -------------------------------
# PDF EXPORT BUTTON
# -------------------------------
st.divider()

if st.button("📄 Export MongoDB to PDF"):
    with st.spinner("Generating PDF..."):
        success = export_mongodb_to_pdf()

    if success:
        st.success(f"PDF exported successfully to:\n{PDF_FILE}")
    else:
        st.error("No data found in MongoDB.")
