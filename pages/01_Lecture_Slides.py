import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
import os
import requests
from PIL import Image
import base64
# ---------------- Page setup ----------------
# st.set_page_config(page_title="Reference List", layout="wide")
st.set_page_config(page_title="Lecture Slide Player", layout="wide")

# ----------------- Tabs -----------------------
tab1, tab_more, tab2, tab3 = st.tabs(
    ["🌀 Lecture Slides", "🌀 More Slides", "🌀 References", "🌀 More Reading"]
)





# --------- SLIDES FOLDER (edit if needed) ----------
slides_path = "pages/Slides/F26/"  # Ensure this is correct relative to your app's location
slide_files = sorted([f for f in os.listdir(slides_path) if f.lower().endswith((".jpeg", ".jpg", ".png", ".webp"))])
num_slides = len(slide_files)
# ---------------------------------------------------

# --------- REMOTE SLIDES (Tab 2: "More Slides") ----------
# Files are named like Morphology26.001.png, Morphology26.002.png, ... on GitHub.
REMOTE_OWNER = "MK316"
REMOTE_REPO = "English-linguistics"
REMOTE_BRANCH = "main"
REMOTE_FOLDER = "pages/Slides/Morphology"
REMOTE_BASENAME = "Morphology26"
REMOTE_EXT = "png"
REMOTE_URL_TEMPLATE = (
    f"https://raw.githubusercontent.com/{REMOTE_OWNER}/{REMOTE_REPO}/{REMOTE_BRANCH}/"
    f"{REMOTE_FOLDER}/{REMOTE_BASENAME}.{{i:03d}}.{REMOTE_EXT}"
)
# ---------------------------------------------------

# ---- Session state init (Tab 1) ----
if "slide_index" not in st.session_state:
    st.session_state.slide_index = 0  # Start with the first slide
if "fit_to_height" not in st.session_state:
    st.session_state.fit_to_height = True
if "vh_percent" not in st.session_state:
    st.session_state.vh_percent = 88
if "display_width_px" not in st.session_state:
    st.session_state.display_width_px = 1200

# ---- Session state init (Tab "More Slides") ----
if "slide_index2" not in st.session_state:
    st.session_state.slide_index2 = 0
if "fit_to_height2" not in st.session_state:
    st.session_state.fit_to_height2 = True
if "vh_percent2" not in st.session_state:
    st.session_state.vh_percent2 = 88
if "display_width_px2" not in st.session_state:
    st.session_state.display_width_px2 = 1200
if "thumb_page2" not in st.session_state:
    st.session_state.thumb_page2 = 0

# Full-width option that works on both older and newer Streamlit versions
_ver = tuple(int(x) for x in st.__version__.split(".")[:2])
WIDE = {"width": "stretch"} if _ver >= (1, 46) else {"use_container_width": True}

THUMBS_PER_PAGE = 25   # thumbnails shown at a time
THUMB_COLS = 5         # thumbnails per row
if "thumb_page" not in st.session_state:
    st.session_state.thumb_page = 0

# ---- Guards ----
if num_slides == 0:
    st.error("No slides found in the specified folder.")
    st.stop()

# ---- Helpers (Tab 1: local files) ----
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

@st.cache_data(show_spinner=False)
def make_thumbnail(img_path: str, mtime: float, width_px: int = 240) -> bytes:
    """Small JPEG preview of a slide (cached; refreshed automatically when the file changes)."""
    im = Image.open(img_path)
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")
    im.thumbnail((width_px, width_px * 2), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=80, optimize=True)
    return buf.getvalue()

def num_thumb_pages() -> int:
    return (num_slides + THUMBS_PER_PAGE - 1) // THUMBS_PER_PAGE

def follow_current_slide():
    """Keep the thumbnail page on the page that contains the current slide."""
    st.session_state.thumb_page = st.session_state.slide_index // THUMBS_PER_PAGE

def go_to_slide(i: int):
    st.session_state.slide_index = i

def change_thumb_page(step: int):
    st.session_state.thumb_page = min(max(st.session_state.thumb_page + step, 0), num_thumb_pages() - 1)

# ---- Helpers (Tab "More Slides": remote GitHub images) ----
@st.cache_data(show_spinner=False, ttl=3600)
def list_remote_slides(url_template: str, max_slides: int = 300) -> list:
    """Probe sequentially numbered files (Name.001.png, Name.002.png, ...) and
    return the URLs that actually exist. Stops at the first missing number,
    assuming contiguous numbering starting at 1."""
    urls = []
    for i in range(1, max_slides + 1):
        url = url_template.format(i=i)
        try:
            r = requests.head(url, timeout=8, allow_redirects=True)
        except requests.RequestException:
            break
        if r.status_code == 200:
            urls.append(url)
        else:
            break
    return urls

@st.cache_data(show_spinner=False, ttl=3600)
def fetch_remote_bytes(url: str) -> bytes:
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.content

