from sqlalchemy.ext.asyncio import AsyncSession
from app.platform.tenants.models import User, Tenant
from app.platform.tenants.schemas import TenantUserCreate
from app.modules.auth.security import hash_password
from app.core.database import get_db
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

async def create_owner_and_tenant(data_model:TenantUserCreate, db:AsyncSession=Depends(get_db)):

  

    hashed_password = hash_password(data_model.password)

    

    new_user = User(
        username = data_model.name,
        email = data_model.email,
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
        await db.refresh(new_tenant)
        
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