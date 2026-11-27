from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from db.database import create_database
from core.security import verify_token
from services.pokemon_service import get_pokemon_service
from repositories.pokemon_repository import get_pokemon_by_number, get_all_pokemons, get_pokemon_using_filter,\
                                          get_tallest_pokemon, get_heaviest_pokemon, get_highest_pokemon
import requests, json
from typing import Optional

create_database()

app = FastAPI()
app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_methods=["*"],
allow_headers=["*"],
)

@app.get("/health")
def get_health():
  return {
    "status" : "ok"
  }

@app.get("/pokemons")
def get_all_pokemons_from_db():
  all_pokemons, error_message = get_all_pokemons()
  if all_pokemons == None :
    raise HTTPException(
    status_code= error_message["status_code"],
    detail= error_message["error"]
  )
  return all_pokemons


@app.get("/pokemons/{number}")
def get_pokemon(number:int):
  pokemon = get_pokemon_by_number(number)
  if pokemon == None :
    raise HTTPException(
      status_code= 404,
      detail= "Not found"
    )
  return pokemon


@app.get("/pokemons/{number}/scan", dependencies=[Depends(verify_token)])
def get_pokemon_by_scan(number:int):
  pokemon, error_message = get_pokemon_service(number)
  # pokemon, error_message = get_pokemon_from_api(number)
  if pokemon == None :
    raise HTTPException(
      status_code= error_message["status_code"],
      detail= error_message["error"]
    )
  return pokemon

@app.get("/stats")
def get_stats():
  pokemon_discovered, error_message = get_all_pokemons()
  if error_message != None :
    raise HTTPException(
    status_code= error_message["status_code"],
    detail= error_message["error"]
  )
  return {
    "discovered" : len(pokemon_discovered),
    "remaining" : 151-len(pokemon_discovered),
    "completion_percentage" : round(len(pokemon_discovered)/151 * 100, 2)
  }

@app.get("/stats/types")
def get_stats_types():
  all_pokemon, error_message = get_all_pokemons()
  if error_message != None :
    raise HTTPException(
    status_code= error_message["status_code"],
    detail= error_message["error"]
  )
  types = dict()
  for pokemon in all_pokemon:
    for pokemon_type in pokemon.types :
      if pokemon_type in types :
        types[pokemon_type] += 1
      else :
        types[pokemon_type] = 1

  return types

@app.get("/stats/records")
def get_stats_records():
  tallest_pokemon, _ = get_tallest_pokemon()
  if tallest_pokemon == None:
    return { None }
  heaviest_pokemon, _ = get_heaviest_pokemon()
  highest_pokemon, _ = get_highest_pokemon()
  return {
    "tallest": {
      "number": tallest_pokemon["number"],
      "name_fr": tallest_pokemon["name"],
      "height": tallest_pokemon["height"]
      },
    "heaviest": {
      "number": heaviest_pokemon["number"],
      "name_fr": heaviest_pokemon["name"],
      "weight": heaviest_pokemon["weight"],
      },
    "highest_number": {
      "number": highest_pokemon["number"],
      "name_fr": highest_pokemon["name"],
      }
  }

@app.get("/search")
def search_pokemons(
    name: Optional[str] = None,
    type: Optional[str] = None,
    min_height: Optional[int] = None,
    max_height: Optional[int] = None,
    min_weight: Optional[int] = None,
    max_weight: Optional[int] = None):
  filter = [
    {"name" : "name", "value" : str(f" LIKE '%{name}%' ") if name != None else None},
    {"name" : "types", "value" : str(f" LIKE '%{type}%' ") if type != None else None},
    {"name" : "height", "value" : str(f" >= {min_height} ") if min_height != None else None},
    {"name" : "height", "value" : str(f" <= {max_height} ") if max_height != None else None},
    {"name" : "weight", "value" : str(f" >= {min_weight} ") if min_weight != None else None},
    {"name" : "weight", "value" : str(f" >= {max_weight} ") if max_weight != None else None}
  ]
  pokemons, error_message = get_pokemon_using_filter(filter)
  if error_message != None :
    raise HTTPException(
    status_code= error_message["status_code"],
    detail= error_message["error"]
  )
  return {
    "count" : len(pokemons),
    "results" : [
      {
      "number": pokemon["number"],
      "name_fr": pokemon["name_fr"],
      "types": json.loads(pokemon["types"]),
      "height": pokemon["height"],
      "weight": pokemon["weight"]
      }
    for pokemon in pokemons]
  }