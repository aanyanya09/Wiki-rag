import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

import requests
import lancedb
import streamlit as st

from huggingface_hub import snapshot_download
from sentence_transformers import SentenceTransformer


HF_REPO_ID = "aanya09shukla/wiki-rag-index"
EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
GROQ_MODEL = "openai/gpt-oss-20b"

QUERY_PREFIX = (
    "Represent this sentence for searching relevant passages: "
)


def get_secret(name):
    try:
        return st.secrets[name]
    except Exception:
        return os.environ.get(name)


@st.cache_resource(show_spinner="Loading Wikipedia index...")
def load_database():

    hf_token = get_secret("HF_TOKEN")

    if not hf_token:
        raise RuntimeError("HF_TOKEN is missing from Streamlit Secrets.")

    repo_path = snapshot_download(
        repo_id=HF_REPO_ID,
        repo_type="dataset",
        token=hf_token,
        allow_patterns=["wiki.lance/**"]
    )

    db = lancedb.connect(repo_path)
    table = db.open_table("wiki")

    return table


@st.cache_resource(show_spinner="Loading embedding model...")
def load_embedding_model():

    return SentenceTransformer(
        EMBEDDING_MODEL,
        device="cpu"
    )


def search(question, k=5):

    table = load_database()
    model = load_embedding_model()

    query_vector = model.encode(
        QUERY_PREFIX + question,
        normalize_embeddings=True,
        show_progress_bar=False
    )

    results = (
        table.search(query_vector)
        .limit(k * 3)
        .to_pandas()
    )

    results = results[["name", "text", "url"]]

    results = results.drop_duplicates(
        subset="name"
    )

    return results.head(k).reset_index(drop=True)


def ask_llm(prompt):

    api_key = get_secret("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY is missing from Streamlit Secrets.")

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": GROQ_MODEL,
            "temperature": 0.2,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        },
        timeout=60
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Groq API error {response.status_code}: {response.text}"
        )

    return response.json()["choices"][0]["message"]["content"]


def answer(question, k=5):

    context_df = search(question, k)

    context = "\n\n".join(
        f"[{i+1}] {row['text']}"
        for i, row in context_df.iterrows()
    )

    prompt = (
        "Answer using ONLY the context below. "
        "If the answer is not available in the context, "
        "say you don't know. Cite sources using references like [1].\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n"
        "Answer:"
    )

    response = ask_llm(prompt)

    return response, context_df