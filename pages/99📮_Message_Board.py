import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Padlet Wall", layout="wide")

# Stretch Streamlit's main container to full width (optional but helps)
st.markdown("""
<style>
  .block-container { max-width: 100% !important; padding-left: 1rem; padding-right: 1rem; }
</style>
""", unsafe_allow_html=True)

st.caption("💙 Leave feedback, suggestions, or messages here. I’ll check them soon! 😍")
st.write("➡️ Click the **+** to post.")

# Use Padlet's EMBED URL (not the normal page URL)
# If your share panel gives a different embed path, paste it here.
padlet_url = "https://padlet.com/embed/mirankim316/F25_engling"

# Center the iframe and give it a generous width; height is the component's outer height.
html = f"""
<div style="display:flex; justify-content:center; width:100%;">
  <iframe
    src="{padlet_url}"
    style="width:100%; max-width:1400px; height:80vh; border:0;"
    allow="camera; microphone; display-capture"
    allowfullscreen
  ></iframe>
</div>
"""

# The Streamlit component height must be >= iframe height; adjust if needed.
components.html(html, height=800, scrolling=True)
