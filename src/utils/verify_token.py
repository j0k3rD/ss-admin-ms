# from fastapi import Depends, HTTPException
# from datetime import datetime, timedelta, timezone
# from jose import jwt, JWTError
# import os
# from dotenv import load_dotenv
# from fastapi.security import OAuth2PasswordRequestForm

# load_dotenv()

# SECRET_KEY = os.getenv("SECRET_KEY")
# ALGORITHM = os.getenv("ALGORITHM")

# oauth2_scheme = OAuth2PasswordRequestForm

# def verify_token(token: str = Depends(oauth2_scheme)):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise HTTPException(status_code=403, detail="Invalid token")
#         if payload["exp"] < datetime.now(timezone.utc):
#             raise Exception("Token has expired")
#         return payload
#     except JWTError:
#         raise HTTPException(status_code=403, detail="Invalid token")