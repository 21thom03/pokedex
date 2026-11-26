from db.database import get_connection
from schemas.pokemon import Pokemon
from schemas.type import Type
import json

def get_all_pokemons():
  connection = get_connection()
  cursor = connection.cursor()
  try :
    cursor.execute(
      """
        SELECT * FROM pokemon ORDER BY number
      """
    )
    pokemon_json = cursor.fetchall()
    connection.commit()
  except Exception as e :
    connection.rollback()
    error_message = {
      "status_code" : 400,
      "error" : f"Error with database : {e}"
    }
  connection.close()
  if not (len(pokemon_json) > 0):
    return None, error_message
  
  all_pokemon = [] 
  for pokemon in pokemon_json :
    all_pokemon.append(Pokemon(
        number=pokemon["number"],
        name= pokemon["name"],
        name_fr= pokemon["name_fr"],
        types= json.loads(pokemon["types"]),
        image_url= pokemon["image_url"],
        height= pokemon["height"],
        weight= pokemon["weight"],
        evolves_from_number= pokemon["evolves_from_number"],
      ))
  return all_pokemon, None

def get_pokemon_by_number(number) -> Pokemon:
  connection = get_connection()
  cursor = connection.cursor()
  cursor.execute(
    """
      SELECT * FROM pokemon WHERE number == ?
    """,
    (
      number,
    )
  )
  pokemon_json = cursor.fetchone()
  connection.commit()
  connection.close()
  if(pokemon_json is None):
    return None
  return Pokemon(
      number=pokemon_json["number"],
      name= pokemon_json["name"],
      name_fr= pokemon_json["name_fr"],
      types= json.loads(pokemon_json["types"]),
      image_url= pokemon_json["image_url"],
      height= pokemon_json["height"],
      weight= pokemon_json["weight"],
      evolves_from_number= pokemon_json["evolves_from_number"],
    )

def push_pokemon_to_db(pokemon:Pokemon) -> dict:
  error_message = None
  print(pokemon.types)
  connection = get_connection()
  cursor = connection.cursor()
  try :
    cursor.execute(
      """
        INSERT INTO pokemon
        (
          number,
          name,
          name_fr,
          types,
          image_url,
          height,
          weight,
          evolves_from_number
        )
        VALUES (? ,? ,? ,? ,? ,? ,? ,?)
      """,
      (
        pokemon.number,
        pokemon.name,
        pokemon.name_fr,
        json.dumps(pokemon.types),
        pokemon.image_url,
        pokemon.height,
        pokemon.weight,
        pokemon.evolves_from_number
      )
    )
    connection.commit()
  except Exception as e :
    connection.rollback()
    error_message = {
      "status_code" : 400,
      "error" : f"Error with database : {e}"
    }
    print(f"\033[35mError: {error_message}\033[00m")
  connection.close()
  return error_message 

def get_type_in_database(technical_type:str) -> dict:
  connection = get_connection()
  cursor = connection.cursor()
  cursor.execute(
    """
      SELECT * FROM pokemon_types WHERE name == ?
    """,
    (
      technical_type,
    )
  )
  type_json = cursor.fetchone()
  connection.commit()
  connection.close()
  if(type_json is None):
    return None
  return type_json["name_fr"]

def push_type_in_database(pokemon_type:Type) -> dict:
  error_message = None
  connection = get_connection()
  cursor = connection.cursor()
  try :
    cursor.execute(
      """
        INSERT INTO pokemon_types
        (
          id,
          name,
          name_fr
        )
        VALUES (? ,? ,?)
      """,
      (
        pokemon_type.id,
        pokemon_type.name,
        pokemon_type.name_fr,
      )
    )
    connection.commit()
  except Exception as e :
    connection.rollback()
    error_message = {
      "status_code" : 400,
      "error" : f"Error with database : {e}"
    }
  connection.close()
  return error_message 