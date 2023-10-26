import streamlit as st
import pandas as pd
from PIL import Image

from utils import footer
favicon = Image.open("favicon.png")
cover_pic = Image.open("news.png")

# page settings
st.set_page_config(
    page_title="South Sudan Basketball",
    page_icon=favicon,
    initial_sidebar_state="collapsed",
    layout="wide"
)


st.image(cover_pic, use_column_width=True)
st.info("News about South Sudan Basketball")


st.warning("Still under development")


footer()
