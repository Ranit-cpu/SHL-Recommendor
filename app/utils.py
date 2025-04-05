import pickle
import faiss
import requests
from bs4 import BeautifulSoup

def load_faiss_index():
    index = faiss.read_index("faiss_index/shl_index.faiss")
    with open("faiss_index/metadata.pkl","rb") as f:
        metadata = pickle.load(f)
    return index,metadata


def extract_text_from_url(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')

    return soup.get_text