def display_bytes_fit_height(raw: bytes, vh_percent: int = 88):
    """Same rendering logic as display_image_fit_height, but starting from raw bytes."""
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

def display_remote_image_fit_height(url: str, vh_percent: int = 88):
    raw = fetch_remote_bytes(url)
    display_bytes_fit_height(raw, vh_percent)

def display_remote_image_fixed_width(url: str, width_px: int, slide_index: int, total: int):
    raw = fetch_remote_bytes(url)
    image = Image.open(io.BytesIO(raw))
    aspect_ratio = image.height / image.width
    new_height = int(width_px * aspect_ratio)
    resized_image = image.resize((width_px, new_height), Image.LANCZOS)
    st.image(resized_image, caption=f"Slide {slide_index + 1} of {total}")

@st.cache_data(show_spinner=False)
def make_thumbnail_from_url(url: str, width_px: int = 240) -> bytes:
    raw = fetch_remote_bytes(url)
    im = Image.open(io.BytesIO(raw))
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        im = bg
    else:
        im = im.convert("RGB")
    im.thumbnail((width_px, width_px * 2), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=80, optimize=True)
    return buf.getvalue()

def num_thumb_pages2(total: int) -> int:
    return (total + THUMBS_PER_PAGE - 1) // THUMBS_PER_PAGE

def follow_current_slide2():
    st.session_state.thumb_page2 = st.session_state.slide_index2 // THUMBS_PER_PAGE

def go_to_slide2(i: int):
    st.session_state.slide_index2 = i

def change_thumb_page2(step: int, total: int):
    st.session_state.thumb_page2 = min(max(st.session_state.thumb_page2 + step, 0), num_thumb_pages2(total) - 1)

# -------- Tabs --------

with tab1:
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
            follow_current_slide()
    with col2:
        if st.button("◀️", key="previous", help="Go back to the previous slide"):
            if st.session_state.slide_index > 0:
                st.session_state.slide_index -= 1
                follow_current_slide()
            else:
                st.warning("This is the first slide.")
    with col3:
        if st.button("▶️", key="next", help="Go to the next slide"):
            if st.session_state.slide_index < num_slides - 1:
                st.session_state.slide_index += 1
                follow_current_slide()
            else:
                st.warning("Final slide")
    with col4:
        # Dropdown selector
        selected_slide = st.selectbox(
            "Go to slide",
            options=[f"Slide {i + 1}" for i in range(num_slides)],
            index=st.session_state.slide_index,
            label_visibility="collapsed",
        )
        selected_idx = int(selected_slide.split()[-1]) - 1
        if selected_idx != st.session_state.slide_index:
            st.session_state.slide_index = selected_idx
            follow_current_slide()

    # Main display (fit to height or fixed width)
    if st.session_state.fit_to_height:
        display_image_fit_height(current_slide_path(), st.session_state.vh_percent)
        st.caption(f"Slide {st.session_state.slide_index + 1} of {num_slides}")
    else:
        display_image_fixed_width(current_slide_path(), st.session_state.display_width_px)

    st.markdown("---")

    # ---- Slide previews (25 at a time); click a number to open that slide ----
    pages = num_thumb_pages()
    page = min(st.session_state.thumb_page, pages - 1)
    first = page * THUMBS_PER_PAGE
    last = min(first + THUMBS_PER_PAGE, num_slides)

    p1, p2, p3 = st.columns([1, 2, 1])
    with p1:
        st.button("◀ Previous 25", key="thumb_prev", on_click=change_thumb_page, args=(-1,),
                  disabled=page == 0, **WIDE)
    with p2:
        st.markdown(
            f"<div style='text-align:center;padding-top:6px;'>Slide previews {first + 1}–{last} of {num_slides}</div>",
            unsafe_allow_html=True,
        )
    with p3:
        st.button("Next 25 ▶", key="thumb_next", on_click=change_thumb_page, args=(1,),
                  disabled=page >= pages - 1, **WIDE)

    for row_start in range(first, last, THUMB_COLS):
        cols = st.columns(THUMB_COLS)
        for j, i in enumerate(range(row_start, min(row_start + THUMB_COLS, last))):
            with cols[j]:
                path = os.path.join(slides_path, slide_files[i])
                st.image(make_thumbnail(path, os.path.getmtime(path)), **WIDE)
                is_current = i == st.session_state.slide_index
                st.button(
                    f"▶ Slide {i + 1}" if is_current else f"Slide {i + 1}",
                    key=f"thumb_{i}",
                    on_click=go_to_slide, args=(i,),
                    type="primary" if is_current else "secondary",
                    **WIDE,
                )


# ------------ Tab "More Slides" (same behavior as Tab 1, remote image source) ------------

