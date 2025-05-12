import streamlit as st
import torch
import json
import random
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

# Load intents and model
with open("intents.json", "r") as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size)
model.load_state_dict(model_state)
model.eval()

# Streamlit app config
st.set_page_config(page_title="🤖 AI Chatbot", layout="centered")
st.markdown("<h1 style='text-align: center;'>🤖 E-Commerce Chatbot</h1>", unsafe_allow_html=True)

# Chat logic
def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = torch.tensor(X, dtype=torch.float32).unsqueeze(0)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                return random.choice(intent["responses"])
    else:
        return "I'm not sure I understand. Can you try rephrasing?"

# Session state to keep chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Input form
with st.form("chat_input", clear_on_submit=True):
    user_msg = st.text_input("Type your message:", "", placeholder="Say something...")
    submitted = st.form_submit_button("Send")

if submitted and user_msg:
    response = get_response(user_msg)
    st.session_state.history.append(("user", user_msg))
    st.session_state.history.append(("bot", response))

# Display chat history
for sender, msg in st.session_state.history:
    if sender == "user":
        st.markdown(f"<div style='text-align: right; color: white; background-color: #3399ff; padding: 8px; border-radius: 10px; margin: 5px 0;'>{msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: left; background-color: #e6e6e6; padding: 8px; border-radius: 10px; margin: 5px 0;'>{msg}</div>", unsafe_allow_html=True)
