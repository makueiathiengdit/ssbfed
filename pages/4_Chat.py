import streamlit as st
from PIL import Image
from utils import log_query, load_css
from nyassd import nyassd_request
favicon = Image.open("favicon.png")

# page settings
st.set_page_config(
    page_title="Chat with NyaSSD",
    page_icon=favicon,
    initial_sidebar_state="collapsed",
    layout="centered"
)

try:
    css = load_css("styles.css")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
except:
    pass


initial_message = "Hello there 🙋🏿‍♀️ My name is NyaSSD,\
                  I am South Sudan basketball chatbot.\
                  you can ask me any question about south sudan basketball"

st.info("# Chat with NyaSSD 👸🏿")

# st.info("Welcome 🙋🏿‍♀️, My name is NyaSSD, \n I am South Sudan basketball chatbot. you can ask me any question about south sudan basketball")

refresh = st.button(label="New Chat", type="primary",
                    key="refresh_btn", use_container_width=True, help="If you encounter a problem click on this button to refresh")

if refresh:
    st.toast("Refreshing chat", icon="⚙")
    st.session_state['messages'] = []
    st.session_state.messages.append(
        {"role": "assistant", "content": initial_message})


if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append(
        {"role": "assistant", "content": initial_message})


for message in st.session_state['messages']:
    with st.chat_message(name=message['role']):
        st.markdown(message['content'])

query = st.chat_input(
    "Ask me about South Sudan basketball e.g who is the president of SSBF")
if query:
    query = str(query).strip()
    with st.chat_message(name="user"):
        st.markdown(query)
    query = query.lower()
    user_messages = [message['content']
                     for message in st.session_state['messages'] if message['role'] == 'user']
    nyassd_messages = [message['content']
                       for message in st.session_state['messages'] if message['role'] == 'assistant']
    payload = {
        "inputs": {

            "past_user_inputs": user_messages,
            "generated_responses": nyassd_messages[1:],
            "text": query
        }
    }

    results = nyassd_request(payload)
    response = ""

    try:
        if 'error' in results:
            response = results["error"]
        elif 'generated_text' in results:
            response = results["generated_text"]
        else:
            response = "Sorry i did not understand. i am still under development"
    except Exception:
        response = "Sorry i did not understand. i am still under development"

    with st.chat_message(name="assistant"):
        st.markdown(response)

    st.session_state.messages.append({"role": "user", "content": query})
    st.session_state.messages.append(
        {"role": "assistant", "content": response})


try:
    log_query(query)
    log_query(response)
except:
    pass
