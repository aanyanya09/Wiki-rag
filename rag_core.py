import os
import requests
import lancedb
import streamlit as st

from huggingface_hub import snapshot_download
from sentence_transformers import SentenceTransformer


def get_secret(name):
    try:
        return st.secrets[name]
    except Exception:
        return os.environ.get(name)


HF_TOKEN = get_secret("HF_TOKEN")

if not HF_TOKEN:
    raise RuntimeError("HF_TOKEN is missing from Streamlit Secrets.")

# Download the index from Hugging Face
repo_path = snapshot_download(
    repo_id="aanya09shukla/wiki-rag-index",
    repo_type="dataset",
    token=HF_TOKEN,
    allow_patterns=["wiki.lance/**"]
)

db = lancedb.connect(repo_path)
table = db.open_table("wiki") 

# Load embedding model
model = SentenceTransformer("BAAI/bge-small-en-v1.5", device="cpu")

QUERY_PREFIX = "Represent this sentence for searching relevant passages: "


def search(question, k=5):
    qvec = model.encode(
        QUERY_PREFIX + question,
        normalize_embeddings=True
    )

    res = table.search(qvec).limit(k * 3).to_pandas()[["name", "text", "url"]]

    return res.drop_duplicates(subset="name").head(k).reset_index(drop=True)


def ask_llm(prompt):
    api_key = get_secret("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing from Streamlit Secrets.")

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": "llama-3.1-8b-instant",
            "temperature": 0.2,
            "messages": [{"role": "user", "content": prompt}]
        },
        timeout=60
    )

    if response.status_code != 200:
       raise RuntimeError(
          f"Groq API error {response.status_code}:
           {response.text}"
       )

    return response.json()["choices"][0]["message"]["content"]


def answer(question, k=5):
    ctx = search(question, k)

    context = "\n\n".join(
        f"[{i+1}] {t}" for i, t in enumerate(ctx["text"])
    )

    prompt = (
        "Answer using ONLY the context below. If the answer is not there, "
        "say you don't know. Cite sources like [1].\n\n"
        f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    )

    return ask_llm(prompt), ctx