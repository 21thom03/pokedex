import requests, json
from schemas.pokemon import Pokemon

POKEAPI_URL = "https://pokeapi.co/api/v2"

def get_pokemon_from_api(number:int):
  api_answer = requests.get(f"{POKEAPI_URL}/pokemon/{number}")
  if api_answer.status_code != requests.codes.ok :
    return None , {
      "status_code" : api_answer.status_code,
      "error" : "Pokemon number non-existent"
      }
  
  pokeapi_info = api_answer.json()

  api_answer = requests.get(f"{POKEAPI_URL}/pokemon-species/{number}")
  if api_answer.status_code != requests.codes.ok :
    return None , {
      "status_code" : api_answer.status_code,
      "error" : "Pokemon inaccesible"
      }
  pokeapi_name_info = api_answer.json()

  name_fr = None
  for name in pokeapi_name_info["names"]:
    if name["language"]["name"]== "fr" :
      name_fr = name["name"]
      break

  pokemon_info = Pokemon(
    number = pokeapi_info["id"], 
    name = pokeapi_info["name"],
    name_fr = name_fr,
    types = [pokemon_type["type"] for pokemon_type in pokeapi_info["types"]],
    image_url = pokeapi_info["sprites"]["front_default"],
    height = pokeapi_info["height"],
    weight = pokeapi_info["weight"],
    evolves_from_number= None
  )
  return pokemon_info, ""
