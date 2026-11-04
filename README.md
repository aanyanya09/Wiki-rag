# Wikipedia RAG — Ask Questions Over 1.47 Million Wikipedia Articles

---

##  Project Overview

**Wikipedia RAG** is a Retrieval-Augmented Generation (RAG) application that answers questions using information retrieved from the Wikimedia Structured Wikipedia Dataset.

Instead of relying entirely on an LLM's internal knowledge, the application searches an indexed collection of approximately **1,468,100 Wikipedia articles**, retrieves relevant information, and generates answers grounded in the retrieved passages.

If the answer cannot be found in the retrieved context, the system is instructed to respond that it doesn't know.

Every answer includes references to its retrieved sources.

**Track:** Build with Open Source
**Event:** Open Source Day — Wikiclub

###  Try the Live Application

[**Open Wikipedia RAG**](https://uixr62wc6apb4f2rs3jqyv.streamlit.app/)

---

## ✨ Features

* 🔍 **Semantic Search:** Search across approximately 1.47 million Wikipedia articles.
* 🧠 **AI-Powered Answers:** Generate context-grounded answers using Groq.
* 📚 **Source References:** View retrieved Wikipedia articles and their links.
* 🎯 **Context-Based Responses:** Answers are generated using retrieved passages rather than unrestricted model knowledge.
* 💬 **Interactive Chat:** Ask questions through a conversational interface.
* ⚡ **Vector Search:** Similarity search powered by LanceDB.
* ☁️ **Cloud Deployment:** Hosted using Streamlit Community Cloud, with the index stored on Hugging Face.

---

## ⚙️ How It Works

Wikipedia RAG follows a Retrieval-Augmented Generation pipeline.

### RAG Architecture

```text
       Wikipedia Dataset
               |
               v
       Data Extraction
               |
               v
       Text Cleaning
               |
               v
     Sentence Transformers
      (BGE-small-en-v1.5)
               |
               v
         LanceDB Index
               |
               v
       User Question
               |
               v
       Query Embedding
               |
               v
       Semantic Retrieval
               |
               v
       Relevant Passages
               |
               v
         Groq LLM API
               |
               v
        Generated Answer
               |
               v
       Sources + Response
```

### Pipeline Explanation

1. **Dataset:** The Wikimedia Structured Wikipedia Dataset, containing approximately 1.47 million articles.
2. **Data Processing:** Article titles, text, and URLs are extracted and cleaned.
3. **Embedding:** Article content is converted into 384-dimensional vectors using `BAAI/bge-small-en-v1.5`.
4. **Vector Storage:** Embeddings and metadata are stored in LanceDB.
5. **Retrieval:** The user's question is embedded and compared against indexed vectors to retrieve relevant articles.
6. **Generation:** Retrieved passages and the question are sent to Groq's LLM API, with instructions to answer using the provided context.
7. **Presentation:** Streamlit displays the generated answer and relevant source references.

---

## 💡 Example Questions

Try asking the application:

* Where is Utuado?
* Which Irish programme promotes science to schools?
* What is artificial intelligence?
* Explain quantum computing.
* How does the human brain work?

You can also ask questions whose answers are not available in the dataset to test the system's ability to handle missing information.

---

## 🛠️ Tech Stack

| Technology            | Purpose                         |
| --------------------- | ------------------------------- |
| Python                | Core programming language       |
| Streamlit             | Interactive web interface       |
| LanceDB               | Vector database                 |
| Sentence Transformers | Text embeddings                 |
| BGE-small-en-v1.5     | Embedding model                 |
| Groq API              | LLM inference                   |
| Hugging Face Hub      | Dataset and index hosting       |
| GitHub                | Version control and source code |

---

## 📂 Project Structure

```text
Wiki-rag/
│
├── app.py              # Streamlit application
├── rag_core.py         # RAG pipeline and retrieval logic
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker configuration
├── README.md           # Project documentation
│
└── upload_index.py     # Hugging Face index upload utility
```

The large LanceDB index is hosted separately on Hugging Face rather than stored in this GitHub repository.

---

## ☁️ Deployment

The application uses:

* **Streamlit Community Cloud:** Hosts the web application.
* **Hugging Face Hub:** Stores the LanceDB index.
* **Groq:** Provides LLM inference.

The application retrieves its index from Hugging Face and uses Streamlit Secrets to access the required credentials.

---

## 📦 About the Wikipedia Index

The indexed dataset is approximately 1.6 GB in size and is not included in this GitHub repository.

It is hosted separately on Hugging Face:

[**View Wiki RAG Index on Hugging Face**](https://huggingface.co/datasets/aanya09shukla/wiki-rag-index)

Access may require permission if the dataset repository is private.

---

##  Privacy and API Usage

* API credentials are stored in Streamlit Secrets or environment variables.
* Credentials are not included in the source code.
* When Groq is used, the user's question and retrieved passages are sent to Groq's API for answer generation.
* The application uses retrieved Wikipedia content as its answer context.

---

##  AI Assistance

AI assistants were used during development for debugging, implementation guidance, and documentation support.

The project team understands the architecture and the underlying RAG workflow.

---

##  Credits

* Wikipedia and Wikimedia contributors for the underlying encyclopedic content.
* Wikimedia Structured Wikipedia Dataset.
* Hugging Face for model and dataset hosting.
* The open-source communities behind Streamlit, LanceDB, and Sentence Transformers.
* Groq for LLM inference.

Built for the **Wikiclub Open Source Day Challenge**.


