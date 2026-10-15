from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.models import User
from app.schemas.schemas import UserCreate
from app.core.security import hash_password




SECRET_KEY = "2a782a3bb64b4351543bd672ffe9bdda01fd0f5c3651c853e96200c1b1c2e26d"
ALGORITHM = "HS256"


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl = "/auth/login"
)

async def get_current_user(  
        token:str=Depends(oauth2_scheme),
        db:AsyncSession=Depends(get_db))->User:

    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate Credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )



    
    # Decoding the payload to get the token
    try:


        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str |None = payload.get("email")


        if user_email is None:
            raise credentials_exceptions
    except JWTError:
        raise credentials_exceptions


    #Quering the database
    query= select(User).where(User.email == user_email)
    results = await db.scalars(query)
    fetch_users = results.first()

    if fetch_users is None:
        return credentials_exceptions

    if not fetch_users.is_active:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = "User is not active"
        )

    return fetch_users


async def create_normal_user(
        data_model:UserCreate,
        tenant_id:int,
        db:AsyncSession
):

    hashed_password_str = hash_password(data_model.password)

    # Create user explicitly bound to the Owner's tenant_id

    new_user = User(
        username = data_model.name,
        email = data_model.email,
        phone_number = data_model.phone_number,
        password = hashed_password_str,
        role = data_model.role,
        tenant_id = tenant_id
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)


    return new_user
