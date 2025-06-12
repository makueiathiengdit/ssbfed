import streamlit as st
import pandas as pd
import requests
from constants import APP_VERSION
import datetime


@st.cache_data
def get_data(filename):
    data = None

    # show spinner on first fetch
    if st.session_state.get('first_fetch', True):
        with st.spinner("Fetching data..."):
            try:
                data = pd.read_csv(filename, parse_dates=[
                                   'date'])
                st.session_state['first_fetch'] = False
            except Exception as e:
                st.error("Fetching data")
    else:
        try:
            data = pd.read_csv(filename, parse_dates=['date'])
            st.session_state['first_fetch'] = False
        except Exception as e:
            st.error(f"Error fetching data {filename}")
            st.error(e)

    return data


def convert(text):
    if "_" in text:
        parts = text.split("_")
        name = f"{parts[0]} {parts[1]}"
        return name.title()
    else:
        return text.title()


def tiny_name(text):
    text = text.lower()
    if "games" in text:
        return text.title()

    if "pct" in text:
        text = text.replace("pct", "")
    if "_" in text:
        part1, part2 = text.split("_")[:2]
        f = ""
        if part1 == "three":
            f = "3PT"
        elif part1 == "two":
            f = "2PT"
        else:
            f = f"{part1[0]}{part2[0]}"
        return f.upper()
    else:
        d = {
            'points': 'PPG',
            'assists': 'AST',
            'steals': 'STL',
            'rebounds': 'REB',
            'blocks': 'BLK',
            'turnovers': 'TOV',
            'efficiency': 'EFF'
        }

        f = text[0] + "PG"
        return d[text]


def shorten(name):
    parts = name.split(" ")
    first_name = parts[0]
    last_name = parts[-1]
    shortened_name = f"{first_name[0]}. {last_name}"
    return shortened_name


converter_fn = {
    'tiny': tiny_name,
    'short': convert
}


def condensed_stats(df, player, converter_fn='tiny'):
    fn = None
    if converter_fn == 'tiny':
        fn = tiny_name
    else:
        fn = convert
    player_stats = df[df['players'] == player]
    items_per_row = 6
    stats_labels = ['games', 'minutes', 'points', 'rebounds', 'assists', 'blocks',
                    'field_goals_made', 'field_goals_attempts',
                    'three_points_made', 'three_points_attempts',
                    'two_points_made', 'two_points_attempts',
                    'free_throws_made', 'free_throws_attempts', 'steals', 'efficiency']

    row1 = ['games', 'minutes', 'points', 'rebounds',
            'assists', 'blocks',]
    row2 = ['field_goals', 'three_points',
            'two_points', 'free_throws', 'steals', 'efficiency']

    player_stats['games'] = len(player_stats)
    metric_stats = player_stats[stats_labels]
    with st.container():
        st.info("Condensed Stats")
        for i in range(2):
            metric_cols = st.columns(items_per_row)
            for j in range(items_per_row):

                with metric_cols[j]:
                    if i == 0:
                        if j == 0:
                            st.metric("Games", value=len(player_stats))
                        else:
                            label = row1[j]
                            val = metric_stats[label].mean()
                            val = f"{val:.1f}"
                            if val == 'nan':
                                val = "-"
                            st.metric(
                                label=fn(label), value=val)
                    else:
                        label = row2[j]
                        if j > 3:
                            val = metric_stats[label].mean()
                            val = f"{val:.1f}"
                        else:
                            val = (metric_stats[label + "_made"].sum()) / \
                                (metric_stats[label +
                                              "_attempts"].sum()) * 100

                            val = f"{val:.1f}"
                        if val == 'nan':
                            val = "-"
                        st.metric(convert(label), value=val)


def display_profile(df, player_nme):
    img_col, details_col = st.columns(2, 8)

    position = df.loc[player_nme, 'position']
    height = df.loc[player_nme, 'height']
    jersey_no = df.loc[player_nme, 'jersey_no']
    debut = df.loc[player_nme, 'debut']
    player_img = df.loc[player_nme, 'image']

    with img_col:
        st.image(player_img, caption=player_nme)
    with details_col:
        st.markdown(f"""
                        <div class="details">
                                <p> Name      </p> <span>: {player_nme}  </span>
                                <p> Position  </p> <span>: {position}  </span>
                                <p> Height    </p> <span>: {height} </span>
                                <p> Jersey NO </p> <span>: {jersey_no}  </span>
                                <p> Debut     </p> <span>: {debut} </span>
                        </div>
                        """,
                    unsafe_allow_html=True
                    )


def title_cast(name):
    name = name.lower()
    return name.title()


def get_value(df, key):
    val = "--"
    try:
        val = df.loc[df[key] != "Unknown", key].iloc[0]
    except:
        pass
    return val


def check_connection():
    availabe = True
    try:
        res = requests.get("https://www.google.com")
        if res.status_code == 200:
            availabe = True
    except requests.ConnectionError:
        availabe = False
    return availabe


def set_precision(val):
    val = float(val)
    return f"{val:.2f}"


def load_css(filename):
    styles = ""
    with open(filename, 'r') as f:
        styles = f.read()
    return styles


def footer():
    st.divider()
    st.success("Built with ❤ by **Awet Thon**")
    st.header("Let's connect on social media")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info(
            '**Twitter: [@awetthon](https://twitter.com/awetthon)**', icon="💡")
    with c2:
        st.info(
            '**Linkedin: [@awetthon](https://linkedin.com/in/awetthon)**', icon="👨🏿‍💻")
    with c3:
        st.info(
            '**GitHub: [@awetthon](https://github.com/makueiathiengdit)**', icon="💻")
    # with st.sidebar():
    # css = load_css("styles.css")
    # st.markdown(f"<style>{css}<style>", unsafe_allow_html=True)
    st.success("Last updated: Sep 2023", icon="ℹ️")

def log_query(query):
    date = datetime.datetime.now()
    with open('log.txt', 'a') as f:
        f.write(f"{date} {query}")
        f.write("\n")
