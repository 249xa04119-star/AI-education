import streamlit as st
import matplotlib.pyplot as plt
from database import init_db, save_result, fetch_results
from ai_utils import simplify_problem

init_db()

st.set_page_config(page_title="AI Adaptive Learning Platform", layout="wide")

st.title("🎓 AI Adaptive Learning & Progress Platform")

# -------------------------
# SUBJECT STRUCTURE
# -------------------------

def get_subjects(class_name, stream=None):
    primary = ["Basic Math", "English", "EVS"]
    upper = ["Mathematics", "Science", "Social Studies", "English"]
    secondary = ["Mathematics", "Physics", "Chemistry", "Biology", "English"]
    
    science_stream = ["Mathematics", "Physics", "Chemistry", "Biology"]
    commerce_stream = ["Accountancy", "Economics", "Business Studies"]
    humanities_stream = ["History", "Political Science", "Geography"]

    if class_name in ["Class 1","Class 2","Class 3","Class 4","Class 5"]:
        return primary
    elif class_name in ["Class 6","Class 7","Class 8"]:
        return upper
    elif class_name in ["Class 9","Class 10"]:
        return secondary
    elif class_name in ["Class 11","Class 12"]:
        if stream == "Science":
            return science_stream
        elif stream == "Commerce":
            return commerce_stream
        elif stream == "Humanities":
            return humanities_stream
    return ["Mathematics"]

# -------------------------
# ROLE SELECTION
# -------------------------

role = st.sidebar.selectbox("Select Role", ["Student", "Teacher"])

if role == "Student":

    name = st.text_input("Enter your name")
    class_name = st.selectbox("Select Class", [f"Class {i}" for i in range(1, 13)])

    stream = None
    if class_name in ["Class 11", "Class 12"]:
        stream = st.selectbox("Select Stream", ["Science", "Commerce", "Humanities"])

    subjects = get_subjects(class_name, stream)
    subject = st.selectbox("Select Subject", subjects)

    st.subheader("📝 Quick Quiz")

    q1 = st.radio("5 + 3 = ?", ["6", "8", "9"])
    q2 = st.radio("10 - 4 = ?", ["5", "6", "7"])

    if st.button("Submit Quiz"):
        score = 0
        if q1 == "8":
            score += 50
        if q2 == "6":
            score += 50

        if score < 40:
            risk = "High Risk 🔴"
        elif score < 60:
            risk = "Moderate Risk 🟠"
        else:
            risk = "Low Risk 🟢"

        st.success(f"Score: {score}%")
        st.info(f"Risk Level: {risk}")

        save_result(name, class_name, subject, score, risk)

        fig, ax = plt.subplots()
        ax.bar(["Score"], [score])
        ax.set_ylim(0, 100)
        st.pyplot(fig)

    st.subheader("📘 AI Word Problem Simplifier")
    problem = st.text_area("Paste your word problem here")

    if st.button("Simplify Problem"):
        if problem:
            explanation = simplify_problem(problem)
            st.write(explanation)

elif role == "Teacher":

    st.subheader("📊 Teacher Dashboard")

    data = fetch_results()

    if data:
        names = [row[0] for row in data]
        scores = [row[3] for row in data]

        fig, ax = plt.subplots()
        ax.bar(names, scores)
        ax.set_ylabel("Score")
        ax.set_title("Student Scores Overview")
        st.pyplot(fig)

        st.table(data)
    else:
        st.info("No student data available yet.")
