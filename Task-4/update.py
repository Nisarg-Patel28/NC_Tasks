import os 
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

DATA_FOLDER = "data"
VECTOR_DB = "vector_store.pkl"

model = SentenceTransformer("all-MiniLM-L6-v2")

def load_text_files():
    texts = []
    for file in os.listdir(DATA_FOLDER):
        if file.endswith(".txt"):
            with open(os.path.join(DATA_FOLDER, file), "r", encoding="utf-8") as f:
                texts.append(f.read())
    return texts


def chunk_text(text, chunk_size=400):
    words = text.split()
    return [" ".join(words[i:i+chunk_size])for i in range(0, len(words), chunk_size)]

def update_vector_database():
    texts = load_text_files()
    chunks = []

    for text in texts:
        chunks.extend(chunk_text(text))

    embeddings = model.encode(chunks)

    if os.path.exists(VECTOR_DB):
        with open(VECTOR_DB, "rb") as f:
            index, stored_chunks = pickle.load(f)
    
    else:
        index = faiss.IndexFlatL2(embeddings.shape[1])
        stored_chunks=[]

    index.add(np.array(embeddings))
    stored_chunks.extend(chunks)

    with open(VECTOR_DB, "wb") as f:
        pickle.dump((index, stored_chunks),f)

    print("Vector database created successfully")

if __name__ == "__main__":
    update_vector_database()