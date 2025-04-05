from app.embedder import get_embedding, rewrite_query_with_gemini
from app.utils import extract_text_from_url, load_faiss_index

def get_recommendations(query=None, url=None):
    if url:
        query = extract_text_from_url(url)

    # Rewrite query for better embedding
    rewritten_query = rewrite_query_with_gemini(query)

    # Generate vector
    query_embedding = get_embedding(rewritten_query)

    # Search in FAISS
    index, metadata = load_faiss_index()
    D, I = index.search([query_embedding], k=10)
    results = [metadata[i] for i in I[0]]
    return results
