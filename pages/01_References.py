import streamlit as st

st.set_page_config(page_title="Reference List", layout="wide")
st.markdown("#### 📚 Reference List (Phonetics & Phonology)")

books = [
    {
        "title": "*A Course in Phonetics* (Peter Ladefoged & Keith Johnson)",
        "intro": "A widely used textbook offering a clear overview of articulatory and acoustic phonetics. Suitable for both beginners and advanced learners.",
        "link": "https://www.cengage.com/c/a-course-in-phonetics-8e-ladefoged/",
        "image": "https://github.com/MK316/English-linguistics/raw/main/pages/images/Ladefoged.png"
    },
    {
        "title": "*Applied English Phonology* (Mehmet Yavaş)",
        "intro": "Bridges phonological theory and its application to English pronunciation, especially in second language learning contexts.",
        "link": "https://www.wiley.com/en-us/Applied+English+Phonology%2C+3rd+Edition-p-9781118944521",
        "image": "https://github.com/MK316/English-linguistics/raw/main/pages/images/AEP.png"
    },
    {
        "title": "*English Phonetics and Phonology* (Philip Carr)",
        "intro": "An introductory guide to English phonology with a focus on theory and analysis. Useful for students studying linguistics or English language.",
        "link": "https://www.wiley.com/en-us/English+Phonetics+and+Phonology%3A+An+Introduction%2C+3rd+Edition-p-9781118511808",
        "image": "https://github.com/MK316/English-linguistics/raw/main/pages/images/Carr.png"
    },
    {
        "title": "*Introducing Phonetics and Phonology* (M. Davenport & Hannah S. J.)",
        "intro": "Covers both the descriptive and theoretical aspects of English phonetics and phonology, with helpful exercises and diagrams.",
        "link": "https://www.cambridge.org/core/books/english-phonetics-and-phonology/0C0DC6BD95A785BE3BE4E3F6E91AEF20",
        "image": "https://github.com/MK316/English-linguistics/raw/main/pages/images/feature.png"
    }
]

# Display books in two columns
cols = st.columns(2)
for i, book in enumerate(books):
    with cols[i % 2]:
        st.image(book["image"], width=150)
        st.markdown(f"**{book['title']}**")
        st.caption(book["intro"])
        st.markdown(f"[🔗 View Online]({book['link']})")
        st.markdown("---")
