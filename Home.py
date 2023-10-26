
from streamlit_lottie import st_lottie
import json

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
from streamlit_extras.metric_cards import style_metric_cards
from utils import get_data, tiny_name, set_precision, footer
from constants import STATS_VARIABLES, APP_VERSION
favicon = Image.open("favicon.png")
cover_pic = Image.open("cover.png")

# page settings
st.set_page_config(
    page_title="South Sudan Basketball Stats",
    page_icon=favicon,
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': "https://twitter.com/awetthon",
        'Report a bug': "https://twitter.com/awetthon",
        'About ': "# South Sudan Basketball Stats web app built with ❤ by [Awet Thon](twitter.com/awetthon)"
    }
)


if 'first_fetch' not in st.session_state:
    st.session_state['first_fetch'] = True


@st.cache_data
def get_player_stats(df=None, player=None):
    return df[df['players'] == player]


# --------------------- fetch team and players stats -----------------
team_stats = get_data("data/team_boxscore.csv")

players_stats = get_data("data/players_boxscore.csv")
players_stats['date'] = players_stats['date'].dt.strftime("%d-%m-%Y")
games_in_brief = get_data("data/games_in_brief.csv")


# ------------------------- Page Header -------------------------
st.header("South Sudan Basketball Stats")
cover_container = st.container()

with cover_container:
    st.image(cover_pic)


#   ------------------------ TABS ---------------------------------

team_tab, players_tab, chat_tab, news_tab, p_tab, q_tab = st.tabs(
    ["Team Stats", "Players Stats", "Chatbot", "News", "Players", "Quarter"])


#  ------------------------- TEAM TAB ------------------------------


with team_tab:

    # Display team stats

    st.info("# Team Stats")

    games_card, wins_card, points_card, fg_card, three_pt_card = st.columns(5)
    # ft_card, rebouns_card, assists_card, _ = st.columns(4)

    # """ fill the cards """
    with games_card:
        st.metric(label="**Games**", value=len(team_stats))
    with wins_card:
        wins = len(team_stats[team_stats['win'] == True])
        st.metric(label="**Wins**", value=wins+1)
    with points_card:
        st.metric(label="**Points per game**",
                  value=team_stats.points.mean().round(1))
    with fg_card:
        st.metric(label="**FG%**",
                  value=team_stats.field_goals_pct.mean().round(1))
    with three_pt_card:
        st.metric(label="**3PT%**",
                  value=team_stats.three_points_pct.mean().round(1))

    # apply streamlit.extras metric styles
    style_metric_cards(border_left_color="#7aa6c2")

    # divider between metrics and chart
    st.divider()

    # plot last n games points
    n = 12

    last_n_games = team_stats.sort_values(by='date', ascending=False).head(n)

    last_n_games = last_n_games.sort_values(by='date')

    last_n_games['date'] = last_n_games['date'].dt.strftime('%d-%m-%Y')

    point_bars = go.Bar(
        x=last_n_games['date'],
        y=last_n_games['points'],
        name='Points',
        text=last_n_games['points'],
        textposition='auto',
        marker_color='#346888'
    )

    fg_bars = go.Bar(
        x=last_n_games['date'],
        y=last_n_games['field_goals_pct'],
        name='FG%',
        text=last_n_games['field_goals_pct'],
        textposition='auto',
        marker_color='#7aa6c2'
    )

    three_pt_bars = go.Bar(
        x=last_n_games['date'],
        y=last_n_games['three_points_pct'],
        name='3PT%',
        text=last_n_games['three_points_pct'],
        textposition='auto',
        marker_color='#9dc6e0'
    )

    fig = go.Figure(data=[point_bars, fg_bars, three_pt_bars])
    fig.update_layout(
        title=f"South Sudan last {n} games",
        barmode='group',  # 'group' for grouped bars,
        xaxis_title='Games',
        # yaxis_title='stats values',
        bargap=0.15,  # gap between individual bars
        bargroupgap=0.1,  # gap between groups
        plot_bgcolor="#E4F1FF"
    )
    # st.info(f"Last {n} games")
    st.plotly_chart(fig, use_container_width=True)

    # --------------- interactive charts -----------------
    with st.expander("**See Interactive charts**", expanded=False):

        preselected_variables = [
            "Points",  "Field Goal PCT", "Three Point PCT"]

        # selected_variables = st.multiselect(
        #     label="Select variable to plot", options=variables.keys(), default=preselected_variables)

        selected_variables = []
        row1 = st.columns(5)
        row2 = st.columns(5)

        i = 0
        #  ---------------- displaying select boxes -----------------#

        # fill first row with five cols
        for col in row1:
            val = False
            with col:
                label = list(STATS_VARIABLES.keys())[i]
                if label in preselected_variables:
                    val = True
                label_checked = st.checkbox(label=label, key=label, value=val)
                if label_checked:
                    selected_variables.append(label)
                i += 1

        # second row cols
        for col in row2:
            val = False
            with col:
                label = list(STATS_VARIABLES.keys())[i]
                if label in preselected_variables:
                    val = True
                label_checked = st.checkbox(label=label, key=label, value=val)
                if label_checked:
                    selected_variables.append(label)
                i += 1

        # create a chart for each selected variable
        charts = []
        for variable in selected_variables:
            charts.append(go.Scatter(
                x=last_n_games['date'],
                y=last_n_games[STATS_VARIABLES[variable]],
                mode="lines+markers",
                name=variable,
                marker=dict(symbol="circle")
            ))

        layout = go.Layout(title=f"stats in last {n} games",
                           plot_bgcolor="#E4F1FF",
                           yaxis_title="Values", xaxis_title="Games", )

        fig = go.Figure(data=charts, layout=layout)
        st.plotly_chart(fig, use_container_width=True)

    # -------------------- game highs ---------------------
    with st.expander("**Game highs**"):
        st.info("Team Game highs")
        variable = st.selectbox(
            label="**Team Game highs**", options=STATS_VARIABLES.keys(), label_visibility="hidden", key="Team Game Highs")

        df = team_stats[['date', STATS_VARIABLES[variable], 'opponent']].sort_values(
            by=STATS_VARIABLES[variable], ascending=False).head(5).reset_index(drop=True)
        # st.table(df)
        df['date'] = df['date'].dt.strftime("%d-%m-%Y")
        st.dataframe(data=df, use_container_width=True, column_config={
            STATS_VARIABLES[variable]: st.column_config.NumberColumn(variable, format="%.2f"),
            'opponent': "Opponent",
            'date': "Date"
        })


