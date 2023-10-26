import streamlit as st
import requests
import json
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"

# API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
headers = {"Authorization": f"Bearer {st.secrets['HUGGING_FACE_API_KEY']}"}


def nyassd_request(payload):
    response = ""
    try:
        payload = json.dumps(payload)
        response = requests.post(API_URL, headers=headers, data=payload)
        return response.json()
    except requests.ConnectionError:
        return {'error': True, 'message': 'No internet connection'}
    except:
        return {'error': True,  'message': 'Something went wrong'}
