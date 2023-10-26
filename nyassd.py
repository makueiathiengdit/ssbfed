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
        response = response.json()

        if "error" in response:
            response = {
                "error": "Something went wrong on our side. And we're working on it"}
        return response
    except requests.ConnectionError:
        response = {"error": "No internet connection"}
        return response
    except Exception:
        response = {"error": "Something went wrong"}
        return response
