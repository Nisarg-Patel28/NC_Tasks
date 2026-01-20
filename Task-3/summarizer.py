from nltk.tokenize import sent_tokenize #It splits the user's input text into sentences
from sklearn.feature_extraction.text import TfidfVectorizer #sklearn is library that provides tool for vectorization, similarity measurement and modeling, TF-IDF converts sentences to numerical vectors
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk #nltk helps you to split, clean and process the text before analysing it

nltk.download('punkt', quiet=True)

def extractive_summarize(text, num_sentences = 3): #This part helps in splitting the text into sentences.
    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text

    vectorizer = TfidfVectorizer(stop_words='english') # This part of the code help to convert the sentences in the numerical vectors.
    tfidf_matrix = vectorizer.fit_transform(sentences)

    sim_matrix = cosine_similarity(tfidf_matrix) #It computes the similarity matrix

    scores = np.sum(sim_matrix, axis=1) #This makes the use of PageRank algorithm to score sentences.

    ranked_sentences = [sentences[i] for i in np.argsort(scores)[-num_sentences:][::-1]] #This selects the top sentences.

    summary = " ".join(ranked_sentences)
    return summary