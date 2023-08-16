from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from typing import Union
from datetime import datetime, timedelta
import server.doctorSchema
SECRET_KEY = "topsercrt"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 14400
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=900)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) 
    return encoded_jwt

async def decode_access_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data={}
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
        load = payload.get("sub")
        if load is None:
            raise credentials_exception
        token_data = server.doctorSchema.TokenData(displayName=payload.get("displayName"),id=int(payload.get("sub")),type=payload.get("type"))
    except ExpiredSignatureError: # <---- this one
       raise HTTPException(status_code=403, detail="token has been expired")
    except JWTError:
        raise credentials_exception
    return token_data

