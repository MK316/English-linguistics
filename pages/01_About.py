import streamlit as st



tab1, tab2 = st.tabs(["Overview", "Schedule"])

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
    st.header("7-Week Schedule")
    st.markdown(
        """
| Week | Date | Slide   | Reading     | Quiz      |
|-----:|:-----|:--------|:------------|:----------|
| 1    | TBD  | Slide 1 | AEP Ch. 1   | —         |
| 2    | TBD  | Slide 2 | AEP Ch. 2   | Quiz 1    |
| 3    | TBD  | Slide 3 | AEP Ch. 3   | —         |
| 4    | TBD  | Slide 4 | AEP Ch. 4   | Quiz 2    |
| 5    | TBD  | Slide 5 | AEP Ch. 5   | —         |
| 6    | TBD  | Slide 6 | AEP Ch. 6   | Quiz 3    |
| 7    | TBD  | Slide 7 | Review Pack | Final Quiz|
        """
    )
