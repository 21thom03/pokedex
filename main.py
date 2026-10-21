from fastapi import FastAPI, HTTPException
from schemas.pokemon import Pokemon
from db.database import get_connection
from clients.pokeapi import get_pokemon_from_api
import requests, json

POKEAPI_URL = "https://pokeapi.co/api/v2"

app = FastAPI()

@app.get("/health")
def get_health():
  return {
    "status" : "ok"
  }

@app.get("/pokemons/{number}")
def get_pokemon(number:int):
  api_answer = requests.get(f"{POKEAPI_URL}/pokemon/{number}")
  if api_answer.status_code != requests.codes.ok :
    raise HTTPException(
      status_code=api_answer.status_code,
      detail="Pokemon number non-existent"
    )
  json_answer = api_answer.json()
  pokemon_info = {
    "number" : json_answer["id"],
    "name" : json_answer["name"],
    "height" : json_answer["height"],
    "weight" : json_answer["weight"],
    }
  return pokemon_info

@app.get("/pokemons/{number}/scan")
def get_pokemon_by_scan(number:int):
  pokemon, error_message = get_pokemon_from_api(number)
  if pokemon == None:
    raise HTTPException(
      status_code= error_message["status_code"],
      detail= error_message["error"]
    )
  return pokemon
