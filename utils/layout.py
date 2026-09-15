import streamlit as st
from PIL import Image
import os

def show_logo():
    logo_path = os.path.join("assets", "logo.png")
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        st.image(logo, width=220)  # Adjust width as needed
    else:
        st.write("GlutenGuard")  # Fallback text
