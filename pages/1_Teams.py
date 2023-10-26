import streamlit as st
import pandas as pd
from PIL import Image
from utils import get_data, load_css
from utils import footer
favicon = Image.open("favicon.png")
cover_pic = Image.open("cover.png")

# page settings
st.set_page_config(
    page_title="Teams",
    page_icon=favicon,
    initial_sidebar_state="expanded",
    layout="wide",
    menu_items={
        'Get Help': "https://twitter.com/awetthon",
        'Report a bug': "https://twitter.com/awetthon",
        'About ': "# South Sudan Basketball Stats web app built with ❤ by [Awet Thon](twitter.com/awetthon)"
    }
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
    st.warning("This page is still under development.")
with women_team_tab:
    st.info("Senior Women's team (The Bright Starlets)")
    st.warning("This page is still under development.")

with men_afrocan_tab:
    st.info("Snior men's afrocan team")
    st.warning("This page is still under development.")

with junior_team_tab:
    st.info("Welcome to South Sudan Junior teams (The Next Gen)")
    st.warning("This page is still under development.")


games_in_brief = get_data("data/games_in_brief.csv")
games_in_brief = pd.read_csv("data/games_in_brief.csv")

st.info("# Games and Results")

css = load_css("styles.css")
st.markdown(f"<style>{css} </style>", unsafe_allow_html=True)


game_container = f"""<div class='game-card-container'>"""

for j in range(0, len(games_in_brief)-2, 2):
    for i in range(2):
        try:
            home_team = games_in_brief.iloc[j]
            away_team = games_in_brief.iloc[j+1]
        except:
            st.stop()

        output = f"""<div class='game-card winner-a'>
                        <div class='game-date'>
                            <h6>{home_team['date']}</h6>
                            <h6>{home_team['tournament']}</h6>
                        </div>
                        <div class='game-results'>
                            <div class='team-a'>
                            <h2>{home_team['team']}</h2>
                            <h3>{home_team['final_score']}</h3>
                            </div>
                            <div class='team-b'>
                            <h2>{home_team['opponent']}</h2>
                            <h3>{away_team['final_score']}</h3>
                            </div>
                        </div>
                        <div class='game-date'>
                            <h6>{home_team['group']}</h6>
                        </div>
                    </div> """
        game_container += output
        j += 1


footer()

st.toast("This page is still work in progress.")
