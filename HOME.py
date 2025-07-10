import streamlit as st

# Your HTML formatted title
title_html = """
<h1 style='text-align: center;'>
    <span style='color: #aed581;'>ExamReady:</span><br>
    <span style='color: #f9a825;'>E</span>
    <span style='color: gray;'>nglish </span>
    <span style='color: #aeea00;'>L</span>
    <span style='color: gray;'>inguistics for </span><br>
    <span style='color: #f9d34c;'>T</span>
    <span style='color: gray;'>eacher</span>
    <span style='color: #00e5ff;'>C</span>
    <span style='color: gray;'>ertification </span>
</h1>
"""

# Initial content
st.markdown(title_html, unsafe_allow_html=True)
st.write("English Linguistics: Phonetics & Phonology")
st.caption("This page will get ready for Fall 2025 semester.")

# Image placed at the bottom of the page
st.image("https://github.com/MK316/GNUET/raw/main/images/bg3.png")
