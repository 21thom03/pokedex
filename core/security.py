from fastapi import HTTPException, Header
TOKEN = "ENSEA2026"

def verify_token(authorization: str = Header(None)) :
  if authorization != f'Bearer {TOKEN}':
    raise HTTPException(
      status_code= 402,
      detail= "Unauthorized : Token invalide"
    )