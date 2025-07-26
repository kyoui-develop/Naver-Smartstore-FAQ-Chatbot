import json

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

from config import (
    PERSIST_DIR, 
    COLLECTION_NAME, 
    EMBEDDING_MODEL_NAME,
    TOP_K
)


class Retriever:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=PERSIST_DIR)
        self.collection = self.client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=embedding_functions.OpenAIEmbeddingFunction(
                model_name=EMBEDDING_MODEL_NAME
            )
        )
    
    def retrieve(self, user_question, top_k=TOP_K):
        documents = self.collection.query(query_texts=[user_question], n_results=top_k)
        return [
            {
                "question": metadata["question"], 
                "answer": metadata["answer"], 
                "related_questions": json.loads(metadata["related_questions"]), 
                "distance": distance
            } for metadata, distance in zip(documents["metadatas"][0], documents["distances"][0])
        ]