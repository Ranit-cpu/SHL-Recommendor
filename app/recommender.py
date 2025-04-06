from app.embedder import get_embedding, rewrite_query_with_gemini
from app.utils import extract_text_from_url, load_faiss_index

def get_recommendations(query: str = None, url: str = None):
    if not query and not url:
        return {"error": "Please provide a query or a URL."}

    # Extract text if URL is provided
    if url:
        query = extract_text_from_url(url)
        if not query:
            return {"error": "Unable to extract text from the provided URL."}

    # Rewrite query using Gemini or fallback
    rewritten_query = rewrite_query_with_gemini(query)
    if not rewritten_query:
        rewritten_query = query  # fallback

    # Generate vector
    query_embedding = get_embedding(rewritten_query)
    if query_embedding is None:
        return {"error": "Failed to get embedding."}

    # Search in FAISS index
    index, metadata = load_faiss_index()
    if not index or not metadata:
        return {"error": "Failed to load FAISS index or metadata."}

    D, I = index.search([query_embedding], k=10)
    results = []

    for i in I[0]:
        if i < len(metadata):  # Ensure index exists
            results.append(metadata[i])
    print(results)
    return results
