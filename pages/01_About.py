import streamlit as st



tab1, tab2 = st.tabs(["🍰 Overview", "🍋 Schedule"])

# --- Tab 1: Overview ---
with tab1:
    st.header("Overview")
    st.write("This platform will offer interactive apps and resources designed to help English education majors prepare for the Teacher Certification Exam.")
    st.caption("Since July 10, 2025")
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
    st.markdown("### 🍒 7-Week Schedule")
    st.markdown("#### Wednesdays (2~5PM)")
    st.markdown(
        """
| Week | Date | Slide   | Reading     | Quiz      |
|-----:|:-----|:--------|:------------|:----------|
| 1    | Sept. 3  | Slides 1~45 |   | —         |
| 2    | Sept. 10  | Slides 46~ | AEP Ch. 1&2   | Quiz #1 (Group 1)    |
| 3    | Sept. 17  | Slides  | AEP Ch. 3   | Quiz #2 (Group 2)        |
| 4    | Sept. 24  | Slides  | AEP Ch. 4   |  Quiz #3 (Group 3)   |
| 5    | Oct. 1*  | Slides  | AEP Ch. 6   | Quiz #4 (Group 4)        |
| 6    | TBA  | Slide 6 | AEP Ch. 7   | ---   |
| 7    | TBA  | Slide 7 | Review Pack | Quiz #5 (Final Quiz)|
        """
    )
    st.divider()
    st.markdown("""

    ### 🍒 Course evaluation

    + Attendance & class participation (5%)
    + Assignment (10%): Readings & question-making
    + Quizzes (35%): 5 quizzes

    """)
