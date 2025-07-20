import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import os
from PIL import Image

st.title("🌱 IPA English Consonant Chart")

tab1, tab2 = st.tabs(["English Consonants", "Diacritics"])

with tab1:
    st.markdown("Consonant chart")
    st.image("https://raw.githubusercontent.com/MK316/English-linguistics/main/pages/images/Cchart.png", caption="Consonant Chart", use_container_width=True)


with tab2:
    st.markdown("📌 Diacritics to describe English sounds. (To be updated)")



    # CSS to adjust the alignment of the dropdown to match the buttons
    st.markdown("""
        <style>
        .stSelectbox div[data-baseweb="select"] {
            margin-top: -30px;  /* Adjust this value to align with the buttons */
        }
        </style>
        """, unsafe_allow_html=True)
    
    # Set up the path to the slides folder
    slides_path = "pages/diacritics/"  # Ensure this is correct relative to your app's location
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
    
    
    # Function to load and displ
