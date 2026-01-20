import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import ollama #Using ollama3 model for the bot

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "analytics" not in st.session_state:
    st.session_state.analytics = {
        "queries": [],
        "topics": [],
        "ratings": []
    }

def get_topic_from_query(query: str) -> str: #This part can be changed according to the necessity
    query = query.lower()
    if "doctor" in query or "symptom" in query or "treatment" in query:
        return "Medical Question"
    elif "python" in query or "java" in query or "code" in query:
        return "Programming Question"
    elif "visa" in query or "university" in query or "abroad" in query:
        return "Education Question"
    else:
        return "General Question"

def bot_response(query: str) -> str: # This means that the query is expected to be the string.
    response = ollama.chat(model="gemma3:4b", messages = [{"role": "user", "content": query}])
    return response ["message"]["content"]

def analytics_dashboard():
    st.sidebar.title("Analytics Dashboard")

    analytics = st.session_state.analytics
    total_queries = len(analytics["queries"])
    st.sidebar.metric("Total Queries", total_queries)

    if total_queries > 0:
        topic_count = Counter(analytics["topics"])
        most_common_topic, count = topic_count.most_common(1)[0]
        st.sidebar.write(f"The most common topic is: {most_common_topic}")

        fig, ax = plt.subplots()
        ax.bar(topic_count.keys(), topic_count.values())
        ax.set_title("Topic Distribution")
        ax.set_ylabel("Number of Queries")
        plt.xticks(rotation=30)
        st.sidebar.pyplot(fig)

    if analytics["ratings"]:
        average_rating = sum(analytics["ratings"]) / len(analytics["ratings"])
        st.sidebar.metric("Average User Rating", f"{average_rating:.2f} ⭐")


#The Streamlit UI code starts from here
st.title("Article Bot")
user_input = st.text_input("Enter your article topic or question: ")

if st.button("Generate"):
    if user_input.strip():
        topic = get_topic_from_query(user_input)
        response = bot_response(user_input)

        st.session_state.chat_history.append(("User", user_input))
        st.session_state.chat_history.append(("Bot", response))

        st.session_state.analytics["queries"].append(user_input) # This will save the analytics of the user input
        st.session_state.analytics["topics"].append(topic)

for role, message in st.session_state.chat_history:
    if role == "User":
        st.markdown(f"User: {message}")
    else :
        st.markdown("Bot: {message}")

if st.session_state.chat_history:
    st.subheader("Rate the response")
    rating = st.slider("Rate according to your satisfaction of the answer", 1,5,3)

    if st.button("Submit the rating"):
        st.session_state.analytics["ratings"].append(rating)
        st.success("Thank for your valuable rating :)")

analytics_dashboard() # This will show the dashboard