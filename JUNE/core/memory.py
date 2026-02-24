import json
import os
from datetime import datetime
import chromadb  # Vector DB for semantic search

class MemoryManager:
    def __init__(self):
        # Using a local directory for persistence
        self.client = chromadb.PersistentClient(path="./june_memory")
        self.collection = self.client.get_or_create_collection("june_memories")
        self.short_term = []  # Last N interactions

    def store(self, query: str, response: str, metadata: dict = {}):
        doc_id = f"mem_{datetime.now().timestamp()}"
        self.collection.add(
            documents=[f"Q: {query}\nA: {response}"],
            ids=[doc_id],
            metadatas=[{"timestamp": str(datetime.now()), **metadata}]
        )

        self.short_term.append({"query": query, "response": response})
        if len(self.short_term) > 20:
            self.short_term.pop(0)

    def retrieve(self, query: str, n_results: int = 5) -> list:
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results.get("documents", [[]])[0]

    def get_short_term(self) -> list:
        return self.short_term
