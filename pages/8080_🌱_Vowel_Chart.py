import streamlit as st

st.set_page_config(page_title="Interactive IPA Vowel Chart")

st.title("🟦 Interactive IPA Vowel Chart")
st.write("Click on any vowel to highlight it.")

# Session state for selection
if "selected" not in st.session_state:
    st.session_state.selected = None

def vowel_button(label, key):
    selected = st.session_state.selected == key
    style = f"""
        <style>
        div[data-testid="stButton"] button[{key}] {{
            background-color: {"darkblue" if selected else "#f0f0f0"};
            color: {"white" if selected else "black"};
            width: 3em;
            height: 2em;
            font-size: 1.2em;
            border-radius: 0.3em;
        }}
        </style>
    """
    # Unique selector workaround using the key as attribute
    st.markdown(f"<div {key}></div>", unsafe_allow_html=True)
    st.markdown(style, unsafe_allow_html=True)
    if st.button(label, key=key):
        st.session_state.selected = key

# Custom row layout with height label on the left
def row_with_label(label, front=None, central=None, back=None):
    col0, col1, col2, col3 = st.columns([1, 2, 2, 2])
    with col0:
        st.markdown(f"**{label}**")
    with col1:
        if front: vowel_button(front, f"{label}_front_{front}")
    with col2:
        if central: vowel_button(central, f"{label}_central_{central}")
    with col3:
        if back: vowel_button(back, f"{label}_back_{back}")

# Table headers
col0, col1, col2, col3 = st.columns([1, 2, 2, 2])
with col0:
    st.markdown(" ")
with col1:
    st.markdown("**front**")
with col2:
    st.markdown("**central**")
with col3:
    st.markdown("**back**")

# High row
row_with_label("high", front="i", central="ɨ", back="u")
row_with_label("high", front="ɪ", central=None, back="ʊ")

# Mid row
row_with_label("mid", front="e", central="ə", back="o")
row_with_label("mid", front="ɛ", central=None, back="ɔ")

# Low row
row_with_label("low", front="æ", central="a", back="ɑ")