with tab_more:
    slide_urls = list_remote_slides(REMOTE_URL_TEMPLATE)
    num_slides2 = len(slide_urls)

    if num_slides2 == 0:
        st.error("No slides found at the remote source.")
    else:
        # Keep index in range if the slide count changed
        if st.session_state.slide_index2 >= num_slides2:
            st.session_state.slide_index2 = 0

        # View controls
        colA, colB = st.columns([2, 3])
        with colA:
            st.toggle("Fit main slide to screen height", key="fit_to_height2")
        with colB:
            if st.session_state.fit_to_height2:
                st.slider("Height % of screen", 60, 95, key="vh_percent2")
            else:
                st.slider("Slide width (px)", 700, 1600, key="display_width_px2")

        # Nav row
        col1, col2, col3, col4 = st.columns([1, 1, 1, 5])
        with col1:
            if st.button("⛳", key="start2", help="Reset to the first slide"):
                st.session_state.slide_index2 = 0
                follow_current_slide2()
        with col2:
            if st.button("◀️", key="previous2", help="Go back to the previous slide"):
                if st.session_state.slide_index2 > 0:
                    st.session_state.slide_index2 -= 1
                    follow_current_slide2()
                else:
                    st.warning("This is the first slide.")
        with col3:
            if st.button("▶️", key="next2", help="Go to the next slide"):
                if st.session_state.slide_index2 < num_slides2 - 1:
                    st.session_state.slide_index2 += 1
                    follow_current_slide2()
                else:
                    st.warning("Final slide")
        with col4:
            selected_slide2 = st.selectbox(
                "Go to slide",
                options=[f"Slide {i + 1}" for i in range(num_slides2)],
                index=st.session_state.slide_index2,
                label_visibility="collapsed",
                key="jump_select2",
            )
            selected_idx2 = int(selected_slide2.split()[-1]) - 1
            if selected_idx2 != st.session_state.slide_index2:
                st.session_state.slide_index2 = selected_idx2
                follow_current_slide2()

        # Main display (fit to height or fixed width)
        current_url = slide_urls[st.session_state.slide_index2]
        if st.session_state.fit_to_height2:
            display_remote_image_fit_height(current_url, st.session_state.vh_percent2)
            st.caption(f"Slide {st.session_state.slide_index2 + 1} of {num_slides2}")
        else:
            display_remote_image_fixed_width(
                current_url, st.session_state.display_width_px2,
                st.session_state.slide_index2, num_slides2,
            )

        st.markdown("---")

        # ---- Slide previews (25 at a time); click a number to open that slide ----
        pages2 = num_thumb_pages2(num_slides2)
        page2 = min(st.session_state.thumb_page2, pages2 - 1)
        first2 = page2 * THUMBS_PER_PAGE
        last2 = min(first2 + THUMBS_PER_PAGE, num_slides2)

        p1, p2, p3 = st.columns([1, 2, 1])
        with p1:
            st.button("◀ Previous 25", key="thumb_prev2", on_click=change_thumb_page2,
                      args=(-1, num_slides2), disabled=page2 == 0, **WIDE)
        with p2:
            st.markdown(
                f"<div style='text-align:center;padding-top:6px;'>Slide previews {first2 + 1}–{last2} of {num_slides2}</div>",
                unsafe_allow_html=True,
            )
        with p3:
            st.button("Next 25 ▶", key="thumb_next2", on_click=change_thumb_page2,
                      args=(1, num_slides2), disabled=page2 >= pages2 - 1, **WIDE)

        for row_start in range(first2, last2, THUMB_COLS):
            cols = st.columns(THUMB_COLS)
            for j, i in enumerate(range(row_start, min(row_start + THUMB_COLS, last2))):
                with cols[j]:
                    url = slide_urls[i]
                    st.image(make_thumbnail_from_url(url), **WIDE)
                    is_current2 = i == st.session_state.slide_index2
                    st.button(
                        f"▶ Slide {i + 1}" if is_current2 else f"Slide {i + 1}",
                        key=f"thumb2_{i}",
                        on_click=go_to_slide2, args=(i,),
                        type="primary" if is_current2 else "secondary",
                        **WIDE,
                    )


# # ------------ Tab2 (References)

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

with tab3:
    st.markdown("#### 📚 More reading (Phonetics & Phonology)")
    st.caption("The following list recommends readings from other textbooks to supplement areas that are not covered or are insufficiently treated in our textbook.")
    st.divider()
    st.markdown("+ [Reading 1](https://drive.google.com/file/d/1m811NW_A-JP6byFHA5bRK-6SmGynGROn/view?usp=sharing): Stress")
    st.markdown("+ [Reading 2](https://drive.google.com/file/d/1YJ4NQ8TXmzBkvmbvQ7iRbNiDHzbZFvkf/view?usp=drive_link): Rhythm")
    st.markdown("+ [Reading 3](https://drive.google.com/file/d/1esJjtujLGfVE0LMlERg-sX52uCm8HJ8G/view?usp=sharing): Intonation")
    st.markdown("+ [Reading 4](https://drive.google.com/file/d/1esJjtujLGfVE0LMlERg-sX52uCm8HJ8G/view?usp=sharing): Distinctive features")
