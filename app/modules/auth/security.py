import bcrypt
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from jwt.exceptions import InvalidTokenError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from app.platform.tenants.schemas import TokenData, GetUser
from app.core.database import get_db
from app.platform.tenants.models import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


# Hash password logic

def hash_password(password:str):

    # Encode the password converting it into bytes
    pw_bytes = password.encode('utf-8')

    # Generate the salt
    salt = bcrypt.gensalt(rounds=12)

    # Hash the password
    hashed_password = bcrypt.hashpw(pw_bytes, salt)

    return hashed_password.decode('utf-8')



# Verify password
def verify_password(plain_password, hashed):
    encoded_incoming_password = plain_password.encode('utf-8')
    encoded_stored_password = hashed.encode('utf-8')

    try:

        return bcrypt.checkpw(encoded_incoming_password, encoded_stored_password)


    except (ValueError, TypeError, AttributeError):
        return False



# JWT Token Logic


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "2a782a3bb64b4351543bd672ffe9bdda01fd0f5c3651c853e96200c1b1c2e26d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Creating the token for user's authentication

def create_token(data:dict, expires_delta:timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt




async def get_current_user(  
        token:Annotated[str, Depends(oauth2_scheme)],
        db:AsyncSession=Depends(get_db))->User:

    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate Credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str |None = payload.get("sub")
        if username is None:
            raise credentials_exceptions
    except JWTError:
        raise credentials_exceptions



    query= select(User).where(User.username == username)
    results = await db.scalars(query)
    fetch_users = results.first()

    if fetch_users is None:
        return credentials_exceptions

    return fetch_users












