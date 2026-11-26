from pydantic import BaseModel, Field
from typing import List

class Type(BaseModel):
  id : int = Field(ge=1)
  name : str = Field(min_lenght=1)
  name_fr : str = Field(min_length=1)
