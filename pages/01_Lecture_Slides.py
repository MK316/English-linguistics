import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import os
from PIL import Image
import base64

# st.set_page_config(page_title="Reference List", layout="wide")
st.set_page_config(page_title="Lecture Slide Player - Chapter 1", layout="wide")
tab1, tab2 = st.tabs(["🌀 Lecture Slides", "🌀 References"])

# CSS to adjust the alignment of the dropdown to match the buttons
st.markdown("""
    <style>
    .stSelectbox div[data-baseweb="select"] {
        margin-top: -30px;  /* Adjust this value to align with the buttons */
    }
    </style>
    """, unsafe_allow_html=True)


# ---------------- Page setup ----------------

st.markdown("#### 📗 Chapter 1: Articulation and Acoustics")

# --------- SLIDES FOLDER (edit if needed) ----------
slides_path = "pages/Slides/"  # Ensure this is correct relative to your app's location
slide_files = sorted([f for f in os.listdir(slides_path) if f.lower().endswith((".jpeg", ".jpg", ".png", ".webp"))])
num_slides = len(slide_files)
# ---------------------------------------------------

# ---- Session state init ----
if "slide_index" not in st.session_state:
    st.session_state.slide_index = 0  # Start with the first slide
if "fit_to_height" not in st.session_state:
    st.session_state.fit_to_height = True
if "vh_percent" not in st.session_state:
    st.session_state.vh_percent = 88
if "display_width_px" not in st.session_state:
    st.session_state.display_width_px = 1200

# ---- Guards ----
if num_slides == 0:
    st.error("No slides found in the specified folder.")
    st.stop()

# ---- Helpers ----
def current_slide_path() -> str:
    return os.path.join(slides_path, slide_files[st.session_state.slide_index])

def display_image_fit_height(img_path: str, vh_percent: int = 88):
    """Embed as a responsive <img> that fits viewport height (no vertical scrolling)."""
    with open(img_path, "rb") as f:
        raw = f.read()
    # Convert to JPEG for faster inline transfer when possible
    try:
        im = Image.open(io.BytesIO(raw))
        if im.mode in ("RGBA", "LA"):
            bg = Image.new("RGB", im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[-1])
            im = bg
        else:
            im = im.convert("RGB")
        buf = io.BytesIO()
        im.save(buf, format="JPEG", quality=90, optimize=True)
        data = buf.getvalue()
        mime = "image/jpeg"
    except Exception:
        data = raw
        mime = "image/png"

    b64 = base64.b64encode(data).decode("ascii")
    data_uri = f"data:{mime};base64,{b64}"

    st.markdown(
        f"""
        <div style="display:flex;justify-content:center;">
          <img
            src="{data_uri}"
            alt="Slide"
            style="
              max-width: 100%;
              max-height: {vh_percent}vh;
              width: auto;
              height: auto;
              object-fit: contain;
              display: block;
            "
          />
        </div>
        """,
        unsafe_allow_html=True,
    )

def display_image_fixed_width(img_path: str, width_px: int = 1200):
    """Resize server-side to the given width, keep aspect ratio, then show."""
    image = Image.open(img_path)
    aspect_ratio = image.height / image.width
    new_height = int(width_px * aspect_ratio)
    resized_image = image.resize((width_px, new_height), Image.LANCZOS)
    st.image(resized_image, caption=f"Slide {st.session_state.slide_index + 1} of {num_slides}")

# -------- Tabs --------
tabs = st.tabs(["Slides"])
with tabs[0]:
    # View controls
    colA, colB = st.columns([2, 3])
    with colA:
        st.toggle("Fit main slide to screen height", key="fit_to_height")
    with colB:
        if st.session_state.fit_to_height:
            st.slider("Height % of screen", 60, 95, key="vh_percent")
        else:
            st.slider("Slide width (px)", 700, 1600, key="display_width_px")

    # Nav row
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
        # Dropdown selector
        selected_slide = st.selectbox(
            "",
            options=[f"Slide {i + 1}" for i in range(num_slides)],
            index=st.session_state.slide_index,
        )
        selected_idx = int(selected_slide.split()[-1]) - 1
        if selected_idx != st.session_state.slide_index:
            st.session_state.slide_index = selected_idx

    # Main display (fit to height or fixed width)
    if st.session_state.fit_to_height:
        display_image_fit_height(current_slide_path(), st.session_state.vh_percent)
        st.caption(f"Slide {st.session_state.slide_index + 1} of {num_slides}")
    else:
        display_image_fixed_width(current_slide_path(), st.session_state.display_width_px)

    st.markdown("---")




# # ------------ Tab2

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
