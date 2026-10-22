from repositories.pokemon_repository import get_pokemon_by_number, push_pokemon_to_db
from clients.pokeapi import get_pokemon_from_api
from schemas.pokemon import Pokemon

def get_pokemon_service(number:int):

  pokemon = get_pokemon_by_number(number)
  if pokemon != None: 
    return pokemon, ""
    
  pokemon, error_message = get_pokemon_from_api(number)
  if pokemon == None:
    return None, error_message
  error_message = push_pokemon_to_db(pokemon)
  return pokemon, error_message

