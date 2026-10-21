from pydantic import BaseModel, Field
from typing import List

class Pokemon(BaseModel):
  number : int = Field(ge=1)
  name : str = Field(min_lenght=1)
  name_fr : str | None
  types : List[dict] = Field(min_lenght=1)
  image_url : str = Field(min_lenght=1)
  height : int = Field(ge=1)
  weight : int = Field(ge=1)
  evolves_from_number : int | None

