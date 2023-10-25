import streamlit as st
from PIL import Image
import requests
from utils import log_query
API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
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
    try:
        response = requests.post(
            API_URL, headers=headers, json=payload)
        return response.json()
    except requests.ConnectionError:
        st.error("No internet")
    return {'error': True, 'message': 'No internet'}


initial_message = "Hello there 🙋🏿‍♀️, My name is NyaSSD,\
                  I am South Sudan basketball chatbot.\
                  you can ask me any question about south sudan basketball"

st.info("# Chat with NyaSSD 👸🏿")

# st.info("Welcome 🙋🏿‍♀️, My name is NyaSSD, \n I am South Sudan basketball chatbot. you can ask me any question about south sudan basketball")


if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append(
        {"role": "assistant", "content": initial_message})


for message in st.session_state['messages']:
    with st.chat_message(name=message['role']):
        st.markdown(message['content'])


query = st.chat_input(
    " Ask me e.g Who is all time leading scorer?")
if query:
    with st.chat_message(name="user"):
        st.markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})
    query_payload = {
        "inputs": {
            "question": f"you're an expert on South Sudan Basketball, based on context given, response appropriately this query {query}",
            "context": """
            
            The South Sudan men's national basketball team is the national basketball team representing South Sudan. Its official name is South Sudan Basketball Federation. It was established in May 2011, and became a member of FIBA in December 2013.[2] They are nicknamed the Bright Stars.

            The most recently founded national basketball team in FIBA, South Sudan has already played at one AfroBasket tournament in 2021, and has qualified for the 2023 FIBA World Cup.
            
            The team played its first unofficial match in Juba against Ugandan club champions Power on 13 July 2011. Power won the match 86–84.[3]

            In 2016, the team played in a exhibition tournament named Indigenous Basketball Competition in Vancouver, Canada.[4]

            On 9 January 2016, it was announced by the South Sudan Basketball Federation that Jerry Steele would become the new head coach of the men's national team for preparation of the 2017 AfroBasket competition. Through the agreement Steele would be under contract until the 2020 Tokyo Olympics.[5]

            In the 2017 AfroBasket qualifiers, the team was placed in Zone 5 Group A, with Egypt, Kenya, Rwanda. South Sudan played its first official international game on 12 March 2017, against Egypt in Cairo.[6] They would lose to Egypt by 11 points (87–76) in the first match on 12 March. Two days later the national team got it first victory in group stage against Kenya by 2 (68–66). The next day, the team relieved its next loss by ten (80–90) to Rwanda, later placing them in the Classification game. On 12 March, the team would beat Kenya in the Classification game in OT (84–89).

            Coach Steele and the South Sudan Basketball Federation parted ways by mutual agreement on 3 October 2017.

            On 7 November 2017, Scott Catt was appointed to be the new head coach of the men's national team by the South Sudan Basketball Federation. Madut Bol, son of the late Manute Bol, was also named as assistant head coach of the men's national team.[7]

            In November 2020, former NBA All-Star Luol Deng became the president of the SSBF.
            He also shortly coached the team. In September 2021, Royal Ivey, assistant coach with the Brooklyn Nets, became the head coach of the team.[9] At AfroBasket 2021, South Sudan made its debut at a major tournament and reached the round of 16 after defeating Uganda and Cameroon in the preliminary round. In the round of 16, South Sudan beat Kenya, in the quarterfinals the team lost to defending champions Tunisia.

            In the following 2023 FIBA World Cup qualification games, the Bright Stars impressed and had an unbeaten record in the first round (6–0), beating the defending African champions Tunisia twice and qualifying for their first World Cup in the third round with two games left. In the second round, again coached by Royal Ivey, they had another successful streak in order to qualify for South Sudan's first-ever World Cup in 2023.[10]

            On August 28, South Sudan earned its first World Cup victory with a dominant win over China in Manila, Philippines.
            South Sudan would qualify for the 2024 Summer Olympics in Paris by finishing as the best African team in the World Cup by beating Angola in their final game. This will be their first-ever Olympics.[12]
            """
        },
    }
    query = query.lower()
    if "hello" in query or "hi" in query or 'hey' in query:
        response = "Hi there"
    elif "awet" in query:
        response = "Awet Thon is a supper fan of South Sudan basketball"
    elif "nyassd" in query:
        response = "I am South Sudan basketball chatbot.\
                  you can ask me any question about south sudan basketball"
    else:
        # temporarily disabled real NyaSSD model, to collect more data.
        # response = nyassd_request(query_payload)
        # try:
        #     response = response['answer']
        # except KeyError:
        #     pass
        # if not response or response == "":
        response = f"Sorry i did not understand. \n i am still under development"

    with st.chat_message(name="assistant"):
        st.markdown(response)
    st.session_state.messages.append(
        {"role": "assistant", "content": response})

    try:
        log_query(query)
    except:
        pass
