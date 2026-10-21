import requests, json
from schemas.pokemon import Pokemon

POKEAPI_URL = "https://pokeapi.co/api/v2"

types = []

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

  pokemon_types = []
  for pokemon_technical_types in pokeapi_info["types"]:
    api_answer = requests.get(f"{POKEAPI_URL}/type/{pokemon_technical_types["type"]["name"]}")
    if api_answer.status_code != requests.codes.ok :
      return None , {
        "status_code" : api_answer.status_code,
        "error" : "Pokemon type inaccessible"
        }
    pokeapi_types = api_answer.json()
    for type_name in pokeapi_types["names"]:
      if type_name["language"]["name"]== "fr" :
        pokemon_types.append({"name" : type_name["name"], "id" : pokeapi_types["id"]})
        types.append({"name_en" : pokemon_technical_types["type"]["name"], "name_fr" : type_name["name"]})

  pokemon_info = Pokemon(
    number = pokeapi_info["id"], 
    name = pokeapi_info["name"],
    name_fr = name_fr,
    types = pokemon_types,
    image_url = pokeapi_info["sprites"]["front_default"],
    height = pokeapi_info["height"],
    weight = pokeapi_info["weight"],
    evolves_from_number= None
  )
  return pokemon_info, ""
