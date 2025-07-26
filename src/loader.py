import pickle

from config import DATA_DIR


def load_faqs():
    with open(f"{DATA_DIR}/smart_store_faqs.pkl", "rb") as f:
        faqs = pickle.load(f)
    return faqs