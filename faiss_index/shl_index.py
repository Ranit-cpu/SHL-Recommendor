# faiss_index/shl_index.py
import faiss
import pickle
import numpy as np
import json
from app.embedder import get_embedding

with open("faiss_index/shl_catalog.json", "r") as f:
    catalog = json.load(f)

texts = [f"{item['title']} {item.get('description', '')}" for item in catalog]
vectors = [get_embedding(text) for text in texts]
vectors = np.array(vectors).astype("float32")

# Build FAISS index
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)

# Save index and metadata
faiss.write_index(index, "faiss_index/shl_index.faiss")
with open("faiss_index/metadata.pkl", "wb") as f:
    pickle.dump(catalog, f)
