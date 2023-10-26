import streamlit as st
import pandas as pd
from utils import get_data, tiny_name, check_connection, set_precision, footer
from constants import STATS_VARIABLES
from PIL import Image


favicon = Image.open("favicon.png")

# page settings
st.set_page_config(
    page_title="Player Comparison",
    page_icon=favicon,
    initial_sidebar_state="expanded",
    layout="wide"
)


players_stats = get_data("data/players_boxscore.csv")
players_stats['date'] = players_stats['date'].dt.strftime("%d-%m-%Y")
players_info = pd.read_csv("data/all_rosters.csv",
                           usecols=['player_name', 'player_img'])


# internet_available = check_connection()

# if "internet_availabe" not in st.session_state:
#     st.session_state['internet_available'] = internet_available

# if not check_connection():
#     st.toast("No internet connection", icon="😔")


def format_df(df):
    formatted_df = df.style \
        .set_table_styles([
            {'selector': 'th:nth-child(1)', 'props': 'text-align: right;'},
            {'selector': 'th:nth-child(3)', 'props': 'text-align: left;'},
            {'selector': 'td:nth-child(1)', 'props': 'text-align: right;'},
            {'selector': 'td:nth-child(3)', 'props': 'text-align: left;'}
        ])
    return formatted_df


css = """
        <style>
                    tr th[scope="col"]:first-child{
                        text-align: right !important;
                    
                    }

                    tr th[scope="col"]{
                        background-color: #346888 !important;
                        color: white;
                    }
                    
                    
                    tr th[scope="col"]:n-child(2){
                        text-align: center !important;
                    }

                    tr th[scope="col"]:last-child{
                        text-align: right !important;
                        background-color: #91C8E4 !important;
                        color: white;
                    }

                    tr th:n-child(2){
                        display:none !important;
                    }

                    tr th.blank {
                        display: none !important;
                    }

                    tr th[scope="row"]{
                        display: none !important;
                    }

                    tr td:n-child(2) {
                        text-align: center !important;
                    }

                    tr td:nth-child(3) {
                        text-align: center !important;
                        
                    }

                    tr td:last-child {
                        text-align: center !important;
                    }

        </style>
    """

st.info("# Player Comparison ")

# ------------------ player comparision ------------- #
player1_col, stats_col, player2_col = st.columns(3)


st.info("Select players to compare")
with st.form("Player Selector"):
    player1_container, player2_container = st.columns(2)

    with player1_container:
        player_1 = st.selectbox(
            "Player 1", options=players_stats['players'].unique(), key="player1", index=1, placeholder="Select player")
    with player2_container:
        player_2 = st.selectbox(
            "Player 2", options=players_stats['players'].unique(), key="player2", index=5, placeholder="Select player")
    compare_btn = st.form_submit_button(
        label="Compare", use_container_width=True)
error_col = st.empty()
if compare_btn and (player_1 == None or player_2 == None):
    with error_col:
        st.error("Please two players to compare")
        st.stop()
elif compare_btn:

    p1 = players_stats[players_stats['players'] == player_1]
    p2 = players_stats[players_stats['players'] == player_2]
    p1_l = len(p1)
    p2_l = len(p2)
    p1 = p1[STATS_VARIABLES.values()].mean().round(2)
    p2 = p2[STATS_VARIABLES.values()].mean().round(2)

    p1['games'] = p1_l
    p2['games'] = p2_l

    keys = ['games']

    for k in STATS_VARIABLES.values():
        keys.append(k)

    results = {
        player_1: p1[keys].values,
        'stats':  keys,
        player_2: p2[keys].values
    }

    results = pd.DataFrame(results)

    results['stats'] = results['stats'].apply(tiny_name)
    results.rename(columns={'stats': ''}, inplace=True)
    results[player_1] = results[player_1].apply(set_precision)
    results[player_2] = results[player_2].apply(set_precision)

    # st.dataframe(results, use_container_width=True, column_config={
    #     'stats': st.column_config.TextColumn(
    #         "Stats"),
    #     player_1: st.column_config.NumberColumn(player_1, format="%.2f", ),
    #     player_2: st.column_config.NumberColumn(
    #         player_2, format="%.2f", )
    # }, hide_index=True)

    # st.dataframe(results, hide_index=True)
    # Apply the custom CSS

    # with st.empty():
    #     st.info("Results")
    # Display the DataFrame
    st.table(format_df(results))
    # st.table(results)

    st.markdown(css, unsafe_allow_html=True)


footer()

st.toast("This page is for coaches and staff only. but for now anyone can see it")
