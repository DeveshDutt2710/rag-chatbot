import openai
import json
import os
from sentence_splitter import SentenceSplitter
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction, SentenceTransformerEmbeddingFunction
from tqdm import tqdm

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = "text-embedding-ada-002"

texts = []
for fname in ["../data/medical_questions.txt", "../data/plan_texts.txt", "../data/angelone_support.txt"]:
    if os.path.exists(fname):
        with open(fname) as f:
            texts.append(f.read())

full_text = "\n".join(texts)
splitter = SentenceSplitter(language="en")
chunks = splitter.split(full_text)
chunks = [c.strip() for c in chunks if len(c.strip()) > 50]

# Save chunks to JSON
os.makedirs("../chat/embeddings", exist_ok=True)
with open("../chat/embeddings/chunks.json", "w") as f:
    json.dump(chunks, f)

# Populate ChromaDB
chroma_client = chromadb.Client()
embedding_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = chroma_client.create_collection(name="rag_collection", embedding_function=embedding_fn)

batch_size = 5000
for i in tqdm(range(0, len(chunks), batch_size)):
    batch_chunks = chunks[i:i+batch_size]
    batch_ids = [str(j) for j in range(i, i+len(batch_chunks))]
    collection.add(documents=batch_chunks, ids=batch_ids)


print("Chunks embedded and stored in ChromaDB memory and chunks.json written.")
