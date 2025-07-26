import os
import json

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import tiktoken

from src.loader import load_faqs
from src.preprocessor import preprocess_faqs
from config import (
    PERSIST_DIR,
    COLLECTION_NAME,
    EMBEDDING_MODEL_NAME,
    MAX_TOKENS
)


def ingest():
    client = chromadb.PersistentClient(path=PERSIST_DIR)
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_functions.OpenAIEmbeddingFunction(
            model_name=EMBEDDING_MODEL_NAME
        )
    )
    
    batch_size = 100
    faqs = preprocess_faqs(load_faqs())
    encoding = tiktoken.encoding_for_model(EMBEDDING_MODEL_NAME)

    for i in range(0, len(faqs), batch_size):
        batch = faqs[i:i+batch_size]
        ids, documents, metadatas = [], [], []

        for idx, faq in enumerate(batch):
            doc_text = faq["question"] + " " + faq["answer"]
            tokens = encoding.encode(doc_text)
            if len(tokens) > MAX_TOKENS:
                doc_text = encoding.decode(tokens[:MAX_TOKENS])
            ids.append(f"faq-{i + idx}")
            documents.append(doc_text)
            metadatas.append({
                "question": faq["question"],
                "answer": faq["answer"],
                "related_questions": json.dumps(faq["related_questions"])
            })

        collection.add(ids=ids, documents=documents, metadatas=metadatas)


if __name__ == "__main__":
    ingest()