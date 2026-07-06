import pandas as pd
from Services.visualizeservice import fetchgolddata
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

def getreviewsforembedding():

    sales, reviews = fetchgolddata()
    df = reviews[["REVIEWID", "REVIEWCOMMENTMESSAGE"]]
    df = df.dropna(subset=["REVIEWCOMMENTMESSAGE"])
    df = df[df["REVIEWCOMMENTMESSAGE"].str.strip() != ""]
    df = df.drop_duplicates(subset=["REVIEWID"])
    return df

def generateembeddings(df):

    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    review = df["REVIEWCOMMENTMESSAGE"].tolist()
    encode = model.encode(review)
    return df , encode
    
VECTOR_STORE_DIR = "./vectorstore"
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)

def build_faiss_index(df, vectors):
    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(vectors).astype('float32'))

    index_path = os.path.join(VECTOR_STORE_DIR, "review_index.faiss")
    mapping_path = os.path.join(VECTOR_STORE_DIR, "review_mapping.csv")

    faiss.write_index(index, index_path)
    df.reset_index(drop=True).to_csv(mapping_path, index=True)

    return index

def search_reviews(query, top_k=5):
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
     
    index = faiss.read_index("./vectorstore/review_index.faiss")
    mapping = pd.read_csv("./vectorstore/review_mapping.csv")
     
    query_vector = model.encode([query]).astype('float32')
     
    distances, indices = index.search(query_vector, top_k)
     
    results = mapping.iloc[indices[0]]
    
    return results