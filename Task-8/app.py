import streamlit as st
from transformers import pipeline
import google.generativeai as genai
import os
import nltk
from nltk.tokenize import sent_tokenize
from dotenv import load_dotenv
load_dotenv()

nltk.download('punkt')

genai.configure(api_key=os.getenv("AIzaSyAdtmJ9e1_GbnU92TmHUhGH1fGVF8kAH84"))

sentiment_analyzer = pipeline ("sentiment-analysis")

def analyze_sentiment(text):
    sentences = sent_tokenize(text)
    sentiments = []

    for sent in sentences:
        result = sentiment_analyzer(sent)[0]
        sentiments.append((result['label'], result['score']))

    sentiment_labels = [s[0] for s in sentiments]
    final_sentiment = max(set(sentiment_labels), key = sentiment_labels.count)

    avg_score = sum([s[1] for s in sentiments]) / len(sentiments)
    return final_sentiment, avg_score, sentiments 

def get_chatbot_response(user_message, sentiment):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"You are a sentiment Analyzer bot. User sentiment: {sentiment}. Message: {user_message}"

    response = model.generate_content(prompt)
    
    return response.text

st.set_page_config(page_title = "Sentiment Analysis Bot")
st.title("Sentiment Analysis Bot")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  
if "sentiment_trend" not in st.session_state:
    st.session_state.sentiment_trend = []

user_input = st.text_input("You:", key = "user_input")

if st.button("Send") and user_input:
    sentiment, score, details = analyze_sentiment(user_input)
    st.session_state.sentiment_trend.append(sentiment)

    bot_response = get_chatbot_response(user_input, sentiment)

    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", bot_response))

for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**👦🏻 {sender}:** {message}")
    else:
        st.markdown(f"**🤖 {sender}:** {message}")