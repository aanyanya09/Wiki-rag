\# Wikipedia RAG: Ask Questions Over Wikipedia



\*\*Track:\*\* Build with Open Source

\*\*Event:\*\* Open Source Day, Wikiclub



\*\*Demo video:\*\* \[PASTE YOUTUBE/DRIVE LINK]

\*\*Live demo:\*\* \[PASTE LINK, OR DELETE THIS LINE]



\## What it is



A Retrieval-Augmented Generation (RAG) app that answers questions using only

the Wikimedia Structured Wikipedia Dataset. It searches 1,468,100 indexed

Wikipedia articles, finds the most relevant passages, and gives them to an LLM

that must answer from those passages. If the answer is not in them, it says

"I don't know." Every answer shows its sources with links.



\## How it works



1\. \*\*Dataset:\*\* the Wikimedia Structured Wikipedia Dataset (Kaggle), about 47 GB raw.

2\. \*\*Parse and clean:\*\* article names, text and URLs were extracted from the 53 source files.

3\. \*\*Embed:\*\* each article text was converted to a 384-number vector with

&#x20;  `BAAI/bge-small-en-v1.5`, so similar meanings sit close together.

4\. \*\*Store:\*\* vectors and metadata were saved in LanceDB, an embedded vector

&#x20;  database that reads from disk (about 1.6 GB compressed).

5\. \*\*Retrieve:\*\* a question is embedded with the same model, and the closest

&#x20;  passages are fetched. Duplicate article titles are removed.

6\. \*\*Generate:\*\* the passages and question go to Llama 3.2 3B (via Ollama),

&#x20;  with the instruction to answer only from the context and cite sources like \[1].

7\. \*\*Show:\*\* a Streamlit app displays the answer, source links and passages.



\## Example questions



\- Where is Utuado? (direct fact)

\- Which Irish programme promotes science to schools? (indirect question)

\- What did I eat yesterday? (not in the data, so the system answers "I don't know")



\## Features



\- Semantic search over 1.47M articles

\- Sources with links and retrieved passages for every answer

\- Adjustable number of retrieved passages and sample questions

\- Light and dark mode (follows the system theme)

\- Runs fully locally (Ollama) or with a hosted LLM (Groq) by setting an environment variable



\## Run locally



1\. Get the index and put it at `./wiki\_index` (the folder that contains `wiki.lance`).

2\. Create an environment (Python 3.11 or 3.12) and install:

&#x20;  `pip install -r requirements.txt`

3\. Install Ollama, then run `ollama pull llama3.2:3b`

4\. Start the app: `streamlit run app.py`



\## Run with Docker



```

docker build -t wiki-rag .

docker run -p 8501:8501 -v <path-to>/wiki\_index:/app/wiki\_index -e OLLAMA\_URL=http://host.docker.internal:11434 wiki-rag

```



To use Groq instead of Ollama, add

`-e LLM\_PROVIDER=groq -e GROQ\_API\_KEY=<your key>`.

API keys are read from environment variables and are never stored in the code.

When Groq is used, the question and retrieved passages are sent to Groq's servers.



\## About the index



The index is not in this repo because of its size (about 1.6 GB).

\[ADD A DRIVE / HUGGING FACE LINK HERE, OR WRITE "Available on request."]



\## Tech stack



Python, Streamlit, LanceDB, sentence-transformers (bge-small-en-v1.5),

Ollama with Llama 3.2 3B, optional Groq API, Docker.



\## AI assistance



We used AI assistants while building this project. All team members understand

and can explain the pipeline.



\## Credits



Content comes from Wikipedia, licensed CC BY-SA 4.0, via the Wikimedia

Structured Wikipedia Dataset. Built for the Wikiclub Open Source Day challenge.

