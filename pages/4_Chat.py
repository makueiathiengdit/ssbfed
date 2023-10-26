import streamlit as st
from PIL import Image
import requests
import json
from utils import log_query
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"

# API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
headers = {"Authorization": f"Bearer {st.secrets['HUGGING_FACE_API_KEY']}"}

favicon = Image.open("favicon.png")

# page settings
st.set_page_config(
    page_title="Chat with NyaSSD",
    page_icon=favicon,
    initial_sidebar_state="expanded",
    layout="wide"
)


def nyassd_request(payload):
    response = ""
    try:
        payload = json.dumps(payload)
        response = requests.post(API_URL, headers=headers, data=payload)
        return response.json()
    except:
        st.write(response)
        return {'error': True, 'message': 'Something went wrong'}


initial_message = "Hello there 🙋🏿‍♀️, My name is NyaSSD,\
                  I am South Sudan basketball chatbot.\
                  you can ask me any question about south sudan basketball"

st.info("# Chat with NyaSSD 👸🏿")

st.info("Welcome 🙋🏿‍♀️, My name is NyaSSD, \n I am South Sudan basketball chatbot. you can ask me any question about south sudan basketball")


if "messages" not in st.session_state:
    st.session_state.messages = []
    # st.session_state.messages.append(
    #     {"role": "assistant", "content": initial_message})


for message in st.session_state['messages']:
    with st.chat_message(name=message['role']):
        st.markdown(message['content'])

query = st.chat_input(
    "Ask me about South Sudan basketball e.g who is the president of SSBF")
if query:
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
            "generated_responses": nyassd_messages,
            "text": query
        }
    }
    results = nyassd_request(payload)
    try:
        error = results['error']
        response = f"Sorry i did not understand. \n i am still under development"
    except KeyError:
        pass
    try:
        response = results['generated_text']
    except:
        response = f"Sorry i did not understand. \n i am still under development"
        # st.write(results)
    # response = results
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
