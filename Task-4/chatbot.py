import os
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VECTOR_DB = os.path.join(BASE_DIR, "vector_store.pkl")

def retrieve_context(user_input):
    if not os.path.exists(VECTOR_DB):
        raise FileNotFoundError(
            f"vector_store.pkl not found. Run vector DB creation script first.\n"
            f"Expected location: {VECTOR_DB}"
        )

    with open(VECTOR_DB, "rb") as f:
        index, stored_chunks = pickle.load(f)

    # rest of your retrieval logic here
    return stored_chunks
