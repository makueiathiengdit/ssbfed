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


# ------------------------- Page Header -------------------------
st.header("South Sudan Basketball Teams")
cover_container = st.container()

with cover_container:
    st.image(cover_pic)


teams = ["Men's Team", "Women's Team", "Men's Afrocan", "Junior Teams"]
men_team_tab, women_team_tab, men_afrocan_tab, junior_team_tab = st.tabs(teams)


with men_team_tab:
    st.info("Senior men's team (The Bright Stars)")
with women_team_tab:
    st.info("Senior Women's team (The Bright Starlets)")
with men_afrocan_tab:
    st.info("Snior men's afrocan team")
with junior_team_tab:
    st.info("Welcome to South Sudan Junior teams (The Next Gen)")


footer()
