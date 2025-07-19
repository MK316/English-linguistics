import streamlit as st

st.set_page_config(page_title="Interactive Vowel Chart")

st.title("🟦 Interactive IPA Vowel Chart")

# Define vowels by height and backness
vowels = {
    'high': {'front': 'i', 'central': 'ɨ', 'back': 'u', 'front2': 'ɪ', 'back2': 'ʊ'},
    'mid': {'front': 'e', 'front2': 'ɛ', 'central': 'ə', 'back': 'o', 'back2': 'ɔ'},
    'low': {'front': 'æ', 'central': 'a', 'back': 'ɑ'}
}

# Initialize selection state in session
if 'selected' not in st.session_state:
    st.session_state.selected = None

# Function to create vowel cell as a button
def vowel_button(label, key):
    is_selected = st.session_state.selected == key
    btn_style = """
        <style>
        div.stButton > button {{
            background-color: {};
            color: {};
            width: 3em;
            height: 2em;
            font-size: 1.2em;
            border-radius: 0.3em;
        }}
        </style>
    """.format('darkblue' if is_selected else '#f0f0f0',
               'white' if is_selected else 'black')

    st.markdown(btn_style, unsafe_allow_html=True)
    if st.button(label, key=key):
        st.session_state.selected = key

# Layout
st.write("Click on any vowel to highlight it.")

# Build the table manually
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**front**")
with col2:
    st.markdown("**central**")
with col3:
    st.markdown("**back**")

# Row: High
col1, col2, col3 = st.columns(3)
with col1:
    vowel_button('i', 'high_front')
    vowel_button('ɪ', 'high_front2')
with col2:
    vowel_button('ɨ', 'high_central')
with col3:
    vowel_button('u', 'high_back')
    vowel_button('ʊ', 'high_back2')

# Row: Mid
col1, col2, col3 = st.columns(3)
with col1:
    vowel_button('e', 'mid_front')
    vowel_button('ɛ', 'mid_front2')
with col2:
    vowel_button('ə', 'mid_central')
with col3:
    vowel_button('o', 'mid_back')
    vowel_button('ɔ', 'mid_back2')

# Row: Low
col1, col2, col3 = st.columns(3)
with col1:
    vowel_button('æ', 'low_front')
with col2:
    vowel_button('a', 'low_central')
with col3:
    vowel_button('ɑ', 'low_back')
