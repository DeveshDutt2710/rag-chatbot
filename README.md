# 📚 Retrieval-Augmented Generation (RAG) Chatbot – Django + OpenAI

This project is a **RAG-based customer support chatbot** built with:

- 🧠 Local embedding (`sentence-transformers`)
- 📦 Vector storage (`ChromaDB`)
- 🧾 Contextual answer generation (via `OpenAI GPT-3.5/GPT-4`)
- 🧱 Django backend with API + web UI

---

## ⚙️ Setup Instructions

### 1. 🚀 Clone the Repository

```bash
git clone https://github.com/your-org/rag-chatbot-django.git
cd rag-chatbot-django
```

### 2. 🐍 Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

Ensure these are installed:
```
openai
chromadb
sentence-transformers
python-dotenv
django
```

### 4. 📁 Create `.env` File

Create a `.env` file in the root folder:

```env
OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXX
OPENAI_MODEL=gpt-3.5-turbo
CHROMA_COLLECTION=rag_collection
CHUNK_PATH=chat/embeddings/chunks.json
```

### 5. 🧩 Prepare Source Data

Make sure you've already extracted and chunked content (PDFs/DOCX) and saved it as:

```
chat/embeddings/chunks.json
```

> If not yet done, run:
```bash
python scripts/parse_pdfs.py
python scripts/parse_docx.py
python scripts/build_index.py
```

### 6. 💬 Run the Django App

```bash
python manage.py migrate
python manage.py runserver
```

Then open [http://127.0.0.1:8000/chat/](http://127.0.0.1:8000/chat/)

---

## 📦 Project Structure

```
├── chat/
│   ├── templates/chat.html   # Frontend UI
│   ├── views.py                   # API + page view
│   ├── rag_pipeline.py           # Core RAG logic
│   └── urls.py
├── scripts/
│   ├── parse_docx.py
│   ├── parse_pdfs.py
│   └── build_index.py            # Preprocess + embed
├── ragchatbot/                      # Django settings
├── .env
├── requirements.txt
└── manage.py
```

---

## ✅ Features

- Context-based answering from support documents only
- Answers “I don’t know” if not found in source
- Modular: can swap OpenAI with Hugging Face, local LLMs
- Built-in script to preprocess docs and build vector index

---

## 🔐 Notes

- Ensure your OpenAI account has active billing / quota
- This project **will incur OpenAI API costs** per request
- You can switch to Hugging Face or local models if needed

---

## 🧠 Optional: Use Hugging Face or Grok

We also support:
- `huggingface_hub.InferenceClient`
- `openrouter.ai` (Grok or OpenChat)

Ask if you want that version instead.
