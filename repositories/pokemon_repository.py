from db.database import get_connection
from schemas.pokemon import Pokemon
import json

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
  if(pokemon_json is None):
    pokemon = None
  else :
    pokemon = Pokemon(
      number=pokemon_json["number"],
      name= pokemon_json["name"],
      name_fr= pokemon_json["name_fr"],
      types= json.loads(pokemon_json["types"]),
      image_url= pokemon_json["image_url"],
      height= pokemon_json["height"],
      weight= pokemon_json["weight"],
      evolves_from_number= pokemon_json["evolves_from_number"],
    )
  connection.commit()
  connection.close()
  return pokemon

def push_pokemon_to_db(pokemon:Pokemon):
  error_message = None
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

  connection.close()
  return error_message 
