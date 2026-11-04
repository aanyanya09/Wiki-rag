import streamlit as st

st.set_page_config(page_title="Wikipedia RAG", page_icon="📚", layout="wide")
st.title("📚 Wikipedia RAG")
st.caption("Ask questions answered only from the provided Wikimedia Wikipedia dataset (1.47M articles).")

try:
    from rag_core import answer
except Exception as e:
    st.error(f"Failed to load rag_core: {e}")
    st.stop()

SAMPLES = [
    "Where is Utuado?",
    "Who is Tom Rivett-Carnac?",
    "What are the Qwartz Electronic Music Awards?",
    "What did I eat yesterday?",
]

with st.sidebar:
    st.header("Settings")
    k = st.slider("Passages to retrieve", 3, 10, 5)
    show_passages = st.toggle("Show retrieved passages", value=True)
    st.header("Sample questions")
    for s in SAMPLES:
        if st.button(s):
            st.session_state["q"] = s

q = st.text_input("Ask a question", key="q")

if q:
    try:
        with st.spinner("Searching and thinking..."):
            text, ctx = answer(q, k=k)
        st.subheader("Answer")
        st.write(text)
        st.subheader("Sources")
        for i, row in enumerate(ctx.itertuples(), start=1):
            st.markdown(f"**[{i}]** [{row.name}]({row.url})")
            if show_passages:
                st.caption(row.text[:400])
    except Exception as e:
        st.error(f"Error: {e}")
