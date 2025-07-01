import os
import json
from dotenv import load_dotenv
import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import openai

class RAGChatbot:
    def __init__(self):
        load_dotenv()

        # Setup OpenAI
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

        # Setup Chroma client and local embedding function
        self.client = chromadb.Client()
        self.embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

        # Load or create Chroma collection
        collection_name = os.getenv("CHROMA_COLLECTION", "rag_collection")
        existing = [c.name for c in self.client.list_collections()]
        if collection_name in existing:
            self.collection = self.client.get_collection(
                name=collection_name,
                embedding_function=self.embedding_fn
            )
        else:
            self.collection = self.client.create_collection(
                name=collection_name,
                embedding_function=self.embedding_fn
            )
            chunks_path = os.getenv("CHUNK_PATH", "chat/embeddings/chunks.json")
            with open(chunks_path) as f:
                chunks = json.load(f)

            batch_size = 5000
            for i in range(0, len(chunks), batch_size):
                batch = chunks[i:i+batch_size]
                ids = [str(j) for j in range(i, i+len(batch))]
                self.collection.add(documents=batch, ids=ids)

    def answer(self, query: str) -> str:
        results = self.collection.query(query_texts=[query], n_results=5)
        context_chunks = results["documents"][0] if results["documents"] else []

        if not context_chunks:
            return "I don't know."

        context = "\n".join(context_chunks[:3])

        system_prompt = "You are a helpful assistant. Use only the provided context to answer the user's question."
        user_prompt = f"""
Context:
{context}

Question: {query}

If the answer is not in the context, respond with "I don't know."
"""

        try:
            completion = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.5,
                max_tokens=300
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            return f"Error from OpenAI: {e}"
