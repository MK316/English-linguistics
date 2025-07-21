import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import os
from PIL import Image

# st.set_page_config(page_title="Reference List", layout="wide")
tab1, tab2 = st.tabs(["🌀 Lecture Slides", "🌀 References"])

# CSS to adjust the alignment of the dropdown to match the buttons
st.markdown("""
    <style>
    .stSelectbox div[data-baseweb="select"] {
        margin-top: -30px;  /* Adjust this value to align with the buttons */
    }
    </style>
    """, unsafe_allow_html=True)

# Set up the path to the slides folder
slides_path = "pages/Slides/"  # Ensure this is correct relative to your app's location
slide_files = sorted([f for f in os.listdir(slides_path) if f.endswith(".jpeg")])
num_slides = len(slide_files)

# Initialize session state variables if they do not exist

# Initialize session state variables if they do not exist
if "slide_index" not in st.session_state:
    st.session_state.slide_index = 0  # Start with the first slide

# Check if there are slides in the folder
if num_slides == 0:
    st.error("No slides found in the specified folder.")
    st.stop()  # Stop the app if there are no slides


# Function to load and display the image based on the current index with resizing
def display_image():
    slide_path = os.path.join(slides_path, slide_files[st.session_state.slide_index])
    image = Image.open(slide_path)
    
    # Set your desired width for resizing
    desired_width = 1200  # Adjust this value as needed
    aspect_ratio = image.height / image.width
    new_height = int(desired_width * aspect_ratio)
    resized_image = image.resize((desired_width, new_height))

    st.image(resized_image, caption=f"Slide {st.session_state.slide_index + 1} of {num_slides}")


with tab1:

    # Arrange 'Start', 'Previous', 'Next', and 'Slide Selector' in a single row
    col1, col2, col3, col4 = st.columns([1, 1, 1, 5])
    
    with col1:
        if st.button("⛳", key="start", help="Reset to the first slide"):
            st.session_state.slide_index = 0

    with col2:
        if st.button("◀️", key="previous", help="Go back to the previous slide"):
            if st.session_state.slide_index > 0:
                st.session_state.slide_index -= 1
            else:
                st.warning("This is the first slide.")

    with col3:
        if st.button("▶️", key="next", help="Go to the next slide"):
            if st.session_state.slide_index < num_slides - 1:
                st.session_state.slide_index += 1
            else:
                st.warning("Final slide")

    with col4:
        # Display slide selector dropdown
        selected_slide = st.selectbox("",
                                      options=[f"Slide {i + 1}" for i in range(num_slides)],
                                      index=st.session_state.slide_index)

        # Update slide index if dropdown selection changes
        selected_slide_index = int(selected_slide.split()[-1]) - 1
        if selected_slide_index != st.session_state.slide_index:
            st.session_state.slide_index = selected_slide_index

    # Display the image
    display_image()

    st.markdown("---")
    st.caption("Part II: Slides 127~ Diachrony, Phonotactices, Rhotacism")
    st.caption("Part II: Slides 152~ Stress, foot")
    st.caption("Part III: Slides 164~ Phonology & Morphology")
    st.caption("Part IV: Slides 180~ Morphology")


# ------------ Tab2

with tab2:
    
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
            "intro": "An introductory guide to English phonology with a focus on theory and analysis. Useful for students studying linguistics or English language. It includes chapters on stress and foot structure.",
            "link": "https://www.wiley.com/en-us/English+Phonetics+and+Phonology%3A+An+Introduction%2C+3rd+Edition-p-9781118511808",
            "image": "https://github.com/MK316/English-linguistics/raw/main/pages/images/Carr.png"
        },
        {
            "title": "*Introducing Phonetics and Phonology* (M. Davenport & Hannah S. J.)",
            "intro": "Covers both the descriptive and theoretical aspects of English phonetics and phonology, with helpful exercises and diagrams. This book provides a clear introduction to distinctive features.",
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
