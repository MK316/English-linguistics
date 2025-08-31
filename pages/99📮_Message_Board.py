import streamlit as st
import streamlit.components.v1 as components

# Must be the first Streamlit call in this file:
st.set_page_config(page_title="Message Board", layout="wide")

# Optional: stretch the main container to full width
st.markdown("""
<style>
  .block-container { max-width: 100% !important; padding-left: 1rem; padding-right: 1rem; }
</style>
""", unsafe_allow_html=True)

st.caption("💙 Leave feedback, suggestions, or messages here. I’ll check them soon! 😍")
st.write("➡️ Click the **+** to post.")

# Use Padlet's EMBED URL: https://padlet.com/embed/<slug>
# PADLET_SLUG = "F25_engling"
PADLET_EMBED = "https://padlet.com/mirankim316/F25_engling"

html = f"""
<div style="display:flex; justify-content:center; width:100%;">
  <iframe
    src="{PADLET_EMBED}"
    style="width:100%; max-width:1400px; height:80vh; border:0;"
    allow="camera; microphone; display-capture"
    allowfullscreen
  ></iframe>
</div>
"""

# The component wrapper height must be >= iframe height
components.html(html, height=800, scrolling=True)
