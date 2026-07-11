import pandas as pd
import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

print("Loading flan-t5 model...")
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
llm_model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")
print("Model loaded.")

VECTOR_STORE_DIR = "./vectorstore"

def load_vector_store():
    index = faiss.read_index(f"{VECTOR_STORE_DIR}/review_index.faiss")
    mapping = pd.read_csv(f"{VECTOR_STORE_DIR}/review_mapping.csv")
    return index, mapping


def retrieve_reviews(question, top_k=5):
    index, mapping = load_vector_store()
    embed_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    query_vector = embed_model.encode([question]).astype('float32')
    distances, indices = index.search(query_vector, top_k)
    results = mapping.iloc[indices[0]]
    return results["REVIEWCOMMENTMESSAGE"].tolist()


def build_prompt(question, reviews):
    context = "\n".join([f"- {r}" for r in reviews])
    prompt = f"""You are a professional customer support analyst.
Based on the following customer reviews, answer the question clearly and professionally in English.

Customer Reviews:
{context}

Question: {question}

Answer in English:"""
    return prompt

def ask_assistant(question: str):
    reviews = retrieve_reviews(question)
    prompt = build_prompt(question, reviews)

    inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)
    outputs = llm_model.generate(**inputs, max_new_tokens=150, num_beams=4, early_stopping=True)
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return {"answer": answer, "sources": reviews}