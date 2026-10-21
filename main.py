from fastapi import FastAPI
from pydantic import BaseModel, Field
import requests, json

POKEAPI_URL = "https://pokeapi.co/api/v2"

app = FastAPI()

@app.get("/health")
def get_health():
  return {
    "status" : "ok"
  }
