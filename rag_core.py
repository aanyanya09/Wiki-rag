import os, lancedb, requests
from sentence_transformers import SentenceTransformer

BASE = os.path.dirname(os.path.abspath(__file__))
INDEX_DIR = os.environ.get("INDEX_DIR", os.path.join(BASE, "wiki_index"))
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "ollama")  # "ollama" or "groq"
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.1-8b-instant")
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

model = SentenceTransformer("BAAI/bge-small-en-v1.5", device="cpu")
table = lancedb.connect(INDEX_DIR).open_table("wiki")

def search(question, k=5):
    qvec = model.encode(QUERY_PREFIX + question, normalize_embeddings=True)
    res = table.search(qvec).limit(k * 3).to_pandas()[["name", "text", "url"]]
    return res.drop_duplicates(subset="name").head(k).reset_index(drop=True)

def ask_llm(prompt):
    if LLM_PROVIDER == "groq":
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {os.environ['GROQ_API_KEY']}"},
            json={"model": GROQ_MODEL, "temperature": 0.2,
                  "messages": [{"role": "user", "content": prompt}]},
            timeout=60)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    try:
        r = requests.post(f"{OLLAMA_URL}/api/generate",
                          json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
                          timeout=300)
        return r.json()["response"]
    except requests.exceptions.ConnectionError:
        return "Ollama is not running. Start it and try again."

def answer(question, k=5):
    ctx = search(question, k)
    context = "\n\n".join(f"[{i+1}] {t}" for i, t in enumerate(ctx["text"]))
    prompt = (
        "Answer using ONLY the context below. If the answer is not there, "
        "say you don't know. Cite sources like [1].\n\n"
        f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    )
    return ask_llm(prompt), ctx
    