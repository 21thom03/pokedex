from fastapi import FastAPI, HTTPException
from schemas.pokemon import Pokemon
from db.database import create_database
from services.pokemon_service import get_pokemon_service
from repositories.pokemon_repository import get_pokemon_by_number
import requests, json

create_database()

app = FastAPI()

@app.get("/health")
def get_health():
  return {
    "status" : "ok"
  }

@app.get("/pokemons/{number}")
def get_pokemon(number:int):
  pokemon = get_pokemon_by_number(number)
  if pokemon == None :
    raise HTTPException(
      status_code= 404,
      detail= "Not found"
    )
  return pokemon


@app.get("/pokemons/{number}/scan")
def get_pokemon_by_scan(number:int):
  pokemon, error_message = get_pokemon_service(number)
  # pokemon, error_message = get_pokemon_from_api(number)
  if pokemon == None :
    raise HTTPException(
      status_code= error_message["status_code"],
      detail= error_message["error"]
    )
  return pokemon
