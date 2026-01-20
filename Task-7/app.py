import streamlit as st
import pandas as pd
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from langdetect import detect
from deep_translator import GoogleTranslator
from sentence_transformers import SentenceTransformer

def load_model():
    with open('qa_data.pkl','rb') as f:
        df = pickle.load(f)
    
    model = SentenceTransformer('distiluse-base-multilingual-cased-v2')
    embeddings = model.encode(df['question'].tolist(), show_progress_bar=False)
    return df,model,embeddings

df,model,embeddings = load_model()

st.title("Multilingual Medical QA Chatbot")
st.markdown("Supported Languages for now:- Hindi-IN, French-FR, Spanish-ES")

user_query = st.text_input("Ask your medical question in the above mentioned languages:")

if user_query:
    try:
        lang = detect(user_query)
        st.markdown(f"Detected language: {lang}")

        support_langs = ["en","fr","hi","es"]
        if lang not in support_langs:
            st.warning("Sorry ! Currently the bot just support these languages. THANK YOU !")
            st.stop()
        
        if lang != 'en':
            translated_input = GoogleTranslator(source=lang, target='en').translate(user_query)
        else:
            translated_input = user_query
        
        query_embedding = model.encode([translated_input])
        scores = cosine_similarity(query_embedding, embeddings)
        idx = np.argmax(scores)

        best_q = df.iloc[idx]['question']
        best_a = df.iloc[idx]['answer']

        if lang != 'en':
            translated_q = GoogleTranslator(source ='en', target=lang).translate(best_q)
            translated_a = GoogleTranslator(source ='en',target=lang).translate(best_a)
        else:
            translated_q = best_q
            translated_a = best_a
        
        st.subheader("The matched Question is:")
        st.write(translated_q)

        st.subheader("The Answer is:")
        st.write(translated_a)
    
    except Exception as e:
        st.error(f"Error: {e}")