from app.vectorstore.load_vectorstore import load_vectorstore
from app.memory.cache import get_cached, set_cached
from langchain.retrievers import ContextualCompressionRetriever
from langchain_community.document_compressors import FlashrankRerank

vectorstore = None
def _ensure_vs():
    global vectorstore
    if vectorstore is None:
        vectorstore = load_vectorstore(persist_dir='/home/kirti/cutomer_support/vector_db')

def retrieve_docs(state, override_k: int = None):
    _ensure_vs()
    cached = get_cached(state.user_query, state.intent)
    if cached and override_k is None:
        state.compressed_docs = cached
        return state

    k = override_k or 10
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={"k": k},
        filter={"intent": state.intent}
    )

    compressor = FlashrankRerank()
    c_retriever = ContextualCompressionRetriever(
        base_retriever=retriever,
        base_compressor=compressor
    )

    compressed_docs = c_retriever.invoke(state.user_query)
    state.compressed_docs = compressed_docs
    if override_k is None:
        set_cached(state.user_query, state.intent, compressed_docs)
    return state
