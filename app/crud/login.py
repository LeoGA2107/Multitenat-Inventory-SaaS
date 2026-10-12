from  app.platform.tenants.schemas import UserLogin
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from sqlalchemy import select
from jwt.exceptions import InvalidTokenError
from app.platform.tenants.models import User
import bcrypt
from app.modules.auth.security import create_token
from jwt.exceptions import PyJWTError, ExpiredSignatureError

async def user_login(data_model:UserLogin, db:AsyncSession=Depends(get_db)):
    
    
    query = select(User).where(User.email==data_model.email)
    results = await db.scalars(query)
    fetch_user = results.first()



    if fetch_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Credentials",
            headers={"WWW-Authenticate":"Bearer"}
            
        )


    hashed_incoming_password = data_model.password.encode('utf-8')
    hashed_stored_password = fetch_user.password.encode('utf-8')

    if  not bcrypt.checkpw(hashed_incoming_password, hashed_stored_password):
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials",
            headers={"WWW-Authenticate":"Bearer"}
            
        )
    

    if fetch_user.is_active is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= "User is not active"
        )

    
    
    try:



        token_claims = {
            "sub":fetch_user.username,
            "email":fetch_user.email,
            "tenant_id":fetch_user.tenant_id,
            "role":fetch_user.role
        }

        jwt_token = create_token(data=token_claims)

        return {
            "access_token":jwt_token,
            "token_type":"bearer"
        }



    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= "Could not generate authentication token",
            headers={"WWW-Authenthicate":"Bearer"}
        )