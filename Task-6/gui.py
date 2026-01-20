import streamlit as st
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

#loading the files
def load_model():
    with open('tfidf_vectorizer.pkl','rb') as f:
        vectorizer = pickle.load(f)
    with open('tfidf_matrix.pkl','rb') as f:
        tfidf_matrix = pickle.load(f)
    with open('qa_data.pkl','rb') as f:
        df = pickle.load(f)
    return vectorizer, tfidf_matrix, df

vectorizer, tfidf_matrix, df = load_model()
st.title("Medical QA Chatbot")
user_query = st.text_input("Enter the Question:-", placeholder = "Enter your question here")

if user_query:
    query_vec = vectorizer.transform([user_query]) #converts the user's question into TF-IDF vector
    similarity = cosine_similarity(query_vec,tfidf_matrix) #compares user's question vector with all other question
    idx = np.argmax(similarity) # Finds the index of the most similar question
    Question = df.iloc[idx]['question']
    Answer = df.iloc[idx]["answer"]
    
    st.subheader("Top Matched Question:")
    st.write(Question)
    
    st.subheader("Answer to your question is :")
    st.write(Answer)