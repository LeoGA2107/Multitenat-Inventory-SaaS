from sqlalchemy.ext.asyncio import AsyncSession
from app.models.models import User, Tenant
from app.schemas.schemas import TenantUserCreate, UserCreate, UserLogin
from app.core.security import hash_password
from app.core.database import get_db
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
import bcrypt
from jwt.exceptions import PyJWTError
from app.core.security import create_token



# Create owner

async def create_owner_and_tenant(data_model:TenantUserCreate, db:AsyncSession):

  

    hashed_password = hash_password(data_model.password)

    

    new_user = User(
        username = data_model.name,
        email = data_model.email,
        phone_number = data_model.phone_number,
        password = hashed_password.decode('utf-8'),
        role = "OWNER"
        )

    new_tenant = Tenant(
        tenantname = data_model.company_name,
        slug = data_model.slug,
        users = [new_user]

        )
    try:

        db.add(new_tenant)
        await db.commit()
        await db.refresh(new_user)
        await db.refresh(new_tenant)

        return {"tenant":new_tenant,
                "owner":new_user
                }


    
    except IntegrityError as err:

        await db.rollback()
        error_message = str(err.orig)

        # 3. Match the constraint name to raise the right exception
        if "users_email_key" in error_message or "users.email" in error_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered."
            )
        elif "tenants_slug_key" in error_message or "tenants.slug" in error_message:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Workspace URL slug is already taken."
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Database constraint violation occurred."
            )




# Login User

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



