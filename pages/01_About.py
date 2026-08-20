import streamlit as st



tab1, tab2 = st.tabs(["🍰 Overview", "🍋 Schedule"])

# --- Tab 1: Overview ---
with tab1:
    st.header("Overview")
    st.write("This platform will offer interactive apps and resources designed to help English education majors prepare for the Teacher Certification Exam.")
    st.caption("Last updated: Aug. 20, 2026")
    st.divider()
    st.markdown(
        """
- **Purpose:** Build core knowledge and test strategies for the Teacher Certification Exam.  
- **What you’ll use:** Lectuer slides, interactive apps, and weekly practice quizzes.  
        """
    )
    st.info("Tip: Skim the slides before reading; it makes the chapter easier to navigate.")

# --- Tab 2: Schedule (Markdown table) ---
with tab2:
    st.markdown("### 🍒 [Course Schedule](https://docs.google.com/spreadsheets/d/1DlN2eMmgFDrhfuHu0iaGX6_EYoEQfOUDJKI72zJs0VA/edit?usp=sharing)")


    ### 🍒 Course evaluation

    + Attendance & class participation (10%)
    + Assignment (20%): quiz-making + TCE question review
    + Quizzes (20%): 5 quizzes
    + Exam (50%)

    """)
