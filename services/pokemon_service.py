from repositories.pokemon_repository import get_pokemon_by_number, push_pokemon_to_db, get_type_in_database, push_type_in_database
from clients.pokeapi import get_pokemon_from_api, get_type_from_api
from schemas.pokemon import Pokemon
from schemas.type import Type

def get_pokemon_service(number:int):
  pokemon = get_pokemon_by_number(number)
  if pokemon != None:
    return pokemon, ""
  
  pokemon, error_message = get_pokemon_from_api(number)
  if pokemon == None:
    return None, error_message

  pokemon_types = []
  for pokemon_technical_types in pokemon.types:
    pokemon_types.append(get_type_service(pokemon_technical_types))
  pokemon.types = pokemon_types

  error_message = push_pokemon_to_db(pokemon)
  return pokemon, error_message

def get_type_service(technical_type) -> Type:
  db_type = get_type_in_database(technical_type)
  if db_type != None:
    return db_type

  pokemon_type, error_message = get_type_from_api(technical_type)
  if pokemon_type == None :
    return None, error_message
  error_message = push_type_in_database(pokemon_type)
  return pokemon_type.name_fr