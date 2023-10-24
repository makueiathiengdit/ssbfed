from utils import shorten, condensed_stats, title_cast, footer, get_value, check_connection
import streamlit as st

import pandas as pd
from PIL import Image
# from time import sleep

favicon = Image.open("favicon.png")

# page settings
st.set_page_config(
    page_title="Men's Team Players",
    page_icon=favicon,
    initial_sidebar_state="expanded",
    layout="wide"
)

internet_available = True
loading_container = st.empty()

with loading_container:
    with st.status(label="Fetching players data...", state='running') as status:
        internet_available = check_connection()
        if internet_available:
            status.update(label="done", state='complete')
        else:
            status.update(
                label="There is no internet connection", state='error')
        st.write("")

if "internet_availabe" not in st.session_state:
    st.session_state['internet_available'] = internet_available


if not internet_available:
    st.toast("No internet connection", icon="😔")

st.markdown("""
            <style>
                .details {
                    display: grid;
                    grid-template-columns: 80px 1fr;
                    gap: 0.01px;
                }
            </style>
            """, unsafe_allow_html=True)


st.info("# South Sudan Basketball Men's Team Players from 2017 to date")
st.divider()
STATS_VARIABLES = {"Points": "points",
                   "Field Goal PCT": "field_goals_pct",
                   "Three Point PCT": "three_points_pct",
                   "Two Point PCT": "two_points_pct",
                   "Free Throw PCT": "free_throws_pct",
                   "Efficiency": "efficiency",
                   "Assists": "assists",
                   "Rebounds": "rebounds",
                   "Steals": "steals",
                   "Blocks": "blocks",
                   }


default_profile = "images/default_profile.jpg"
df = pd.read_csv("data/players_boxscore.csv", parse_dates=['date'])
df['date'] = pd.to_datetime(df['date'], format="%d-%m-%Y").dt.date

roster = pd.read_csv('data/all_rosters.csv')

df = df.sort_values(by='date', ascending=False)


df['players'] = df['players'].apply(title_cast)

total_players = df['players'].unique()
items_per_row = 2


with st.container():

    for i in range(0, len(total_players)-1):
        cols = st.columns(items_per_row)
        for j in range(items_per_row):
            index = i * items_per_row + j
            if index == len(total_players):
                st.stop()

            height = "Unknown"
            position = "Unknown"
            player_stats = df[df['players'] ==
                              total_players[index]].reset_index()
            player_stats = player_stats.sort_values(by='date')
            player_name = total_players[index]

            player_info = roster[roster['player_name']
                                 == total_players[index]].reset_index()

            h_val = get_value(player_info, 'height')
            pos_val = get_value(player_info, 'position')
            p_img = get_value(player_info, 'player_img')

            if not internet_available:
                p_img = default_profile

            if p_img == "--":
                p_img = default_profile

            height = h_val
            position = pos_val

            debut = player_stats['date'].iloc[0]

            jersey_no = player_stats['jersey_number'].iloc[-1]

            with cols[j]:
                img_col, detail_col = st.columns([2, 6])
                with img_col:
                    st.image(p_img, width=150, caption=shorten(
                        total_players[index]))
                with detail_col:
                    st.markdown(f"""
                                    <div class="details">
                                        <p> Name       </p> <b><span>: {player_name}   </span></b>
                                        <p> Position   </p> <b><span>: {position}      </span></b>
                                        <p> Jersey NO  </p> <b><span>: {jersey_no}     </span></b>
                                        <p> Height     </p> <b><span>: {height}        </span></b>
                                        <p> Debut      </p> <b><span>: {debut}         </span></b>
                                    </div>
                                """,
                                unsafe_allow_html=True
                                )
                with st.expander("See Details"):
                    condensed_stats(
                        df, total_players[index], converter_fn='short')
        st.divider()


footer()


st.toast(
    "We recommend viewing this site on device with large screen for better experience. 🙏🏿")
