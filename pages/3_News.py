import streamlit as st
import pandas as pd
from PIL import Image

from utils import footer
favicon = Image.open("favicon.png")
cover_pic = Image.open("cover.png")

# page settings
st.set_page_config(
    page_title="South Sudan Basketball",
    page_icon=favicon,
    initial_sidebar_state="collapsed"
)


st.info("News about South Sudan Basketball")


st.warning("Still under development")