# --------------------- Players tab --------------------------

with players_tab:
    st.info("# Players Stats")
    st.info("**Leaders**")

    # ------ average stats ---------------
    # variable = st.radio("Metric", options=variables.keys(), horizontal=True)
    variable = st.selectbox(
        label="**Leaders**", options=STATS_VARIABLES.keys(), label_visibility="hidden", key="Average Stats")

    vs = ['players']
    for v in STATS_VARIABLES.values():
        vs.append(v)

    df2 = players_stats[vs].groupby(by='players').mean()

    df2 = df2.sort_values(
        STATS_VARIABLES[variable], ascending=False).head(5)

    # ---------- per game stats ----------------
    st.dataframe(df2[STATS_VARIABLES[variable]].reset_index(), use_container_width=True, column_config={
        STATS_VARIABLES[variable]: st.column_config.NumberColumn(
            variable, format="%.2f", help=f"{variable} per game")
    }, hide_index=True)

    # ---------------------- players game high stats -------------------------
    with st.expander("**Game Highs**"):
        variable = st.selectbox(
            label="**Leaders**", options=STATS_VARIABLES.keys(), label_visibility="hidden", key="Game Highs")

        df = players_stats[['date', 'players',  STATS_VARIABLES[variable], 'opponent']].sort_values(
            by=STATS_VARIABLES[variable], ascending=False).head(5).reset_index(drop=True)

        # --------------- show results in dataframe ---------------
        st.dataframe(data=df, use_container_width=True, column_config={
            'players': "Player",
            STATS_VARIABLES[variable]: st.column_config.NumberColumn(variable),
            'opponent': "Opponent",
            'date': "Date"
        }, hide_index=True)

    # ------------------ player comparision ------------- #
    player1_col, stats_col, player2_col = st.columns(3)

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
                text-align: left !important;
                background-color: #7aa6c2 !important;
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
                text-align: right !important;
            }

            tr td:nth-child(3) {
                text-align: center !important;
                
            }

            tr td:last-child {
                text-align: left !important;
            }

        </style>
    """

    with st.expander(label="**Player comparision**", expanded=False):

        with st.form("Player Selector"):
            player1_container, player2_container = st.columns(2)

            with player1_container:
                player_1 = st.selectbox(
                    "Player 1", options=players_stats['players'].unique(), key="player1", index=None, placeholder="Select player")
            with player2_container:
                player_2 = st.selectbox(
                    "Player 2", options=players_stats['players'].unique(), key="player2", index=None, placeholder="Select player")
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
            p1 = p1[STATS_VARIABLES.values()].mean()
            p2 = p2[STATS_VARIABLES.values()].mean()

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
            results[player_1] = results[player_1].apply(set_precision)
            results[player_2] = results[player_2].apply(set_precision)

            st.info("Results")
            # st.dataframe(results, use_container_width=True, column_config={
            #     'stats': st.column_config.TextColumn(
            #         "Stats"),
            #     player_1: st.column_config.NumberColumn(player_1, format="%.2f"),
            #     player_2: st.column_config.NumberColumn(
            #         player_2, format="%.2f")
            # }, hide_index=True)

            st.table(results)
            st.markdown(css, unsafe_allow_html=True)

    st.info("To see all players and their stats, click [here](/Players)")

st.divider()


def nyassd(prompt):
    return "Hello there"


# ---------------- chatbot tab ---------------
with chat_tab:
    st.info("Hello 🙋🏿‍♀️, My name is NyaSSD, South Sudan basketball chatbot. you can ask me any question about south sudan basketball")

    # question = st.text_area(label="Question", label_visibility="hidden",
    #                         placeholder="Ask me any question about south sudan basketball e.g who is the best three point shooter", disabled=True)

    # submit = st.button("Ask", type="primary", use_container_width=True)
    # reply_container = st.empty()
    st.info("To chat, click [here](/Chat)")

    # if submit and question is not None:
    #     with reply_container:
    #         st.info("I am still under development. Hope to chat with you soon.")

# --------------------- news tab ------------------
with news_tab:
    st.info("Latest news, articles around South Sudan Basketball")


lottie = None
with open("images/animation.json", 'r') as f:
    lottie = json.load(f)


with st.sidebar:
    st.info("Oh my... Wang!! throws it down!!!")
    st_lottie(lottie)
    st.subheader(f"Version {APP_VERSION}")


with p_tab:
    st.info("Players")
    p_df = players_stats.copy()
    # p_df.sort_values(by='date', inplace=True)
    p_df['games'] = players_stats.groupby(
        'players')['minutes'].transform('count')
    p_df = p_df.drop_duplicates(subset=['players']).sort_values(
        by='games', ascending=False)

    st.dataframe(p_df[['players', 'games', 'date']].reset_index(
        drop=True), column_config={
            'players': "Player Name",
            'date': "Debut Date",
            'games': st.column_config.NumberColumn("Games Played", help="Games Played excluding friendly matches")}, use_container_width=True)
    st.info("To see all players and their stats, click [here](/Players)")


with q_tab:
    st.info("This is a demo. advanced stats coming soon")
    qs = games_in_brief[games_in_brief['team'] ==
                        'South Sudan'][['date', 'Q1', 'Q2', 'Q3', 'Q4', 'opponent']]
    qs = qs.reset_index()
    # st.dataframe(qs)

    qs = qs[:10]
    qs['date'] = qs['date'].dt.strftime(f"%d-%m-%Y")
    qs.sort_values(by="date", inplace=True)

    q1 = go.Bar(
        x=qs.index,
        y=qs['Q1'],
        name="Q1",
        text="Q1",
        textposition='auto',
        marker_color="#346888"
    )
    q2 = go.Bar(
        x=qs.index,
        y=qs['Q2'],
        name="Q2",
        text="Q2",
        textposition='auto',
        marker_color="#7aa6c2"

    )
    q3 = go.Bar(
        x=qs.index,
        y=qs['Q3'],
        name="Q3",
        text="Q3",
        textposition='auto',
        marker_color="#9dc6e0"

    )
    q4 = go.Bar(
        x=qs.index,
        y=qs['Q4'],
        name="Q4",
        text="Q4",
        textposition='auto',
        marker_color="#346888"

    )
    l = go.Scatter(
        x=qs.index,
        y=qs['Q4'],
        name="Q4",
        text="Q4",
        textposition='top left',
        marker_color="#346888"
    )

    fig = go.Figure(data=[q1, q2, q3, q4])
    fig.update_layout(
        title=f"Quater by quarter",
        barmode='group',  # 'group' for grouped bars,
        xaxis_title='Quarters',
        # yaxis_title='stats values',
        bargap=0.3,  # gap between individual bars
        bargroupgap=0.3,  # gap between groups
        plot_bgcolor="#E4F1FF"
    )
    # st.info(f"Last {n} games")
    st.plotly_chart(fig, use_container_width=True)


footer()


if st.session_state.get('first_time', True):
    # st.balloons()
    st.session_state['first_time'] = False

    st.toast(
        "We recommend viewing this site on device with large screen for better experience. 🙏🏿")
