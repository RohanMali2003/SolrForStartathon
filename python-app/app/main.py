from fastapi import FastAPI
from solr_connector import get_core_metadata, get_random_documents

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Solr FastAPI Backend is Running!"}

@app.get("/metadata")
def get_metadata():
    return get_core_metadata()

@app.get("/random-documents")
def get_random_docs():
    return get_random_documents()